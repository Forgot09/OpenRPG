import time
import sys
import os
import subprocess as sp

datalist = {} #몬스터, 아이템, 무기
account = [] #닉네임, 레벨, 경험치, 골드, 소지아이템

class Game:
	def appdata(self, datafile):
		global datalist
		tempdata = datafile.readlines()
		for i in tempdata:
			if '\n' in i:
				i = i.rstrip('\n')
			temp = i.split('/')
			datalist[temp[0]] = temp[1:]
	
	def run(self):
		while 1:
			pass
	
	def loadacc(self):
		global account
		if os.path.isfile('data/account.dat'):
			with open('data/account.dat', 'r') as accdata:
				accdata = accdata.readline()
				account = accdata.split('/')
		else:
			print('닉네임을 만들어주세요')
			username = input('>>>')
			account.append(username)
	
	def saveacc(self, data):
		savedata = ''
		for i in data:
			savedata = savedata + i + '/'
		with open('data/account.dat', 'w') as file:
			file.write(savedata)

class Server:
	pass

class ComputeFunc:
	pass

class World:
	def town(self):
		pass
	
	def dungeon(self, level):
		pass

print('=====OpenRPG v0.01-dev=====\n옛날감성 텍스트 RPG')
while 1:
	print('[S : 게임시작, E : 나가기]')
	ans = input('>>>')
	if ans == 'S' or ans == 's':
		print('로딩중...')
		g = Game()
		cf = ComputeFunc()
		server = Server()
		try:
			g.appdata(open('data/moster.dat'))
			g.appdata(open('data/items.dat'))
			g.appdata(open('data/weapon.dat'))
		except:
			print('게임파일이 손상되었습니다')
			input('나가시려면 Enter를 누르세요')
			sys.exit()
		g.loadacc()
		g.run()
		
	elif ans == 'E' or ans == 'e':
		sys.exit()
