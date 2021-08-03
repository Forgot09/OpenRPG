import time
import sys
import os
import subprocess as sp
from random import randrange

datalist = {} #몬스터, 아이템, 무기
account = [] #닉네임, 레벨, 경험치, 골드, 소지무기, 소지아이템

'''
weapon.dat 형식 : 이름/가격/추가시간/판매여부(대장간:1, 상점:2)
monster.dat 형식 : 이름/레벨/출현던전/경험치
items.dat 형식 : 이름/판매여부/가격(상점)
'''

class Game:
	def appdata(self, datafile, type):
		global datalist
		tempdata = datafile.readlines()
		tempdict = {}
		templist = []
		for i in tempdata:
			if '\n' in i:
				i = i.rstrip('\n')
			temp = i.split('/')
			tempdict[temp[0]] = temp[1:]
			templist.append(tempdict)
		datalist[type] = templist
	
	def run(self):
		world = World()
		cf = ComputeFunc()
		server = Server()
		statue = world.town()
		while 1:
			if 'go_to_dungeon' in statue:
				statue = world.dungeon(statue.split(':')[1])
			elif statue == 'go_to_town':
				statue = world.town()
	
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
			account.append('1') #레벨
			account.append('0') #경험치
			account.append('500') #골드
	
	def saveacc(self):
		savedata = ''
		for i in account:
			savedata = savedata + i + '/'
		with open('data/account.dat', 'w') as file:
			file.write(savedata)

class Server:
	pass

class ComputeFunc:
	pass

town_building = ['집', '대장간', '상점', '던전으로 가기']
kindof_dungeon = ['뒷산']
home_content = ['정보 보기', '저장', '저장 및 나가기']

class World:
	g = Game()
	def town(self):
		while 1:
			g.saveacc()
			print('=====마을=====')
			mkstring(town_building)
			print('이동할 곳을 입력하세요')
			move_place = input('>>>')
			if not move_place in town_building:
				print('없는 곳입니다')
				continue
			else:
				if move_place == '집':
					print('===집===')
					mkstring(home_content)
					ans = input('>>>')
					if not ans in home_content:
						print('없는 활동입니다')
					else:
						if ans == '정보 보기':
							print('OpenRPG - v0.02-dev')
							print('닉네임 : '+account[0])
							print('레벨 : '+account[1])
							print('경험치 : '+account[2])
							print('골드 : '+account[3])
						elif ans == '저장':
							g.saveacc()
							print('저장되었습니다')
						elif ans == '저장 및 나가기':
							g.saveacc()
							sys.exit()
				elif move_place == '대장간':
					print('===대장간===')
				elif move_place == '상점':
					print('===상점===')
				elif move_place == '던전으로 가기':
					mkstring(kindof_dungeon)
					print('이동할 던전을 입력하세요')
					move_place = input('>>>')
					if not move_place in kindof_dungeon:
						print('없는 던전입니다')
						continue
					else:
						return 'go_to_dungeon:'+move_place
	
	def dungeon(self, type):
		monster_list= datalist['monster']
		print('====='+type+'=====')
		if type == '뒷산':
			print('비교적 평화로운 뒷산입니다')
		while 1:
			waiting_time = randrange(1, 5)
			spawn_able = []
			print('몬스터 찾는중...')
			for i in monster_list:
				name = list(i.keys())[0]
				spawnpoint = i[name][1]
				level = i[name][0]
				xp = i[name][2]
				if type in spawnpoint:
					templist = [name, spawnpoint, level, xp]
					spawn_able.append(templist)
			if len(account[4]) >= 1:
				weapon_name = list(account[4].keys())[0]
				weapon_buff = float(account[4][weapon_name])
			else:
				weapon_buff = 0
			num = randrange(0, len(spawn_able)-1)
			numsize = '1'+'0'*(int(spawn_able[num][2]) * 2)
			attack_num = randrange(int(numsize), int('9'*(int(spawn_able[num][2])*3)))+weapon_buff
			attack_time = (100-int(spawn_able[num][2]))/100
			time.sleep(waiting_time)
			print('몬스터 출현!')
			print(name+', '+'Lv.'+spawn_able[num][2])
			print(attack_num)
			starttime = time.time()
			ans = input('>>>')
			endtime = time.time()
			if endtime - starttime <= attack_time and attack_num == ans:
				print('승리!')
				print('보상 : '+spawn_able[num][3]+'XP')
				player_xp = int(account[2])
				player_xp += int(spawn_able[num][3])
				account[2] = str(player_xp)
			else:
				print('실패!')
			print('[C : 계속하기, E : 그만하기]')
			ans = input('>>>')
			if ans == 'E' or ans == 'e':
				return 'go_to_town'
			else:
				continue

def mkstring(list):
	string = ''
	for i in range(0, len(list)):
		if not i == len(list)-1:
			string = string+list[i]+', '
		else:
			string = string+list[i]
	print('《'+string+'》')

print('=====OpenRPG v0.02-dev=====\n옛날감성 텍스트 RPG')
while 1:
	print('[S : 게임시작, E : 나가기]')
	ans = input('>>>')
	if ans == 'S' or ans == 's':
		print('로딩중...')
		g = Game()
		try:
			g.appdata(open('data/monster.dat'), 'monster')
			g.appdata(open('data/items.dat'), 'items')
			g.appdata(open('data/weapon.dat'), 'weapon')
		except:
			print('게임파일이 손상되었습니다')
			input('나가시려면 Enter를 누르세요')
			sys.exit()
		g.loadacc()
		g.run()
		
	elif ans == 'E' or ans == 'e':
		sys.exit()
