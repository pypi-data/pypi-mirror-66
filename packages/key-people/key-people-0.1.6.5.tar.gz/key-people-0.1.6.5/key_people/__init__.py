import os
import pkg_resources
import importlib.util
import sqlite3

def create_Table(c):
	c.execute('''CREATE TABLE stocks
             (symbol text, name text, key_person_1 text, key_person_2 text, key_person_3 text, key_person_4 text, key_person_5 text, key_person_6 text)''')

def find_Ticker(ticker, c):
	c.execute('SELECT * FROM stocks WHERE symbol=?', ticker)
	return c.fetchmany()

def add_Entry(entry, c):
	c.execute('INSERT INTO stocks VALUES (?,?,?,?,?,?,?,?)', entry)

def add_Many_Entry(entries, c):
	c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?,?,?,?)', entries)

def open_Connection(file):
	conn = sqlite3.connect(file)
	c = conn.cursor()
	return conn, c

def commit_Close(conn):
	conn.commit()
	conn.close()

class Key_people:
	def __init__(self):
		DB_FILE = pkg_resources.resource_filename('key-people', 'DB/Stocks.db')
		self.conn, self.c = db.open_Connection(DB_FILE)

	def entry(self, ticker):
		ticker = ticker.upper()
		ticker = (ticker, )
		results = db.find_Ticker(ticker, self.c)[0]
		ticker = results[0]
		company_Name = results[1]
		people = []
		for x in results[2:]:
			if x != 'NULL':
				people.append(x)
		return entry(ticker, company_Name, people)

class entry:
	def __init__(self, ticker, company_Name, people):
		self.key_People = people
		self.company_Name = company_Name
		self.ticker = ticker

def get_key_people(ticker):
	ticker = ticker.upper()
	DB_FILE = pkg_resources.resource_filename('key-people', 'DB/Stocks.db')
	conn, c = db.open_Connection(DB_FILE)
	ticker = (ticker, )
	results = db.find_Ticker(ticker, c)[0]
	ticker = results[0]
	company_Name = results[1]
	people = []
	for x in results[2:]:
		if x != 'NULL':
			people.append(x)
	conn.close()
	return people