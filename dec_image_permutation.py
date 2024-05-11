from PIL import Image
#----------------------------------------------------------------------------------------------------------------
# Open the ENCRYPTED image file
image = Image.open('enc_image.png')


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
"""for i in range(10):
   print(hex_pixels[i])"""
print("pixels")
print(hex_pixels)

#---------------------------------------------------------------------------------------------
#open ENCRYPTED TRANSPOSITION KEY txt file
# Open the text file in read mode
with open("enc_key.txt", "r") as file:
    # Read the contents of the file into a variable
    trans_key = file.read()

trans_key_str = list(trans_key)
trans_key_int = list(map(int, trans_key_str))

"""for i in range(10):
   print(trans_key_int[i])"""


#----------------------------------------------------------------------------------------------------
#decrypt transposition
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

# Test
org_pixels = decrypt_transposition(hex_pixels, trans_key_int)

"""for i in range(10):
   print(org_pixels[i])"""

print("org_pixels: ", org_pixels)
#---------------------------------------------------------------------------------------------------------
#Decrypt permutation
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

print('permuted')
"""for i in range(10):
   print(org_pixels[i])"""
print(org_pixels)
#--------------------------------------------------------------------------------------------------
# Create the image
from PIL import Image

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
hex_codes = org_pixels

# Image size (width, height)
image_dimension = (width,height )

image_final = create(hex_codes, image_dimension)

# Save the image
image_final.save('dec_image.png','PNG')

# Display the image
image_final.show()