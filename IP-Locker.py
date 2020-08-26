from colorama import Fore, Back, Style
import os
import sys
import time

ufw_command = "sudo ufw deny from {ip} to any port {port} > /dev/null 2>&1"
iptables_command = "sudo iptables - A INPUT -s {ip} -i eth1 -p tcp -m state --state NEW -m tcp --dport {port} - j DROP > /dev/null 2>&1"

COMMAND = ""
PATH = ""

WARNING = Fore.WHITE + "[" + Fore.RED + " ! " + Fore.WHITE + "] " + Fore.WHITE
ATTENTION = Fore.WHITE + "[" + Fore.YELLOW + " ! " + Fore.WHITE + "] " + Fore.WHITE
FINE = Fore.WHITE + "[" + Fore.GREEN + " ! " + Fore.WHITE + "] " + Fore.WHITE
OTHER = Fore.WHITE + "[" + Fore.BLUE + " * " + Fore.WHITE + "] " + Fore.WHITE
QUESTION = Fore.WHITE + "[" + Fore.GREEN + " ? " + Fore.WHITE + "] " + Fore.WHITE

Y_N = Fore.GREEN + "[Y]es" + Fore.WHITE + " / " + Fore.RED + "[N]o" + Fore.WHITE

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def verifyPerms():
    if os.name == "nt":
        clear()
        print(WARNING + "Windows is not supported yet.")
        exit()
    if not os.geteuid() == 0:
        clear()
        print(WARNING + "This script must be run as root!\n")
        exit()
        
def yesORno():
    value = input()
    return value.lower() in "yes"



def askFile():
    clear()
    print(QUESTION + "do you want to use a custom file? " + Y_N)
    if yesORno():
        return use_custom_path()
    else:
        return "./range.txt"

def use_custom_path():
    print(FINE + "Ok, now give me the path of the file")
    print(FINE + "Example /path/to/file/ips.txt\n\n")
    path = input()
    if os.path.isfile(path) == True:
        return path
    else:
        print(WARNING + "Ooo, this is not a file, please try again.")
        return use_custom_path()



def loadFile():
    global PATH, COMMAND
    file = open(PATH, 'r')
    return file.readlines()

def blacklist():
    lines = loadFile()
    clear()
    for x in lines:
        #clear()
        try:
            os.system(COMMAND.format(ip=x, port="22") + " & clear")
            print(f"{OTHER} BlackListing IP {x}")
        except KeyboardInterrupt:
            sys.exit(WARNING + "Exit.")
            break
    print(FINE + "Done, Bye!")
    exit()


def what_command():
    global COMMAND
    clear()
    print(QUESTION + "what do you want to use? IPTABLES or UFW ? \n")
    print(Fore.YELLOW + "[ 1 ] " + Fore.WHITE + "IPTABLES")
    print(Fore.YELLOW + "[ 2 ] " + Fore.WHITE + "UFW")
    i = input()
    if i == "1":
        COMMAND = iptables_command
        blacklist()
    elif i == "2":
        COMMAND = ufw_command
        blacklist()
    else:
        what_command() 

def start():
    global PATH
    print(ATTENTION + "Loading...\n")
    time.sleep(1)
    verifyPerms()
    time.sleep(1)
    PATH = askFile()
    what_command()



if __name__ == '__main__':
    start()




