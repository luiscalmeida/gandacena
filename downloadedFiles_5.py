import sys
from Registry import Registry

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
def email_attachments(reg):
	print " "
	print "***** EMAIL ATTACHMENTS *****"
	print " "
	# %USERPROFILE%\AppData\Local\Microsoft\Outlook 


# Log of transfered files from skype
def skype_history(reg):
	print " "
	print "***** SKYPE HISTORY *****"
	print " "
	# C:\Users\<username>\AppData\Roaming\Skype\<skype-name> 


# Internet Explorer download history
def downloads_IE(reg): #index.dat file
	print " "
	print "***** DOWNLOADS INTERNET EXPLORER *****"
	print " "
	# %userprofile%\AppData\Local\Microsoft\Windows\History\History.IE5 
	# %userprofile%\AppData\Local\Microsoft\Windows\History\Low\History.IE5 


#Firefox built-in download manager keeps download history
def downloads_FF(reg): #downloads.sqlite
	print " "
	print "***** DOWNLOADS FIREFOX *****"
	print " "
	# %userprofile%\AppData\Roaming\Mozilla\Firefox\Profiles\<random text>.default\downloads.sqlite	