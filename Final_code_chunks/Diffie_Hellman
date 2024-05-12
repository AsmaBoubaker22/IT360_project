def key_generation():
 # Diffie-Hellman Code
 import numpy as np
 import random
 import sympy
 def generate_primitive_root(p):
    # Find factors of p-1
    factors = sympy.factorint(p - 1)
    # Iterate through random numbers until a primitive root is found
    while True:
        q = random.randint(2, p - 1)
        if all(pow(q, (p - 1) // factor, p) != 1 for factor in factors):
            return q
 p=sympy.randprime(1,200000)
 q= generate_primitive_root(p)
 print('prime number p:', p)
 print('primitive root q:', q)
 print('Please share these two numbers with the other party.')
 private_key = int(input("Enter your private key :"))

 #calculate public key to share
 public_key = pow(q,private_key,p)
 print('this is your public key :', public_key)

 #calculate shared key
 print('Please share your public key with the other party.')
 public2_key=int(input("Enter the other party public key :"))
 shared_key = pow(public2_key,private_key,p)

 #result
 print('this is your shared secret key: ', shared_key)
