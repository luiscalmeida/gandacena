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
	return int(hex, 16)

def parse_date(date):
	hex_date = reg_format_value_bin(date)
	parsed_date = hex_date.split(",")
	if convert(str(parsed_date[10])) < 10:
		return str(convert((str(parsed_date[1]) + str(parsed_date[0])))) + "/" + str(convert(str(parsed_date[2]))) + "/" + str(convert(str(parsed_date[6]))) + " " + str(convert(str(parsed_date[8]))) + ":" + str(0) + str(convert(str(parsed_date[10])))
	else:
		return str(convert((str(parsed_date[1]) + str(parsed_date[0])))) + "/" + str(convert(str(parsed_date[2]))) + "/" + str(convert(str(parsed_date[6]))) + " " + str(convert(str(parsed_date[8]))) + ":" + str(convert(str(parsed_date[10])))

def reg_format_value_bin(value):
    ret = []
    s = ",".join(["%02x" % (ord(c)) for c in value.value()])
    if value.value_type() == Registry.RegBin:
        pass
    else:
        s = "hex(%d):" % (value.value_type()) + s
    name_len = len(value.name()) + 2 + 1  # name + 2 * '"' + '='
    split_index = 80 - name_len
    while len(s) > 0:
        if len(s) > split_index:
            while s[split_index] != ",":
                split_index -= 1
            ret.append(s[:split_index + 1] + "\\")
            s = "  " + s[split_index + 1:]
        else:
            ret.append(s)
            s = ""
        split_index = 80
    return "\r\n".join(ret)

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


# Information about the networks to which the user connected and when the connection happened
def network_history(reg):
	print (bcolors.BOLD + ("=" * 24) + " NETWORK HISTORY " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "SOFTWARE\Microsoft\WindowsNT\CurrentVersion\NetworkList"
	print("---------------------------------------")
	try:
		global aux
		aux = 0
		global nodate
		nodate = 1
		key = reg.open("Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles")
		print("All networks connected by the user:")
		for conn in key.subkeys():
			aux = 0
			nodate = 1
			for v in conn.values():
				if v.name() == "ProfileName":
					print success + "SSID: %s" % (v.value())
					aux = 1
				if v.name() == "DateCreated":
					print "   First Time Connected: %s" % (parse_date(v))
					nodate = 0
				if v.name() == "DateLastConnected":
					print "   Last Time Connected: %s" % (parse_date(v))
					nodate = 0
			if nodate == 1:
				print "   First Time Connected: No information!"
				print "   Last Time Connected: No information!"
		print " "
	except:
		print fail + "No Profiles file"
	print " "
	# SOFTWARE\Microsoft\WindowsNT\CurrentVersion\NetworkList
