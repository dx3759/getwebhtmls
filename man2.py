#!/usr/bin/python
#-*- coding:utf8-*-

#"for get all the html"


import BeautifulSoup,re,Queue
import urllib,urllib2
import optparse
import threading
import logging
import doctest
import threading2


#I think i will get all the options and args
parser = optparse.OptionParser()
parser.add_option('-u','--urls', dest = "urls",help = "the urls ",metavar = "URLS")
parser.add_option('-d','--deep',type = 'int', dest = "deep",help = "the deep", metavar = "DEEP",default = 0)
parser.add_option('-f' , '--file',type = 'string' , dest = 'logfile', help = "the file is to record the logs", metavar = "LOGFILE",default = '/tmp/tmp.log')
parser.add_option('-l','--loglevel',type = 'int' ,dest = 'loglevel',help = 'for loglevel(1-5),the number is big,the level is heigh',metavar = 'LOGLEVEL(1-5)',default = 1)
parser.add_option('--testself',dest = 'test',help = 'self test or test myself')
parser.add_option('-t','--thread',type = 'int',dest = 'number' ,help = 'the threadnumber',metavar = 'NUMBER',default =10)
parser.add_option('--dbfile',dest = 'filepath' ,help = 'the db file path',metavar = 'DBFILE',default ='test.db')
options,args = parser.parse_args()
print "all the optins",options
print "all the args",args

#workingQueue is ready to do.resultQueue is having done.
workingQueue = Queue.Queue()
resultQueue = Queue.Queue()


def analyseurl(urls):
	"""
	功能：分析urls,返回列表格式的字典

	字典格式：{'name':names,'urls':url}
	"""
	returns=[]
	print urls
	html = urllib2.urlopen(urls,timeout=30)
	try:
		data = html.read()
		rr = re.compile(r"""content\=["|']text\/html\;charset\=(\w*?)["|']""")
		m = rr.search(data)
		if m:
			code = m.group(1)
			print 'code=',code###
		if code:
			data = data.decode(code)
		print 'reading'
		print data[:1000]
	except:
		print 'error on reading'
	soup = BeautifulSoup.BeautifulSoup(data)
	temp = soup.findAll('a',href=re.compile(r'http.*'))
	print 'analysing'
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
	pass




if __name__ == '__main__':
	#analyseurl('http://www.baidu.com')
	pass
