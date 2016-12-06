import sqlite3
import sys
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

success = bcolors.BOLD + bcolors.OKGREEN + "[-]" + bcolors.ENDC

def firefox_db_visited_urls(path):  # places.sqlite
	conn = sqlite3.connect(path)
	c = conn.cursor()
	contacts = c.execute("SELECT * FROM 'moz_places'")
	for row in c.fetchall():
		print success + row[1]
	conn.close()

def firefox_db_typed_urls(path):  # places.sqlite
	conn = sqlite3.connect(path)
	c = conn.cursor()
	contacts = c.execute("SELECT * FROM 'moz_inputhistory'")
	for row in c.fetchall():
		print success + row[1]
	conn.close()

## needed to cross moz_places with moz_historyvisits, too complicated
def firefox_db_visit_numb(path):  # places.sqlite
	conn = sqlite3.connect(path)
	c = conn.cursor()
	contacts = c.execute("SELECT * FROM 'moz_historyvisits'")
	for row in c.fetchall():
		print success + row[0]
	conn.close()

def firefox_db_bookmarks(path):  # places.sqlite
	bookmarks = []
	conn = sqlite3.connect(path)
	c = conn.cursor()
	contacts = c.execute("SELECT * FROM 'moz_bookmarks'")
	for row in c.fetchall():
		if not row[5] in bookmarks:
			bookmarks.append(row[5])
			print success + row[5]
	conn.close()

def firefox_db_downloads(path):  # places.sqlite
	index = 0
	conn = sqlite3.connect(path)
	c = conn.cursor()
	contacts = c.execute("SELECT * FROM 'moz_annos'")
	for row in c.fetchall():
		if index % 3 == 0:
			print success + row[4]
		index = index + 1
	conn.close()

#firefox_db_visited_urls("../places.sqlite")
#firefox_db_typed_urls("../places.sqlite")
#firefox_db_visit_numb("../places.sqlite")
#firefox_db_bookmarks("../places.sqlite")
#firefox_db_downloads("../places.sqlite")