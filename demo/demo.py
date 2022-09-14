# -*- coding:utf-8 -*-
###
#    Author:         Steven HELLEC
#    Creation Date:  Thursday, September 1st 2022, 4:40:16 pm
###
from sh_crypt import GenKeySH, SymCryptSH, AsymCryptSH
import random as rnd

###############################
## Symetric Cipher

# Create key generator
seed = rnd.randint(1, 1e12)
key_gen = GenKeySH(seed)

key = key_gen.gen_sym_key(path_store="mykey.txt")
# Ex : 'e169344ae15719669ed2fecea1ac4773'

password = "Hello World !!"

crypt = CryptSH(key)

encrypt_password = crypt.encrypt_message(password)
# Ex : '469feb93adc2af609a98e6b7cee859bb'

crypt.decrypt_message(encrypt_password)
# 'Hello World !!'

###############################
## Asymetric Cipher

key_gen = GenKeySH()

priv_key, public_key = key_gen.gen_asym_key()
# We can store the key with parameters path_store="file_path".

crypt = AsymCryptSH()

crypt.add_key(priv_key)
crypt.add_key(public_key)

message = "Hello World !!!"

# Encrypt / Decrypt Message
message_enc = crypt.encrypt_message(message)

crypt.decrypt_message(message_enc)

# Sign message / check signature

signature = crypt.sign_message(message)

if crypt.check_sign_message(signature, message):
    print("Signature is valid")
else:
    print("Signature is invalid")
