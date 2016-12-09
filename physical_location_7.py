import sys,os
import re
import pickle
from Registry import Registry
from os import listdir
from os.path import isfile, join
from string import *
from binascii import *

#
#------------Key Utils-----------------------
#print values of key
def print_values(key):
        for value in [v for v in key.values() \
                if v.value_type() == Registry.RegSZ or v.value_type() == Registry.RegExpandSZ]:
                        print "%s = %s" % (value.name(), value.value())

#print all keys in registry: call print_keys(reg.root())
def print_keys(key, depth=0):
        print "\t" * depth + key.path()

        for subkey in key.subkeys():
                print_keys(subkey, depth + 1)

#find key and open it
def open_key(reg, path):
        try:
                return reg.open(path)
        except Registry.RegistryKeyNotFoundException:
                print("Can't find any keys (later will erase this print. User doesn't need to know)")
#----------------------------------------
#
#CODE
#
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


def control_set_check(sys_reg): 
    	"""
    	Determine which Control Set the system was using
    	"""
    	registry = Registry.Registry(sys_reg)
    	key = registry.open("Select")    
    	for v in key.values():
       		if v.name() == "Current":
			return v.value() 


def timezone_settings(sys_reg):
	"""
	Time Zone Settings
	"""
	results = []
    	current_control_set = "ControlSet00%s" % control_set_check(sys_reg)
    	k = "%s\\Control\\TimeZoneInformation" % current_control_set
   	registry = Registry.Registry(sys_reg)
   	key = registry.open(k)
    	results.append(bcolors.BOLD + ("=" * 24) + " TIME ZONE SETTINGS " + ("=" * 24))    
    	results.append(bcolors.ENDC + "Searching in:")
	results.append(plus + sys_reg + k)
    	results.append("---------------------------------------")
	try:
    		for v in key.values():
        		if v.name() == "ActiveTimeBias":
            			results.append(success + " ActiveTimeBias: %s" % v.value())
       	 		if v.name() == "Bias":
            			results.append(success + " Bias...: %s" % v.value())
			if v.name() == "TimeZoneKeyName":
            			results.append(success + " Time Zone Name...: %s" % str(v.value()))
		return results
	except:
		print(fail + "Failed to retrieve values for:" + sysreg + path)

def network_history(reg):
	print("network history")

def cookies(user):
	path1 = "./mnt/Users/" + user
	paths = [path1 + "/AppData/Roaming/Microsoft/Windows/Cookies/",
		 path1 + "/AppData/Roaming/Microsoft/Windows/Cookies/Low/"]

	print(bcolors.BOLD + ("=" * 24) + " COOKIES " + ("=" * 24))
	print(bcolors.ENDC + "Searching in: ")
	for pth in paths:
		print(plus + pth)
	print("---------------------------------------")

	filesbool = 0
	
	cookies = open("./Output/Cookies.txt", 'a')
	for path in paths:
		files1 = [f for f in listdir(path)]
		try:
			if files1:
				filesbool = 1
				for f1 in files1:
					f =open(path + f1,'r')
					buf = f.read()
					cookies.write(buf)
					f.close()
			if filesbool == 0:
				print(fail + "No Cookies found on: " + path)
			else:
				print(success + "Cookies from " + path + " on file: Output/Cookies.txt")
		except:
			print(fail + "Failed to retrieve Cookies on: " + path)
	cookies.close()


def removenonascii(s):
    	l=""
    	for i in s:
        	if(ord(i)==46 or ord(i)==47 or ord(i)==72 or ord(i) in range(97,97+26) or ord(i) in range(65,65+26)):
        		l=l+i
   	lines=l.split('\n')

	res = []
   	for line in lines:
        	if line.startswith("http"):
			res = res + [line.split("URL")[0]]
	return res


def browser_search(user):
	path_h1 = "./mnt/Users/" + user + "/AppData"
	paths = [path_h1 + "/Roaming/Microsoft/Windows/Cookies/",
		 path_h1 + "/Roaming/Microsoft/Windows/Cookies/Low/",
		 path_h1 + "/Local/Microsoft/Windows/History/History.IE5/",
		 path_h1 + "/Local/Microsoft/Windows/History/History.IE5/Low/", 
		 path_h1 + "/Local/Microsoft/Windows/Temporary Internet Files/Content.IE5/", 
		 path_h1 + "/Local/Microsoft/Windows/Temporary Internet Files/Low/Content.IE5/",
		 path_h1 + "/Roaming/Microsoft/Internet Explorer/UserData/", 
		 path_h1 + "/Roaming/Microsoft/Internet Explorer/UserData/Low/"]
		
	files1 = ""
	res = []

	print(bcolors.BOLD + ("=" * 24) + " INTERNET EXPLORER HISTORY " + ("=" * 24))
        print(bcolors.ENDC + "Searching in: ")
	for path in paths:
        	print(plus + path)
        print("---------------------------------------")
	
	filesbool = 0

	for filepath in paths:
		try:
			files1 = [f for f in listdir(filepath)]
			if files1:
				for e in files1:
					if "index.dat" in e:
						filesbool = 1
						infile =open(filepath + e,"r")
						for line in infile:
 							arr=line.split("Cho")
							for s in arr:
    								webs = removenonascii(s)
								if webs:
									for sites in webs:
										print(plus + filepath + e)
										print('\t' + success + sites)
								res = res + [s]
						infile.close()
			else:
				print(fail + "Browser history not found on: " + filepath)
		except:
			print(fail + "Directory doesn't exist: " + filepath)
	if filesbool == 0:
		print(fail + "Can't find browser search terms")	
	else:
		try:
			with open("./Output/BrowserSearch.txt", "w") as f:
				pickle.dump(res,f)
			print(bcolors.BOLD + "For more advanced info check: Output/BrowserSearch.txt")
			#outfile.close()
		except:
			print(fail + "Couldnt output advanced info to file")
