#coding=utf-8

import os
import re
import time
import sys
import subprocess

from threading import Thread

aliveInfo = re.compile(r" Received = 1")
status = ("No response","Partial Response","Alive")


class IpAddr(Thread):
    def __init__(self, ip):
        Thread.__init__(self)
        self.ip = ip
        self.status = 0
        
    def run(self):
		ping_ok = []
		try:
			p = subprocess.Popen([r'./ping.sh',self.ip],stdout=subprocess.PIPE)
			result = p.stdout.read()
			Status = 0
			if result =='1\n':
				Status = 1
				print Status,self.ip,'----ping failed----'
			else:
				print Status,self.ip,'----ping success----'
		except:
			print self.ip
	
class LifeIp() :    
    def __init__(self) :
		self.pingList = []
		ip_conf_file = open("ip_conf.txt", 'r')
		for line in ip_conf_file :
			if line :
				conf_item = line.replace('\n', '').split(',')
				for i in conf_item:
					self.pingList.append(i)
	

    def getStatus(self) :
        for ip in self.pingList :
		    if ip:
				pingIp = IpAddr(ip)
				self.pingList.append(pingIp)
				pingIp.start()
                        
    def showStatus(self) :
        for pingIp in self.pingList :
            pingIp.join()
            print pingIp.ip + ' : ' + status[pingIp.status]

      
if __name__ == '__main__':
    print time.ctime()    
    ci = LifeIp()
    ci.getStatus() 
    #ci.showStatus()