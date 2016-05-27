#!/usr/bin/python
#-*- coding: UTF-8 -*-
# cheungmine
import os
import sys

import time
import datetime

import codecs

import optparse
import ConfigParser

import signal
import subprocess
import select

import logging  
from logging.handlers import RotatingFileHandler

## log settings: SHOULD BE CONFIGURED BY config
LOG_PATH_FILE = "./my_service_mgr.log"
LOG_MODE = 'a'
LOG_MAX_SIZE = 4*1024*1024 # 4M per file
LOG_MAX_FILES = 4          # 4 Files: my_service_mgr.log.1, printmy_service_mgrlog.2, ...  
LOG_LEVEL = logging.DEBUG  

LOG_FORMAT = "%(asctime)s %(levelname)-10s[%(filename)s:%(lineno)d(%(funcName)s)] %(message)s"  

handler = RotatingFileHandler(LOG_PATH_FILE, LOG_MODE, LOG_MAX_SIZE, LOG_MAX_FILES)
formatter = logging.Formatter(LOG_FORMAT)
handler.setFormatter(formatter)

Logger = logging.getLogger()
Logger.setLevel(LOG_LEVEL)
Logger.addHandler(handler) 


# color output 
#
pid = os.getpid()


def print_error(s):
    print '\033[31m[%d: ERROR] %s\033[31;m' % (pid, s)

def print_info(s):
    print '\033[32m[%d: INFO] %s\033[32;m' % (pid, s)

def print_warning(s):
    print '\033[33m[%d: WARNING] %s\033[33;m' % (pid, s)
    

def start_child_proc(command, merger):
    try:
        if command is None:
            raise OSError, "Invalid command "
        child = None
        
        if merger is True:
            #merge stout and stderr
            child = subprocess.Popen(command,
                stderr=subprocess.STDOUT,
                stdout=subprocess.PIPE)
        else:
            child = subprocess.Popen(command,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE)
            
        return child
    
    except subprocess.CalledProcessError:
        pass # handle errors in the called executable
    except OSError:
        pass # executable not found

    raise OSError, "Failed to run command!"
    
def run(command):
    print_info("start child process with command" + ''.join(command))
    Logger.info("start child process with command" + ''.join(command))
    
    child = start_child_proc(command, True)
    line = ''
    
    failover = 0
    
    while True:
        while child.poll() != None:
            failover = failover+1
            print_warning("child process shutdow with returncode: " + str(child.returncode))
            Logger.critical("child process shutdow with returncode: " + str(child.returncode))
            
            print_warning("restart child process again, times=%d" % failover)
            Logger.info("restart child process again, times=%d" % failover)
            child = start_child_proc(command, True)
            
            
        ch = child.stdout.read(1)
        if ch !='' and ch!='\n':
            line += ch
            
        if ch == '\n':
            print_info(line)
            Logger.info(line)
            line=''
   
            
    Logger.exception("!!!should never run to this!!!")  
 
if __name__ == "__main__":
    run(["php","./aa.php"])