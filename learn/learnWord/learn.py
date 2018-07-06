import random
import os
import searchWord
from keyinput import run as answer
know = 0
unknow = 0

incognizant_word_list = list()
addrA = './incognizant.txt'
addrB = './wordlist.txt'
local_addr = addrB
#读取本地不认识的单词文本
def isExisWord(select_word):
	with open(addrA,'r')as f:
		origin_text = f.read()
	word_list = origin_text.split('\n')[:-1]
	for item in word_list:
		if select_word == item:
			return False
	remarkWord(select_word)
	
#读取本地考研单词文本
def readWordList():
	with open(local_addr,'r')as f:
		origin_text = f.read()
	word_list = origin_text.split('\n')
	return word_list[:-1]

#出题逻辑
def learn():
	world_list = readWordList()
	count = len(world_list)
	while True:	
			os.system('clear')
			n = random.randint(0,count-1)
			select_word = world_list[n]
			work_func(select_word)

def show(print_list):
	os.system('clear')
	for item in print_list:
		print (item)
#记录认不出的单词
def remarkWord(incognizant_word):
	with open('incognizant.txt','a')as f:
		f.write(incognizant_word+'\n')
#处理的逻辑
def work_func(select_word):
	global know,unknow 
	show_list = searchWord.getWordInfo(select_word)
	#首先显示单词 看认识不
	print ('\033[0;33m' + select_word + '\033[0m')
	print ('\033[0;34m' + '\nDo you remember it?\n' + '\033[0m')
	flag = answer()

	if flag == 'q':
		os.system('clear')
		print ('\033[0;31m' + '本次测试认出单词: %d\n未认出单词: %d\n'%(know,unknow)+ '\033[0m')
		exit()

	if flag  == False:
		unknow +=1
		#展示例句
		show(show_list[1])
		print ('\033[0;34m' + '\nDo you remember it(second)?\n' + '\033[0m')


		flag = answer()
		if flag == False:
		#展示所有
		#标记起来
			isExisWord(select_word)
			show(show_list[0])
		#如果推出的话 打印
		elif flag == 'q':
			os.system('clear')
			print ('\033[0;31m' + '本次测试认出单词: %d\n未认出单词: %d\n'%(know,unknow)+ '\033[0m')
			exit()
		else:
			pass
	else:
		know+=1
		return 0
	print ('\033[0;34m' + '\n是否进入下一个?\n' + '\033[0m')
	while answer()!=True:
		pass
	return 0
		
def main():
	global local_addr,addrA
	#需要两个函数 一个监听键盘输入 另一个是出问题
	mode = input('1.learn\t2.review\n').strip()
	if mode == '2':
		local_addr = addrA
	learn()
main()
	
	
