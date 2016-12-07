import sys
import mmap
import contextlib

import argparse

from Registry import Registry

from Evtx.Evtx import FileHeader
from Evtx.Views import evtx_file_xml_view

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



def ascii(s):
    	return s.encode('ascii', 'replace').decode('ascii')

def show_logons(arg):
	print(("=" * 24) + "Successful/Failed Logons" + ("=" * 24))
        print("Searching in dir: ")
        print("[+] %s" % arg)
        #print("[+] %s" % path_h2)
        print("---------------------------------------")	

	tag = "</EventID>"
	
    	with open(arg, 'r') as f:
        	with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as buf:
        	    	fh = FileHeader(buf, 0x0)
            		print("<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"yes\" ?>")
            		print("<Events>")
            		for xml, record in evtx_file_xml_view(fh):
				ascxml = ascii(xml)
				if ("4624" + tag) in ascxml:
					print("Event ID - 4624 - Successful Logon")
					print("----------------------------------")
					print(ascxml) 
				elif ("4625" + tag) in ascxml:
					print("Event ID - 4625 - Failed Logon")
                                        print("------------------------------")
                                        print(ascxml)
				elif ("4634" + tag) in ascxml:
					print("Event ID - 4234 - Successful Logoff")
                                        print("-----------------------------------")
                                        print(ascxml)
	print("</Events>")

def show_logtimes(reg):

	path = "SAM\Domains\Account\Users"

	print(("=" * 24) + "Last Login Time" + ("=" * 24))
        print("Searching in dir: ")
        print("[+] %s" % path)
        #print("[+] %s" % path_h2)
        print("---------------------------------------")


	try:
        	key = open_key(reg, path)
        except:
                print "No keys on " + path
	#incomplete
	print_keys(key)
