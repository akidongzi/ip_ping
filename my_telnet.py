#coding=utf-8

import os
import re
import time
import sys
import subprocess

from threading import Thread 

status = ("No response", " Partial response", "|Alive")


class IpAddr(Thread):
	def __init__(self, ip):
		Thread.__init__(self)
		self.ip = ip
		self.status = 0
	
	def run(self):
		ping_ok = []
		try:
			p = subprocess.Popen([r'./ping.sh', self.ip], stdout =subprocess.PIPE)
			result = p.stdout.read()
			Status = 0
			if resultl == '1\n':
				Status = 1
				print Status,self.ip,'----ping failed ------'
			else:
				print Status,self.ip,'----ping success-------'
				
		except Exception, e:
			print self.ip