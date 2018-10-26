#!/usr/bin/env python
# -*- coding:utf-8 -*-
from reflection.config import Config


class Object(object):
    """
    定义Object类，解决"TypeError: __bases__ assignment: 'B' deallocator differs from 'object'" 问题
    """
    pass


def importc(path):
    """
    import class of the path
    :param path:
    :return:
    """
    items = path.split(".")
    mod_path = ".".join(items[:-1])
    cls_name = items[-1]
    mod = __import__(mod_path, fromlist=[cls_name])
    return getattr(mod, cls_name)


def assemble(ancestors):
    """
    assemble new class from setting
    :param ancestors:
    Setting Example:
    # {
    #     "the.class.path": {
    #         "args": ["a1", "a2"],
    #         "kwargs": {
    #             "kw1": "Hello",
    #             "kw2": "World"
    #         }
    #     }
    # }
    :return:
    """
    mods = dict()       # key: class; value: mod args

    # class DynamicMix(object): # 发生错误：TypeError: __bases__ assignment: 'B' deallocator differs from 'object'
    class DynamicMix(Object):
        def __init__(self):
            for mod in mods:
                params = mods.get(mod)
                if params:
                    if "args" in params and "kwargs" in params:
                        mod.__init__(self, *params.get("args"), **params.get("kwargs"))
                    elif "args" in params:
                        mod.__init__(self, *params.get("args"))
                    elif "kwargs" in params:
                        mod.__init__(self, **params.get("kwargs"))
                    else:
                        mod.__init__(self)
                else:
                    mod.__init__(self)

    for cls_path in ancestors:
        mod = importc(cls_path)
        mods[mod] = ancestors[cls_path]     # args
        if mod not in DynamicMix.__bases__:
            DynamicMix.__bases__ = (mod, ) + DynamicMix.__bases__

    return DynamicMix


def load_config():
    """
    load base classes from yaml
    :return:
    """
    config = Config("config.yaml")
    # print(config)
    class_setting = dict()
    for item in config["dynamic"]["inherit"].values():
        cls_path = item["path"]
        del item["path"]
        class_setting[cls_path] = dict(item)

    return class_setting


if __name__ == '__main__':
    classes = load_config()
    # classes = {
    #     "reflection.test_class.A": {
    #         "args": ["a1", "a2"],
    #         "kwargs": {
    #             "kw1": "yesyes",
    #             "kw2": "yesyes2"
    #         }
    #     },
    #     "reflection.test_class.B": {
    #         "args": ["b1", "b2", "b3"],
    #         "kwargs": {
    #             "kwb": "nono",
    #             # "n2": "no2"
    #         }
    #     },
    #     "reflection.test_class.C": None,
    # }

    Target = assemble(classes)
    print(Target.__bases__)
    target = Target()
    target.prints()
    target.get_hash()
    target.get_class()
    target.get_attr()


