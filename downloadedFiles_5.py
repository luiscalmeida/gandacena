import sys
import os
from pprint import pprint
#import pasco
from Registry import Registry
import skype_db

################################ UTILS ################################

def print_values(key):
	for value in [v for v in key.values()]:
		#if v.value_type() == Registry.RegSZ or v.value_type() == Registry.RegExpandSZ:
		print "%s = %s" % (value.name(), value.value())

def open_key(reg, path):
	try:
		return reg.open(path)
	except Registry.RegistryKeyNotFoundException:
		print("Can't find any keys (later will erase this print. User doesn't need to know)")
		#sys.exit(-1)

#######################################################################
#######################################################################



# (MRU - most recently used) tracks opened and saved files within a windows shell dialog box
def open_save_MRU(reg):
	print " "
	print "***** OPEN SAVE MRU *****"
	print " "
	#input_hive = raw_input() #com input ./mnt/Users/admin11/NTUSER.DAT
	#input_hive = "./mnt/Users/admin11/NTUSER.DAT"
	#reg = Registry.Registry(input_hive)
	#rec(reg.root())
	key = open_key(reg, "Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePIDlMRU")
	print_values(key)


# downloads via e-mail attachments
def email_attachments(reg, user):
	print " "
	print "***** EMAIL ATTACHMENTS *****"
	print " "
	# %USERPROFILE%\AppData\Local\Microsoft\Outlook 


# Log of transfered files from skype
def skype_history(reg, user):
	print " "
	print "***** SKYPE HISTORY *****"
	print " "
	try:
		for entry in os.listdir("./mnt/Users/" + user + "/AppData/Roaming/Skype"):
			if entry != "Content" and entry != "DataRv" and entry != "My Skype Received Files" \
			and entry != "RootTools" and entry != "shared.lck" and entry != "shared.xml" \
			and entry != "shared_dynco" and entry != "shared_httpfe":
				skype_name = entry
		skype_db.skype_db_contacts("./mnt/Users/" + user + "/AppData/Roaming/Skype/" + skype_name + "/main.db")
		skype_db.skype_db_transfers("./mnt/Users/" + user + "/AppData/Roaming/Skype/" + skype_name + "/main.db")
	except:
		print "No Skype Directory"
	# C:\Users\<username>\AppData\Roaming\Skype\<skype-name> 


# Internet Explorer download history
def downloads_IE(reg, user): #index.dat file
	print " "
	print "***** DOWNLOADS INTERNET EXPLORER *****"
	print " "
	"""ip = pasco.IndexParser()
	for match in ip.parse("./m"):
		if match:
			pprint(match)"""
	# %userprofile%\AppData\Local\Microsoft\Windows\History\History.IE5 
	# %userprofile%\AppData\Local\Microsoft\Windows\History\Low\History.IE5 


#Firefox built-in download manager keeps download history
def downloads_FF(reg, user): #downloads.sqlite
	print " "
	print "***** DOWNLOADS FIREFOX *****"
	print " "
	random_dir = os.listdir("./mnt/Users/" + user + "/AppData/Roaming/Mozilla/Firefox/Profiles")
	firefox_db_downloads("./mnt/Users/" + user + "/AppData/Roaming/Mozilla/Firefox/Profiles" + random_dir[0] + "/places.sqlite")
	# %userprofile%\AppData\Roaming\Mozilla\Firefox\Profiles\<random text>.default\downloads.sqlite	
