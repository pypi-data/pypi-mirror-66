__all__ = [
    'set_default',
    'MultiDict'
]

"""
额外工具
"""

def set_default(obj):
    """
    用于json序列化  在数据中存在set() 将其转化为 list()
        data = json.dumps(data, default=helper.set_default, ensure_ascii=False,
                          indent=4)
    :param obj:
    :return:
    """
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


class MultiDict(dict):
    """
    多层级自动赋值字典 -> item['20161101']["age"]["444"] = 2
    附1:
        dict 只能单层级赋值 item['20161101'] = 2
        defaultdict 只能双层级赋值 item['20161101']["age"] = 2

    附2：
        实现多层级自动赋值 除了可以重载__getitem__魔术方法，也可以实现__missing__魔术方法（择其一就行）
        例：
            def __missing__(self, key):
                value = self[key] = type(self)()
                return value
    """

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value