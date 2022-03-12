import sqlite3 

DIR_PATH = "F:\\parsa\\HOKM_BOT\\mysql-branch\\"
con = sqlite3.connect(DIR_PATH + "HOKM_BOT_DB.db")
cur = con.cursor()
cur.execute("""CREATE TABLE all_playrs(
					chat_id VARCHAR PRIMARY KEY,
					ingame INT,
					gameid VARCHAR(10)
					);""")
cur.execute("""CREATE TABLE all_games(
					gameid VARCHAR(10) PRIMARY KEY,
					player1 VARCHAR(13)
					);""")
cur.execute("""CREATE TABLE carts(
					gameid VARCHAR(10) PRIMARY KEY,
					shekl VARCHAR(1),
					adad INT
					);""")
con.commit()