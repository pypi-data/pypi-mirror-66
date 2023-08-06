import datetime
import enum

import attr

from dbnd._core.utils.timezone import make_aware, utcnow


RESULT_PARAM = "result"

CURRENT_DATETIME = utcnow()
CURRENT_TIME_STR = CURRENT_DATETIME.strftime("%Y%m%d_%H%M%S")
CURRENT_DATE = CURRENT_DATETIME.date()


class EnvLabel(object):  # env label
    dev = "dev"
    test = "test"
    staging = "stage"
    qa = "qa"
    prod = "prod"


class CloudType(object):
    local = "local"
    gcp = "gcp"
    aws = "aws"
    azure = "azure"


class TaskExecutorType(object):
    local = "local"


class OutputMode(object):
    regular = "regular"
    prod_immutable = "prod_immutable"


class _ConfigParamContainer(object):
    _type_config = True

    @classmethod
    def is_type_config(self, cls):
        # we can't use issubclass as there are "generic" types that will fail this check
        return getattr(cls, "_type_config", False)


class _TaskParamContainer(object):
    pass


class DescribeFormat(object):
    short = "short"
    long = "long"
    verbose = "verbose"


# Compute Types


class SparkClusters(enum.Enum):
    local = "local"
    dataproc = "dataproc"
    databricks = "databricks"
    emr = "emr"
    qubole = "qubole"


class ApacheBeamClusterType(object):
    local = "local"
    dataflow = "dataflow"


class ClusterPolicy(object):
    NONE = "none"
    CREATE = "create"
    KILL = "kill"
    EPHERMAL = "ephermal"

    ALL = [NONE, CREATE, KILL, EPHERMAL]


class EmrClient(object):
    LIVY = "livy"
    STEP = "step"


class TaskType(object):
    pipeline = "pipeline"
    python = "python"
    spark = "spark"
    pyspark = "pyspark"
    dataflow = "dataflow"
    docker = "docker"


class TaskRunState(enum.Enum):
    SCHEDULED = "scheduled"
    QUEUED = "queued"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

    CANCELLED = "cancelled"

    UPSTREAM_FAILED = "upstream_failed"
    SKIPPED = "skipped"
    UP_FOR_RETRY = "up_for_retry"

    @staticmethod
    def final_states():
        return TaskRunState.finished_states() | {
            TaskRunState.UPSTREAM_FAILED,
            TaskRunState.SKIPPED,
        }

    @staticmethod
    def final_states_str():
        return [s.value for s in TaskRunState.final_states()]

    @staticmethod
    def finished_states():
        return {TaskRunState.SUCCESS, TaskRunState.FAILED, TaskRunState.CANCELLED}

    @staticmethod
    def direct_fail_states():
        return {TaskRunState.FAILED, TaskRunState.CANCELLED}

    @staticmethod
    def states_lower_case():
        return [state.name.lower() for state in TaskRunState]


REUSED = "reused"


class RunState(enum.Enum):
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SHUTDOWN = "shutdown"
    CANCELLED = "cancelled"


class AlertStatus(enum.Enum):
    TRIGGERED = "TRIGGERED"
    RESOLVED = "RESOLVED"
    ACKNOWLEDGED = "ACKNOWLEDGED"


class SystemTaskName(object):
    driver_submit = "dbnd_driver_submit"
    driver = "dbnd_driver"
    task_submit = "dbnd_task_submit"

    driver_and_submitter = {driver_submit, driver}


@attr.s
class _DbndDataClass(object):
    def asdict(self, filter=None):
        return attr.asdict(self, recurse=False, filter=filter)


HEARTBEAT_DISABLED = make_aware(datetime.datetime.fromtimestamp(0))


class ParamValidation(enum.Enum):
    warn = "warn"
    error = "error"
    disabled = "disabled"


class DbndTargetOperationType(enum.Enum):
    init = "init"
    read = "read"
    write = "write"
    reuse = "reuse"
    log = "log"


class DbndTargetOperationStatus(enum.Enum):
    OK = "OK"
    NOK = "NOK"


class SystemMetrics(enum.Enum):
    Duration = "Duration"
    TotalCpuTime = "Total CPU Time"
    TotalWallTime = "Total Wall Time"
    ColdTotalCpuTime = "Cold Total CPU Time"
    ColdTotalWallTime = "Cold Total Wall Time"

    @staticmethod
    def duration_metrics():
        """Used to select metrics for removal during metrics re-generation"""
        return [
            s.value
            for s in [
                SystemMetrics.Duration,
                SystemMetrics.TotalCpuTime,
                SystemMetrics.TotalWallTime,
                SystemMetrics.ColdTotalCpuTime,
                SystemMetrics.ColdTotalWallTime,
            ]
        ]


class UpdateSource(enum.Enum):
    dbnd = "dbnd"
    airflow_monitor = "airflow_monitor"
    airflow_tracking = "airflow_tracking"

    def __eq__(self, other):
        if isinstance(other, UpdateSource):
            return self.value == other.value
        elif isinstance(other, str):
            return str(self) == other or str(self.value) == other

        return False
