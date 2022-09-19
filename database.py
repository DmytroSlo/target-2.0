import sqlite3

with sqlite3.connect('db/database.db') as db:
	cursor = db.cursor()
	query = """ CREATE TABLE IF NOT EXISTS targets(id INTEGER KEY, SN TEXT, Action TEXT, Punct INTEGER) """
	cursor.execute(query)


with sqlite3.connect('db/database.db') as db:
	cursor = db.cursor()
	query = """ INSERT INTO targets (sn, action, punct)VALUES ('32B20604949320551', 'BGAPR', '0.5') """
	query1 = """	INSERT INTO targets (sn, action, punct)VALUES ('32B20604949320551', 'REP', '1') """
	query2 = """ INSERT INTO targets (sn, action, punct)VALUES ('32B20604977320551', 'REP', '1') """
	query3 = """ INSERT INTO targets (sn, action, punct)VALUES ('32B20604935320551', 'HOLD', '0.5') """
	query4 = """ INSERT INTO targets (sn, action, punct)VALUES ('32B20604155320551', 'BGAPR', '0.5') """
	cursor.execute(query)
	cursor.execute(query1)
	cursor.execute(query2)
	cursor.execute(query3)
	cursor.execute(query4)
	db.commit()