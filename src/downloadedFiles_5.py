import sys
import os
from pprint import pprint
#from pasco import *
from libs.Registry import Registry
import skype_db
import firefox_db

################################ UTILS ################################

def print_values(key):
	for value in [v for v in key.values()]:
		#if v.value_type() == Registry.RegSZ or v.value_type() == Registry.RegExpandSZ:
		print "%s = %s" % (value.name(), value.value())

def open_key(reg, path):
	try:
		return reg.open(path)
	except Registry.RegistryKeyNotFoundException:
		print(fail + "Can't find any keys")
		#sys.exit(-1)

#######################################################################
#######################################################################

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

plus = bcolors.BOLD + bcolors.OKBLUE + "[+]" + bcolors.ENDC
fail = bcolors.BOLD + bcolors.FAIL + "[-]" + bcolors.ENDC
success = bcolors.BOLD + bcolors.OKGREEN + "[-]" + bcolors.ENDC

# (MRU - most recently used) tracks opened and saved files within a windows shell dialog box
def open_save_MRU(reg):
	print (bcolors.BOLD + ("=" * 24) + " OPEN SAVE MRU " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePIDlMRU"
	print("---------------------------------------")
	try:
		i = []
		i.append(0)
		key = open_key(reg, "Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePIDlMRU")
		files = ""
		word = ""
		index = 0
		for value in key.subkeys():
			for v in value.values():
				for c in v.value():
					if((ord(c) >= 32 and ord(c) <= 125) or(ord(c) == 0) or(ord(c) == 9) or(ord(c) == 10) or(ord(c) == 13)):
						word = word + c
					else:
						word = word + "%"
				files = files + word + "%"
				word = ""
		for f in files.split("%"):
			if("." in f and len(f)>2 and len(f.split(".")) > 2):
				i[0] += 1
				if not "*" in f:
					print success + f	
				"""for a in f:
					if (a == "" or a == " ") and index == 0:
						pass
					else:
						sys.stdout.write(a)
					index = index + 1
				index = 0
				sys.stdout.write("\n")"""
		if i[0] == 0:
			print "No Recently used files within a windows shell dialog box"
	except:
		print fail + "No OpenSavePidlMRU key"
	print " "


# downloads via e-mail attachments
def email_attachments(reg, user):
	print (bcolors.BOLD + ("=" * 24) + " EMAIL ATTACHMENTS " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "C:\Users\<username>\AppData\Local\Microsoft\Outlook"
	print("---------------------------------------")
	try:
		for entry in os.listdir("./mnt/Users/" + user + "/AppData/Local/Microsoft/Outlook"):
			if entry.endswith(".pst"):
				print success + entry
	except:
		print fail + "No Outlook installed"
	print " "
	# %USERPROFILE%\AppData\Local\Microsoft\Outlook 


# Log of transfered files from skype
def skype_history(reg, user):
	print (bcolors.BOLD + ("=" * 24) + " SKYPE HISTORY " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "C:\Users\<username>\AppData\Roaming\Skype\<skype-name>\main.db"
	print("---------------------------------------")
	try:
		skype_dir = "./mnt/Users/" + user + "/AppData/Roaming/Skype"
		for entry in os.listdir(skype_dir):
			if entry != "Content" and entry != "DataRv" and entry != "My Skype Received Files" \
			and entry != "RootTools" and entry != "shared.lck" and entry != "shared.xml" \
			and entry != "shared_dynco" and entry != "shared_httpfe":
				skype_name = entry
		print "Contacts:"
		skype_db.skype_db_contacts(skype_dir + "/" + skype_name + "/main.db")
		print "Transfers:"
		skype_db.skype_db_transfers(skype_dir + "/" + skype_name + "/main.db")
	except:
		print fail + "No Skype Directory"
	print " "
	# C:\Users\<username>\AppData\Roaming\Skype\<skype-name> 


# Internet Explorer download history
def downloads_IE(reg, user): #index.dat file
	print (bcolors.BOLD + ("=" * 24) + " DOWNLOADS INTERNET EXPLORER " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "C:\Users\<username>\AppData\Local\Microsoft\Windows\History\History.IE5\index.dat"
	print("---------------------------------------")
	try:
		ip = pasco.IndexParser()
		for match in ip.parse(".mnt/Users/" + user + "/AppData/Local/Microsoft/Windows/History/History.IE5/index.dat"):
			if match:
				pprint(match)
	except:
		print fail + "No index.dat file"
	print " "
	# %userprofile%\AppData\Local\Microsoft\Windows\History\History.IE5 
	# %userprofile%\AppData\Local\Microsoft\Windows\History\Low\History.IE5 


#Firefox built-in download manager keeps download history
def downloads_FF(reg, user): #downloads.sqlite
	print (bcolors.BOLD + ("=" * 24) + " DOWNLOADS FIREFOX " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "C:\Users\<username>\AppData\Roaming\Mozilla\Firefox\Profiles\<random text>.default\downloads.sqlite"
	print("---------------------------------------")
	try:
		random_dir = os.listdir("./mnt/Users/" + user + "/AppData/Roaming/Mozilla/Firefox/Profiles")
		firefox_db.firefox_db_downloads("./mnt/Users/" + user + "/AppData/Roaming/Mozilla/Firefox/Profiles/" + random_dir[0] + "/places.sqlite")
		#random_dir = os.listdir("./mnt/Users/" + user + "/AppData/Roaming/Mozilla/Firefox/Profiles")
		#firefox_db_downloads("./mnt/Users/" + user + "/AppData/Roaming/Mozilla/Firefox/Profiles/" + random_dir[0] + "/places.sqlite")
	except:
		print fail + "No Mozilla\Firefox Directory"
	#print " "
	# %userprofile%\AppData\Roaming\Mozilla\Firefox\Profiles\<random text>.default\downloads.sqlite	
