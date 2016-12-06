import sys
import os
import binascii
from Registry import Registry

################################ UTILS ################################

def print_values(key):
	for value in [v for v in key.values()]:
		if v.value_type() == Registry.RegSZ or v.value_type() == Registry.RegExpandSZ:
			print success + "%s = %s" % (value.name(), value.value())

def open_key(reg, path):
	try:
		return reg.open(path)
	except Registry.RegistryKeyNotFoundException:
		print(fail + "Can't find any keys")

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

def control_set_check(reg): 
	"""	Determine which Control Set the system was using """
	registry = Registry.Registry(reg)
	key = registry.open("Select")    
	for v in key.values():
		if v.name() == "Current":
			return v.value()

# tracks GUI-based programs launched from the desktop
def user_assist(reg):
	print (bcolors.BOLD + ("=" * 24) + " USER ASSIST " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist"
	print("---------------------------------------")
	try:
		key = open_key(reg, "Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist")
		print_values(key)
	except:
		print fail + "No UserAssist key"
	print " "
	# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\


# tracks the executables used by an app to open files on key OpenSaveMRU
def last_visited_MRU(reg):
	print (bcolors.BOLD + ("=" * 24) + " LAST VISITED MRU " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedMRU"
	print("---------------------------------------")
	try:
		key = open_key(reg, "Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedMRU")
		for value in key.values():
			print success + value
	except:
		print fail + "No LastVisitedMRU key"
	print " "
	# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedMRU


#Start -> Run commands executed
def run_MRU(reg):
	print (bcolors.BOLD + ("=" * 24) + " RUN MRU " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"
	print("---------------------------------------")
	try:	
		key = open_key(reg, "Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU")
		#print_values(key)
		order = []
		string = []
		i = []
		i.append(0)
		for v in key.values():
			if v.name() == "MRUList":
				for i in v.value():
					order.append(i)
		for index in order:
			for value in key.values():
				if value.name() != "MRUList":
					if index == value.name():
						string.append(value.value())
		for s in string:
			print success + s
	except:
		print fail + "No RunMRU key"
	print " "
	# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU


def reg_format_value_bin(value):
    """
    result should look like the following (after the '='):
     "ProductLocalizedName"=hex:40,00,25,00,50,00,72,00,6f,00,67,00,72,00,61,00,\
       6d,00,46,00,69,00,6c,00,65,00,73,00,25,00,5c,00,57,00,69,00,6e,00,64,00,6f,\
       00,77,00,73,00,20,00,44,00,65,00,66,00,65,00,6e,00,64,00,65,00,72,00,5c,00,\
       45,00,70,00,70,00,4d,00,61,00,6e,00,69,00,66,00,65,00,73,00,74,00,2e,00,64,\
       00,6c,00,6c,00,2c,00,2d,00,31,00,30,00,30,00,30,00,00,00
    so we:
      - format into one big line of hex
      - search for places to split, at about 80 chars or less
      - split, with the former receiving a backslash, and the latter getting the
         prefixed whitespace
    if the type of value is RegBin, then we use the type prefix "hex:",
    otherwise, the type prefix is "hex(%d):" where %d is the value_type constant.
    eg. RegExpandSZ is "hex(3)"
    @rtype: str
    """
    ret = []

    s = ",".join(["%02x" % (ord(c)) for c in value.value()])

    if value.value_type() == Registry.RegBin:
        s = "hex:" + s
    else:
        s = "hex(%d):" % (value.value_type()) + s

    # there might be an off by one error in here somewhere...
    name_len = len(value.name()) + 2 + 1  # name + 2 * '"' + '='
    split_index = 80 - name_len
    while len(s) > 0:
        if len(s) > split_index:
            # split on a comma
            while s[split_index] != ",":
                split_index -= 1
            ret.append(s[:split_index + 1] + "\\")
            s = "  " + s[split_index + 1:]
        else:
            ret.append(s)
            s = ""
        split_index = 80

    return "\r\n".join(ret)

# tracks executables (for identification of compatibility issues purposes)
def app_compatibility_cache(reg, path):
	print (bcolors.BOLD + ("=" * 24) + " APP COMPATIBILITY CACHE " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache"
	print("---------------------------------------")
	try:
		current_control_set = "ControlSet00%s" % control_set_check(path)
		p = "%s\Control\Session Manager\AppCompatCache" % current_control_set
		key = reg.open(p)
		for v in key.values():
			print success + reg_format_value_bin(v)
	except:
		print fail + "No AppCompatCache key"
	print " "
	# SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache


# frequently accessed items on Start menu
def jump_lists(reg, user):
	print (bcolors.BOLD + ("=" * 24) + " JUMP LISTS " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations"
	print("---------------------------------------")
	try:
		for entry in os.listdir("./mnt/Users/" + user + "/AppData/Roaming/Microsoft/Windows/Recent/AutomaticDestinations"):
			print success + entry
	except:
		print fail + "No AutomaticDestinations folder"
	print " "
	# C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations


# files created when an app runs for the first time in a certain location (for speed up purposes)
def prefetch(reg):
	print (bcolors.BOLD + ("=" * 24) + " PREFETCH " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "C:\Windows\Prefetch\(exename)-(hash).pf"
	print("---------------------------------------")
	try:
		entries = []
		i = 0
		for entry in os.listdir("./mnt/Windows/Prefetch"):
			if entry.endswith(".pf"):
				entries.append(entry)
		entries = list(set(entries))
		for entry in sorted(entries):
			#print ssca_vista_hash_function(entry)
			i = i + 1
			if i % 5 == 0:
				sys.stdout.write("\n")
			else:
				if len(entry.split("-")[0]) > 18:
					sys.stdout.write(success + entry.split("-")[0] + "  ")
				elif len(entry.split("-")[0]) > 12:
					sys.stdout.write(success + entry.split("-")[0] + "\t")
				elif len(entry.split("-")[0]) < 4:
					sys.stdout.write(success + entry.split("-")[0] + "\t\t\t")
				else:
					sys.stdout.write(success + entry.split("-")[0] + "\t\t")
	except:
		print fail + "No Prefetch folder"
	print " "
	# C:\Windows\Prefetch\(exename)-(hash).pf


# programs or apps launched during boot
def auto_run(reg):
	print (bcolors.BOLD + ("=" * 24) + " AUTO RUN " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Run"
	print plus + "NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\RunOnce"
	print("---------------------------------------")
	try:
		key = open_key(reg, "Software\Microsoft\Windows\CurrentVersion\Run")
		print_values(key)
		print " "
	except:
		print fail + "No Run key"
	try:
		key = open_key(reg, "Software\Microsoft\Windows\CurrentVersion\RunOnce")
		print_values(key)
	except:
		print fail + "No RunOnce key"
	print " "

	# HKLM\Software\Microsoft\Windows\CurrentVersion\Runonce
	# HKLM\Software\Microsoft\Windows\CurrentVersion\policies\Explorer\Run
	# HKLM\Software\Microsoft\Windows\CurrentVersion\Run
	# HKCU\Software\Microsoft\Windows2NT\CurrentVersion\Windows\Run
	# HKCU\Software\Microsoft\Windows\CurrentVersion\Run
	# HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce
	# (ProfilePath)\Start2Menu\Programs\Startup