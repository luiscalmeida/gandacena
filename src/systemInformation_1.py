import sys
import os
from libs.Registry import Registry

################################ UTILS ################################

def print_values(key):
	for value in [v for v in key.values()]:
		if v.value_type() == Registry.RegSZ or v.value_type() == Registry.RegExpandSZ:
			print success + "%s = %s" % (value.name(), value.value())

def open_key(reg, path):
	try:
		return reg.open(path)
	except Registry.RegistryKeyNotFoundException:
		print fail + "Can't find any keys (later will erase this print. User doesn't need to know)"
		#sys.exit(-1)

def convert(hex):
	int(hex, 16)

def parse_date(date):
		d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16 = date.split(" ")
		return convert(d2+d1) + "/" + convert(d4+d3) + "/" + convert(d6+d5) + "/" + convert(d12+d11) + "/" + convert(d16+d15)

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

#######################################################################
#######################################################################


# Information about the Operative System
def system_information(reg):
	print (bcolors.BOLD + ("=" * 24) + " SYSTEM INFORMATION  " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "SOFTWARE\Microsoft\WindowsNT\CurrentVersion"
	print("---------------------------------------")
	try:
		key = reg.open("Microsoft\Windows NT\CurrentVersion")
		for v in key.values():
			if v.name() == "ProductName":
				print success + "Operative System: %s" % (v.value())
		for v in key.values():
			if v.name() == "EditionID":
				print "   Edition: %s" % (v.value())
		for v in key.values():
			if v.name() == "CurrentVersion":
				print "   Current Version: %s" % (v.value())
		for v in key.values():
			if v.name() == "CurrentType":
				print "   Current Type: %s" % (v.value())
		for v in key.values():
			if v.name() == "InstallationType":
				print "   Installation Type: %s" % (v.value())
		for v in key.values():
			if v.name() == "SystemRoot":
				print "   SystemRoot: %s" % (v.value())
		for v in key.values():
			if v.name() == "RegisteredOwner":
				print "   Registered Owner: %s" % (v.value())
		print " "
	except:
		print fail + "No CurrentVersion file"
	print " "
	# SOFTWARE\Microsoft\WindowsNT\CurrentVersion
