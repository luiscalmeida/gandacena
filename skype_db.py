import sqlite3
import sys

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

def skype_db_contacts(path):
	conn = sqlite3.connect('../main.db')
	c = conn.cursor()
	contacts = c.execute("SELECT * FROM 'Contacts'")
	for row in c.fetchall():
		sys.stdout.write(success +row[3])
		if len(row[3]) > 20:
			sys.stdout.write(" \t: ")
		elif len(row[3]) >= 12:
			sys.stdout.write(" \t\t: ")
		elif len(row[3]) < 4:
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
		print success + row
	conn.close()

#skype_db_transfers("../main.db")