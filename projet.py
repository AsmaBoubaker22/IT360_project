from PIL import Image

# Open the image file
image = Image.open(r'C:\test\image.jpeg')  # Replace 'example_image.jpg' with the path to your image file


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

#for i in range(10):
#     print(hex_pixels[i])


#--------------------------------------------------------------------------------------
#transposition
import random

def generate_random_keys(image_size):
    random_keys = [random.randint(1, 6) for _ in range(image_size)]
    return random_keys

random_keys = generate_random_keys(len(hex_pixels))
random_keys_final = ''.join(list(map(str,random_keys)))
#print("Random Keys:", random_keys_final)


transposition_key=generate_random_keys(len(hex_pixels))
transposition_key_pixels=' '.join(map(str,transposition_key))
#print(transposition_key_pixels)
def transpose_pixel(pixel_code, transposition_key):

    # Convert pixel code to a list of characters
    pixel_list = list(pixel_code)

    # Convert single integer key to a list containing that integer
    if not isinstance(transposition_key, list):
        transposition_key = [transposition_key]

    # Apply transposition using the key
    transposed_pixel = [pixel_list[i] for i in transposition_key]

    # Convert transposed pixel back to a string
    transposed_pixel = ''.join(transposed_pixel)

    return transposed_pixel

transposed_pixel=transpose_pixel(hex_pixels,transposition_key)
#print (transposed_pixel)

seperator_size = 6
# Split the string into chunks of 6 characters each
chunks = [transposed_pixel[i:i+seperator_size] for i in range(0, len(transposed_pixel), seperator_size)]
# Join the chunks together with the separator
transposed_pixel_size = ' '.join(chunks)
transposed_pixel_final=transposed_pixel_size.split()

#print(len(transposed_pixel_final))
#for i in range(10):
#    print(transposed_pixel_final[i])


#--------------------------------------------------------------------------------------------
#convert the pixels back to image 

from PIL import Image
# Get the dimensions (width and height) of the image
width, height = image.size

# Print the dimensions
print("Width:", width)
print("Height:", height)

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
hex_codes = transposed_pixel_final 

# Image size (width, height)
image_dimension = (width,height )

# Create the image
image_final = create(hex_codes, image_dimension)

# Save the image
from PIL.ExifTags import TAGS
image_final.save('C:/test/output1.jpg', 'JPEG', exif='metadata')

#image_final.show()
'''
$kabb -n image.jpg -enc  
secret key:
to generate --help , recommend -g '''


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
shared_secret = b'1248978564653346'
aes_key = derive_aes_key(shared_secret)
print("Derived AES Key:", aes_key.hex())



#----------------------------------------------------------------------------------------------------------
#aes encryption
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
    return iv, ciphertext

# Example text to encrypt
text = random_keys_final

# Generate a random key (16 bytes for AES-128)
key = aes_key

# Encrypt the text
iv, ciphertext = encrypt_text(text, key)

# Print IV and ciphertext
#print("IV:", iv)
print("Ciphertext:", ciphertext)

