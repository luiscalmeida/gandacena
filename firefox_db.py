import sqlite3
import sys
import os

def firefox_db_visited_urls(path):  # places.sqlite
	conn = sqlite3.connect(path)
	c = conn.cursor()
	contacts = c.execute("SELECT * FROM 'moz_places'")
	for row in c.fetchall():
		print row[1]
	conn.close()

def firefox_db_typed_urls(path):  # places.sqlite
	conn = sqlite3.connect(path)
	c = conn.cursor()
	contacts = c.execute("SELECT * FROM 'moz_inputhistory'")
	for row in c.fetchall():
		print row[1]
	conn.close()

## needed to cross moz_places with moz_historyvisits, too complicated
def firefox_db_visit_numb(path):  # places.sqlite
	conn = sqlite3.connect(path)
	c = conn.cursor()
	contacts = c.execute("SELECT * FROM 'moz_historyvisits'")
	for row in c.fetchall():
		print row[0]
	conn.close()

def firefox_db_bookmarks(path):  # places.sqlite
	bookmarks = []
	conn = sqlite3.connect(path)
	c = conn.cursor()
	contacts = c.execute("SELECT * FROM 'moz_bookmarks'")
	for row in c.fetchall():
		if not row[5] in bookmarks:
			bookmarks.append(row[5])
			print row[5]
	conn.close()

def firefox_db_downloads(path):  # places.sqlite
	index = 0
	conn = sqlite3.connect(path)
	c = conn.cursor()
	contacts = c.execute("SELECT lastModified FROM 'moz_annos'")
	for row in c.fetchall():
		if index % 3 == 0:
			print row[4]
		index = index + 1
	conn.close()

#firefox_db_visited_urls("../places.sqlite")
#firefox_db_typed_urls("../places.sqlite")
#firefox_db_visit_numb("../places.sqlite")
#firefox_db_bookmarks("../places.sqlite")
#firefox_db_downloads("../places.sqlite")