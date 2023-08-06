__all__ = [
    'get_now_time',
    'convert_str_to_stamp',
    'convert_stamp_to_str',
]

"""
时间相关处理
"""
import datetime
import time


def get_now_time(fmt="%Y-%m-%d %H:%M:%S") -> str:
    """返回当前时间字符串格式"""
    return datetime.datetime.now().strftime(fmt)


def convert_str_to_stamp(dt_str: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> int:
    """
    将时间字符串转时间戳
    :param str dt_str: 时间格式字符串 "2019-09-17 17:55:34"
    :param str fmt: 时间格式字符串模板
    :return: int 10位int型时间戳
    """
    return int(time.mktime(time.strptime(dt_str, fmt)))


def convert_stamp_to_str(stamp: float, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    将时间戳转字符串
    :param stamp: 时间戳  传10位的int或float都行
    :param fmt: 时间格式字符串模板
    :return:
    """
    return time.strftime(fmt, time.localtime(stamp))


def convert_dt_to_str(dt: datetime.datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    数据库查出的datetime 转格式化字符串
    :param datetime.datetime dt: datetime格式数据
    :param str fmt: 时间格式字符串模板
    :return:
    """
    return dt.strftime(fmt)


