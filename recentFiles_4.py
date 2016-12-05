import sys
import os
from Registry import Registry

################################ UTILS ################################

def print_values(key):
	for value in [v for v in key.values()]:
		if v.value_type() == Registry.RegSZ or v.value_type() == Registry.RegExpandSZ:
			print "%s = %s" % (value.name(), value.value())

def open_key(reg, path):
	try:
		return reg.open(path)
	except Registry.RegistryKeyNotFoundException:
		print "Can't find any keys (later will erase this print. User doesn't need to know)"
		#sys.exit(-1)

#######################################################################
#######################################################################



# tracks last files and folders opened (used to populate "Recent" menu on Start Menu)
def recent_files(reg):
	print " "
	print "***** RECENT FILES *****"
	print " "
	key = open_key(reg, "Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs")
	print_values(key)
	# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs
	print " "

# recent files opened with office tools
def office_recent_files(reg):
	print " "
	print "***** OFFICE RECENT FILES *****"
	print " "
	# NTUSER.DAT\Software\Microsoft\Office\VERSION
	# NTUSER.DAT\Software\Microsoft\Office\10.0\Excel|Recent Files ..... different for every MS office tool 

# recently browsed folders on explorer
def shell_bags(reg): 
	print " "
	print "***** SHELL BAGS *****"
	print " "
	key = open_key(reg, "Software\Microsoft\Windows\Shell\Bags")
	print_values(key)
	#key = open_key(reg, "Software\Microsoft\Windows\ShellNoRoam\Bags")
	#print_values(key)
	# NTUSER.DAT\Software\Microsoft\Windows\Shell\Bags 
	# NTUSER.DAT\Software\Microsoft\Windows\ShellNoRoam\Bags 

# .lnk files automatically created by windows for recent items
def shortcut_files(reg, user): 
	print " "
	print "***** SHORTCUT FILES *****"
	print " "
	# os.chdir(path)
	# os.chdir("./mnt/Users/admin11/AppData/Roaming/Microsoft/Windows/Recent")
	for entry in os.listdir("./mnt/Users/" + user + "/AppData/Roaming/Microsoft/Windows/Recent"):
		if entry != "AutomaticDestinations" and entry != "CustomDestinations":  #exclude these folders
			print entry
	# C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Recent\ 
	# instead of Recent -> Recent Items


# files accessed on the browser like "file:\\C:\dir\file.txt"
def recent_browser_files(reg, user):
	print " "
	print "***** RECENT BROWSER FILES *****"
	print " "
	# %userprofile%\AppData\Local\Microsoft\Windows\History\History.IE5\index.dat