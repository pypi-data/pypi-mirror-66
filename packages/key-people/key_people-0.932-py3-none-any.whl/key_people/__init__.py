import os
import pkg_resources
import sqlite3
from .database_management import open_connection
from .database_management import find_ticker
from .generate_possible_names import generate_possible_names


class Company:
	def __init__(self, ticker):
		self.ticker = ticker
		DB_FILE = pkg_resources.resource_filename('key_people', 'DB/Stocks.db')
		self.conn, self.c = open_connection(DB_FILE)
		NICKNAME_FILE = pkg_resources.resource_filename('key_people', 'DB/Nicknames.db')
		self.n_conn, self.n_c = open_connection(NICKNAME_FILE)
		self.terms = self.pop(ticker)

		

	def pop(self, c):
		ticker = self.ticker.upper()
		results = find_ticker(ticker, self.c)[0]
		ticker = results[0]
		company_name = results[1]
		people = []
		for x in results[2:]:
			if x != 'NULL':
				x = generate_possible_names(x, c)
				people.append(x)

		return {'ticker': ticker, 'company_name': company_name, 'key_people_nicknames': people}

def get_terms(ticker):
	DB_FILE = pkg_resources.resource_filename('key_people', 'DB/Stocks.db')
	conn, c = open_connection(DB_FILE)

	ticker = ticker.upper()
	results = find_ticker(ticker, c)
	ticker = results[0]
	company_name = results[1]
	people = []
	conn.close()
	NICKNAME_FILE = pkg_resources.resource_filename('key_people', 'DB/Nicknames.db')
	conn, c = open_connection(NICKNAME_FILE)
	for x in results[2:]:
		if x != 'NULL':
			x = generate_possible_names(x, c)
			people.append(x)

	return {'ticker': ticker, 'company_name': company_name, 'key_people_nicknames': people}