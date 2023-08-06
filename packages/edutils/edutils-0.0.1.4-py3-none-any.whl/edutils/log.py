__all__ = [
    'Logger'
]

"""
定义log
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from typing import List


class Logger:
    """
    日志类
    """
    FORMAT = "[%(levelname)s %(asctime)s %(filename)s:%(funcName)s:%(lineno)d] %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def init_logger(path: str, name: str = None, to_console: bool = False, is_debug: bool = False,
                    is_root_logger: bool = False, to_parent: bool = False,
                    size: int = 500, cnt: int = 4):
        """
        初始化日志对象 输入到文件 适用于单进程下多线程情况

        :param path: 日志文件完整路径 E:/pyworkspace18-10/entrances-control-worker/utils/helper.py
        :param name: 日志名
        :param to_console: 是否输出到控制台
        :param is_root_logger: 是否使用根日志
        :param to_parent: 是否将子logger传递给父logger
        :param is_debug: 是否设置日志级别为 DEBUG, 默认一律为INFO
        :param size: 文件大小 M
        :param cnt: 日志文件数 实际数为 cnt+1
        :return:
        """
        handlers_li = []

        # 滚动日志文件
        rotate_file_handler = RotatingFileHandler(
            path,
            maxBytes=size * 1024 * 1024,
            backupCount=cnt,
            encoding="utf8"
        )
        rotate_file_handler.setFormatter(logging.Formatter(
            fmt=Logger.FORMAT,
            datefmt=Logger.DATE_FORMAT
        ))
        handlers_li.append(rotate_file_handler)

        if to_console:
            # 日志输出到控制台handler
            stream_handler = logging.StreamHandler()  # 默认是sys.stderr
            stream_handler.setFormatter(logging.Formatter(
                fmt=Logger.FORMAT,
                datefmt=Logger.DATE_FORMAT
            ))
            handlers_li.append(stream_handler)

        if is_root_logger:
            logger = logging.getLogger()  # 不设值name 返回根日志
        elif name:
            logger = logging.getLogger(name)
        else:
            filename_and_ext: List[str] = os.path.basename(path).split(".")
            logger_name = filename_and_ext[0]
            logger = logging.getLogger(logger_name)

        if not to_parent:
            # to_parent=False 不允许子logger传递内容到父logger
            logger.propagate = False

        if is_debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        for handler in handlers_li:
            logger.addHandler(handler)
        return logger