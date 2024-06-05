#!/usr/bin/python
from PIL import Image
from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import argparse



def main():
    parser=argparse.ArgumentParser(prog='kabb',description='new kabb command to encrypt an image')
    parser.add_argument('-n','--image',metavar='IMAGE_FILE',help='name of the image file to encrypt',required=False)
    parser.add_argument('-f','--file',metavar='FILE_PATH',help='name of the file path')
    parser.add_argument('-enc','--encrypt',action='store_true',help='encrypt the image')  
    parser.add_argument('-g','--generate_key',action='store_true',help='generate shared key using diffie-hellman')    
    parser.add_argument('-dec','--decrypt',action='store_true',help='decrypt the image')   
    args=parser.parse_args()
    
    if args.encrypt:
        import image_encryption
        print("*Please make sure your shared key is an integer ")
        shared_key=input("enter you shared secret key :")
        def verify(sahred_key):
            try:
                return int(shared_key)
            except (ValueError , TypeError) : 
                return "default"
        s=verify(shared_key)       
        if  (type(s)==int ):   
            image_encryption.encryption(args.image,shared_key)
        else: 
            print("if you do not have a key type -g to generate it ")
            print("*the key should be integer*")
            
    
    if args.generate_key:
        import Diffie_Hellman
        #Diffie_Hellman.key_generation()
    if args.decrypt:
        import image_decryption
        image_decryption.image_decryption(args.image,args.file)
        
          
if __name__=="__main__":
    main()
