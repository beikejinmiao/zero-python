#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
父子进程使用'标准输入输出'通信
模仿Storm multilang调用Python程序：storm.py
"""
import json
import time
from subprocess import Popen, PIPE

from libs.timer import SimpleTimer

count = 1


proc = Popen(["python", "child.py"], stdin=PIPE, stdout=PIPE, stderr=PIPE)


def send2child():
    global count
    msg2child = {"name": "your mama" + str(count)}
    # print(json.dumps(msg2child))
    # print("end")
    # sys.stdout.flush()
    proc.stdin.write(json.dumps(msg2child) + "\n")
    proc.stdin.write("end\n")
    proc.stdin.flush()
    count += 1


def read_msg():
    print(proc.stdout.readline())


def run():
    timer = SimpleTimer(1, 5, send2child)
    timer.daemon = True
    timer.start()
    while True:
        time.sleep(0.7)
        send2child()
        read_msg()


if __name__ == '__main__':
    run()



