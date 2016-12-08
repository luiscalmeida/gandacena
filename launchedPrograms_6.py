import sys
import os
import binascii
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

def reg_format_value_bin(value):
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

def print_values(key):  # ADD INDEX
	for value in [v for v in key.values()]:
		if v.value_type() == Registry.RegSZ or v.value_type() == Registry.RegExpandSZ:
			print success + "%s = %s" % (value.name(), value.value())

def print_values_fail_tab(key, name):  # ADD INDEX
	index = []
	index.append(0)
	for value in [v for v in key.values()]:
		if v.value_type() == Registry.RegSZ or v.value_type() == Registry.RegExpandSZ:
			print "    " + success + "%s = %s" % (value.name(), value.value())
			index[0] += 1
	if index[0] == 0:
		print "    " + fail + name

def print_values_fail(key, name):  # ADD INDEX
	index = []
	index.append(0)
	for value in [v for v in key.values()]:
		if v.value_type() == Registry.RegSZ or v.value_type() == Registry.RegExpandSZ:
			print "    " + success + "%s = %s" % (value.name(), value.value())
			index[0] += 1
	if index[0] == 0:
		print fail + name

def open_key(reg, path):
	try:
		return reg.open(path)
	except Registry.RegistryKeyNotFoundException:
		print(fail + "Can't find any keys")

def open_key_tab(reg, path):
	try:
		return reg.open(path)
	except Registry.RegistryKeyNotFoundException:
		print "\t" + bcolors.FAIL + "[-]" + bcolors.ENDC + "Can't find any keys"
		return False
		#sys.exit(-1)

#######################################################################
#######################################################################

# tracks GUI-based programs launched from the desktop
def user_assist(reg):
	print (bcolors.BOLD + ("=" * 24) + " USER ASSIST " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist"
	print("---------------------------------------")
	try:
		key = open_key(reg, "Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist")
		print_values_fail(key, "No executables on User Assist")
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
	#try:
	result = []
	index = []
	index.append(0)
	word = ""
	key = open_key(reg, "Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU")
	for value in key.values():
		for letter in value.value():
			if ord(letter) > 126 or ord(letter) < 32:
				pass
			else:
				word += letter
		result.append(word)
		word = ""
	for i in result:
		if "exe" in i:
			str = i.split(".")
			if str[1].startswith("exe"):
				print success + str[0] + ".exe"
				index[0] += 1
	if index[0] == 0:
		print fail + "No executables on LastVisitedMRU"
	#except:
	#	print fail + "No LastVisitedMRU key"
	#print " " 
	# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedMRU


#Start -> Run commands executed
def run_MRU(reg):
	print (bcolors.BOLD + ("=" * 24) + " RUN MRU " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"
	print("---------------------------------------")
	try:	
		key = open_key_tab(reg, "Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU")
		print "RunMRU services in order (first is most recently ran):"
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
		result = []
		for v in key.values():
			if(v.name() == "AppCompatCache"):
				word = ""
				for letter in v.value():
					if ord(letter) > 122 or ord(letter) < 45:
						pass
					else:
						word += letter
				#print word #+ reg_format_value_bin(v)
				final_word = ""
				ind = []
				ind.append(0)
				for w in word.split(".exe"):
					for l in w[::-1]:
						if ind[0] == 0:
							if l == ":":
								ind[0] += 1
								final_word += l
							else:
								final_word += l
						else:
							final_word += l
							break
					ind[0] = 0
					result.append(final_word[::-1] + ".exe")
					final_word = ""
				for r in result:
					print success + r
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
		index = []
		index.append(0)
		for entry in os.listdir("./mnt/Users/" + user + "/AppData/Roaming/Microsoft/Windows/Recent/AutomaticDestinations"):
			print success + entry
			index[0] += 1
		if index[0] == 0:
			print "    " + fail + "No Jump List files"
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
		index = []
		index.append(0)
		index.append(0)
		key = open_key(reg, "Software\Microsoft\Windows\CurrentVersion\Run")
		print "Run:"
		print_values_fail_tab(key, "No Auto Run files on Run")
	except:
		print "    " + fail + "No Run key"
	try:
		key = open_key(reg, "Software\Microsoft\Windows\CurrentVersion\RunOnce")
		print "Run Once:"
		print_values_fail_tab(key, "No Auto Run files on RunOnce")
	except:
		print "    " + fail + "No RunOnce key"
	print " "

	# HKLM\Software\Microsoft\Windows\CurrentVersion\Runonce
	# HKLM\Software\Microsoft\Windows\CurrentVersion\policies\Explorer\Run
	# HKLM\Software\Microsoft\Windows\CurrentVersion\Run
	# HKCU\Software\Microsoft\Windows2NT\CurrentVersion\Windows\Run
	# HKCU\Software\Microsoft\Windows\CurrentVersion\Run
	# HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce
	# (ProfilePath)\Start2Menu\Programs\Startup