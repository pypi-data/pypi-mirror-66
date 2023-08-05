import os
import pkg_resources
import importlib.util
db = importlib.__import__('database_Management')



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