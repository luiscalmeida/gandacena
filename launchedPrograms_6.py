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
		print("Can't find any keys (later will erase this print. User doesn't need to know)")

#######################################################################
#######################################################################



# tracks GUI-based programs launched from the desktop
def user_assist(reg):
	print " "
	print "***** USER ASSIST *****"
	print " "
	key = open_key(reg, "Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist")
	print_values(key)
	# HCU\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\
	# HCU == NTUSER.DAT ???


# tracks the executables used by an app to open files on key OpenSaveMRU
def last_visited_MRU(reg):
	print " "
	print "***** LAST VISITED MRU *****"
	print " "
	key = open_key(reg, "Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedMRU")
	print_values(key)
	#NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedMRU


#Start -> Run commands executed
def run_MRU(reg):
	print " "
	print "***** RUN MRU *****"
	print " "
	key = open_key(reg, "Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU")
	print_values(key)
	# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU


# tracks executables (for identification of compatibility issues purposes)
def app_compatibility_cache(reg):
	print " "
	print "***** APP COMPATIBILITY CACHE *****"
	print " "
	# SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache


# frequently accessed items on Start menu
def jump_lists(reg):
	print " "
	print "***** JUMP LISTS *****"
	print " "
	# C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations
	for entry in os.listdir("./mnt/Users/admin11/AppData/Roaming/Microsoft/Windows/Recent/AutomaticDestinations"):
		print entry


# files created when an app runs for the first time in a certain location (for speed up purposes)
def prefetch(reg):
	print " "
	print "***** PREFETCH *****"
	print " "
	entries = []
	i = 0
	for entry in os.listdir("./mnt/Windows/Prefetch"):
		if entry.endswith(".pf"):
			entries.append(entry)
	entries = list(set(entries))
	for entry in sorted(entries):
		i = i + 1
		if i % 5 == 0:
			sys.stdout.write("\n")
		else:
			sys.stdout.write(entry.split("-")[0] + "\t\t")
	# C:\Windows\Prefetch\(exename)-(hash).pf


# programs or apps launched during boot
def auto_run(reg): #maybe too much
	print " "
	print "***** AUTO RUN *****"
	print " "
	key = open_key(reg, "Software\Microsoft\Windows\CurrentVersion\Run")
	print_values(key)
	print " "
	key = open_key(reg, "Software\Microsoft\Windows\CurrentVersion\RunOnce")
	print_values(key)
	print " "
	#key = open_key(reg, "Software\Microsoft\Windows\CurrentVersion\Windows\Run")
	#print_values(key)

	# HKLM\Software\Microsoft\Windows\CurrentVersion\Runonce
	# HKLM\Software\Microsoft\Windows\CurrentVersion\policies\Explorer\Run
	# HKLM\Software\Microsoft\Windows\CurrentVersion\Run
	# HKCU\Software\Microsoft\Windows2NT\CurrentVersion\Windows\Run
	# HKCU\Software\Microsoft\Windows\CurrentVersion\Run
	# HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce
	# (ProfilePath)\Start2Menu\Programs\Startup
	print " "