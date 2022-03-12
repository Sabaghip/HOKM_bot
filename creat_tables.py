import sqlite3 

DIR_PATH = "F:\\parsa\\HOKM_BOT\\mysql-branch\\"
con = sqlite3.connect(DIR_PATH + "HOKM_BOT_DB.db")
cur = con.cursor()
cur.execute("""CREATE TABLE all_players(
					chat_id VARCHAR PRIMARY KEY,
					ingame INT,
					gameid VARCHAR(10),
					points INT,
					level INT
					);""")
cur.execute("""CREATE TABLE all_games(
					gameid VARCHAR(10) PRIMARY KEY,
					players_num INT,
					p1_chatid VARCHAR(13),
					p2_chatid VARCHAR(13),
					p3_chatid VARCHAR(13),
					p4_chatid VARCHAR(13),
					p1_carts VARCHAR(150),
					p2_carts VARCHAR(150),
					p3_carts VARCHAR(150),
					p4_carts VARCHAR(150),
					p1_name VARCHAR(13),
					p2_name VARCHAR(13),
					p3_name VARCHAR(13),
					p4_name VARCHAR(13),
					zamin_carts VARCHAR(35),
					hokm VARCHAR(1),
					hakem INT,
					turn INT,
					dast VARCHAR(1),
					team1_wins INT,
					team2_wins INT,
					last_win INT,
					p1_msg_cartsid INT,
					p2_msg_cartsid INT,
					p3_msg_cartsid INT,
					p4_msg_cartsid INT,
					p1_msg_zaminid INT,
					p2_msg_zaminid INT,
					p3_msg_zaminid INT,
					p4_msg_zaminid INT,
					team1_wins_t INT,
					team2_wins_t INT,
					size_zamin INT,
					lasthigh_shekl VARCHAR(1),
					lasthigh_adad INT,
					roundstowin INT,
					p1msg VARCHAR(20),
					p2msg VARCHAR(20),
					p3msg VARCHAR(20),
					p4msg VARCHAR(20)
					);""")
con.commit()