import os
import pkg_resources
import sqlite3
from .database_management import open_connection
from .database_management import find_ticker

class Key_people:
	def __init__(self):
		DB_FILE = pkg_resources.resource_filename('key_people', 'DB/Stocks.db')
		self.conn, self.c = open_connection(DB_FILE)

	def search(self, ticker):
		ticker = ticker.upper()
		ticker = (ticker, )
		results = find_ticker(ticker, self.c)[0]
		ticker = results[0]
		company_name = results[1]
		people = []
		for x in results[2:]:
			if x != 'NULL':
				people.append(x)
		return Entry(ticker, company_name, people)

class Entry:
	def __init__(self, ticker, company_name, people):
		self.key_people = people
		self.company_name = company_name
		self.ticker = ticker

def search(ticker):
	ticker = ticker.upper()
	DB_FILE = pkg_resources.resource_filename('key_people', 'DB/Stocks.db')
	conn, c = open_connection(DB_FILE)
	ticker = (ticker, )
	results = find_ticker(ticker, c)[0]
	ticker = results[0]
	company_name = results[1]
	people = []
	for x in results[2:]:
		if x != 'NULL':
			people.append(x)
	conn.close()
	return people
	
def search_company_name(ticker):
	ticker = ticker.upper()
	DB_FILE = pkg_resources.resource_filename('key_people', 'DB/Stocks.db')
	conn, c = open_connection(DB_FILE)
	ticker = (ticker, )
	results = find_ticker(ticker, c)[0]
	company_name = results[1]
	conn.close()
	return company_name