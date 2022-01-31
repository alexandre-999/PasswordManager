#! /usr/bin/env python3
#Password Manager
import random
import string
import sys
import pyperclip
import hashlib, binascii, os
import json
import pathlib
import pprint
import webbrowser

def appName():
	YELLO = '\033[33m'
	END = '\033[0m'
	print()
	print(YELLO + "     ########    ###     ######   ######  ##     #     ##   #####   ########  ######" + END)
	print(YELLO + "     ##    ##  ##   ##  ##       ##        ##   ###   ##  ##     ## ##     ## ##    ##" + END)
	print(YELLO + "     ######## #########  ######   ######    ## ## ## ##   ##     ## ########  ##    ##" + END)
	print(YELLO + "     ##       ##     ##       ##       ##    ###   ###    ##     ## ##    ##  ##    ##" + END)
	print(YELLO + "     ##       ##     ##  ######   ######     ##    ##       #####   ##     ## ######" + END)
	print()

def view_account():
	print("Displays the account name.")
	with open("AccountPass.json") as f:
		account_list = json.load(f)
		for k in account_list:
			pprint.pprint(k)

def PW_CP(name):
	with open("AccountPass.json") as f:
		account_list = json.load(f)
		if name in account_list:
			pyperclip.copy(account_list[name][2])
			print("Copy your password!!")
			print("Display the user name of the account: ")
			print(account_list[name][1])
		else:
			print("That account does not exist.")

def pushaccount(accountname, website, username, password):
	with open("AccountPass.json") as f:
		push_account = json.load(f)
		push_account[accountname] = [website, username, password]
	with open("AccountPass.json", "w") as f:
		json.dump(push_account,f)
	print("Registered an account.")

def register():
	done = str(input("Register your new account? (y/n):"))
	while True:
		if done == 'y':
			while done == 'y':
				if os.path.isfile("AccountPass.json"):
					accountname = str(input("Your account-name: "))
					with open("AccountPass.json") as f:
						cheack = json.load(f)
						if accountname in cheack:
							print("That account exists") 
							view_account()
							continue
				else:
					accountname = str(input("Your account-name: "))
				username = str(input("Your user-name: "))
				website = str(input("URL: "))
				yes_or_no = str(input("Make your Password? (y/n): "))
				if yes_or_no == "y":
					digit = int(input("How many digit do you want? (integer only) ")) 
					password = ""
					for i in range(digit):
						char = random.choice(string.ascii_letters)
						password += char
					print(f"Here's your password: {password}")
				elif yes_or_no == "n":
					password = str(input("Enter your Password: ")) 
					print(f"Here's your password: {password}")
				else:
					print(f"Please only enter 'y' or 'n'")
					done = str(input("Register your new account? (y/n):"))	
					continue
				if os.path.isfile("AccountPass.json"):
					pushaccount(accountname, website, username,password)
				else:
					account = {}
					account[accountname] = [website, username, password]
					with open("AccountPass.json", "w") as f:
						json.dump(account,f)
				done = str(input("Register your new account? (y/n):"))
		elif done == "n":
			print("Complete account registration")
			break 
		else:
			print("Please only enter 'y' or 'n'")
			done = str(input("Register your new account? (y/n):"))
			continue

def hash_password(password):
	"""Hash a password for storing."""
	salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
	pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
	pwdhash = binascii.hexlify(pwdhash)
	return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
	"""Verify a stored password against one provided by user"""
	salt = stored_password[:64]
	stored_password = stored_password[64:]
	pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
	pwdhash = binascii.hexlify(pwdhash).decode('ascii')
	return pwdhash == stored_password

def websearch(keys):
	with open("AccountPass.json") as f:
		account = json.load(f)
		if keys in account:
			url = account[keys][0]
			webbrowser.open(url, 2)
		else:
			print("That account does not exist.")

def announce():
    print('※ Enter the string you want to work within the first argument.\n  The following is an input example.')
    print(' ◯ python pwManager.py search: After entering your password, a list of registered accounts will be displayed.')
    print(' ◯ python pwManager.py register: Register a new account.')
    sys.exit()

def search(arguments):
	if arguments == "search":
		if os.path.isfile("loginPass.json"):
			with open("loginPass.json") as f:
				login = json.load(f)
				if arguments in login:
					provided_password = str(input("Enter Your Login Passowrd: "))
					stored_password = login[arguments]
					if verify_password(stored_password, provided_password):
						if not os.path.isfile("AccountPass.json"):
							register()
						view_account()
						name = str(input("Enter the account name for which you want to copy the password.: "))
						PW_CP(name)
						websearch(name)
					else:
						for i in range(1, 6):
							print("Password is different. Please enter Password again." , i , "回目")
							provided_password = str(input("Enter Your Login Passowrd: "))
							stored_password = login[arguments]	
							if verify_password(stored_password, provided_password):
								view_account()
								name = str(input("Enter the account name for which you want to copy the password.: "))
								PW_CP(name)
								websearch(name)	
								break
							elif i < 5:
								continue
							else:
								print("Will delete your file data of unauthorized access.")
								de1 = pathlib.Path('AccountPass.json')
								de2 = pathlib.Path('loginPass.json')
								de1.unlink()
								de2.unlink()
								break
		else:
			account = {}
			logPass = str(input("Register Your Login Passowrd: ")) 
			stored_password = hash_password(logPass)
			account[arguments] = stored_password
			with open("loginPass.json","w") as f:	
				json.dump(account, f)
			
	elif arguments == "register":
		register()
	else:
		announce()

if __name__ == "__main__":
	appName()
	arguments  = sys.argv[1]	
	# arguments  = ""
	search(arguments)