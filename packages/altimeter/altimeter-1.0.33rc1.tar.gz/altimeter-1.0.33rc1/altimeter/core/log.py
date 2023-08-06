"""Provides a class Logger with methods for logging."""
from contextlib import contextmanager
from dataclasses import dataclass
import logging
import os
import sys
import threading
from typing import cast, Any, Dict, List, Tuple, Type, Union

import structlog


@dataclass(frozen=True)
class EventName:
    """Dataclass for log event names.

    Args:
        name: name of this event
    """

    name: str


class LogEventMeta(type):
    """Metaclass for LogEvents. This allows EventNames to specified in subclasses of BaseLogEvent
    as empty typed variables e.g.

        AuthToAccountStart: EventName

    Rather than requiring

        AuthToAccountStart: EventName("AuthToAccountStart")
    """

    def __new__(
        mcs, name: str, bases: Tuple[Type, ...], namespace: Dict[str, Any]
    ) -> "LogEventMeta":
        for annotation in namespace.get("__annotations__", []):
            namespace[annotation] = EventName(annotation)
        return cast(LogEventMeta, super().__new__(mcs, name, bases, namespace))


@dataclass(frozen=True)
class BaseLogEvent(metaclass=LogEventMeta):
    """Base class for LogEvent classes"""


@dataclass(frozen=True)
class LogEvent(BaseLogEvent):
    """Contains EventNames for logging."""

    AuthToAccountStart: EventName
    AuthToAccountEnd: EventName
    AuthToAccountFailure: EventName

    GraphLoadedSNSNotificationStart: EventName
    GraphLoadedSNSNotificationEnd: EventName

    MetadataGraphUpdateStart: EventName
    MetadataGraphUpdateEnd: EventName

    NeptuneLoadStart: EventName
    NeptuneLoadEnd: EventName
    NeptuneLoadPolling: EventName
    NeptuneLoadError: EventName

    PruneNeptuneGraphStart: EventName
    PruneNeptuneGraphEnd: EventName
    PruneNeptuneGraphError: EventName
    PruneNeptuneGraphSkip: EventName

    PruneNeptuneGraphsStart: EventName
    PruneNeptuneGraphsEnd: EventName
    PruneNeptuneGraphsError: EventName

    PruneNeptuneMetadataGraphStart: EventName
    PruneNeptuneMetadataGraphEnd: EventName

    ReadFromFSStart: EventName
    ReadFromFSEnd: EventName

    ReadFromS3Start: EventName
    ReadFromS3End: EventName

    ScanResourceTypeStart: EventName
    ScanResourceTypeEnd: EventName

    WriteToFSStart: EventName
    WriteToFSEnd: EventName

    WriteToS3Start: EventName
    WriteToS3End: EventName


class Singleton(type):
    """Singleton Metaclass"""

    _instances: Dict[Type[Any], Any] = {}

    def __call__(cls, *args: Any, **kwargs: Union[int, str, Dict]) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


LoggableTypes = Union[int, str, Dict]

LOGGER_STACK = threading.local()


def _get_loggers() -> List[structlog.BoundLogger]:
    if not hasattr(LOGGER_STACK, "LOGGERS"):
        LOGGER_STACK.LOGGERS = []
    return LOGGER_STACK.LOGGERS


class Logger(metaclass=Singleton):
    """Logger singleton.  Provides contextmanager 'bind' which can be use to bind
    keys to the logger using 'with' syntax, they will be removed from the logger
    in subsequent calls."""

    def __init__(self, log_tid: bool = True) -> None:
        self._log_tid = log_tid
        log_processors = [
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
        ]

        if os.environ.get("DEV_LOG", None):
            log_processors.append(structlog.dev.ConsoleRenderer(colors=True, force_colors=True))
        else:
            log_processors.append(structlog.processors.JSONRenderer(sort_keys=True))

        structlog.configure(
            logger_factory=structlog.stdlib.LoggerFactory(), processors=log_processors
        )

        root = logging.getLogger()
        if root.handlers:
            for handler in root.handlers:
                root.removeHandler(handler)

        logging.basicConfig(
            level=os.environ.get("LOG_LEVEL", "INFO"), stream=sys.stdout, format="%(message)s"
        )
        logging.getLogger("botocore").setLevel(logging.ERROR)

    def _get_current_logger(self) -> structlog.BoundLogger:
        loggers = _get_loggers()
        if not loggers:
            logger = structlog.get_logger()
            if self._log_tid:
                logger = logger.bind(tid=threading.get_ident())
            loggers.append(logger)
        return loggers[-1]

    def debug(self, event: EventName, **kwargs: LoggableTypes) -> None:
        """Create DEBUG level log entry.

        Args:
            event: EventName object for this event
            kwargs: log event k/vs
        """
        self._get_current_logger().debug(event=event.name, **kwargs)

    def info(self, event: EventName, **kwargs: LoggableTypes) -> None:
        """Create INFO level log entry.

        Args:
            event: EventName object for this event
            kwargs: log event k/vs
        """
        self._get_current_logger().info(event=event.name, **kwargs)

    def warn(self, event: EventName, **kwargs: LoggableTypes) -> None:
        """Create WARN level log entry.

        Args:
            event: EventName object for this event
            kwargs: log event k/vs
        """
        self._get_current_logger().warn(event=event.name, **kwargs)

    def warning(self, event: EventName, **kwargs: LoggableTypes) -> None:
        """Create WARN level log entry.

        Args:
            event: EventName object for this event
            kwargs: log event k/vs
        """
        self._get_current_logger().warning(event=event.name, **kwargs)

    def err(self, event: EventName, **kwargs: LoggableTypes) -> None:
        """Create ERROR level log entry.

        Args:
            event: EventName object for this event
            kwargs: log event k/vs
        """
        self._get_current_logger().err(event=event.name, **kwargs)

    def error(self, event: EventName, **kwargs: LoggableTypes) -> None:
        """Create ERROR level log entry.

        Args:
            event: EventName object for this event
            kwargs: log event k/vs
        """
        self._get_current_logger().error(event=event.name, **kwargs)

    @contextmanager
    def bind(self, **bindings: LoggableTypes) -> structlog.BoundLogger:
        """Context manager to bind a set of k/vs to the logger.  The k/vs will be removed
        when the with block exits."""
        new_logger = self._get_current_logger().bind(**bindings)
        loggers = _get_loggers()
        loggers.append(new_logger)
        try:
            yield
        finally:
            loggers.pop()
