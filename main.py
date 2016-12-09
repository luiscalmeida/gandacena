import sys
import os
from libs.Registry import Registry

from src import systemInformation_1
from src import networkHistory_2
from src import usbDevices_3
from src import recentFiles_4
from src import downloadedFiles_5
from src import launchedPrograms_6
from src import physical_location_7 as physloc
from src import account_usage_8 as accman
from src import browser_usage_9 as browser

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
    print "\t\t99 - Exit"

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
	software="./mnt/Windows/System32/config/SOFTWARE"
	system="./mnt/Windows/System32/config/SYSTEM"
	ntuser="./mnt/Users/" + user + "/NTUSER.DAT"
	sam="./mnt/Windows/System32/config/SAM"
	security_evt="./mnt/Windows/System32/winevt/Logs/Security.evtx"
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
				print " "
				reg = Registry.Registry(software)
				systemInformation_1.system_information(reg)
				print " "
			elif command == 2:
				print " "
				reg = Registry.Registry(software)
				networkHistory_2.network_history(reg)
				print " "
			elif command == 3:
				print " "
				reg = Registry.Registry(system)
				usbDevices_3.plugged_devices(reg, system)
				print " "
			elif command == 4:
				print " "
				reg = Registry.Registry(ntuser)	
				#reg = Registry.Registry("./mnt/Users/" + user + "/NTUSER.DAT")
				recentFiles_4.recent_files(reg, user)
				recentFiles_4.office_recent_files(reg)
				recentFiles_4.shell_bags(reg)
				recentFiles_4.shortcut_files(reg, user)
				recentFiles_4.recent_browser_files(reg, user)
				print " "
			elif command == 5:
				print " "
				reg = Registry.Registry(ntuser)
				#reg = Registry.Registry("./mnt/Users/" + user + "/NTUSER.DAT")
				downloadedFiles_5.open_save_MRU(reg)
				downloadedFiles_5.email_attachments(reg, user)
				downloadedFiles_5.skype_history(reg, user)
				downloadedFiles_5.downloads_IE(reg, user)
				downloadedFiles_5.downloads_FF(reg, user)
				print " "
			elif command == 6:
				reg = Registry.Registry(ntuser)
					#reg = Registry.Registry("./mnt/Users/" + user + "/NTUSER.DAT")
				launchedPrograms_6.user_assist(reg)
				launchedPrograms_6.last_visited_MRU(reg)
				launchedPrograms_6.run_MRU(reg)
				reg = Registry.Registry(system)
					#reg = Registry.Registry("./mnt/Windows/System32/config/SYSTEM")
				launchedPrograms_6.app_compatibility_cache(reg, system)
				launchedPrograms_6.jump_lists(reg, user)
				launchedPrograms_6.prefetch(reg)
				reg = Registry.Registry(ntuser)
					#reg = Registry.Registry("./mnt/Users/" + user + "/NTUSER.DAT")
				launchedPrograms_6.auto_run(reg)
				print " "
			elif command == 7:
				#begin time zone
				if not os.path.exists("./Output"):
					os.makedirs("Output")
				reg = Registry.Registry(system)
				res = physloc.timezone_settings(system)
				for e in res:
					print(e)
				print

				#begin network history
				reg = Registry.Registry(software)
                                networkHistory_2.network_history(reg)

				#begin cookies
				physloc.cookies(user)
				print

				#begin browser search
				physloc.browser_search(user)
				print
				
				#begin firefox history	
				physloc.firefox_history(user)
				print
			elif command == 8:
				#begin logons
				if not os.path.exists("./Output"):
                                        os.makedirs("Output")
				accman.show_logons(security_evt)
				print
				
				#begin logs info
				reg = Registry.Registry(sam)
				accman.show_logtimes(reg)
				print
			elif command == 9:
				#begin browser files
				if not os.path.exists("./Output"):
                                        os.makedirs("Output")	
				reg = Registry.Registry(ntuser)
				recentFiles_4.recent_browser_files(reg, user)
				
				#begin downloaded files
				downloadedFiles_5.downloads_IE(reg, user)
                                downloadedFiles_5.downloads_FF(reg, user)
				print
				
				#begin browser history
				physloc.browser_search(user)
				print
				physloc.firefox_history(user)
				print
				
				#begin cookies
				physloc.cookies(user)
				print

				#begin keys
				browser.keys(ntuser)
				print
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
