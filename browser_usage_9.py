import sys
from Registry import Registry

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


def print_keysvalues(key, depth=0):
        print "\t" * depth + key.path()

        for subkey in key.subkeys():	
		for value in subkey.values():
			print(value.name())
			print(value.value())
                	print_keysvalues(subkey, depth + 1)

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


def keys(ntuser):
	IEpath= "\Software\Microsoft\Internet Explorer"
	
	print(bcolors.BOLD + ("=" * 24) + " IE KEY VALUES " + ("=" * 24))
        print(bcolors.ENDC + "Searching in: ")
        print(plus + ntuser)
	print('\t' + plus + IEpath)
        print("---------------------------------------")

	reg = Registry.Registry(ntuser)
	try:
		key = reg.open(IEpath)
		print_keysvalues(key)
	except:
		print(fail + "Couldn't find IE Keys")

