import logging
import typing

from typing import Any, Dict, Tuple, Type, Union

from dbnd._core.current import current_task_run, get_databand_run
from dbnd._core.decorator.func_task_call import FuncCall
from dbnd._core.decorator.task_decorator_spec import args_to_kwargs
from targets.inline_target import InlineTarget


logger = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    from dbnd._core.task.task import Task


def create_dynamic_task(func_call):
    # type: (FuncCall) -> Task
    task_cls, call_args, call_kwargs = (
        func_call.task_cls,
        func_call.call_args,
        func_call.call_kwargs,
    )
    from dbnd import pipeline, PipelineTask
    from dbnd._core.decorator.func_task_decorator import _default_output

    parent_task = current_task_run().task
    dbnd_run = get_databand_run()

    if task_cls._conf__decorator_spec is not None:
        # orig_call_args, orig_call_kwargs = call_args, call_kwargs
        call_args, call_kwargs = args_to_kwargs(
            task_cls._conf__decorator_spec.args, call_args, call_kwargs
        )

    # Map all kwargs to the "original" target of that objects
    # for example: for DataFrame we'll try to find a relevant target that were used to read it
    # get all possible value's targets
    call_kwargs_as_targets = dbnd_run.target_origin.get_for_map(call_kwargs)
    for p_name, value_origin in call_kwargs_as_targets.items():
        call_kwargs[p_name] = InlineTarget(
            root_target=value_origin.origin_target,
            obj=call_kwargs[p_name],
            value_type=value_origin.value_type,
            source=value_origin.origin_target.source,
        )

    call_kwargs.setdefault("task_is_dynamic", True)
    call_kwargs.setdefault(
        "task_in_memory_outputs", parent_task.settings.dynamic_task.in_memory_outputs
    )

    # in case of pipeline - we'd like to run it as regular task
    # if False and issubclass(task_cls, PipelineTask):
    #     # TODO: do we want to support this behavior
    #     task_cls = task(task_cls._conf__decorator_spec.item).task_cls

    if issubclass(task_cls, PipelineTask):
        # if it's pipeline - create new databand run
        # create override _task_default_result to be object instead of target
        task_cls = pipeline(
            task_cls._conf__decorator_spec.item, _task_default_result=_default_output
        ).task_cls

        # instantiate inline pipeline
        t = task_cls(*call_args, **call_kwargs)
        return t
    else:
        # instantiate inline task
        t = task_cls(*call_args, **call_kwargs)

        # update upstream/downstream relations - needed for correct tracking
        # we can have the task as upstream , as it was executed already
        if not parent_task.task_dag.has_upstream(t):
            parent_task.set_upstream(t)
        return t


def run_dynamic_task(task):
    # type: (Task) -> Union[Task, Any]
    from dbnd import PipelineTask

    dbnd_run = get_databand_run()

    if isinstance(task, PipelineTask):
        # if it's pipeline - create new databand run
        run = dbnd_run.context.dbnd_run_task(task)
        task_run = run.get_task_run(task.task_id)
    else:
        task_run = dbnd_run.run_dynamic_task(
            task, task_engine=current_task_run().task_engine
        )

    t = task_run.task
    # if we are inside run, we want to have real values, not deferred!
    if t.task_definition.single_result_output:
        return t.__class__.result.load_from_target(t.result)
        # we have func without result, just fallback to None
    return t


def run_dynamic_task_safe(task, func_call):
    try:
        from dbnd._core.decorator.func_task_call import TaskCallState, CALL_FAILURE_OBJ

        task._dbnd_call_state = TaskCallState(should_store_result=True)
        # this is the real run of the decorated function
        return run_dynamic_task(task)
    except Exception:
        if task and task._dbnd_call_state:
            if task._dbnd_call_state.finished:
                # if function was invoked and finished - than we failed in dbnd post-exec
                # just return invoke_result to user
                logger.warning("Error during dbnd post-exec, ignoring", exc_info=True)
                return task._dbnd_call_state.result
            if task._dbnd_call_state.started:
                # if started but not finished -> it was user code exception -> re-raise
                raise

        # not started - our exception on pre-exec, run user code
        logger.warning("Error during dbnd task-pre-execute, ignoring", exc_info=True)
        return func_call.invoke()
    finally:
        # we'd better clean _invoke_result to avoid memory leaks
        task._dbnd_call_state = None


def create_and_run_dynamic_task_safe(func_call):
    try:
        task = create_dynamic_task(func_call)
    except Exception:
        logger.warning("Failed during dbnd task-create, ignoring", exc_info=True)
        return func_call.invoke()

    return run_dynamic_task_safe(task=task, func_call=func_call)
