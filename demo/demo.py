# -*- coding:utf-8 -*-
###
#    Author:         Steven HELLEC
#    Creation Date:  Thursday, September 1st 2022, 4:40:16 pm
###
from sh_crypt import GenKeySH, CryptSH
import random as rnd

# Create key generatore
seed = rnd.randint(1, 1e12)
key_gen = GenKeySH(seed)

key = key_gen.gen_sym_key(path_store="mykey.txt")
# Ex : 'e169344ae15719669ed2fecea1ac4773'

password = "Hello World !!"

crypt = CryptSH(key)

encrypt_password = crypt.encrypt_password(password)
# Ex : '469feb93adc2af609a98e6b7cee859bb'

crypt.decrypt_password(encrypt_password)
# 'Hello World !!'