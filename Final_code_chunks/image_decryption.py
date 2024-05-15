#!/usr/bin/python
from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF




def image_decryption(image_path,file_path):
 #---------------------------------------------------------------------------------------------
 #DECRYPT EMBEDDED KEY TXT FILE
 #input shared key
 shared_key = int(input("Enter your shared key :"))
 shared_key = (str(shared_key)).encode()

 # Open the text file in read mode
 with open(file_path, "rb") as file:
     # Read the contents of the file into a variable
     enc_key = file.read()

 #AES decryption



 class Encryptor:
     def __init__(self, key):
         self.key = key

     def pad(self, s):
         return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

     def encrypt(self, message):
         message = self.pad(message)
         iv = Random.new().read(AES.block_size)
         cipher = AES.new(self.key, AES.MODE_CBC, iv)
         return iv + cipher.encrypt(message)

     def decrypt(self, cipherText):
         iv = cipherText[:AES.block_size]
         cipher = AES.new(self.key, AES.MODE_CBC, iv)
         plaintext = cipher.decrypt(cipherText[AES.block_size:])
         return plaintext.rstrip(b"\0")

 #converting shared key to a usable
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

 aes_key = derive_aes_key(shared_key)
 encryptor = Encryptor(aes_key)

 #decrypt
 decrypted_key = encryptor.decrypt(enc_key)
 decrypted_key = decrypted_key.decode('utf-8')

 #Verification of shared key

 #transform key string to list of integers
 trans_key_str = list(decrypted_key)
 trans_key_int = list(map(int, trans_key_str))

 #------------------------------------------------------------------------------------------------------------
 # IMAGE CONVERSION TO PIXELS
 from PIL import Image
 image = Image.open(image_path)

 # Convert the image to RGB mode
 image = image.convert('RGB')
 width, height = image.size

 # Access pixel data and convert to hex
 hex_pixels = []
 for x in range(width):
     for y in range(height):
         # Get the RGB values of the pixel at position (x, y)
         r, g, b = image.getpixel((x, y))
         # Convert RGB values to hexadecimal format and concatenate
         hex_code = '{0:02x}{1:02x}{2:02x}'.format(r, g, b)
         # Append the hex code to the list
         hex_pixels.append(hex_code)


 #----------------------------------------------------------------------------------------------------
 #TRANSPOSITION DECRYPTION
 def decrypt_transposition(enc_pixels, enc_key):
   org_pixels = []
   for pixel, key in zip(enc_pixels, enc_key):
    if key != 5 :
     n = len(pixel)
     columns_with_1_character = n % key
     full_columns = key - columns_with_1_character

     if full_columns != 0:
         characters_per_full_column = (n - columns_with_1_character) // full_columns
     else:
         characters_per_full_column = 0  # All columns have only 1 character

     columns = []
     idx = 0

     for _ in range(full_columns):
         if idx < n:
             columns.append(pixel[idx:idx + characters_per_full_column])
             idx += characters_per_full_column

     for _ in range(columns_with_1_character):
         if idx < n:
             columns.append(pixel[idx:idx + 1])
             idx += 1

     # Reconstruct the original string
     original_pixel = []
     # Iterate row-wise to reconstruct the original string
     max_row_length = max((len(col) for col in columns), default=0)
     for row in range(max_row_length):
         for column in columns:
             if row < len(column):
                 original_pixel.append(column[row])

     original_pixel=''.join(original_pixel)
     org_pixels.append(original_pixel)
    else:
     org_pixels.append(pixel)
   return org_pixels

 #Original pixels list
 org_pixels = decrypt_transposition(hex_pixels, trans_key_int)


 #---------------------------------------------------------------------------------------------------------
 #PERMUTATION DECRYPTION
 if len(org_pixels) % 2 == 0:
     for i in range(0, int(len(org_pixels) / 2), 2):
         perm1 = org_pixels[i]
         #print("perm1:",perm1)
         perm2 = org_pixels[(len(org_pixels) - 1) - i]
         #print("perm2:",perm2)
         org_pixels[i] = perm2
         org_pixels[(len(org_pixels) - 1) - i] = perm1

 else:
     for i in range(0, int((len(org_pixels) + 1) / 2), 2):
         perm1 = org_pixels[i]
         perm2 = org_pixels[(len(org_pixels) - 1) - i]
         org_pixels[i] = perm2
         org_pixels[(len(org_pixels) - 1) - i] = perm1


 #--------------------------------------------------------------------------------------------------
 #PIXELS CONVERSION TO IMAGE
 from PIL import Image

 #width and height of the image
 width, height = image.size
 #print("Width:", width)
 #print("Height:", height)

 from PIL import Image, ImageDraw

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

 hex_codes = org_pixels

 image_dimension = (width,height)

 image_final = create(hex_codes, image_dimension)

 #Save the image
 image_final.save('dec_image.PNG','PNG')

 # Display the image
 image_final.show()
