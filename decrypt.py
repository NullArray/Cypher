import os
import sys

from multiprocessing import Pool
from Crypto.PublicKey import RSA
from base64 import b64decode


with open('privkey', 'r') as keyfile:
	keyData = keyfile.read().replace('\n', '')

	
keyDER = b64decode(keyData)	
key = RSA.importKey(keyDER)


def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):

    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)


def single_arg_decrypt_file(in_filename):
    decrypt_file(key, in_filename)


def select_files():
    
    ext = ".crypt"
           
    files_to_dec = []
    for root, dirs, files in os.walk("/"):
        for file in files:
            if file.endswith(str(ext)):
                files_to_dec.push(os.path.join(root, file))

    pool = Pool(processes=4)
    pool.map(single_arg_decrypt_file, files_to_dec)


if __name__=="__main__":
	select_files()
