#!/usr/bin/env python3
import requests
import argparse
import time
from concurrent.futures import ThreadPoolExecutor

# To parse the arguments
parse = argparse.ArgumentParser()

parse.add_argument("-d", "--domain", required=True, help="target domain")
parse.add_argument("-ds", "--type", required=True, help="subdomain or directory enumeration")
parse.add_argument("-p", "--port", type=int, default=80, help="target port")
parse.add_argument("-T", "--threads", type=float, default=50, help="for speed")
parse.add_argument("-w", "--wordlist", type=str, help="enter wordlist location")
parse.add_argument("-P", "--protocol", type=str, default="http", help="if http or https protocol is used")

args = parse.parse_args()

target = f"Target == {args.protocol}://{args.domain}:{args.port}/"
print(target)
 
# now add requests to it
def subdomain(word):
	word = word.strip()
	fullurl =f"{args.protocol}://{word}.{args.domain}:{args.port}/"
	try:
		response = requests.get(fullurl, timeout=10)
		size = len(response.content)  
		if response.status_code == 200:
			print('\033[92m' + fullurl + ' STATUS= [' + str(response.status_code) + ']' + ', [SIZE=' + str(size) + ']')
		elif 300 <=response.status_code <= 399:
			print('\033[93m' + fullurl + ' STATUS= [' + str(response.status_code) + ']' + ', [SIZE=' + str(size) + ']')
		elif 400 <=response.status_code <= 499:
			print('\033[91m' + fullurl + ' STATUS= [' + str(response.status_code) + ']' + ', [SIZE=' + str(size) + ']')
		elif 500 <=response.status_code:
			print('\033[97m' + fullurl + ' STATUS= [' + str(response.status_code) + ']' + ', [SIZE=' + str(size) + ']')
		else:
			print(response.status_code)
	except requests.exceptions.RequestException:
		pass

def Directory(word):
	word = word.strip()
	fullurl =f"{args.protocol}://{args.domain}:{args.port}/{word}"
	try:
		response = requests.get(fullurl, timeout=10)
		size = len(response.content)  
		if response.status_code == 200:
			print('\033[92m' + fullurl + ' STATUS= [' + str(response.status_code) + ']' + ', [SIZE=' + str(size) + ']')
		elif 300 <=response.status_code <= 399:
			print('\033[93m' + fullurl + ' STATUS= [' + str(response.status_code) + ']' + ', [SIZE=' + str(size) + ']')
		elif 400 <=response.status_code <= 499:
			print('\033[91m' + fullurl + ' STATUS= [' + str(response.status_code) + ']' + ', [SIZE=' + str(size) + ']')
		elif 500 <=response.status_code:
			print('\033[97m' + fullurl + ' STATUS= [' + str(response.status_code) + ']' + ', [SIZE=' + str(size) + ']')
		else:
			print(response.status_code)
	except requests.exceptions.RequestException:
		pass

# choosing subdomain or directory search
if args.type == 's':
    worker = subdomain
elif args.type == 'd':
    worker = Directory
else:
    print("Invalid type. Use 's' or 'd'")
    exit()

with open(args.wordlist, "r") as f:
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        executor.map(worker, f)
