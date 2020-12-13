#!/usr/bin/python3

import os, signal

for line in os.popen("ps -ef | grep pr2.py | grep -v grep"):
    fields = line.split()
    pid = fields[1]
    print("pid = " + str(pid))
    os.kill(int(pid), signal.SIGKILL)
