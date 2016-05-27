#!/usr/bin/python
#coding=utf-8

import subprocess

status = ''

#child = subprocess.Popen(["ping","-c","5","www.hao123.com"])
child = subprocess.Popen(["ping","-c","5","www.hao.com"])
out = child.communicate()
print  out
