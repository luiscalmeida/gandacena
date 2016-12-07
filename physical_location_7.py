import sys,os
import re
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
    	results.append(("=" * 24) + "Time Zone Settings" + ("=" * 24))    
    	results.append("[+] %s" % k)
    	results.append("---------------------------------------")
    	for v in key.values():
        	if v.name() == "ActiveTimeBias":
            		results.append("[-] ActiveTimeBias: %s" % v.value())
       	 	if v.name() == "Bias":
            		results.append("[-] Bias...: %s" % v.value())
		if v.name() == "TimeZoneKeyName":
            		results.append("[-] Time Zone Name...: %s" % str(v.value()))
	return results

def network_history(reg):
	print("network history")

def cookies(user):
	path1 = "./mnt/Users/" + user + "/AppData/Roaming/Microsoft/Windows/Cookies/"
	path2 = path1 + "Low/"

	print(("=" * 24) + "Cookies" + ("=" * 24))
	print("Searching in dirs: ")
	print("[+] %s" % path1)
	print("[+] %s" % path2)	
	print("---------------------------------------")

	files1 = [f for f in listdir(path1) if isfile(join(path1,f))]
	files2 = [f for f in listdir(path2) if isfile(join(path2,f))]

	if not files1:
		return
	else:
		with open("cookies.txt","a") as cookies:
			for f1 in files1:
				with open(f1,'r') as f:
					cookies.write(f.read())
					f.close()
			cookies.close()

	if not files2:
		return
	else:
		with open("cookies.txt","a") as cookies:
                        for f2 in files2:
                                with open(f2,'r') as f:
                                        cookies.write(f.read())
					f.close()
			cookies.close()
	return "cookies.txt"

def removenonascii(s):
    	l=""
    	for i in s:
        	if(ord(i)==46 or ord(i)==47 or ord(i)==72 or ord(i) in range(97,97+26) or ord(i) in range(65,65+26)):
        		l=l+i
   	lines=l.split('\n')

   	for line in lines:
        	if line.startswith("http"):
			print line.split("URL")[0]


def browser_search(user):
	path_h1 = "./mnt/Users/" + user + "/AppData/Local/Microsoft/Windows/Temporary Internet Files/Content.IE5/"
	path_h2 = "./mnt/Users/" + user + "/AppData/Local/Microsoft/Windows/History/Content.IE5/"
	files1 = ""
	files2 = ""
	res = []

	print(("=" * 24) + "Internet Explorer History" + ("=" * 24))
        print("Searching in dirs: ")
        print("[+] %s" % path_h1)
        print("[+] %s" % path_h2)
        print("---------------------------------------")
	
	try:
		files1 = [f for f in listdir(path_h1) if isfile(join(path_h1,f))]
		files2 = [f for f in listdir(path_h2) if isfile(join(path_h2,f))]
	except Exception as e:
		print("%s" % e)
	
	if files1:
		for e in files1:
			if "index" in e:
				infile =open(e,"r")
				for line in infile:
    					arr=line.split("Cho")

				for s in arr:
    					removenonascii(s)
					res = res + [s]
				infile.close()
	if files2:
		for e in files2:
			if "index" in e:
				infile =open(e,"r")
                		for line in infile:
                        		arr=line.split("Cho")

                		for s in arr:
                        		removenonascii(s)
                        		res = res + [s]
				infile.close()
    	return res		
	
