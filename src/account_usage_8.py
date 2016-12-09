import sys
import mmap
import contextlib

import argparse

from libs.Registry import Registry

from libs.Evtx.Evtx import FileHeader
from libs.Evtx.Views import evtx_file_xml_view

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



def ascii(s):
    	return s.encode('ascii', 'replace').decode('ascii')

def show_logons(arg):
	print(bcolors.BOLD + ("=" * 24) + " LOGONS " + ("=" * 24))
        print(bcolors.ENDC + "Searching in: ")
        print(plus + arg)
        #print("[+] %s" % path_h2)
        print("---------------------------------------")	

	tag = "</EventID>"
	tagtype = "\"LogonType\">"
	tagdata = "</Data>"
	
	l = open("./Output/LogonEvents.txt",'w')
	
    	with open(arg, 'r') as f:
        	with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as buf:
        	    	fh = FileHeader(buf, 0x0)
            		l.write("<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"yes\" ?>")
            		l.write("<Events>")
            		for xml, record in evtx_file_xml_view(fh):
				ascxml = ascii(xml)
				if ("4624" + tag) in ascxml:
					evtype = ""
					if (tagtype + "2" + tagdata) in ascxml:
						evtype = "Logon via console"
					elif (tagtype + "3" + tagdata) in ascxml:
                                                evtype = "Network logon"
					elif (tagtype + "4" + tagdata) in ascxml:
                                                evtype = "Batch logon"
					elif (tagtype + "5" + tagdata) in ascxml:
                                                evtype = "Windows Service logon"
					elif (tagtype + "7" + tagdata) in ascxml:
                                                evtype = "Credentials used to unlock screen"
					elif (tagtype + "8" + tagdata) in ascxml:
                                                evtype = "Network logon sending credentials"
					elif (tagtype + "9" + tagdata) in ascxml:
                                                evtype = "Different credentials than logged on user"
					elif (tagtype + "10" + tagdata) in ascxml:
                                                evtype = "Remove interactive logon"
					elif (tagtype + "11" + tagdata) in ascxml:
                                                evtype = "Cached credentials used to logon"
					print(success + "Event ID - 4624 - Successful Logon - " + evtype)
					l.write('\n' + "Event ID - 4624 - Successful Logon - " + evtype + '\n')
					l.write("----------------------------------\n")
					l.write(ascxml)
					#print(ascxml) 
				elif ("4625" + tag) in ascxml:
					print(success + "Event ID - 4625 - Failed Logon")
					l.write('\n' + "Event ID - 4625 - Failed Logon - " + '\n')
					l.write("----------------------------------\n")
                                        l.write(ascxml)
					#print(ascxml)
				elif ("4634" + tag) in ascxml:
					print(success + "Event ID - 4234 - Successful Logoff")
					l.write('\n' + "Event ID - 4234 - Successful Logoff" + '\n')
					l.write("----------------------------------\n")
                                        l.write(ascxml)
					#print(ascxml)
	l.write("</Events>")
	print(bcolors.BOLD + "More detailed on file: Output/LogonEvents.txt")
	l.close()

def show_logtimes(reg):

	path = "SAM\Domains\Account\Users\\"

	print(bcolors.BOLD + ("=" * 24) + " LAST LOGIN TIME " + ("=" * 24))
        print(bcolors.ENDC + "Searching in: ")
        print(plus + path)
        #print("[+] %s" % path_h2)
        print("---------------------------------------")


	try:
        	key = open_key(reg, path)
        except:
                print fail + "No keys on " + path

	sub = key.subkeys()
	for e in sub:
		print_values(e)
		for f in e.values():
			if ("User" and "Password") in f.name():
				print(success + "Key value name: " + f.name() + " with value: ")
				print('\t' + f.value())
			else:
				print(success + "Key value name: " + f.name())
		for i in e.subkeys():
			print(success + "Values of " + i.name() + ":")
			print_values(i)
			print("---")
			for v in i.values():
				print(v.name() + " - " + str(v.value()))
			print("---------------------")
			
