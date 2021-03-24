#!/usr/bin/env python3

#AJ2K
#28/08/2020
#./comments.py -H http://google.com -o newfile.txt --proxies 127.0.0.1:8080
#./comments.py -H http://google.com

import requests, argparse, sys, colorama, re
from bs4 import BeautifulSoup, Comment
from colorama import Fore, Style, init, Back
from requests.packages.urllib3.exceptions import InsecureRequestWarning
init(autoreset=True) # reset style automagically

# ~~~~~~~ GET ARGUMENTS, DEFINE FUNCTIONS, SET VARIABLES
def error(): # good old error
     parser.print_help() # basically -h
     quit() # close

parser = argparse.ArgumentParser(description='Args') # Welcome message
requiredNamed = parser.add_argument_group('Required Arguments') # Required group
requiredNamed.add_argument("-H", dest="Host",  help="protocol:host eg http(s)://x.x.x.x", required=True) # the host
requiredNamed.add_argument("-o", dest="Outfile", help="default WEB-comments.txt", required=False) # outfile
parser.add_argument("-p", dest="Proxy", help="host:port eg 127.0.0.1:8080", required=False) # proxy
args = parser.parse_args() # parser

try:
     url = args.Host # set url to -H arg
     filename = args.Outfile # set filename to -o arg
except:
     error() # if the above fails then error out

if args.Proxy is None: # if proxy isn't set
     proxybool = False # set bool to false
else: # if proxy is set
     proxiesarg = args.Proxy # set proxiesarg to the --proxies arg
     proxybool = True # set proxybool to true

if args.Outfile is None: # if -o is empty
     Outfile = "WEB-comments.txt" # set default outfile
else: # if -o isn't empty
     Outfile = args.Outfile # set Outfile to -o flag

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MAKE WEB REQUEST FOR PAGE/SET PROXY
try:
     requests.packages.urllib3.disable_warnings(InsecureRequestWarning) # remove nasty SSL warning
except:
     print(Fore.GREEN + Style.BRIGHT + Back.BLACK + "You may get some SSL warnings")

if (proxybool): # if proxy is set
     proxy = {
     "http": proxiesarg, # http proxy
     "https": proxiesarg # https proxy
     }
     try: # try make request with proxy
          request = requests.get(url, proxies=proxy, verify=False) # make GET request with proxy, don't verify SSL
     except: # On failure
          print(Fore.RED + Style.BRIGHT + Back.WHITE + "FAILURE - is the proxy correct? is the host down?"); error() # error text then error out
else: # if proxy is not set
     try:
          request = requests.get(url, verify=False) # make GET request, don't verify SSL
     except:
          print(Fore.RED + Style.BRIGHT + Back.WHITE + "FAILURE - is the host down?"); error() # generic error
try:
     BYTES = request.content.decode('utf-8') # read response
except:
     try:
          BYTES = request.content.decode('utf-16')
     except:
          print(Fore.RED + Style.BRIGHT + Back.WHITE + "Could not read HTTP source as utf-8 or utf-16 :("); error; # generic error
try:
     request.close() # close connection
except:
     print(Fore.RED + Style.BRIGHT + Back.WHITE + "Failed to close request"); error() # generic error

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FORMAT
try:
     file = open(Outfile, 'w+') # open file for writing
except:
     print(Fore.RED + Style.BRIGHT + Back.WHITE + "Could not open file for writing"); error() # generic error

"""
try:
     soup = BeautifulSoup(BYTES, 'lxml') # prepare to search
except:
     print(Fore.RED + Style.BRIGHT + Back.WHITE + "Could not initialize BeautifulSoup"); error() # generic error

try:
     print(Fore.GREEN + Style.BRIGHT + "START OF HTML COMMENTS...")
     for x in soup.findAll(text=lambda text:isinstance(text, Comment)): # search for comments
          out = "<!-- " +x+ " -->\n" # formatting
          file.write(out) # write
          print(Fore.BLUE + Style.BRIGHT + out) # output to terminal
except:
     print(Fore.RED + Style.BRIGHT + Back.WHITE +"FAILURE in loop"); error() # generic error
"""

print(Fore.GREEN + Style.BRIGHT + "START OF SINGLE LINE JS COMMENTS...")
file.write("START OF SINGLE LINE JS COMMENTS...\n") # write
for line in BYTES.splitlines():
     if(re.search("//", line)):
          if not re.search("http", line) and not re.search("scr", line) and not re.search("href", line):
               print(Fore.BLUE + Style.BRIGHT + line)
               file.write(line + "\n") # write

print(Fore.GREEN + Style.BRIGHT + "\nSTART OF MULTI LINE JS OR CSS COMMENTS...")
file.write("\nSTART OF MULTI LINE JS OR CSS COMMENTS...\n")
jsmulti = False
for line in BYTES.splitlines():
     if(re.search("\*/", line)) and jsmulti:
          print(Fore.BLUE + Style.BRIGHT + line + "\n")
          file.write(line + "\n\n") # write
          jsmulti = False
     if (jsmulti):
          print(Fore.BLUE + Style.BRIGHT + line)
          file.write(line + "\n") # write
     else:
          if(re.search("/\*", line)):
               if(re.search("\*/", line)):
                    jsmulti = False
                    print(Fore.BLUE + Style.BRIGHT + line + "\n")
                    file.write(line + "\n\n")
               else:
                    jsmulti = True
                    print(Fore.BLUE + Style.BRIGHT + line)
                    file.write(line + "\n") # write

print(Fore.GREEN + Style.BRIGHT + "\nSTART OF MULTI LINE HTML COMMENTS...")
file.write("\nSTART OF MULTI LINE HTML COMMENTS...\n")
htmlmulti = False
for line in BYTES.splitlines():
     if(re.search("-->", line)) and htmlmulti:
          print(Fore.BLUE + Style.BRIGHT + line + "\n")
          file.write(line + "\n\n")
          htmlmulti = False
     if (htmlmulti):
          print(Fore.BLUE + Style.BRIGHT + line)
          file.write(line + "\n")
     else:
          if(re.search("<!--", line)):
               if(re.search("-->", line)):
                    print(Fore.BLUE + Style.BRIGHT + line + "\n")
                    htmlmulti = False
                    file.write(line + "\n\n")
               else:
                    print(Fore.BLUE + Style.BRIGHT + line)
                    htmlmulti = True
                    file.write(line + "\n")
