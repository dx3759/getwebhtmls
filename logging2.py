#!/usr/bin/python
#-*- coding:utf-8 -*-

import logging
import threading
import Queue

#logging.basicConfig(level = logging.DEBUG,
#                   format = '%(asctime)s %(levelname)-8s %(message)s',
#                   datefmt = '%a,%d %b %Y %H:%M:%S',
#                   filename = '/tmp/myapp.log',
#                   filemode = 'w')

class logging2(threading.Thread):
	"""定义一个写日志的线程，调用logging写入文件"""
	A_Queue = Queue.Queue() #用来存放 日志队列

	def __init__(self):
		threading.Thread.__init__(self)
		self.name = 'logging2'

	def run(self):
		while 1:
			data = logging2.A_Queue.get()
			print 'data',data
			loglevel = data.keys()[0]
			content = data.values()[0]
			getattr(logging,loglevel)(conten)

def debug(content):
	logging2.A_Queue.put({'debug':content})

def info(content):
	logging2.A_Queue.put({'info':content})

def warning(content):
	logging2.A_Queue.put({'warning':content})

def error(content):
	logging2.A_Queue.put({'error':content})

def critical(content):
	logging2.A_Queue.put({'critical':content})

def init(levels,files):
	"""开始写日志线程"""
	if levels == 1:
		levels =  logging.DEBUG
	elif levels == 2:
		levels = logging.INGO
	elif levels == 3:
		levels = logging.WARNING
	elif levels == 4:
		levels = logging.ERROR
	elif levels == 5:
		levels = logging.CRITICAL
	logging.basicConfig(level = levels,format = '%(asctime)s %(levelname)-8s %(message)s',datefmt = '%a,%d %b %Y %H:%M:%S',filename = files,filemode = 'w')
	cc = logging2()
	cc.setDaemon(True)
	cc.start()


