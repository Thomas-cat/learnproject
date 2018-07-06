import requests 
import os
import re
import ssl
import json
import urllib3
from threading import Thread
from keyinput import run as changePage
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context
content_list = list()
def getContent(url):
		global content_list
		ret = requests.get(url,verify = False)
		data = ret.content.decode('utf-8')
		data = json.loads(data)['data']
		title = data['title_en']
		title = '\033[0;31m' + title + '\033[0m'
		date = '\033[0;32m' + data['date'] + '\033[0m'
		title = title+'\n'+date
		data = data['content']
		reg = re.compile(r'<!\[CDATA\[(.*?)\]',re.S)
		reg2 = re.compile(r'</para>',re.S)
		ret = reg2.sub('<![CDATA[\n]]>',data)
		article  = reg.findall(ret)
		article[0] = title
		for i in range(1,len(article)):
			if article[i]!='\n':
				article[i]= '\033[0;34m' + article[i] + '\033[0m'
		content_list.append(article)
def getArticleList(page):
		article_list = []
		url = 'https://www.shanbay.com/api/v2/news/articles/?ipp=10&page='+str(page)
		ret = requests.get(url,verify=False)
		data = ret.content.decode('utf-8')
		datas = json.loads(data)['data']['objects']
		for item in datas:
			if item['grade']>=5:
				url = 'https://www.shanbay.com/api/v2/news/articles/'+item['id']+'/'
				article_list.append(url)
		for url in article_list:
			getContent(url)
def show():
	global content_list
	count = len(content_list)
	flag = 0

	os.system('clear')
	for item in content_list[flag]:
		print (item)

	while True:
			ret = changePage()
			if ret == True:
				flag+=1
			else:
				flag-=1
			if flag < 0:
				flag = 0
			if flag >= count:
				flag = count-1
			os.system('clear')
			for item in content_list[flag]:
				print (item)

def main():
	threads = []
	for i in range(1,6):
		th = Thread(target=getArticleList,args = (i,))
		threads.append(th)
		th.start()
	for th in threads:
		th.join()
	show()
main()
