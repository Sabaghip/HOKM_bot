import random
import os
import telebot
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup,ReplyKeyboardRemove
import time
import atexit
from keep_alive import keep_alive

#--------------------------------------------------
TOKEN="5173702413:AAHR-gwmXY_e362HiaSM2ItzOC9JJKOnFOs"
bot=telebot.TeleBot(TOKEN)
directory=""
#--------------------------------------------------

hide_keyboard=ReplyKeyboardRemove()



def my_end():
	bot.send_message(36010289,"program terminated!")

atexit.register(my_end)


class cart():
	played=0
	def __init__(self,shekl,adad):
		self.shekl=shekl
		self.adad=adad
	def play(self):
		self.played=1


class player():
	msg_zamin_id=0
	msg_carts_id=0
	message = " "
	def __init__(self,name,carts,chatid,game_id):
		self.name=name
		self.carts=carts
		self.chatid=chatid
		self.game_id=game_id






games_list=[]
players_list=[]
players=[]
randoms=[]
hokm=""
hakem=0
turn=0
zamin=[cart(" ",0),cart(" ",0),cart(" ",0),cart(" ",0)]
dast=""
team1_wins=0
team2_wins=0
last_win=0
team1_wins_t=0
team2_wins_t=0
size_zamin=0
rounds_to_win=0
last_high=cart("♠️",1)

def nothing():
	pass



def get_n(start,end,matn):

	while 1:
		try:
			choice=int(input(matn))
		except ValueError:
			print("invalid input.")
		else:
			break
	while(choice>end or choice<start):
		print("wrong input.")
		choice=int(input(matn))
	return choice

def is_higher(last,current,hokm,dast):
	if current.shekl==hokm and last.shekl!=hokm:
		return 1
	if current.shekl!=hokm and last.shekl==hokm:
		return 0
	if current.shekl!=dast and current.shekl!=hokm:
		return 0
	if current.adad==1:
		return 1
	if last.adad==1:
		return 0
	if current.adad>last.adad:
		return 1
	else:
		return 0


def sort(carts,hokm):
	res=[]
	k=0
	z=0
	for i in range(len(carts)):
		if(carts[i].shekl==hokm):
			res.append(carts[i])
			k+=1
	for i in range(0,k):
		for j in range(0,k-1):
			if (res[j].adad<res[j+1].adad and res[j].adad!=1) or res[j+1].adad==1:
				res[j],res[j+1]=res[j+1],res[j]
	z+=k
	k=0
	for i in range(len(carts)):
		if(carts[i].shekl=="♣️" and hokm!="♣️"):
			res.append(carts[i])
			k+=1
	for i in range(z,k+z):
		for j in range(z,z+k-1):
			if (res[j].adad<res[j+1].adad and res[j].adad!=1) or res[j+1].adad==1:
				res[j],res[j+1]=res[j+1],res[j]

	z+=k
	k=0
	for i in range(len(carts)):
		if(carts[i].shekl=="♥️" and hokm!="♥️"):
			res.append(carts[i])
			k+=1
	for i in range(z,k+z):
		for j in range(z,z+k-1):
			if (res[j].adad<res[j+1].adad and res[j].adad!=1) or res[j+1].adad==1:
				res[j],res[j+1]=res[j+1],res[j]

	z+=k
	k=0
	for i in range(len(carts)):
		if(carts[i].shekl=="♦️" and hokm!="♦️"):
			res.append(carts[i])
			k+=1
	for i in range(z,k+z):
		for j in range(z,z+k-1):
			if (res[j].adad<res[j+1].adad and res[j].adad!=1) or res[j+1].adad==1:
				res[j],res[j+1]=res[j+1],res[j]

	z+=k
	k=0
	for i in range(len(carts)):
		if(carts[i].shekl=="♠️" and hokm!="♠️"):
			res.append(carts[i])
			k+=1
	for i in range(z,k+z):
		for j in range(z,z+k-1):
			if (res[j].adad<res[j+1].adad and res[j].adad!=1) or res[j+1].adad==1:
				res[j],res[j+1]=res[j+1],res[j]



	return res


def have_dast(carts,dast):
	for i in carts:
		if i.shekl==dast:
			return 1
	return 0

def my_split(x,y):
	z=x.split(y)
	if(z[0]==''):
		z.pop(0)
	if len(z)==0:
		return z
	if(z[len(z)-1]==''):
		z.pop(len(z)-1)
	return z

def reset_round(hakem):
	global turn
	global team1_wins
	global team2_wins
	global last_win
	turn=hakem
	team1_wins=0
	team2_wins=0
	last_win=hakem
	matn="Team 1 : "+players[0].name+"   -   "+players[2].name+"    "+str(team1_wins_t)+"("+str(team1_wins)+")"+"\nTeam 2 : "+players[1].name+"   -   "+players[3].name+"    "+str(team2_wins_t)+"("+str(team2_wins)+")"
	for p in players:
		p.carts.clear()
		if p!=hakem:
			bot.edit_message_text(matn+"\nhakem is "+players[hakem].name+"\nwaiting for hokm...",chat_id=p.chatid,message_id=p.msg_carts_id)
			bot.edit_message_text("zamin",chat_id=p.chatid,message_id=p.msg_zamin_id)
	randoms=[]
	carts=[]
	for i in range(13):
		carts.append(cart("♠️",i+1))
	for i in range(13):
		carts.append(cart("♣️",i+1))
	for i in range(13):
		carts.append(cart("♥️",i+1))
	for i in range(13):
		carts.append(cart("♦️",i+1))
	for i in range(52):
		s=random.randint(0,len(carts)-1)
		randoms.append(carts[s])
		carts.pop(s)
	players[0].carts=randoms[0:13]
	players[1].carts=randoms[13:26]
	players[2].carts=randoms[26:39]
	players[3].carts=randoms[39:52]


def entekhab_adad(adad):
	if adad<11 and adad>1:
		return str(adad)
	elif adad==1:
		return "A"
	elif adad==11:
		return "J"
	elif adad==12:
		return "Q"
	elif adad==13:
		return "K"



#-------------------------------------------------------------------------------------------------------------------------------------


def update_game(game_id):
	global players
	for i in range(len(players)):
		players.pop(0)
	global zamin
	zamin=[cart(" ",0),cart(" ",0),cart(" ",0),cart(" ",0)]
	global hokm
	global hakem
	global turn
	global dast
	global team1_wins
	global team2_wins
	global last_win
	global team1_wins_t
	global team2_wins_t
	global size_zamin
	global last_high
	global rounds_to_win
	hokm=""
	hakem=0
	turn=0
	dast=""
	team1_wins=0
	team2_wins=0
	last_win=0
	size_zamin=0

	f=open(directory+str(game_id)+"_game.txt","r")
	data=f.read()
	f.close()

	data=my_split(data,"\n")
	tedad=data[0]
	cartsx=my_split(data[3],">")
	p1=my_split(data[1]," ")
	p2=my_split(data[2]," ")
	p3=my_split(data[12]," ")
	p4=my_split(data[13]," ")
	for i in range(int(tedad)):
		players_id=int(p1[i])
		players_name=p2[i]
		carts_player=my_split(cartsx[i],"|")
		carts=[]
		for j in range(len(carts_player)):
			cart_x=my_split(carts_player[j]," ")
			carts.append(cart(cart_x[1],int(cart_x[0])))
		players.append(player(players_name,carts,players_id,game_id))
		players[i].msg_carts_id=int(p3[i])
		players[i].msg_zamin_id=int(p4[i])
	zamin_c=my_split(data[4],"|")
	for i in range(len(zamin_c)):
		zamin_x=my_split(zamin_c[i],"^")
		zamin[i].shekl=zamin_x[1]
		zamin[i].adad=int(zamin_x[0])
	hokm=data[5]
	hakem=int(data[6])
	turn=int(data[7])
	dast=data[8]
	team1_wins=int(data[9])
	team2_wins=int(data[10])
	last_win=int(data[11])
	team1_wins_t=int(data[14])
	team2_wins_t=int(data[15])
	size_zamin=int(data[16])
	l_h=my_split(data[17]," ")
	last_high=cart(l_h[1],int(l_h[0]))
	rounds_to_win=int(data[18])
	messages = data[19].split(">")
	for i in range(int(tedad)):
		players[i].message = messages[i]



def update_file(game_id):

	f=open(directory+str(game_id)+"_game.txt","w")
	f.write(str(len(players))+"\n")

	for i in players:
		f.write(str(i.chatid)+" ")

	f.write("\n")
	for i in players:
		f.write(str(i.name)+" ")

	f.write("\n")
	for i in players:
		for j in i.carts:
			f.write(str(j.adad)+" "+j.shekl+"|")
		f.write(">")

	f.write("\n")
	for i in zamin:
		f.write(str(i.adad)+"^"+i.shekl+"|")

	f.write("\n"+hokm+"\n"+str(hakem)+"\n"+str(turn)+"\n"+dast+"\n"+str(team1_wins)+"\n"+str(team2_wins)+"\n"+str(last_win)+"\n")
	for i in players:
		f.write(str(i.msg_carts_id)+" ")
	f.write("\n")
	for i in players:
		f.write(str(i.msg_zamin_id)+" ")
	f.write("\n"+str(team1_wins_t)+"\n"+str(team2_wins_t)+"\n"+str(size_zamin)+"\n"+str(last_high.adad)+" "+last_high.shekl+"\n"+str(rounds_to_win))
	f.write("\n")
	for i in players :
		f.write(i.message + ">")
	f.close()


def add_game(game_id):
	f=open(directory+"all_games.txt","a")
	f.write(str(game_id)+"\n")
	f.close()
	games_list.append([str(game_id)])

def add_player_to_game(player,game_id):
	global games_list
	games_list.clear()
	f=open(directory+"all_games.txt","r")
	games_temp=my_split(f.read(),"\n")
	for i in games_temp:
		game=my_split(i," ")
		game=[int(x) for x in game]
		games_list.append(game)
	f.close()
	for i in games_list:
		if i[0]==game_id:
			i.append(player)
	f=open(directory+"all_games.txt","w")
	for i in games_list:
		for j in i:
			f.write(str(j)+" ")
		f.write("\n")
	f.close()


	for i in range(len(players_list)):
		players_list.pop(0)
	f=open(directory+"all_players.txt","r")
	players_temp=my_split(f.read(),"\n")
	for i in players_temp:
		players_list.append(int(i))
	f.close()
	players_list.append(player)
	f=open(directory+"all_players.txt","w")
	for i in players_list:
		f.write(str(i))
		f.write("\n")
	f.close()


def update_gamelist():
	games_list.clear()
	f=open(directory+"all_games.txt","r")
	games_temp=my_split(f.read(),"\n")
	for i in games_temp:
		game=my_split(i," ")
		game=[int(x) for x in game]
		games_list.append(game)
	f.close()



def search_player(chatid):
	f=open(directory+"all_players.txt","r")
	plist=my_split(f.read(),"\n")
	f.close()
	for i in plist:
		if(chatid==int(i)):
			return 1
	return 0


def get_player_game(userchatid):
	for game in games_list:
		for p in game[1:]:
			if int(p)==userchatid:
				return int(game[0])
	return 0


def make_randoms(game_id):
	f=open(directory+"carts.txt","r")
	carts_temp1=my_split(f.read(),"\n")
	f.close()
	randoms=[]
	for i in carts_temp1 :
		carts_temp2=i.split(">")
		if int(carts_temp2[0])==game_id:
			carts_string=my_split(carts_temp2[1],"|")
			for cartx in carts_string:
				randoms.append(cart(cartx.split(" ")[1],int(cartx.split(" ")[0])))
	return randoms


def delete_game(game_id):
	update_gamelist()
	update_game(game_id)
	for i in players:
		bot.delete_message(i.chatid,i.msg_carts_id)
		bot.delete_message(i.chatid,i.msg_zamin_id)
	f=open(directory+"all_players.txt","r")
	data=f.read()
	f.close()
	players1=my_split(data,"\n")
	players2=[int(p) for p in players1]
	players3=players2
	for game in games_list:
		if game[0]==game_id:
			for g in game:
				for p in players2:
					if p==g:
						players3.remove(p)
						break
	f=open(directory+"all_players.txt","w")
	for p in players3 :
		f.write(str(p)+"\n")
	f.close()
	for i in range(len(games_list)):
		if games_list[i][0]==game_id:
			games_list.pop(i)
			break
	f=open(directory+"all_games.txt","w")
	for i in games_list:
		for j in i:
			f.write(str(j)+" ")
		f.write("\n")
	f.close()
	os.remove(directory+str(game_id)+"_game.txt")
	f=open(directory+"carts.txt","r")
	data=f.read()
	f.close()
	data=my_split(data,"\n")
	f=open(directory+"carts.txt","w")
	for i in data:
		if int(i.split(">")[0])!=game_id:
			f.write(i+"\n")
	f.close()
	



#-------------------------------------------------------------------------------------------------------------------------------------


def show_cards():
	global hokm
	global hakem
	global turn
	for i in range(4):
		reply_k=InlineKeyboardMarkup()
		reply_zamin=InlineKeyboardMarkup()


		reply_zamin.row(InlineKeyboardButton(players[0].message,callback_data="none"),InlineKeyboardButton(players[0].name,callback_data="none"),InlineKeyboardButton(players[0].message,callback_data="none"))


		reply_zamin.row(InlineKeyboardButton(players[1].message,callback_data="none"),InlineKeyboardButton(" ",callback_data="none"),zamin[0].adad != 0 and InlineKeyboardButton(zamin[0].shekl+entekhab_adad(zamin[0].adad),callback_data="none") or InlineKeyboardButton("-",callback_data="none"),InlineKeyboardButton(" ",callback_data="none"),InlineKeyboardButton(players[3].message,callback_data="none"))

		reply_zamin.row(InlineKeyboardButton(players[1].name,callback_data="none"),zamin[1].adad != 0 and InlineKeyboardButton(zamin[1].shekl+entekhab_adad(zamin[1].adad),callback_data="none") or InlineKeyboardButton("-",callback_data="none"),InlineKeyboardButton(hokm,callback_data="none"),zamin[3].adad != 0 and InlineKeyboardButton(zamin[3].shekl+entekhab_adad(zamin[3].adad),callback_data="none") or InlineKeyboardButton("-",callback_data="none"),InlineKeyboardButton(players[3].name,callback_data="none"))

		reply_zamin.row(InlineKeyboardButton(players[1].message,callback_data="none"),InlineKeyboardButton(" ",callback_data="none"),zamin[2].adad != 0 and InlineKeyboardButton(zamin[2].shekl+entekhab_adad(zamin[2].adad),callback_data="none") or InlineKeyboardButton("-",callback_data="none"),InlineKeyboardButton(" ",callback_data="none"),InlineKeyboardButton(players[3].message,callback_data="none"))


		reply_zamin.row(InlineKeyboardButton(players[2].message,callback_data="none"),InlineKeyboardButton(players[2].name,callback_data="none"),InlineKeyboardButton(players[2].message,callback_data="none"))

		bot.edit_message_text("zamin :",chat_id=players[i].chatid,reply_markup=reply_zamin,message_id=players[i].msg_zamin_id)
		buttons_temp=[]
		for j in range(len(players[i].carts)):
			if len(buttons_temp)==3:
				reply_k.row(*buttons_temp)
				for iii in range(3):
					buttons_temp.pop(0)
			if i==turn :
				if dast=="":
					buttons_temp.append(InlineKeyboardButton(players[i].carts[j].shekl+entekhab_adad(players[i].carts[j].adad),callback_data="player "+str(i)+" "+str(j)))
				else:
					if have_dast(players[i].carts,dast)==1:
						if players[i].carts[j].shekl==dast:
							buttons_temp.append(InlineKeyboardButton(players[i].carts[j].shekl+entekhab_adad(players[i].carts[j].adad),callback_data="player "+str(i)+" "+str(j)))
						else:
							buttons_temp.append(InlineKeyboardButton(players[i].carts[j].shekl+entekhab_adad(players[i].carts[j].adad),callback_data="none"))
					else:
						buttons_temp.append(InlineKeyboardButton(players[i].carts[j].shekl+entekhab_adad(players[i].carts[j].adad),callback_data="player "+str(i)+" "+str(j)))

			else:
				buttons_temp.append(InlineKeyboardButton(players[i].carts[j].shekl+entekhab_adad(players[i].carts[j].adad),callback_data="none"))
		reply_k.row(*buttons_temp)
		for iii in range(len(buttons_temp)):
			buttons_temp.pop(0)
		matn=str(rounds_to_win)+" round(s) game\nTeam 1 : "+players[0].name+"   -   "+players[2].name+"    "+str(team1_wins_t)+"("+str(team1_wins)+")\nTeam 2 : "+players[1].name+"   -   "+players[3].name+"    "+str(team2_wins_t)+"("+str(team2_wins)+")\n"+"  Hokm is "+hokm+"\n"+players[turn].name+" turn"
		bot.edit_message_text(matn,chat_id=players[i].chatid,reply_markup=reply_k,message_id=players[i].msg_carts_id)


def entekhabe_hokm(carts,userchatid):
	global hokm
	global hakem
	global turn
	reply_k=InlineKeyboardMarkup()
	for i in carts[0:5]:
		reply_k.add(InlineKeyboardButton(i.shekl+entekhab_adad(i.adad),callback_data="none"))
	bot.edit_message_text("your carts : ",chat_id=userchatid,message_id=players[hakem].msg_zamin_id,reply_markup=reply_k)
	reply_k1=InlineKeyboardMarkup()
	reply_k1.row_width=2
	reply_k1.add(InlineKeyboardButton("♠️",callback_data="hokm: ♠️"),InlineKeyboardButton("♣️",callback_data="hokm: ♣️"),InlineKeyboardButton("♦️",callback_data="hokm: ♦️"),InlineKeyboardButton("♥️",callback_data="hokm: ♥️"))
	bot.edit_message_text("choose hokm : ",chat_id=userchatid,message_id=players[hakem].msg_carts_id,reply_markup=reply_k1)



@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
	try:
		global hokm
		global hakem
		global turn
		global last_win
		global dast
		global team1_wins
		global team2_wins
		global last_high
		global team1_wins_t
		global team2_wins_t
		global size_zamin
		global rounds_to_win
		if call.data.startswith("hokm:"):
			update_game(get_player_game(call.message.chat.id))
			hokm=call.data.split()[1]
			for p in players :
				p.carts=sort(p.carts,hokm)
			update_file(get_player_game(call.message.chat.id))
			show_cards()
		if call.data.startswith("player"):
			update_gamelist()
			game_id=get_player_game(call.message.chat.id)
			update_game(game_id)
			if players[turn].chatid==call.message.chat.id :

				player_i=int(call.data.split()[1])
				cart_i=int(call.data.split()[2])
				if size_zamin==0:
					dast=players[player_i].carts[cart_i].shekl
					last_high=players[player_i].carts[cart_i]
					last_win=player_i
				if is_higher(last_high,players[player_i].carts[cart_i],hokm,dast)==1:
					last_high=players[player_i].carts[cart_i]
					last_win=player_i
				zamin[turn].shekl=players[player_i].carts[cart_i].shekl
				zamin[turn].adad=players[player_i].carts[cart_i].adad
				size_zamin+=1
				players[player_i].carts.pop(cart_i)
				turn+=1
				if turn==4:
					turn=0
				if size_zamin==4:
					show_cards()
					time.sleep(1)
					dast=""
					turn=last_win

					if last_win==0 or last_win==2:
						team1_wins+=1
					else:
						team2_wins+=1
					for i in range(4):
						zamin[i].shekl=" "
						zamin[i].adad=0
					size_zamin=0


					if team1_wins==7:
						if team2_wins==0:
							team1_wins_t+=1
							if hakem==1 or hakem==3:
								for p in players:
									bot.send_message(p.chatid,"team 1 scored a hakem kot !")
								team1_wins_t+=1
							else:
								for p in players:
									bot.send_message(p.chatid,"team 1 scored a kot !")
						else:
							for p in players:
								bot.send_message(p.chatid,"team 1 won a round !")

						team1_wins_t+=1
						if int(team1_wins_t)>=int(int(rounds_to_win)/2)+1:
							for i in players:
								bot.send_message(i.chatid,"Team 1 won the game !")
							delete_game(int(get_player_game(players[hakem].chatid)))
							return
						if hakem==1:
							hakem=2
						if hakem==3:
							hakem=0
						reset_round(hakem)
						update_file(get_player_game(call.message.chat.id))
						entekhabe_hokm(players[hakem].carts[0:5],players[hakem].chatid)
					elif team2_wins==7:
						if team1_wins==0:
							team2_wins_t+=1
							if hakem==0 or hakem==2:
								for p in players:
									bot.send_message(p.chatid,"team 2 scored a hakem kot !")
								team2_wins_t+=1
							else:
								for p in players:
									bot.send_message(p.chatid,"team 2 scored a kot !")
						else:
							for p in players:
								bot.send_message(p.chatid,"team 2 won a round !")

						team2_wins_t+=1
						if int(team2_wins_t)>=int(int(rounds_to_win)/2)+1:
							for i in players:
								bot.send_message(i.chatid,"Team 2 won the game !")
							delete_game(int(get_player_game(players[hakem].chatid)))
							return
						if hakem==0:
							hakem=1
						if hakem==2:
							hakem=3
						reset_round(hakem)
						update_file(get_player_game(call.message.chat.id))
						entekhabe_hokm(players[hakem].carts[0:5],players[hakem].chatid)
					else:
						update_file(game_id)
						show_cards()
				else:
					update_file(game_id)
					show_cards()



		if call.data.startswith("make_game "):
			if search_player(call.message.chat.id)==1:
				bot.send_message(call.message.chat.id,"you are in a game!")
			else:
				global randoms
				data=call.data.split(" ")
				random_int=int(data[1])
				userchatid=call.message.chat.id
				userusername=call.message.chat.first_name
				rounds_to_win=int(data[2])
				add_game(random_int)
				add_player_to_game(userchatid,random_int)
				reply_m=ReplyKeyboardMarkup()
				reply_m.add("leave game","cancel")
				bot.send_message(userchatid,"you started a "+str(data[2])+" round(s) game\nsend game link to your friends and wait for them to join :\nhttps://t.me/hokm_pbot?start="+str(random_int),reply_markup=reply_m)
				msg=bot.send_message(userchatid,"team 1 : "+userusername+"\nteam 2 : "+"\nwaiting for players...")
				msg1=bot.send_message(userchatid,"zamin")
				carts=[]

				for i in range(13):
					carts.append(cart("♠️",i+1))
				for i in range(13):
					carts.append(cart("♣️",i+1))
				for i in range(13):
					carts.append(cart("♥️",i+1))
				for i in range(13):
					carts.append(cart("♦️",i+1))
				randoms.clear()
				for i in range(52):
					s=random.randint(0,len(carts)-1)
					randoms.append(carts[s])
					carts.pop(s)
				players.clear()
				players.append(player(userusername,randoms[0:13],userchatid,random_int))
				players[0].msg_carts_id=msg.message_id
				players[0].msg_zamin_id=msg1.message_id
				f=open(directory+"carts.txt","a")
				f.write(str(random_int)+">")
				for i in randoms:
					f.write(str(i.adad)+" "+i.shekl+"|")
				f.write("\n")
				f.close()
				randoms.clear()
				update_file(random_int)
				bot.delete_message(call.message.chat.id,call.message.message_id)


		if call.data.startswith("delete this message"):
			bot.delete_message(call.message.chat.id,call.message.message_id)

		if call.data.startswith("none"):
			bot.answer_callback_query(call.id,"you cant choose this!")
	except Exception as e:
		bot.send_message(36010289,"error in callback.")
		print(e)





@bot.message_handler(content_types=['text'])

def botmain(user):
	try:
		global games_list
		global players_list
		global players
		global randoms
		global hokm
		global hakem
		global turn
		global zamin
		usertext=user.text
		userusername=user.chat.first_name
		userchatid=user.chat.id
		#======================================================================================================
		if userchatid==36010289:
			if usertext=="games list":
				update_gamelist()
				matn="games:\n"
				for game in games_list:
					matn=matn+str(game[0])+":\n"
					for i in game[1:]:
						matn=matn+str(i)+"  "+bot.get_chat(int(i)).first_name+"\n"
					matn=matn+"\n"
				bot.send_message(36010289,matn)
			if usertext.startswith("delete game "):
				data=usertext.split(" ")
				update_game(int(data[2]))
				for p in players:
					bot.send_message(p.chatid,"admin deleted the game.")
				delete_game(int(data[2]))
				bot.send_message(36010289,"game "+str(data[2])+" deleted")


		#======================================================================================================

		if usertext=="/start":
			if search_player(userchatid)==1:
				reply_m=ReplyKeyboardMarkup()
				reply_m.add("leave game","cancel")
				bot.send_message(userchatid,"khob baadesh?",reply_markup=reply_m)
			else:
				reply_m=ReplyKeyboardMarkup()
				reply_m.add("new game","cancel")
				bot.send_message(userchatid,"khob baadesh?",reply_markup=reply_m)



		elif usertext=="new game":
			if search_player(userchatid)==1:
				bot.send_message(userchatid,"you are in a game!")
			else:
				random_int=random.randint(1,100000)
				reply_m=InlineKeyboardMarkup()
				reply_m.row(InlineKeyboardButton("1",callback_data="make_game "+str(random_int)+" 1"),InlineKeyboardButton("3",callback_data="make_game "+str(random_int)+" 3"),InlineKeyboardButton("5",callback_data="make_game "+str(random_int)+" 5"),InlineKeyboardButton("7",callback_data="make_game "+str(random_int)+" 7"))
				reply_m.row(InlineKeyboardButton("9",callback_data="make_game "+str(random_int)+" 9"),InlineKeyboardButton("11",callback_data="make_game "+str(random_int)+" 11"),InlineKeyboardButton("13",callback_data="make_game "+str(random_int)+" 13"),InlineKeyboardButton("cancel",callback_data="delete this message"))
				msg_temp=bot.send_message(userchatid,"OK!",reply_markup=hide_keyboard,reply_to_message_id=user.message_id)
				bot.delete_message(userchatid, msg_temp.message_id)
				bot.send_message(userchatid,"How many rounds :",reply_markup=reply_m,reply_to_message_id=user.message_id)

		elif usertext=="leave game":
			if search_player(userchatid)==1:
				update_gamelist()
				update_game(get_player_game(userchatid))
				for p in players:
					bot.send_message(p.chatid,userusername+" left the game.",reply_markup=hide_keyboard)
				delete_game(get_player_game(userchatid))
			else:
				bot.send_message(userchatid,"you are not in a game.",reply_markup=hide_keyboard)

		elif usertext=="cancel":
			msg_temp = bot.send_message(userchatid, "OK!", reply_markup=hide_keyboard)
			bot.delete_message(userchatid, msg_temp.message_id)




		elif usertext.startswith("/start "):
			update_gamelist()
			id_game=int(usertext.split()[1])
			for i in games_list :
				if int(id_game)==int(i[0]) :
					if search_player(userchatid)==1:
						reply_m=ReplyKeyboardMarkup()
						reply_m.add("leave game","cancel")
						bot.send_message(userchatid,"you are in a game!",reply_markup=reply_m)
					else:
						update_game(id_game)
						if len(players)==4:
							bot.send_message(userchatid,"game is full.")
						else:
							randoms=make_randoms(id_game)
							add_player_to_game(userchatid,id_game)
							if len(players)==1:
								players.append(player(userusername,randoms[13:26],userchatid,id_game))
								reply_m=ReplyKeyboardMarkup()
								reply_m.add("leave game","cancel")
								bot.send_message(userchatid,"you joined the game.",reply_markup=reply_m)
								msg=bot.send_message(userchatid,"team2")
								msg1=bot.send_message(userchatid,"zamin")
								players[1].msg_carts_id=msg.message_id
								players[1].msg_zamin_id=msg1.message_id
								for p in players:
									matn="team 1 : "+players[0].name+"\nteam 2 : "+players[1].name+"\nwaiting for players..."
									bot.edit_message_text(matn,chat_id=p.chatid,message_id=p.msg_carts_id,)
								update_file(id_game)
							elif len(players)==2:
								players.append(player(userusername,randoms[26:39],userchatid,id_game))
								reply_m=ReplyKeyboardMarkup()
								reply_m.add("leave game","cancel")
								bot.send_message(userchatid,"you joined the game.",reply_markup=reply_m)
								msg=bot.send_message(userchatid,"team 1 :\nyour teamate is "+players[0].name)
								msg1=bot.send_message(userchatid,"zamin")
								players[2].msg_carts_id=msg.message_id
								players[2].msg_zamin_id=msg1.message_id
								for p in players:
									bot.edit_message_text("team 1 : "+players[0].name+"  -  "+players[2].name+"\nteam 2 : "+players[1].name+"\nwaiting for players...",chat_id=p.chatid,message_id=p.msg_carts_id)
								update_file(id_game)
							elif len(players)==3:
								reply_m=ReplyKeyboardMarkup()
								reply_m.add("leave game","cancel")
								players.append(player(userusername,randoms[39:52],userchatid,id_game))
								bot.send_message(userchatid,"you joined the game.",reply_markup=reply_m)
								msg=bot.send_message(userchatid,"team 2 : \nyour teamate is "+players[1].name)
								msg1=bot.send_message(userchatid,"zamin")
								players[3].msg_carts_id=msg.message_id
								players[3].msg_zamin_id=msg1.message_id

								global hakem
								global turn
								hakem=random.randint(0,3)
								turn=hakem
								update_file(id_game)
								matn="team 1: "+players[0].name+" - "+players[2].name+"\nteam 2: "+players[1].name+" - "+players[3].name+"\n"+players[hakem].name+" is hakem"
								for p in players :
									bot.edit_message_text(matn,chat_id=p.chatid,message_id=p.msg_carts_id)

								entekhabe_hokm(players[hakem].carts,players[hakem].chatid)
		else:
			if(search_player(userchatid) == 1):
				update_gamelist()
				game_id = get_player_game(userchatid)
				update_game(game_id)
				for p in players:
					if(p.chatid == userchatid):
						p.message = usertext
						break
				update_file(game_id)



	except Exception as e:
		bot.send_message(36010289,"error in message handler.")
		print(e)

@bot.message_handler(content_types=['voice'])
def botmain1(user):
	userchatid = user.chat.id
	if(search_player(userchatid) == 1):
				update_gamelist()
				game_id = get_player_game(userchatid)
				update_game(game_id)
				for p in players:
					if(p.chatid != userchatid):
						bot.send_voice(p.chatid, user.voice.file_id, caption = user.chat.first_name)	

@bot.message_handler(content_types=['photo'])
def botmain1(user):
	userchatid = user.chat.id
	if(search_player(userchatid) == 1):
				update_gamelist()
				game_id = get_player_game(userchatid)
				update_game(game_id)
				for p in players:
					if(p.chatid != userchatid):
						bot.send_photo(p.chatid, user.photo[0].file_id, caption = user.chat.first_name)

@bot.message_handler(content_types=['animation'])
def botmain1(user):
	userchatid = user.chat.id
	if(search_player(userchatid) == 1):
				update_gamelist()
				game_id = get_player_game(userchatid)
				update_game(game_id)
				for p in players:
					if(p.chatid != userchatid):
						bot.send_animation(p.chatid, user.animation.file_id, caption = user.chat.first_name)

@bot.message_handler(content_types=['sticker'])
def botmain1(user):
	userchatid = user.chat.id
	if(search_player(userchatid) == 1):
				update_gamelist()
				game_id = get_player_game(userchatid)
				update_game(game_id)
				for p in players:
					if(p.chatid != userchatid):
						temp = bot.send_sticker(p.chatid, user.sticker.file_id)
						bot.send_message(p.chatid, user.chat.first_name, reply_to_message_id = temp.message_id)

try:
    bot.stop_polling
    bot.remove_webhook()
    keep_alive()
    bot.infinity_polling()
except Exception as e:
    logging.info(e)
    bot.remove_webhook()
    bot.stop_polling
    keep_alive()
    bot.infinity_polling()