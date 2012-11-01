#!/usr/bin/python
#-*- coding:utf-8 -*-
import threading
import Queue
import sys,time
import re
import urllib2

class MyThread(threading.Thread):
	"""This is  for running"""
	def __init__(self,workQueue,resultQueue,timeout = 30):
		threading.Thread.__init__(self)

		self.timeout = timeout
		self.setDaemon(True)
		self.workQueue = workQueue
		self.resultQueue = resultQueue
		self.start()

	def run(self):
		"""get and run and put"""
		try:
			callable , args = self.workQueue.get(timeout = self.timeout)
		#我们要执行的任务
			res = callable(args)#res为列表
			if res:
				for temp in res:
					self.resultQueue.put(temp)#以什么格式放入呢
		except Queue.Empty:#队列为空时，结束还是等待呢
			pass
		except:
			self.raise_exc(SystemExit)

class MyThread2(threading.Thread):
	"""this is for print the schedule"""
	def __init__(self,work,result,deep,sleeptime):
		self.time = 0
		self.work = work
		self.result = result
		self.deep = deep
		self.stime = sleeptime
		self.start()

	def run(self):
		while True:
			if self.time == 0:
				print '时间    深度    当前完成    待完成'
				self.time = 1
			else:
				print time.ctime,'    ',
				print self.deep,'   ',
				print self.result.qsize,'   ',
				print self.work.qsize
			if self.work.qsize == 0:
				self.raise_exc(SystemExit)
			time.sleep(self.stime)


class  ThreadPool(object):
	def __init__(self, workQueue,resultQueue, num_of_threads = 10):
		super(ThreadPool , self).__init__(self)
		self.workQueue = workQueue
		self.resultQueue = resultQueue
		self.thread =[]
		self.__createThreadPool(num_of_threads)

	def __createThreadPool( self, num_of_threads):
		""" 新建线程，并准备执行"""
		for i in range( num_of_threads):
			thread = MyThread(self.workQueue,self.resultQueue)
			self.thread.append(thread)
		
	def wait_for_complete(self):
		"""线程完成"""
		pass

	def add_jobs(self,callable,args):
		"""添加工作到工作队列"""
		self.workQueue.put((callable,args))

def test_job(url):
	html = urllib2.urlopen(url)
	data = html.read()
	rr = re.compile(r"""content\=["|']text\/html\;charset\=(\w*?)["|']""")
	m = rr.search(data)
	if m:
		code = m.group(1)
		print 'code=',code###
	if code:
		print data[:1000]
		data = data.decode(code)
		print data[:1000]
		print type(data)

if __name__ =='__main__':
	test_job('http://www.baidu.com')

