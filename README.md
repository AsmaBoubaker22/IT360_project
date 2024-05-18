# IT360_project

The project code will run in the LINUX CMD.

 1 - main.py : is the main project code that links all other files and will be used in the CMD.
 
 2 - image.png : the image to be encrypted and used (note: the image must be png, since jpg type is not well suited for the project).
 
 3 - image_encryption.py : the encryption code that will be imported by main.py. It is divided into several parts; pixels' transformation, permutation, transposition, AES-192 encryption, pixels conversion...
 
 4 - image_decryption.py : the decryption code that will be imported by main.py. It is divided into several parts; pixels' decryption, AES-192 decryption, permutation, transposition, pixels conversion into image ...
 
 5 - Diffie_Hellman.py : the key exchange algorithm code. this code will generate a prime and a base value as well as a shared secret key based on the user private key.

 *To run the code on LINUX CMD, all files should be in the same directory, and some other steps should be done (explained here : https://linuxhandbook.com/run-python/ )

 *Arguments that can be used:
 
   -enc : to encrypt
   
   -dec : to decrypt
   
   -n : image path
   
   -g : generate a shared key using Diffie_Hellman
   
