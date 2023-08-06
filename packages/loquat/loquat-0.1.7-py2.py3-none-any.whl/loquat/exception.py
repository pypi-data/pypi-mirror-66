class BaseError(Exception):
    """Base Error"""


class ArgumentError(BaseError):
    """Arguments error"""


class ConfigError(BaseError):
    """raise config error"""
