from PIL import Image, ExifTags
import json
import piexif
import piexif.helper

def decode_text(image_path):
    # %% Read in exif data
    exif_dict = piexif.load(image_path)
    # Extract the serialized data
    user_comment = piexif.helper.UserComment.load(exif_dict["Exif"][piexif.ExifIFD.UserComment])
    # Deserialize
    return user_comment

def encode_text (text_to_encode, image_path):
    # load existing exif data from image
    exif_dict = piexif.load(image_path)
    # insert custom data in usercomment field
    exif_dict["Exif"][piexif.ExifIFD.UserComment] = piexif.helper.UserComment.dump(
        text_to_encode,
        encoding="unicode"
    )
    # insert data into image
    piexif.insert(
        piexif.dump(exif_dict),
        image_path
    )

    
encode_text("test009", "C:/test/image.jpg");
output = decode_text("C:/test/image.jpg")
print(output)
