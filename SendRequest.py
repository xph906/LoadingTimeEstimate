import requests
import time
import logging
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse
from pylab import *

#Data will be parameter if it's GET
#Data will be data if it's POST
#Return value will be (response,time)
def sendRequest(url,method,data,headers):
	logger = logging.getLogger('sendRequest')
	method = method.upper()
	try:
		if method == "GET":
			r = None
			starting_time = time.time()
			r = requests.get(url,params=data,headers=headers,timeout=20)
			response = r.text
			end_time = time.time()
			return response, end_time-starting_time
		elif method == "HEAD":
			starting_time = time.time()
			r = requests.head(url,params=data,headers=headers,timeout=20)
			resp_head = r.headers
			end_time = time.time()
			#logger.info(resp_head)
			return resp_head,end_time-starting_time
	except Exception as e:
		logger.error("SendRequest Exception: "+str(e))
		return None, NOne		

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
				o = urlparse(url)
				if (o != None) and (o.netloc == host):
					#print url
					final_rs.append(url)
			except Exception as e:
				logger.warning("Exception in parsing URL "+str(url) +" "+str(e))
		return final_rs

if __name__=="__main__":
	logging.basicConfig(filename="logs", filemode='w', level=logging.ERROR, \
                        format='%(asctime)s\t%(levelname)s\t%(message)s', datefmt='[%Y-%m-%d %I:%M:%S]')
	logger = logging.getLogger('sendRequest')
	headers = { 'User-Agent' : "Mozilla" }
	data = {""}
	url = "http://www.sina.com.cn"
	
	rsp, interval = sendRequest(url,"GET",None,headers)
	logger.info("GET Content-Len:"+str(len(rsp))+"Time:"+str(interval))
	size_type_map = {}
	size_type_map[len(rsp)] = interval
	urls = extractURLFromWebPageWithHost(rsp,"www.sina.com.cn")
	for url in urls:
		rsp, interval = sendRequest(url,"HEAD",None,headers)
		logger.error("HEAD %s Content-Len: %7d Interval: %f ",url,len(rsp),interval)
		rsp, interval = sendRequest(url,"GET",None,headers)
		logger.error("HEAD %s Content-Len: %7d Interval: %f ",url,len(rsp),interval)
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
		