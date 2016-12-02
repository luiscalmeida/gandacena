import sys
from Registry import Registry

################################ UTILS ################################

def print_values(key):
	for value in [v for v in key.values()]:
		#if v.value_type() == Registry.RegSZ or v.value_type() == Registry.RegExpandSZ:
		print "%s = %s" % (value.name(), value.value())

def open_key(reg, path):
	try:
		key = reg.open(path)
	except Registry.RegistryKeyNotFoundException:
		print("Can't find any keys (later will erase this print. User doesn't need to know)")
		sys.exit(-1)

#######################################################################
#######################################################################



# (MRU - most recently used) tracks opened and saved files within a windows shell dialog box
def open_save_MRU():
	input_hive = raw_input() #com input ./mnt/Users/admin11/NTUSER.DAT
	reg = Registry.Registry(input_hive)
	open_key(reg, "Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePIDIMRU")
	print_values(key)


# downloads via e-mail attachments
def email_attachments():
	# %USERPROFILE%\AppData\Local\Microsoft\Outlook 


# Log of transfered files from skype
def skype_history():
	# C:\Users\<username>\AppData\Roaming\Skype\<skype-name> 


# Internet Explorer download history
def downloads_IE(): #index.dat file
	# %userprofile%\AppData\Local\Microsoft\Windows\History\History.IE5 !Win7: %userprofile%\AppData\Local\Microsoft\Windows\History\Low\History.IE5 


#Firefox built-in download manager keeps download history
def downloads_FF(): #downloads.sqlite
	# %userprofile%\AppData\Roaming\Mozilla\Firefox\Profiles\<random text>.default\downloads.sqlite	