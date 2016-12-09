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

def control_set_check(reg): 
	"""
	Determine which Control Set the system was using
	"""
	registry = Registry.Registry(reg)
	key = registry.open("Select")    
	for v in key.values():
		if v.name() == "Current":
			return v.value()

def parse(info):
	if ";" in info:
		split1, split2 = info.split(";")
		return split2
	else:
		return info

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

# Information about USB's connected, when they were connected, etc.
def plugged_devices(reg, path):
	print (bcolors.BOLD + ("=" * 24) + " PLUGGED DEVICES " + ("=" * 24))
	print bcolors.ENDC + "Searching in:"
	print plus + "SYSTEM\CurrentControlSet\Enum\USBSTOR"
	print("---------------------------------------")
	try:
		print "USBSTOR:"
		output = []
		final_output = []
		line = []
		global aux
		aux = 0
		global noname
		noname = 1
		global name
		name = ""
		global mfg
		mfg = ""
		global contains
		contains = 0
		current_control_set = "ControlSet00%s" % control_set_check(path)
		path = "%s\Enum\USBSTOR" % current_control_set
		key = reg.open(path)
		for usbfile in key.subkeys():
			for v in usbfile.subkeys():
				aux = 0
				noname = 1
				line = []
				name = ""
				mfg = ""
				for k in v.values():
					if k.name() == "FriendlyName":
						name = success + "Name: " + k.value()
						aux = 1
						noname = 0
					if k.name() == "DeviceDesc" and noname == 1:
						if ";" in k.value():
							name = success + "Name: " + parse(k.value())
							aux = 1
						else:
							name = success + "Name: " + k.value()
							aux = 1
					if k.name() == "Mfg" and aux == 1:
						mfg = "   Manufacturer: " + parse(k.value())
				output.append(name)
				output.append(mfg)
	except:
		print "    " + fail + "No USBSTOR key"
	print " "
	try:
		print "USB:"
		path = "%s\Enum\USB" % current_control_set
		key = reg.open(path)
		for usbfile in key.subkeys():
			for v in usbfile.subkeys():
				aux = 0
				noname = 1
				line = []
				name = ""
				mfg = ""
				for k in v.values():
					if k.name() == "FriendlyName":
						name = success + "Name: " + k.value()
						aux = 1
						noname = 0
					if k.name() == "DeviceDesc" and noname == 1:
						if ";" in k.value():
							name = success + "Name: " + parse(k.value())
							aux = 1
						else:
							name = success + "Name: " + k.value()
							aux = 1
					if k.name() == "Mfg" and aux == 1:
						mfg = "   Manufacturer: " + parse(k.value())
				output.append(name)
				output.append(mfg)
		for entry in output:
			if "Name" in entry:
				if entry not in final_output:
					final_output.append(entry)
					contains = 1
			if "Manufacturer" in entry and contains == 1:
				final_output.append(entry)
				contains = 0	
		for v in final_output:
			print "    " + v
	except:
		print "    " + fail + "No USB key"
	print " "
	#SYSTEM\CurrentControlSet\Enum\USBSTOR
