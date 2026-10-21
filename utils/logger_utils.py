"""
日志配置模块

提供全局彩色日志对象，支持项目级初始化。
"""
import logging
import colorlog

# 初始化全局日志对象
logger = logging.getLogger()

# 日志格式常量
_LOG_FORMAT = '%(log_color)s%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s'
_LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
_LOG_COLORS = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}


def _create_colored_handler() -> logging.Handler:
    """创建并返回彩色日志处理器。"""
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        _LOG_FORMAT,
        datefmt=_LOG_DATEFMT,
        log_colors=_LOG_COLORS
    ))
    return handler


# 模块加载时配置默认处理器
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    logger.addHandler(_create_colored_handler())


def configure_project_logging() -> logging.Logger:
    """
    初始化/配置项目全局日志（彩色输出）。

    幂等设计：可重复调用，仅在无处理器时添加。

    Returns:
        logging.Logger: 配置完成的日志对象
    """
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        logger.addHandler(_create_colored_handler())
    return logger
