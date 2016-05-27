#coding=utf-8

import subprocess

def check_ip_ping():
	ping_ok = []
	pingList = []
	ip_conf_file = open("ip_conf.txt", 'r')
	for line in ip_conf_file :
		if line :
			conf_item = line.replace('\n', '').split(',')
			for i in conf_item:
				pingList.append(i)
	record = pingList
	for i in range(0,len(record)):
		p = subprocess.Popen([r'./ping.sh',record[i]],stdout=subprocess.PIPE)
		result = p.stdout.read()
		Status = 0
		if result =='1\n':
			Status = 1
			print i,record[i],'----ping failed----'
		else:
			ping_ok.append(record[i])
			print i,record[i],'----ping success----'
			
check_ip_ping()