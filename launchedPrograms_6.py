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



# tracks GUI-based programs launched from the desktop
def user_assist():
	# HCU\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\
	# HCU == NTUSER.DAT ???


# tracks the executables used by an app to open files on key OpenSaveMRU
def last_visited_MRU():
	#NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedMRU


#Start -> Run commands executed
def run_MRU():
	# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU


# tracks executables (for identification of compatibility issues purposes)
def app_compatibility_cache():
	# SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache


# frequently accessed items on Start menu
def jump_lists():
	# C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations


# files created when an app runs for the first time in a certain location (for speed up purposes)
def prefetch():
	# C:\Windows\Prefetch\(exename)-(hash).pf


# programs or apps launched during boot
def auto_run(): #maybe too much
	# HKLM\Software\Microsoft\Windows\CurrentVersion\Runonce
	# HKLM\Software\Microsoft\Windows\CurrentVersion\policies\Explorer\Run
	# HKLM\Software\Microsoft\Windows\CurrentVersion\Run
	# HKCU\Software\Microsoft\Windows2NT\CurrentVersion\Windows\Run
	# HKCU\Software\Microsoft\Windows\CurrentVersion\Run
	# HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce
	# (ProfilePath)\Start2Menu\Programs\Startup