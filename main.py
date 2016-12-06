import sys
import os
from Registry import Registry

import recentFiles_4
import downloadedFiles_5
import launchedPrograms_6
import physical_location_7 as physloc

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def greeting():
	print " "
	print bcolors.BOLD + bcolors.FAIL + "\t /****************************************\\"
	print "\t|**************** xTractor ****************|"
	print "\t \\****************************************/"
	print " "

def menu():
    print bcolors.BOLD + bcolors.FAIL + "\t\t    Select from the menu:\n"
    print "\t\t1 - System information"
    print "\t\t2 - List all networks connected"
    print "\t\t3 - List all devices plugged in"
    print "\t\t4 - List recent files"
    print "\t\t5 - List recent downloaded files"
    print "\t\t6 - List recent launched programs"
    print "\t\t7 - Physical location"
    print "\t\t8 - Login history"
    print "\t\t9 - Browser history"
    print "\t\t0 - Help"
    print "\t\t98 - About this tool"
    print "\t\t99 - Exit\n"

def help():
    print bcolors.BOLD + bcolors.ENDC + "\tHelp menu:\n"
    print "\t1 - Operating system's information as it's version, architecture, etc.."
    print "\t2 - ESSID(name), IP and date of connections to any AP's stored in the system."
    print "\t3 - Names and dates of connections of USB, external storage devices, input and output devices to the system."
    print "\t4 - Recently opened or modified files of any extension."
    print "\t5 - Recently downloaded files from Chrome, Firefox or InternetExplorer."
    print "\t6 - Recently executable programs executed on the system."
    print "\t7 - Information about the possible physical location where this system may have been used most of the time."
    print "\t8 - Names of recently logged in or logged out users on the system."
    print "\t9 - Recently searched URL's on Chrome, Firefox or InternetExplorer."
    print "\t0 - Will display this menu."
    print "\t98 - Will display info about the tool and team that implemented it."
    print "\t99 - Will exit the tool."
    print "\n"

def about():
    print bcolors.BOLD + bcolors.ENDC + "\txTractor is a post-mortem forensic tool designed to run on linux operating systems."
    print "\tIt will expect a file system image (dd image) as input and will extract certain data from the file system's windows registry and other sources."
    print "\tIt was develop by a team of three young IT engineers as a subject of Ciber Security Forensic course."
    print "\t2016 Instituto Superior Tecnico"
    print "\n"

def prompt():
	print bcolors.BOLD + bcolors.ENDC
	sys.stdout.write(' > ')
	sys.stdout.flush()

def get_user():
	users = []
	for entry in os.listdir("./mnt/Users"):
		if entry != "All Users" and entry != "Default" \
				and entry != "Default User" and entry != "desktop.ini" and entry != "informant" \
				and entry != "Public" and entry != "temporary":
			users.append(entry)
	choice = ""
	if len(users) == 0 :
		print " "
		print "No users in the file system! Exiting xTractor"
		sys.exit()
	elif len(users) == 1:
		print " "
		print "IMPORTANT: As this file system only has one user we will explore that one: " + bcolors.ENDC + users[0]
		print " "
		choice = users[0]
		return choice
	print bcolors.BOLD + bcolors.FAIL + "Choose the user you pretend to explore from the list below (write exactly as it is written):\n"
	for entry in users:
		print bcolors.ENDC + "\t" + entry
	prompt()
	choice = raw_input()
	while(not choice in users):
		print "\n" + bcolors.FAIL + "Inexistent user. Please write one from the list"
		prompt()
		choice = raw_input()
	print " "
	return choice
	"""for entry in os.listdir("./mnt/Users"): #exclude these folders/files
		if entry != "All Users" and entry != "Default" \
		and entry != "Default User" and entry != "desktop.ini" and entry != "informant" \
		and entry != "Public" and entry != "temporary":
			return entry"""

#imprime todas as keys num registry
def rec(key, depth=0):
	print("Key: " + key.name() + " Depth: " + str(depth))
	print "\t" * depth + key.path()
	
	for subkey in key.subkeys():
		rec(subkey,depth + 1)

def main():
	greeting()
	user = str(get_user())
	while True:
		menu()
		prompt()
		command = raw_input()
		if command.isdigit():
			command = int(command)
			if command == 0:
				print " "
				help()
			elif command == 1:
				regabrir = raw_input()
				#exemplo de input para dar:
				#./mnt/Users/admin11/NTUSER.DAT

				reg = Registry.Registry(regabrir)
				#abre registo e imprime todas as keys
				#rec(reg.root())
				print " "
			elif command == 2:
				print " "
				yoyo = raw_input()
				#com input ./mnt/Users/admin11/NTUSER.DAT
				reg = Registry.Registry(yoyo)
				try:
					#usei o 1 para imprimir as keys e saquei uma a toa de la
	    				key = reg.open("System\CurrentControlSet\Control\Network\NetworkLocationWizard")
				except Registry.RegistryKeyNotFoundException:
					print("Fuck you")
					sys.exit(-1)
				for value in [v for v in key.values()]: 
					#if v.value_type() == Registry.RegSZ or v.value_type() == Registry.RegExpandSZ:
	    				print "%s %s" % (value.name(),value.value())
			elif command == 3:
				print " "
			elif command == 4:
				print " "
				#reg = Registry.Registry("../NTUSER.DAT")
				
				reg = Registry.Registry("./mnt/Users/" + user + "/NTUSER.DAT")
				recentFiles_4.recent_files(reg)
				recentFiles_4.office_recent_files(reg)
				recentFiles_4.shell_bags(reg)
				recentFiles_4.shortcut_files(reg, user)
				recentFiles_4.recent_browser_files(reg, user)
				print " "
			elif command == 5:
				print " "
				reg = Registry.Registry("../NTUSER.DAT")
				#reg = Registry.Registry("./mnt/Users/" + user + "/NTUSER.DAT")
				downloadedFiles_5.open_save_MRU(reg)
				downloadedFiles_5.email_attachments(reg, user)
				downloadedFiles_5.skype_history(reg, user)
				downloadedFiles_5.downloads_IE(reg, user)
				downloadedFiles_5.downloads_FF(reg, user)
				print " "
			elif command == 6:
				reg = Registry.Registry("../NTUSER.DAT")
				#reg = Registry.Registry("./mnt/Users/" + user + "/NTUSER.DAT")
				launchedPrograms_6.user_assist(reg)
				launchedPrograms_6.last_visited_MRU(reg)
				launchedPrograms_6.run_MRU(reg)
				reg = Registry.Registry("../regBackup/SYSTEM")
				#reg = Registry.Registry("./mnt/Windows/System32/config/SYSTEM")
				launchedPrograms_6.app_compatibility_cache(reg, "../regBackup/SYSTEM")
				launchedPrograms_6.jump_lists(reg, user)
				launchedPrograms_6.prefetch(reg)
				reg = Registry.Registry("../NTUSER.DAT")
				#reg = Registry.Registry("./mnt/Users/" + user + "/NTUSER.DAT")
				launchedPrograms_6.auto_run(reg)
				print " "
			elif command == 7:
				#Need func to ask for user
	                        #reg = Registry.Registry("./mnt/Users/admin11/NTUSER.DAT")
	                        #begin---timezone
	                        reg = Registry.Registry("./mnt/Windows/System32/config/SYSTEM")
	                        res = physloc.timezone_settings("./mnt/Windows/System32/config/SYSTEM")
	                        for e in res:
	                                print(e)
	                        #begin---network history
	                        physloc.network_history(reg)
	                        #begin cookies
	                        res = physloc.cookies(user)
	                        if not res:
	                                print("No Cookies found")
	                        else:
	                                print("Cookies in file: " + res)
	                        #begin browser search
	                        physloc.browser_search(user)
	                        if not res:
	                                print("No History Found")
	                        else:
	                                for e in res:
	                                        print(res)
	                        print " "
			elif command == 8:
				print " "
			elif command == 9:
				print " "
			elif command == 98:
				print " "
				about()
			elif command == 99:
				print "\tThank you for using xTractor!\n"
				sys.exit()
			else:
				print " "
				print "Invalid choice! Try again"
				print " "
		else:
			print " "
			print "Invalid choice! Try again"
			print " "



main()
