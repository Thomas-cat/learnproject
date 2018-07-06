import requests
import time
import re
from bs4 import BeautifulSoup
from lxml import etree
def changeColor(text,mode):
	if text=='':
		return text
	if mode == 0:
		return '\033[0;31m' + text + '\033[0m'
	if mode == 1:
		return '\033[34;47m' + text + '\033[0m'
	if mode == 2:
		return '\033[35;47m' + text + '\033[0m'
	if mode == 3:
		return '\033[31;47m' + text + '\033[0m'
	if mode == 4:
		return ('\033[0;33m' + text + '\033[0m')
	if mode == 5:
		return '\033[30;43m' + text + '\033[0m'
def getWordgroup():
	global soup
	try:
			a = soup.find('div',id="wordGroup2")
			b = a.find_all('p',class_='wordGroup')
	except:
		return None
	tmp = list()
	for x in b:
		string = x.get_text().strip()
		string = re.sub(r'\s{3,}',',',string)
		string = string.split(',')
		tmp.append(string)
	if len(tmp) > 4:
		return tmp[0:4]
	return string
def getCtran():
		global soup
		a = soup.find('div',class_ = 'trans-container')
		try:
			b = a.find_all('li')
		except:
			return None
		ctran = list()
		for x in b:
			ctran.append(changeColor(x.string,3))
		return ctran
def getPhonetic():
		global soup
		a = soup.find('div',class_='baav')
		try:
			b = a.find_all('span',class_ = 'phonetic')
			phonetic = list()
		except:
			return None
		for i in b:
			phonetic.append(i.string)
		return phonetic
def isKey(word):
	if re.compile(r'[a-z]+.$').match(word):
		return True
def getE2Ctran():
		global soup
		EEtran = list()
		try:
				a = soup.find_all(id="tEETrans" )[0]
				b = a.find_all('ul')[0]
				c = b.find_all('li')
		except:
			return None

		for i in range(0,len(c)):
			if isKey(c[i].span.string):
				q = str() 		
				temp_c = list()
				q = c[i].span.string[:-1]
				q = changeColor(q,0)

				EEtran.append([q,temp_c])

				if c[i].ul:
					continue
				else:
					if q == '':
						return None
					try:
						a = c[i].p.string
						if a == None:
							a = ''
					except:
						a = ''
					try:
						b  = c[i].find(class_='def').string
					except:
						b  = ''
					temp_c.append([changeColor(b,1),changeColor(a,2)])
			else:
				try:
					temp_c
				except:
					return None
				try:
					a = c[i].p.string
					if a == None:
						a = ''
				except:
					a = ''
				try:
					b  = c[i].find(class_='def').string
				except:
					b  = ''
				temp_c.append([changeColor(b,1),changeColor(a,2)])
		return EEtran
def show(mode):
	#展示英文解释
	if mode == 1:
		pass
	if mode == 2:
		pass
	if mode == 3:
		pass
def initSearch():
	global word
	phonetic = getPhonetic()
	ctran = getCtran()
	EEtran = getE2Ctran()
	wordgroup = getWordgroup()
	modeA = list()
	modeB = list()
	if phonetic:
			if len(phonetic) == 1:
				tmp = '%s\t英:%s'%(word,phonetic[0])
			if len(phonetic) == 2:
				tmp = '%s\t英:%s\t美:%s'%(word,phonetic[0],phonetic[1])
			tmp = changeColor(tmp,4)
			modeB.append(changeColor(word,4))
			modeA.append(tmp)
	if ctran:
			for tran in ctran:
				if tran!='':
					modeA.append(tran)
			modeA.append('')
	if wordgroup:
		i = 1
		try:
				for item in wordgroup:
					tmp =  ('%d.'%i+'\n'+changeColor(item[0],5)+'\n'+changeColor(item[1],5)+'\n')
					modeA.append(tmp)
					i+=1
		except:
			pass
	if EEtran:
			for i in range(len(EEtran)):
				modeA.append(EEtran[i][0])
				modeB.append(EEtran[i][0])
				j = 1
				k = 0 
				for item in EEtran[i][1]:
					if k>=4:
						break
					if item[1]!='':
					 tmp =  ('%d.\n%s\n%s\n'%(j,item[0],item[1]))
					 modeA.append(tmp)
					 modeB.append(tmp)
					else:
					 tmp =  ('%d.\n%s\n'%(j,item[0]))
					 modeA.append(tmp)
					 modeB.append(tmp)
					j+=1
					k+=1
	return [modeA,modeB]
def getWordInfo(search_word):
		global soup,word
		word = search_word
		keyfrom = 'new-fanyi.smartResult'
		url = 'http://dict.youdao.com/search?q=%s&keyfrom=new-fanyi.smartResult'%word
		ret = requests.get(url)
		content = ret.content.decode('utf-8')
		soup = BeautifulSoup(content,"lxml")
		word_info = initSearch()
		return word_info
