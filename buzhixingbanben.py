#!/usr/bin/python
#-*- coding:utf8-*-

#"for get all the html"


import BeautifulSoup,re,Queue
import urllib,urllib2
import optparse
import threading
import logging2
import doctest
import threading2
import time
import sqlite3

#I think i will get all the options and args
parser = optparse.OptionParser()
parser.add_option('-u','--urls', dest = "urls",help = "the urls ",metavar = "URLS")
parser.add_option('-d','--deep',type = 'int', dest = "deep",help = "the deep", metavar = "DEEP",default = 0)
parser.add_option('-f' , '--file',type = 'string' , dest = 'logfile', help = "the file is to record the logs", metavar = "LOGFILE",default = '/tmp/tmp.log')
parser.add_option('-l','--loglevel',type = 'int' ,dest = 'loglevel',help = 'for loglevel(1-5),the number is big,the level is heigh',metavar = 'LOGLEVEL(1-5)',default = 1)
parser.add_option('--testself',dest = 'test',help = 'self test or test myself')
parser.add_option('-t','--thread',type = 'int',dest = 'number' ,help = 'the threadnumber',metavar = 'NUMBER',default =10)
parser.add_option('--dbfile',dest = 'dbfile' ,help = 'the db file path',metavar = 'DBFILE',default ='test.db')
parser.add_option('--key',dest = 'key' ,help = 'the key is here,if you want a chinese,you must be utf-8 in your system,or change the code.',metavar = 'KEY',default ='.*')
options,args = parser.parse_args()
print "all the optins",options
print "all the args",args

#workQueue is ready to do.resultQueue is having done.alldone is finish task
workQueue = Queue.Queue()
resultQueue = Queue.Queue()
alldoneQueue = Queue.Queue()


#logging2 初始化，以后可以使用logging2来插入log
logging2.init(options.loglevel,options.logfile)

#decode the key 
keyinsys = options.key.decode('utf-8')

#sqlite3 here
#conn = sqlite3.connect(options.dbfile)
#cor = conn.cursor()
#cor.execute('create table if not exists keyofhtml( id integer primary key,urls text,key text,htmls text)')


def analyseurl(urls):
	"""
	功能：分析urls,返回列表格式的字典

	字典格式：{'name':names,'urls':url}
	这里将符合要求的页面信息插入数据库,还包括日志信息
	还包括 key的判断？？？？

	mm = re.compile('''\<a.*?href\=['|"](http\w*?)['|"].*?\>''')
	"""
	returns=[]
	html = urllib2.urlopen(urls,timeout=50)
	#try:
	if True:
		data = html.read()
		if data:
			print 'data done'
		conn = sqlite3.connect(options.dbfile)
		cor = conn.cursor()
		cor.execute('create table if not exists keyofhtml( id integer primary key,urls text,key text,htmls text)')
		print 0,'0'
		rr = re.compile(r"""content\=["|']text\/html['|"]\W*?\;\W*?charset\=['|"](\w*?)["|']""")
		m = rr.search(data)
		print 1,'1'
		if m:
			print 2
			code = m.group(1)
		if code:
			print 3
			data = data.decode(code)
		print 4
		rekey = re.compile('.*')
		good = rekey.search(data)
		if good:
			print 'good'
			data = data.replace("'",'"')#纠结的单引号怎么处理？
			sqls = "insert into keyofhtml(urls,key,htmls) values('%s','%s','%s')"
			cor.execute(sqls%(urls,keyinsys,data))
			conn.commit()
			print 'donessss'
		conn.close()
		logging2.debug('reading '+urls)
		logging2.info('what should i write here')
		logging2.warning('a warning here')
		logging2.error('a error test here')
		logging2.critical('what is a critical??')
		#print 'reading'
	#except:
		#print 'error'
		#logging2.error('error ong reading '+urls)
	print '.....'
	print urls
	print keyinsys
	print data[:100]
	print '??'
	soup = BeautifulSoup.BeautifulSoup(data)
	temp = soup.findAll('a',href=re.compile(r'http.*'))#为什么不直接用re匹配a标签
	logging2.debug('analysing '+urls)
	#print 'analysing'
	for tt in temp:
		hrefs = tt['href']#have?
		if hrefs.startswith('http'):
			if tt.string:#span?????
				returns.append({'name':tt.string,'urls':hrefs})
			else:
				returns.append({'name':'NoName','urls':hrefs})
		else:
			continue
	return returns


def main():
	i = 0
	th = threading2.ThreadPool(workQueue,resultQueue,options.number)
	td = threading2.MyThread2(workQueue,resultQueue,i,10)

	while i <= options.deep:
		if i == 0:
			th.add_jobs(analyseurl,options.urls)
			i += 1
			th.wait_for_done()
			td.deep = i
		else:#这里还有问题,现在为方案一
			if resultQueue.qsize():#当前任务队列完成，结果队列满了
				while resultQueue.qsize():#有任务，取出任务
					t = resultQueue.get()
					alldoneQueue.put(t)
					th.add_jobs(analyseurl,t['urls'])
				###如何新建线程呢
				th.createThreadPool(options.number)
				th.wait_for_done()
				i += 1
				td.deep = i
	if resultQueue.qsize():
		#print 'done and result to alldone'
		while resultQueue.qsize():
			t = resultQueue.get()
			alldoneQueue.put(t)
	print '干完了，结束'
	return 0

if __name__ == '__main__':
	#analyseurl('http://www.baidu.com')
	main()
	print 'alldone',alldoneQueue.qsize()
