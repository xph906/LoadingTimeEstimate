import requests
import sys
import time
import logging
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse
import socket
#from pylab import *

#Data will be parameter if it's GET
#Data will be data if it's POST
#Return value will be (response,time)
def sendRequest(url,method,data,headers):
	logger = logging.getLogger('sendRequest')
	method = method.upper()
	try:
		o = urlparse(url)
		host = o.netloc
		starting_time = time.time()
		ip = socket.gethostbyname(host)
		end_time = time.time()
		dns_time = end_time - starting_time
		
		if method == "GET":
			r = None
			starting_time = time.time()
			r = requests.get(url,params=data,headers=headers,timeout=20)
			response = r.text
			end_time = time.time()
			return response, end_time-starting_time,dns_time
		elif method == "HEAD":
			starting_time = time.time()
			r = requests.head(url,params=data,headers=headers,timeout=20)
			resp_head = r.headers
			end_time = time.time()
			#logger.info(resp_head)
			return resp_head,end_time-starting_time,dns_time
	except Exception as e:
		logger.error("SendRequest Exception: "+str(e))
		return None, None		


def extractURLFromWebPageWithHost(body,host):
	soup = BeautifulSoup(body)
	if soup == None:
		return None
	rs = soup.findAll('a')
	if host == None:
		return rs
	else:
		if '*' in host:
			logger.warning("FIXME: extractURLFromWebPage needs to handle wildcard")
			return None
		final_rs = []
		for item in rs:
			url = item.get('href')
			try:
				print url
				o = urlparse(url)
				if (o != None) and (host in o.netloc):
					print url
					final_rs.append(url)
			except Exception as e:
				logger.warning("Exception in parsing URL "+str(url) +" "+str(e))
		return final_rs

if __name__=="__main__":
	logging.basicConfig(filename="logs", filemode='w', level=logging.ERROR, \
                        format='%(asctime)s\t%(levelname)s\t%(message)s', datefmt='[%Y-%m-%d %I:%M:%S]')
	logger = logging.getLogger('sendRequest')
	headers = { 'User-Agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36" }
	data = {"arg1":"val2","arg2":"val2"}
	url = sys.argv[1]
	o = urlparse(url)
	host = sys.argv[2]
	
	rsp, interval, dns_time = sendRequest(url,"GET",None,headers)
	print rsp
	logger.error("GET  %40s Content-Len: %7d Interval: %.6f DNS: %f",url,len(rsp),interval,dns_time)
	size_type_map = {}
	size_type_map[len(rsp)] = interval
	urls = extractURLFromWebPageWithHost(rsp,host)
	for url in urls:
		rsp, interval,dns_time = sendRequest(url,"HEAD",None,headers)
		if rsp == None:
			continue
		logger.error("HEAD %40s Content-Len: %7d Interval: %.6f DNS: %f",url,len(rsp),interval,dns_time)
		rsp, interval, dns_time = sendRequest(url,"GET",None,headers)
		logger.error("GET  %40s Content-Len: %7d Interval: %.6f DNS: %f",url,len(rsp),interval,dns_time)
		size_type_map[len(rsp)] = interval
		
	#x = []
	#y = []
	#for item in size_type_map:
	#	x.append(item)
	#	y.append(size_type_map[item])
	#	print str(item),' => ',size_type_map[item]
	#plot(x,y,'ro')
	#show()
		
	#rsp, interval = sendRequest(url,"HEAD",None,headers)
	#logger.info("HEAD Content-Len:"+str(len(rsp))+"Time:"+str(interval))
		
