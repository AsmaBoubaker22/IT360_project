#!/usr/bin/env python3
from PIL import Image

# Open the image file
image = Image.open(r'/home/liveuser/Downloads/image.jpeg')  # Replace 'example_image.jpg' with the path to your image file


#------------------------------------------------------------------------------------------
# Convert the image to RGB mode (in case it's not already)
image = image.convert('RGB')

# Get the width and height of the image
width, height = image.size

# Access pixel data and convert to hex
hex_pixels = []
for y in range(height):
    for x in range(width):
        # Get the RGB values of the pixel at position (x, y)
        r, g, b = image.getpixel((x, y))
        # Convert RGB values to hexadecimal format and concatenate
        hex_code = '{0:02x}{1:02x}{2:02x}'.format(r, g, b)
        # Append the hex code to the list
        hex_pixels.append(hex_code)

# Print or store the list of hex codes
#for i in range(10):
#     print(hex_pixels[i])


#----------------------------------------------------------------------------------------------
#permutation 
'''if len(hex_pixels)%2 == 0 :
    for i in range(0,int(len(hex_pixels)/2) , 2 ):
        perm1 = hex_pixels[i]
        perm2 = hex_pixels[(len(hex_pixels)-1)-i]
        hex_pixels[i] = perm2
        hex_pixels[(len(hex_pixels)-1)-i] = perm1
    
else :
    for i in range(0,int((len(hex_pixels)+1)/2) , 2 ):
        perm1 = hex_pixels[i]
        perm2 = hex_pixels[(len(hex_pixels)-1)-i]
        hex_pixels[i] = perm2
        hex_pixels[(len(hex_pixels)-1)-i] = perm1

#for i in range(10):
#     print(hex_pixels[i])

#--------------------------------------------------------------------------------------

#transposition
import random

def generate_random_keys(image_size):
    random_keys = [random.randint(1, 6) for _ in range(image_size)]
    return random_keys


transposition_key=generate_random_keys(len(hex_pixels))
for i in range(10):
     print(transposition_key[i])

transposition_key_str=' '.join(map(str,transposition_key))
#print(transposition_key_str)
def transpose_pixel(pixel_code, transposition_key):
    transposed_pixels = []
    for pixel, key in zip(pixel_code, transposition_key):
        cipher = [''] * key
        for column in range(key):
            pointer = column
            while pointer < len(pixel):
                cipher[column] += pixel[pointer]
                pointer += key
        cipher = ''.join(cipher)
        transposed_pixels.append(cipher)
    return transposed_pixels

transposed_pixels = transpose_pixel(hex_pixels,transposition_key)

print('transposed_pixel_final')
for i in range(10):
    print(transposed_pixels[i])


#--------------------------------------------------------------------------------------------
'''#convert the pixels back to image 

from PIL import Image
# Get the dimensions (width and height) of the image
width, height = image.size

# Print the dimensions
#print("Width:", width)
#print("Height:", height)

from PIL import Image, ImageDraw
import os
import shutil
import tempfile
def create(hex_codes, image_size):
    # Create a new image with the specified size
    img = Image.new('RGB', image_size)

    # Create a pixel map
    pixels = img.load()

    # Iterate over each pixel in the image and set its color based on the hex codes
    for x in range(image_size[0]):
        for y in range(image_size[1]):
            # Calculate the index of the hex code based on the current pixel position
            index = (x * image_size[1] + y) % len(hex_codes)
            # Convert the hex code to RGB format
            rgb_color = tuple(int(hex_codes[index][i:i+2], 16) for i in (0, 2, 4))
            # Set the color of the current pixel
            pixels[x, y] = rgb_color

    return img

# Example list of hex codes
hex_codes = transposed_pixels

# Image size (width, height)
image_dimension = (width,height )

# Create the image
image_final = create(hex_codes, image_dimension)

# Save the image
from PIL.ExifTags import TAGS
image_final.save('/home/liveuser/Downloads/asma2.jpeg', 'JPEG')

#image_final.show()
'''
$kabb -n image.jpg -enc  
secret key:
to generate --help , recommend -g ''''


#---------------------------------------------------------------------------------------------
#transform diffie secret key into suitable key for AES
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import os

def derive_aes_key(shared_secret):
    # Perform key derivation using HKDF
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,  # AES-256 key size (32 bytes)
        salt=None,
        info=b'diffie-hellman-secret-to-aes-key',
        backend=default_backend()
    )
    aes_key = hkdf.derive(shared_secret)
    return aes_key

# Example usage:
# shared_secret is the Diffie-Hellman shared secret obtained from the key exchange process
#shared_secret = b'1248978564653346'
#aes_key = derive_aes_key(shared_secret)
#print("Derived AES Key:", aes_key.hex())



#----------------------------------------------------------------------------------------------------------
#aes encryption for transposition key 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

def encrypt_text(text, key):
    # Convert text to bytes
    plaintext = text.encode('utf-8')
    
    # Generate a random IV
    iv = get_random_bytes(AES.block_size)
    
    # Create AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Pad the plaintext to match block size
    padded_plaintext = pad(plaintext, AES.block_size)
    
    # Encrypt the padded plaintext
    ciphertext = cipher.encrypt(padded_plaintext)
    
    # Return IV and ciphertext
    encrypt_text_return=[iv,ciphertext]
    return encrypt_text_return

# Example text to encrypt
#text = transposition_key

# Generate a random key (16 bytes for AES-128)
#key = aes_key

# Encrypt the text
#iv, ciphertext = encrypt_text(text, key)

# Print IV and ciphertext
#print("IV:", iv)
#print("Ciphertext:", ciphertext)

import argparse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad 
import numpy as np
import random
import sympy 

#permutation function 
def permutation(hex_pixels):
    if len(hex_pixels)%2 == 0 :
        for i in range(0,int(len(hex_pixels)/2) , 2 ):
         perm1 = hex_pixels[i]
         perm2 = hex_pixels[(len(hex_pixels)-1)-i]
         hex_pixels[i] = perm2
         hex_pixels[(len(hex_pixels)-1)-i] = perm1
    
    else :
        for i in range(0,int((len(hex_pixels)+1)/2) , 2 ):
         perm1 = hex_pixels[i]
         perm2 = hex_pixels[(len(hex_pixels)-1)-i]
         hex_pixels[i] = perm2
         hex_pixels[(len(hex_pixels)-1)-i] = perm1

    permutated_image=hex_pixels
    return permutated_image

#transposition function
import random
def transposition(permutated_image):
    def generate_random_keys(image_size):
        random_keys = [random.randint(1, 6) for _ in range(image_size)]
        return random_keys
    transposition_key=generate_random_keys(len(permutated_image))
    for i in range(10):
         print(transposition_key[i])

    transposition_key_str=' '.join(map(str,transposition_key))
    #print(transposition_key_str)
    def transpose_pixel(pixel_code, transposition_key):
        transposed_pixels = []
        for pixel, key in zip(pixel_code, transposition_key):
            cipher = [''] * key
            for column in range(key):
                 pointer = column
            while pointer < len(pixel):
                cipher[column] += pixel[pointer]
                pointer += key
        cipher = ''.join(cipher)
        transposed_pixels.append(cipher)
        transposed_pixels_return=[transposition_key,transposed_pixels]
        return transposed_pixels_return
    transposed_pixels = transpose_pixel(permutated_image,transposition_key)
    #print('transposed_pixel_final')
    return transposed_pixels

#encrypt_aes_image function
'''def encrypt_aes(image,shared_key):
        cipher=AES.new(shared_key,AES.MODE_ECB)
        padded_image_data=pad(image,AES.block_size)
        encrypted_image_data=cipher.encrypt(padded_image_data)
        return encrypted_image_data'''

def encrypt_image(image_file,transposition_key,shared_key=None,encrypt_with_aes=False):
        with open(image_file,'rb') as f:
             image_data =f.read()
        permuted_image=permutation(image_file)
        transposed_image=transposition(permuted_image,transposition_key)
        derived_aes_key=derive_aes_key(shared_key)
        encrypted_aes_key=encrypt_text(transposed_image[0], derived_aes_key[1])
        
        with open(image_file+'.enc','wb')as f:
            f.write(encrypted_data)
        print(f"Image encrypted and saved as {image_file}.enc")
        return(image_file)
        
#diffie hellman function

p=sympy.randprime(1,200000)
q=random.random()
def diffie_hellman(p,q):
    private_key=int(input("Enter your private key :"))
    public_key=pow(q,private_key,p)
    return private_key,public_key


#command creation 
def main():
    parser=argparse.ArgumentParser(prog='kabb',description='new kabb command to encrypt an image')
    parser.add_argument('-n','--image',metavar='IMAGE_FILE',help='name of the image file to encrypt',required=True)
    parser.add_argument('-enc','--encrypt',action='store_true',help='encrypt the image')  
    parser.add_argument('-g','--generate-key',action='store_true',help='generate shared key using diffie-hellman')      
    args=parser.parse_args()
    
    if args.generate_key:
        shared_key=pow(q,diffie_hellman(p,q)[0],p)
        print("shared key :",shared_key)
    if args.encrypt:
        shared_key=input("enter you shared secret key :") 
        permuted_image=permutation(image)
        transposed_image=transposition(permuted_image)
        derived_aes_key=derive_aes_key(shared_key)
        encrypted_aes_key=encrypt_text(transposed_image[0], derived_aes_key[1])
        encrypt_image(args.image,shared_key,encrypt_with_aes=bool(shared_key))
        if shared_key
    
if __name__=="__main__":
    main()


