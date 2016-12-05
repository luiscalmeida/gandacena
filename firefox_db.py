import sqlite3
import sys

def skype_db_contacts(path):
	conn = sqlite3.connect('../main.db')
	c = conn.cursor()
	contacts = c.execute("SELECT * FROM 'Contacts'")
	for row in c.fetchall():
		sys.stdout.write(row[3])
		if len(row[3]) > 23:
			sys.stdout.write(" \t: ")
		elif len(row[3]) >= 15:
			sys.stdout.write(" \t\t: ")
		elif len(row[3]) < 7:
			sys.stdout.write(" \t\t\t\t: ")
		else:	
			sys.stdout.write(" \t\t\t: ")
		if not row[6] is None:
			sys.stdout.write(row[6].encode('utf-8', 'ignore'))
		if not row[15] is None:
			sys.stdout.write(" \t\t: ")
			sys.stdout.write(str(row[15]))
		sys.stdout.write("\n")
	conn.close()

def skype_db_transfers(path):
	conn = sqlite3.connect('../main.db')
	c = conn.cursor()
	contacts = c.execute("SELECT * FROM 'Transfers'")
	for row in c.fetchall():
		print row
	conn.close()

#skype_db_transfers("../main.db")