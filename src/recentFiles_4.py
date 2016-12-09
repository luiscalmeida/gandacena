import sys
import os
import firefox_db
from libs.Registry import Registry

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
		return False
		#sys.exit(-1)

def open_key_tab(reg, path):
	try:
		return reg.open(path)
	except Registry.RegistryKeyNotFoundException:
		print "\t" + bcolors.FAIL + "[-]" + bcolors.ENDC + "Can't find any keys"
		return False
		#sys.exit(-1)

def open_key_false(reg, path):
	try:
		return reg.open(path)
	except Registry.RegistryKeyNotFoundException:
		return False
		#sys.exit(-1)

#######################################################################
#######################################################################


plus = bcolors.BOLD + bcolors.OKBLUE + "[+]" + bcolors.ENDC
fail = bcolors.BOLD + bcolors.FAIL + "[-]" + bcolors.ENDC
success = bcolors.BOLD + bcolors.OKGREEN + "[-]" + bcolors.ENDC

# tracks last files and folders opened (used to populate "Recent" menu on Start Menu)
def recent_files(reg, user):
	print (bcolors.BOLD + ("=" * 24) + " RECENT FILES " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs"
	print("---------------------------------------")
		
	try:
		global var
		var = ""
		global word
		word = ""
		key = open_key(reg, "Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs")
		for v in key.subkeys():
			print success + v.name() + ":"
			for vv in v.values():
				word = ""
				if not vv.name() == "MRUListEx":
					for l in vv.value():
						if ord(l) > 122 and ord(l) < 45:
							word += ""
						else:
							word += l
					var = ""
					for block in word.split("*"):
						#print block
						var = block
						var = var[:-14]
					if not "." in var and v.name() != "Folder":
						var = var + v.name()
					#if var.endswith(v.name()):
					print  "\t" + success + var  #should be value if we could convert binary to string
	except:
		print fail + "No RecentDocs key"
	print " " 
	
	"""try:
		counter=[]
		counter.append(0)
		for entry in os.listdir("./mnt/Users/" + user + "/Recent"):
			if entry != "AutomaticDestinations" and entry != "CustomDestinations"\
			and not entry.endswith(".ini") and not entry.endswith(".lnk"):  #exclude these folders
				counter[0] += 1
				print success + entry
		if counter[0] == 0:
			print fail + "No recent documents"
	except:
		print fail + "No Recent folder"
	print " " """
	# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs

# recent files opened with office tools
def office_recent_files(reg):
	print (bcolors.BOLD + ("=" * 24) + " OFFICE RECENT FILES " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "NTUSER.DAT\Software\Microsoft\Office\VERSION\Word\File MRU"
	print plus + "NTUSER.DAT\Software\Microsoft\Office\VERSION\PowerPoint\File MRU"
	print("---------------------------------------")
	try:
		key = open_key_false(reg, "Software\Microsoft\Office")
		for v in key.subkeys():
			if v.name().startswith("0") or v.name().startswith("1") or v.name().startswith("2"):
				print "Version " + v.name()
				key1 = open_key_false(reg, "Software\Microsoft\Office\\" + str(v.name()) + "\Word\File MRU")
				if key1 != False:
					print "    " + success + "Word:"
					for v in key1.values():
						print "\t" + success + v.value().split("*")[1]
				key2 = open_key_false(reg, "Software\Microsoft\Office\\" + str(v.name()) + "\PowerPoint\File MRU")
				if key2 != False:	
					print "    " + success + "PowerPoint:"
					for v in key2.values():
						print "\t" + success + v.value().split("*")[1]
				if(key1 == False and key2 == False):
					print "    " + fail + "No documents found on Office " + v.name()
	except:
		print fail + "No Office installed"
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
		result = []
		index = []
		index.append(0)
		key = open_key(reg, "Software\Microsoft\Windows\Shell\Bags")
		for v in key.subkeys():
			for vv in v.subkeys():
				if not vv.name() in result:
					index[0] += 1
					result.append(vv.name())
					print success + vv.name()
		if index[0] == 0:
			print "No Shell\Bags items found"
	except:
		print fail + "No Shell\Bags key"
	print " "
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
			if entry.endswith(".lnk"):  #exclude these folders
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
	print plus + "C:\Users\<username>\AppData\Roaming\Mozilla\Firefox\Profiles\<random text>.default\downloads.sqlite"
	print("---------------------------------------")
	print "Firefox:"
	try:
		random_dir = os.listdir("./mnt/Users/" + user + "/AppData/Roaming/Mozilla/Firefox/Profiles")
		firefox_db.firefox_db_files("./mnt/Users/" + user + "/AppData/Roaming/Mozilla/Firefox/Profiles/" + random_dir[0] + "/places.sqlite")
	except:
		print "    " + fail + "No Mozilla Firefox installed"
	try:
		result = []
		counter = []
		counter.append(0)
		print "Internet Explorer:"
		key = open_key(reg, "Software\Microsoft\Internet Explorer\TypedURLs")
		for v in key.values():
			result.append(v.value())
		for vv in result:
			if vv.startswith("file:\\\\"):
				counter[0] = counter[0] + 1
		if counter[0] != 0:
			for vvv in result:
				print "    " + success + vvv
		else:
			print "    " + fail + "No files opened on the browser"
	except:
		print fail + "No TypedURLs key"
	print " "
	# %userprofile%\AppData\Local\Microsoft\Windows\History\History.IE5\index.dat

#def recent_deleted_files()
