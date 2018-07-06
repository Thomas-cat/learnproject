import requests
import time
import os 
import re
from bs4 import BeautifulSoup
from lxml import etree
def changeColor(text,mode):
	if text=='':
		return text
	try:
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
	except:
		return ''
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

def getC2Etran(content):
	a = etree.HTML(content)
	b = a.xpath("//div[@class='trans-container']//p//a/text()")
	for i in range(len(b)):
		b[i] = '\033[0;31m' + b[i] + '\033[0m'	
	return b
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
def initSearch():
	global word
	phonetic = getPhonetic()
	ctran = getCtran()
	wordgroup = getWordgroup()
	now_word =str() 

	if phonetic:
			if len(phonetic) == 1:
				A = '%s\t英:%s'%(word,phonetic[0])
			if len(phonetic) == 2:
				A = '%s\t英:%s\t美:%s'%(word,phonetic[0],phonetic[1])
			A = changeColor(A,4)
			now_word +=A
			now_word +='\n'
			print (A)
	if ctran:
			for tran in ctran:
				if tran!='':
					print (tran)
					now_word+=tran
					now_word +='\n'
			print ('')
	if wordgroup:
		i = 1
		for item in wordgroup:
			print ('%d.'%i+'\n'+changeColor(item[0],5)+'\n'+changeColor(item[1],5)+'\n')
			i+=1
	EEtran = getE2Ctran()
	if EEtran:
			for i in range(len(EEtran)):
				print (EEtran[i][0])
				j = 1
				k = 0 
				for item in EEtran[i][1]:
					if k>=4:
						break
					if item[1]!='':
					 print ('%d.\n%s\n%s\n'%(j,item[0],item[1]))
					else:
					 print ('%d.\n%s\n'%(j,item[0]))
					j+=1
					k+=1
		
	return now_word
def main():
		global soup,word
		last_word = str()
		while(1):
				tip = 'please input a word( 1.save_word 2.review_word 3.exit ):\n'
				tip = '\033[0;34m' + tip + '\033[0m'
				word = input(tip)
				if word.strip() == '1':
					if last_word != '':
						with open('word.txt','a') as f:
							f.write(last_word.strip())
							f.write('\n')
						print ('\033[32m' + 'Save Success!' + '\033[0m'+'\n')
					else:
						print ('\033[31m' + 'Error: Save Without Search!' + '\033[0m'+'\n')
					continue
					
				if word.strip() == '2':
					with open('word.txt','r') as f:
						print (f.read())
					continue

				if word == 'exit_' or word.strip() == '3' or word.strip() == 'q':
					exit()
				
				os.system('clear')
				keyfrom = 'new-fanyi.smartResult'
				url = 'http://dict.youdao.com/search?q=%s&keyfrom=new-fanyi.smartResult'%word
				ret = requests.get(url)
				content = ret.content.decode('utf-8')
				if re.compile(r'[\u4e00-\u9fa5]+',re.S).match(word):
					ret = getC2Etran(content)
					print (word+'\n')
					for item in ret:
						print (item)
					print ('')
					continue
				soup = BeautifulSoup(content,"lxml")
				last_word = initSearch()
main()
