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



# tracks last files and folders opened (used to populate "Recent" menu on Start Menu)
def recent_files():
	# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs


# recent files opened with office tools
def office_recent_files():
	# NTUSER.DAT\Software\Microsoft\Office\VERSION
	# NTUSER.DAT\Software\Microsoft\Office\10.0\Excel|Recent Files ..... different for every MS office tool 

# recently browsed folders on explorer
def shell_bags(): 
	# NTUSER.DAT\Software\Microsoft\Windows\Shell\Bags 
	# NTUSER.DAT\Software\Microsoft\Windows\ShellNoRoam\Bags 

# .lnk files automatically created by windows for recent items
def shortcut_files(): 
	# C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Recent\ 


# files accessed on the browser like "file:\\C:\dir\file.txt"
def recent_browser_files():
	# %userprofile%\AppData\Local\Microsoft\Windows\History\History.IE5\index.da