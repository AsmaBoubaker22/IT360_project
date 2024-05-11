from PIL import Image

# Open the image file
image = Image.open(r'C:\test\image.png')
# Replace 'example_image.jpg' with the path to your image file

# Convert the image to RGB mode (in case it's not already)
image = image.convert('RGB')

# Get the width and height of the image
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

# Print or store the list of hex codes
#for hex_code in hex_pixels:
#    print(hex_code)
print('original')
"""for i in range(10):
     print(hex_pixels[i])"""
print(hex_pixels)

#------------------------------------------------------------------------------------------------------------------
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

print('permutationnn')
"""for i in range(10):
     print(hex_pixels[i])"""

#------------------------------------------------------
#FINAAAAAL VERSIIIIIIOOOONNNNNNN
#transposition
import random

def generate_random_keys(image_size):
    random_keys = [random.randint(1, 4) for _ in range(image_size)]
    return random_keys


transposition_key=generate_random_keys(len(hex_pixels))
"""for i in range(10):
     print(transposition_key[i])"""

transposition_key_str = ''.join(map(str,transposition_key))
#print(transposition_key_pixels)
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
"""for i in range(10):
    print(transposed_pixels[i])"""
print(transposed_pixels)

#-------------------------------------------------------------------------------------

# Create the image
from PIL import Image

# Replace "your_image_file.jpg" with the path to your image

# Get the dimensions (width and height) of the image
width, height = image.size

# Print the dimensions
print("Width:", width)
print("Height:", height)
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

# Example list of hex codes
hex_codes = transposed_pixels

# Image size (width, height)
image_dimension = (width,height )

image_final = create(hex_codes, image_dimension)

# Save the image
image_final.save('enc_image.png','PNG')

# Display the image
image_final.show()

# Open a text file in write mode
with open("enc_key.txt", "w") as file:
     #Write the variable to the file
     file.write(transposition_key_str)
