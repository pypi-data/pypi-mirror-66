# coding=utf-8

"""
基于Tornado Log的logger实现.
"""
import logging
import logging.handlers
import os
import sys
from typing import Dict, Any, cast, Union, Optional

bytes_type = bytes
unicode_type = str
basestring_type = str

try:
    import colorama  # type: ignore
except ImportError:
    colorama = None

try:
    import curses
except ImportError:
    curses = None  # type: ignore

_TO_UNICODE_TYPES = (unicode_type, type(None))


def _unicode(value: Union[None, str, bytes]) -> Optional[str]:  # noqa: F811
    """Converts a string argument to a unicode string.

    If the argument is already a unicode string or None, it is returned
    unchanged.  Otherwise it must be a byte string and is decoded as utf8.
    """
    if isinstance(value, _TO_UNICODE_TYPES):
        return value
    if not isinstance(value, bytes):
        raise TypeError("Expected bytes, unicode, or None; got %r" % type(value))
    return value.decode("utf-8")


def _stdout_supports_color() -> bool:
    try:
        if hasattr(sys.stderr, "isatty") and sys.stderr.isatty():
            if curses:
                curses.setupterm()
                if curses.tigetnum("colors") > 0:
                    return True
            elif colorama:
                if sys.stderr is getattr(
                        colorama.initialise, "wrapped_stderr", object()
                ):
                    return True
    except Exception:
        # Very broad exception handling because it's always better to
        # fall back to non-colored logs than to break at startup.
        pass
    return False


def _safe_unicode(s: Any) -> str:
    try:
        return _unicode(s)
    except UnicodeDecodeError:
        return repr(s)


class LogFormatter(logging.Formatter):
    """
    Log formatter used in Tornado.
    """

    DEFAULT_FORMAT = "%(color)s%(asctime)s %(levelname)s --- [%(process)d %(threadName)s] %(name)s - " \
                     "%(filename)s %(lineno)d : %(end_color)s %(message)s"
    DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    DEFAULT_COLORS = {
        logging.DEBUG: 4,  # Blue
        logging.INFO: 2,  # Green
        logging.WARNING: 3,  # Yellow
        logging.ERROR: 1,  # Red
    }

    def __init__(
            self,
            fmt: str = DEFAULT_FORMAT,
            datefmt: str = DEFAULT_DATE_FORMAT,
            color: bool = True,
            colors: Dict[int, int] = DEFAULT_COLORS,
    ) -> None:
        r"""
        :arg bool color: Enables color support.
        :arg str fmt: Log message format.
          It will be applied to the attributes dict of log records. The
          text between ``%(color)s`` and ``%(end_color)s`` will be colored
          depending on the level if color support is on.
        :arg dict colors: color mappings from logging level to terminal color
          code
        :arg str datefmt: Datetime format.
          Used for formatting ``(asctime)`` placeholder in ``prefix_fmt``.
        """
        logging.Formatter.__init__(self, datefmt=datefmt)
        self._fmt = fmt

        self._colors = {}  # type: Dict[int, str]
        if color and _stdout_supports_color():
            if curses is not None:
                fg_color = curses.tigetstr("setaf") or curses.tigetstr("setf") or b""

                for levelno, code in colors.items():
                    # Convert the terminal control characters from
                    # bytes to unicode strings for easier use with the
                    # logging module.
                    self._colors[levelno] = unicode_type(
                        curses.tparm(fg_color, code), "ascii"
                    )
                self._normal = unicode_type(curses.tigetstr("sgr0"), "ascii")
            else:
                # If curses is not present (currently we'll only get here for
                # colorama on windows), assume hard-coded ANSI color codes.
                for levelno, code in colors.items():
                    self._colors[levelno] = "\033[2;3%dm" % code
                self._normal = "\033[0m"
        else:
            self._normal = ""

    def format(self, record: Any) -> str:
        try:
            message = record.getMessage()
            assert isinstance(message, basestring_type)  # guaranteed by logging
            record.message = _safe_unicode(message)
        except Exception as e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)

        record.asctime = self.formatTime(record, cast(str, self.datefmt))

        if record.levelno in self._colors:
            record.color = self._colors[record.levelno]
            record.end_color = self._normal
        else:
            record.color = record.end_color = ""

        formatted = self._fmt % record.__dict__

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            lines = [formatted.rstrip()]
            lines.extend(_safe_unicode(ln) for ln in record.exc_text.split("\n"))
            formatted = "\n".join(lines)
        return formatted.replace("\n", "\n    ")


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


class ExactLogLevelFilter(logging.Filter):
    def __init__(self, level):
        self.__level = level

    def filter(self, log_record):
        return log_record.levelno == self.__level


def _pretty_logging(options: Dict, logger: logging.Logger) -> None:
    # 如果没有设置日志级别
    if options['logging_level'] is None or options['logging_level'].lower() == "none":
        return

    if options['log_file_path']:
        rotate_mode = options['log_rotate_mode']
        if rotate_mode == "size":
            channel = logging.handlers.RotatingFileHandler(
                filename=options['log_file_path'],
                maxBytes=options['log_file_max_size'],
                backupCount=options['log_file_num_backups'],
                encoding="utf-8",
            )  # type: logging.Handler
        elif rotate_mode == "time":
            channel = logging.handlers.TimedRotatingFileHandler(
                filename=options['log_file_path'],
                when=options['log_rotate_when'],
                interval=options['log_rotate_interval'],
                backupCount=options['log_file_num_backups'],
                encoding="utf-8",
            )
        else:
            error_message = (
                    'The value of log_rotate_mode option should be "size" or "time", not "%s".' % rotate_mode
            )
            raise ValueError(error_message)
        channel.setFormatter(LogFormatter(color=False))
        # 添加通过级别过滤
        if options['log_to_level_files']:
            channel.addFilter(ExactLogLevelFilter(logging.getLevelName(options['logging_level'])))
        logger.addHandler(channel)

    if options['log_to_stderr'] or (options['log_to_stderr'] is False and not logger.handlers):
        # Set up color if we are in a tty and curses is installed
        channel = logging.StreamHandler()
        channel.setFormatter(LogFormatter())
        logger.addHandler(channel)


def _log_level_files(default_options, logger):
    """对不同级别的日志分文件记录"""

    log_level_path = {
        'DEBUG': os.path.join(default_options['log_file_path'], 'debug/debug.log'),
        'INFO': os.path.join(default_options['log_file_path'], 'info/info.log'),
        'WARN': os.path.join(default_options['log_file_path'], 'warn/warn.log'),
        'ERROR': os.path.join(default_options['log_file_path'], 'error/error.log')
    }
    log_levels = log_level_path.keys()
    for level in log_levels:
        log_path = os.path.abspath(log_level_path[level])
        if not os.path.exists(os.path.dirname(log_path)):
            os.makedirs(os.path.dirname(log_path))

        default_options.update({'log_file_path': log_path, 'logging_level': level})

        _pretty_logging(options=default_options, logger=logger)


def initialize_logging(logger: logging.Logger = None, options: Dict = None):
    """
    :param logger:
    :param options:
        {
        'log_file_path':'日志文件路径。如果log_level_files==True则为目录，否则为文件路径',
        'logging_level':'日志级别（DEBUG/INFO/WARN/ERROR）',
        'log_to_level_files':'是否按照日志的级别分别记录。默认为False',
        'log_to_stderr':'是否将日志输出发送到stream（如果可能的话，将其着色）。如果未配置其他日志记录，则默认使用stream。',
        'log_file_max_size':'每个文件最大的大小，默认：100 * 1000 * 1000',
        'log_file_num_backups':'要保留的日志文件数',
        'log_rotate_when':'时间间隔的类型（'S', 'M', 'H', 'D', 'W0'-'W6'）',
        'log_rotate_interval':'TimedRotatingFileHandler的interval值',
        'log_rotate_mode':'类型（size/time）'
        }
    :return:
    """

    if logger is None:
        logger = logging.getLogger()

    if options is None:
        options = {}

    default_options = {
        'log_file_path': '',
        'logging_level': 'DEBUG',
        'log_to_level_files': False,
        'log_to_stderr': True,
        'log_file_max_size': 100 * 1000 * 1000,
        'log_file_num_backups': 30,
        'log_rotate_when': 'D',
        'log_rotate_interval': 1,
        'log_rotate_mode': 'time'
    }
    default_options.update(options)

    # 设置日志级别
    logger.setLevel(getattr(logging, default_options['logging_level'].upper()))

    if default_options['log_to_level_files']:
        _log_level_files(default_options, logger)
    else:
        _pretty_logging(options=default_options, logger=logger)
