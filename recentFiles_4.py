import sys
import os
from Registry import Registry

################################ UTILS ################################

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_values(key):
	for value in [v for v in key.values()]:
		if v.value_type() == Registry.RegSZ or v.value_type() == Registry.RegExpandSZ:
			print "%s = %s" % (value.name(), value.value())

def open_key(reg, path):
	try:
		return reg.open(path)
	except Registry.RegistryKeyNotFoundException:
		print bcolors.FAIL + "[-]" + bcolors.ENDC + "Can't find any keys"
		#sys.exit(-1)

#######################################################################
#######################################################################


plus = bcolors.BOLD + bcolors.OKBLUE + "[+]" + bcolors.ENDC
fail = bcolors.BOLD + bcolors.FAIL + "[-]" + bcolors.ENDC
success = bcolors.BOLD + bcolors.OKGREEN + "[-]" + bcolors.ENDC

# tracks last files and folders opened (used to populate "Recent" menu on Start Menu)
def recent_files(reg):
	print (bcolors.BOLD + ("=" * 24) + " RECENT FILES " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs"
	print("---------------------------------------")
	try:
		key = open_key(reg, "Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs")
		for v in key.subkeys():
			for vv in v.subkeys():
				print success + vv.name()
	except:
		print fail + "No RecentDocs key"
	print " "
	#print_values(key)
	# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs
	print " "

# recent files opened with office tools
def office_recent_files(reg):
	print (bcolors.BOLD + ("=" * 24) + " OFFICE RECENT FILES " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "NTUSER.DAT\Software\Microsoft\Office\VERSION\Word\Data"
	print plus + "NTUSER.DAT\Software\Microsoft\Office\VERSION\Excel\Recent Files"
	print("---------------------------------------")
	try:
		key = open_key(reg, "Software\Microsoft\Office")
		for v in key.subkeys():
			#print v.name()
			key = open_key(reg, "Software\\Microsoft\\Office\\" + v.name() + "\\Word\\Data")
			for v in key.values():
				print success + v.name()
			key = open_key(reg, "Software\\Microsoft\\Office\\" + v.name() + "\\Excel\\Recent Files")
			for v in key.values():
				print success + v.name()
	except:
		print fail + "Deprecated method on this version of Office"
	print " "
	# NTUSER.DAT\Software\Microsoft\Office\VERSION
	# NTUSER.DAT\Software\Microsoft\Office\10.0\Excel|Recent Files ..... different for every MS office tool 

# recently browsed folders on explorer
def shell_bags(reg):
	print (bcolors.BOLD + ("=" * 24) + " SHELL BAGS " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "NTUSER.DAT\Software\Microsoft\Windows\Shell\Bags"
	print("---------------------------------------")
	try:
		key = open_key(reg, "Software\Microsoft\Windows\Shell\Bags")
		for v in key.subkeys():
			for vv in v.subkeys():
				print success + vv.name()
	except:
		print fail + "No Shell\Bags key"
	print " "
	#print_values(key)
	#key = open_key(reg, "Software\Microsoft\Windows\ShellNoRoam\Bags")
	#print_values(key)
	# NTUSER.DAT\Software\Microsoft\Windows\Shell\Bags 
	# NTUSER.DAT\Software\Microsoft\Windows\ShellNoRoam\Bags 

# .lnk files automatically created by windows for recent items
def shortcut_files(reg, user): 
	print (bcolors.BOLD + ("=" * 24) + " SHORTCUT FILES " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "C:\Users\\" + user + "\AppData\Roaming\Microsoft\Windows\Recent"
	print("---------------------------------------")
	# os.chdir(path)
	# os.chdir("./mnt/Users/admin11/AppData/Roaming/Microsoft/Windows/Recent")
	try:
		for entry in os.listdir("./mnt/Users/" + user + "/AppData/Roaming/Microsoft/Windows/Recent"):
			if entry != "AutomaticDestinations" and entry != "CustomDestinations":  #exclude these folders
				print success + entry
	except:
		print fail + "No Recent folder"
	print " "
	# C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Recent\ 
	# instead of Recent -> Recent Items


# files accessed on the browser like "file:\\C:\dir\file.txt"
def recent_browser_files(reg, user):
	print (bcolors.BOLD + ("=" * 24) + " RECENT BROWSER FILES " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "C:\Users\\" + user + "\AppData\Local\Microsoft\Windows\History\History.IE5\index.dat"
	print("---------------------------------------")


	print " "
	# %userprofile%\AppData\Local\Microsoft\Windows\History\History.IE5\index.dat

#def recent_deleted_files()