import sys

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

def main():
	greeting()
	while True:
		menu()
		prompt()
		command = int(raw_input(" "))
		print " "
		if command == 0:
			help()
		elif command == 1:
			print " "
		elif command == 2:
			print " "
		elif command == 3:
			print " "
		elif command == 4:
			print " "
		elif command == 5:
			print " "
		elif command == 6:
			print " "
		elif command == 7:
			print " "
		elif command == 8:
			print " "
		elif command == 9:
			print " "
		elif command == 98:
			about()
		elif command == 99:
			print "\tThank you for using xTractor!\n"
			sys.exit()
		else:
			print "Invalid choice! Try again"




main()