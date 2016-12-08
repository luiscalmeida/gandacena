import sys
import os
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
		output = []
		final_output = []
		global aux
		aux = 0
		current_control_set = "ControlSet00%s" % control_set_check(path)
		path = "%s\Enum\USBSTOR" % current_control_set
		key = reg.open(path)
		for usbfile in key.subkeys():
			for v in usbfile.subkeys():
				for k in v.values():
					if k.name() == "FriendlyName":
						output.append(success + "Name: " + k.value())
						aux = 1
					if k.name() == "Mfg" and aux == 1:
						output.append("   Manufacturer: " + parse(k.value()))
		path = "%s\Enum\USB" % current_control_set
		key = reg.open(path)
		for usbfile in key.subkeys():
			for v in usbfile.subkeys():
				for k in v.values():
					aux = 0
					if k.name() == "FriendlyName":
						if k.value() not in output:
							output.append(success + "Name: " + k.value())
							aux = 1
					if k.name() == "Mfg" and aux == 1:
							output.append("   Manufacturer: " + parse(k.value()))
							output.append(" ")
					if k.name() == "DeviceDesc":
						if ";" in k.value():
							if parse(k.value()) not in output:
								output.append(success + "Name: " + parse(k.value()))
								aux = 1
						else:
							if k.value() not in output:
								output.append(success + "Name: " + k.value())
								aux = 1
					if k.name() == "Mfg":
						output.append("   Manufacturer: " + parse(k.value()))
		for entry in output:
			if entry not in final_output:
				final_output.append(entry)
		for v in final_output:
			print v
	except:
		print fail + "No Profiles file"
	print " "
	#SYSTEM\CurrentControlSet\Enum\USBSTOR