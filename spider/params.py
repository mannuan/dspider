# -*- coding:utf-8 -*-

PROJECT_HEALTH = ['health','warning','error']

PROJECT_STATUS = ['stop','start']

PROJECT_SUCCESS = 'ok'

SPIDERPY_PROCESS_CMD = 'ps -ax | grep \'python run_spider.py %s .*\' | sed \'/grep/d\' | awk \'{print $1}\''

SPIDERPY_START_CMD = 'gnome-terminal -e \"python run_spider.py %s %s %s %s\"'

SPIDER_LOGS_DIR = './logs/log_%s.txt'