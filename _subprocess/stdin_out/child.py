#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import json
import time


fwrite = open("message.txt", "w+")


def send2parent(msg):
    print(json.dumps(msg))
    sys.stdout.flush()


# reads lines and reconstructs newlines appropriately
def read_msg():
    msg = ""
    while True:
        line = sys.stdin.readline()
        if not line:
            raise Exception('Read EOF from stdin')
        if line[0:-1] == "end":
            break
        msg = msg + line
    return json.loads(msg[0:-1])
    # return msg[0:-1]


def run():
    count = 1
    while True:
        msg = read_msg()
        fwrite.write("%d: \n%s\n" % (count, msg))
        fwrite.flush()
        count += 1
        msg[count] = count
        send2parent(msg)

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        pass
    finally:
        fwrite.close()

