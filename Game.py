import time
import sys
import os
import subprocess as sp
from random import randrange

datalist = {} #몬스터, 아이템, 무기
account = [] #닉네임, 레벨, 경험치, 골드, 소지무기, 소지아이템

#{'monster':[['슬라임', '1', '뒷산', '10'], ['벌레']]...

'''
weapon.dat 형식 : 이름/가격/추가시간/판매여부(1:대장간)/설명
monster.dat 형식 : 이름/레벨/출현던전/경험치
items.dat 형식 : 이름/가격/효과/판매여부(1:상점)/설명
'''

class Game:
	def appdata(self, datafile, type):
		global datalist
		tempdata = datafile.readlines()
		templist = []
		for i in tempdata:
			if '\n' in i:
				i = i.rstrip('\n')
			temp = i.split('/')
			templist.append(temp)
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
		
		if os.path.isfile('data/invenweapon.dat'):
			weapon_list = []
			with open('data/invenweapon.dat', 'r') as data:
				data.readlines()
				for i in data:
					if '\n' in i:
						i = i.rstrip('\n')
					weapon_list.append(i)
			account.append(weapon_list) #소지무기
		else:
			account.append([])
		if os.path.isfile('data/inventory.dat'):
			inven_list = []
			with open('data/inventory.dat', 'r') as data:
				data.readlines()
				for i in data:
					if '\n' in i:
						i = i.rstrip('\n')
					inven_list.append(i)
			account.append(inven_list) #소지아이템
		else:
			account.append([])
	
	def saveacc(self):
		savedata = ''
		for i in range(0, 3):
			savedata = savedata + account[i] + '/'
		with open('data/account.dat', 'w') as file:
			file.write(savedata)
		savedata = ''
		invenlist = account[4]
		for i in invenlist:
			savedata = savedata + i + '\n'
		with open('data/invenweapon.dat', 'w') as file:
			file.write(savedata)
		savedata = ''
		invenlist = account[5]
		for i in invenlist:
			savedata = savedata + i + '\n'
		with open('data/inventory.dat', 'w') as file:
			file.write(savedata)

class Server:
	pass

class ComputeFunc:
	pass

town_building = ['집', '대장간', '상점', '숲','던전으로 가기', '퀘스트']
kindof_dungeon = ['뒷산', '동굴']
home_content = ['정보 보기', '저장', '저장 및 종료']
smithy_selling = []
shop_selling = []

class World:
	g = Game()
	def town(self):
		global smithy_selling, shop_selling, account
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
							print('OpenRPG - v0.10-beta')
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
					selling(['weapon', '1', smithy_selling, '대장장이'])
				elif move_place == '상점':
					print('===상점===')
					selling(['items', '1', shop_selling, '상인'])
				elif move_place == '던전으로 가기':
					mkstring(kindof_dungeon)
					print('이동할 던전을 입력하세요')
					move_place = input('>>>')
					if not move_place in kindof_dungeon:
						print('없는 던전입니다')
						continue
					else:
						return 'go_to_dungeon:'+move_place
				elif move_place == '퀘스트':
					quest()
	
	def dungeon(self, type):
		global account
		monster_list= datalist['monster']
		print('====='+type+'=====')
		if type == '뒷산':
			print('비교적 평화로운 뒷산입니다')
		elif type == '동굴':
			print('습하고 으스스한 동굴입니다')
		while 1:
			waiting_time = randrange(1, 5)
			spawn_able = []
			print('몬스터 찾는중...')
			for i in monster_list:
				name = i[0]
				spawnpoint = i[2]
				level = i[1]
				xp = i[3]
				if type == spawnpoint:
					templist = [name, spawnpoint, level, xp]
					spawn_able.append(templist)
			if len(account[4]) >= 1:
				weapon_buff = float(account[4][2])
			else:
				weapon_buff = 0
			num = randrange(0, len(spawn_able)-1)
			numsize = '1'+'0'*(int(spawn_able[num][2]) * 2)
			if len(account[5]) >= 1:
				if 'ADDTIME' in account[5][2]:
					weapon_buff += float(account[5][2].split(':')[1])
			attack_num = randrange(int(numsize), int('9'*(int(spawn_able[num][2])*3)))+weapon_buff
			attack_time = (100-int(spawn_able[num][2]))/10
			time.sleep(waiting_time)
			print('몬스터 출현!')
			print(spawn_able[num][0]+', '+'Lv.'+spawn_able[num][2])
			print(attack_num)
			starttime = time.time()
			ans = input('>>>')
			endtime = time.time()
			if endtime - starttime <= attack_time and attack_num == int(ans):
				print('승리!')
				print('보상 : '+spawn_able[num][3]+'XP')
				player_xp = int(account[2])
				player_xp += int(spawn_able[num][3])
				account[2] = str(player_xp)
				checkquest(spawn_able[num][0])
				checklevel()
			else:
				print('실패!')
			g.saveacc()
			print('[C : 계속하기, I : 정보 보기, E : 마을로 가기]')
			ans = input('>>>')
			if ans == 'E' or ans == 'e':
				return 'go_to_town'
			elif ans == 'I' or ans == 'i':
				print('OpenRPG - v0.10-beta')
				print('닉네임 : '+account[0])
				print('레벨 : '+account[1])
				print('경험치 : '+account[2])
				print('골드 : '+account[3])
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

def say(string):
	print(string)
	time.sleep(1)

def selling(list):
	global account
	print(account)
	info = datalist[list[0]]
	for i in info:
		if i[3] == list[1]:
			list[2].append(i[0])
	say(list[3]+' : 뭐 살거라도 있어?')
	mkstring(list[2])
	say(list[3]+' : 살거를 골라봐')
	ans = input('>>>')
	if not ans in list[2]:
		say(list[3]+' : 잘가')
	else:
		for i in info:
			if not ans in i:
				continue
			else:
				price = i[1]
				if list[0] == 'weapon':
					plus_time = i[2]
				elif list[0] == 'item':
					cmd = i[3]
				description = i[4]
				break
		print('설명 : '+description)
		say(list[3]+' : '+ans+'은(는) '+price+'골드야')
		say(list[3]+' : 정말 살거야? [응, 아니]')
		yon = input('>>>')
		if yon == '응':
			gold = int(account[3])
			if gold >= int(price):
				gold -= int(price)
				account[3] = str(gold)
				say(list[3]+' : 자, 여기 '+ans+'이야')
				account[4] = [ans, plus_time]
			else:
				say(list[3]+' : 돈이 부족해')
		else:
			say(list[3]+' : 잘가')

quest_list = ['슬라임 3마리 잡기', '벌레 10마리 잡기']
reward_list = ['500 골드', '800 골드']
have_quest = []
quest_data = []
def quest():
	global have_quest, account
	if len(have_quest) == 0:
		num = randrange(0, len(quest_list))
		have_quest.append(quest_list[num])
		have_quest.append(reward_list[num])
		say('마을 주민 : 퀘스트를 주겠네')
		print('내용 : '+have_quest[0])
		print('보상 : '+have_quest[1])
	else:
		quest_complete = checkquest('check')
		if quest_complete:
			say('마을 주민 : 보상을 주겠네')
			if '골드' in have_quest[1]:
				gold = int(account[3])
				gold += int(have_quest[1].split(' ')[0])
				account[3] = str(gold)
			have_quest = []
			quest_data = []
		else:
			say('마을 주민 :  퀘스트는 잘 하고있나?')
			say('마을 주민 : 아직 안끝난것 같은데?')

def checkquest(type):
	global quest_data
	if type == 'check':
		if have_quest[0] == '슬라임 3마리 잡기':
			if quest_data.count('슬라임') >= 3:
				return True
			else:
				return False
		elif have_quest[0] == '벌레 10마리 잡기':
			if quest_data.count('벌레') >= 10:
				return True
			else:
				return False
	else:
		quest_data.append(type)

def checklevel():
	global account
	level = account[1]
	xp = account[2]
	next_level_limit = (int(level)+1) * 100
	if int(xp) >= int(next_level_limit):
		level = str(int(level) + 1)
		account[1] = level

print('=====OpenRPG v0.10-beta=====\n옛날감성 텍스트 RPG')
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
