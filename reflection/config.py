#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from ruamel.yaml import YAML


class Config(object):
    def __init__(self, filename):
        self.filename = filename
        self.yaml = YAML()
        self.cfg = dict()
        with open(filename, "rb") as f:
            self.cfg = self.yaml.load(f)

    def __setitem__(self, key, value):
        self.cfg[key] = value

    def __getitem__(self, item):
        # if item in self.cfg:
        #     return self.cfg[item]
        # else:
        #     return None           # 通过if判断item是否存在时在此处陷入死循环
        return self.cfg[item]

    def __delitem__(self, key):
        del self.cfg[key]

    def __repr__(self):
        return str(dict(self.cfg))

    def save(self):
        with open(self.filename, "w") as f:
            self.yaml.dump(self.cfg, f)


if __name__ == '__main__':
    conf = Config("config.yaml")
    conf["mode"] = "local"
    conf["dynamic"]["inherit"]["cls1"]["path"] = "1.1.1.1"
    # if "test" in conf:
    #     del conf["test"]

    # conf.save()

    print(conf)


