#!/usr/bin/python
#-*- coding:utf8-*-

#"for get all the html"


import BeautifulSoup,re
import urllib,urllib2
import optparse

#I think i will get all the options and args
parser = optparse.OptionParser()
parser.add_option('-u','--urls', dest = "urls",help = "the urls ",metavar = "URLS")
parser.add_option('-d','--deep',type = 'int', dest = "deep",help = "the deep", metavar = "DEEP")
parser.add_option('-f' , '--file',type = 'string' , dest = 'logfile', help = "the file is to record the logs", metavar = "LOGFILE")
parser.add_option('-l','--loglevel',type = 'string' ,dest = 'loglevel',help = 'for loglevel(1-5),the number is big,the level is heigh',metavar = 'LOGLEVEL(1-5)')
parser.add_option('--testself',dest = 'test',help = 'self test or test myself')
parser.add_option('-t','--thread',type = 'int',dest = 'number' ,help = 'the threadnumber',metavar = 'NUMBER')
options,args = parser.parse_args()
print "all the optins",options
print "all the args",args

def anaurl(urls,deeps=0):
	"""分析urls,默认deeps为0,深度优先搜索缺点 ：占用内存太大"""
	if deeps == 0:
		try:
			returns=[]
			print urls
			html = urllib2.urlopen(urls,timeout=50)
			data = html.read()
			print 'reading'
			soup = BeautifulSoup.BeautifulSoup(data)
			temp = soup.findAll('a',href=re.compile(r'http.*'))
			print 'analysing'
			for tt in temp:
				hrefs = tt['href']#have?
				if hrefs.startswith('http'):
					if tt.string !=None:#span?????
						returns.append({'name':tt.string,'urls':hrefs})
					else:
						returns.append({'name':'NoName','urls':hrefs})
				else:
					continue
		except Exception,e:
			print e
			print dir(e)
		return returns
	else:#非0
		#try:
		tempb = []
		b = anaurl(urls)
		print b
		for i in b:
			tempb.extend(anaurl(i['urls'], deeps-1))
			print 1
		print 2
		print 'tempb',tempb
		b.extend(tempb)
		return b
		#except:
			#print 'error ~0'
	
if __name__ == '__main__':
	pass
	#tb = anaurl(options.urls,options.deep)
	#if len(tb)>0:
	#	print len(tb)
