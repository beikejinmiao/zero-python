#!/usr/bin/env python
# -*- coding:utf-8 -*-


class A(object):
    def __init__(self, x1, x2, kw1="yes", kw2="yes2"):
        self.x1 = x1
        self.x2 = x2
        self.kw1 = kw1
        self.kw2 = kw2

    def prints(self):
        print(self.__dict__)

    def get_hash(self):
        print("__hash__: %s" % self.__hash__)


class B(object):
    def __init__(self, x1, x2, x3, kwb="no"):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.kwb = kwb

    def prints(self):
        print(self.__dict__)

    def get_class(self):
        print("__class__: %s" % self.__class__)


class C(object):
    def get_attr(self):
        print("dir(self): %s" % dir(self))


class Mix(B, A, C):
    def __init__(self, x1, x2, x3, kw1="yes", kwb="no"):
        super(Mix, self).__init__(x1, x2, x3)        # 只会初始化第一个类
        # A.__init__(self, x1, x2, kw1=kw1)
        # B.__init__(self, x1, x2, x3, kwb=kwb)

if __name__ == '__main__':
    mix = Mix("x1", "x2", "x3")
    print(Mix.__bases__)
    mix.prints()
    mix.get_hash()
    mix.get_class()
    mix.get_attr()

