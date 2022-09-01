# -*- coding:utf-8 -*-
###
#    Author:         Steven HELLEC
#    Creation Date:  Friday, August 26th 2022, 7:13:31 pm
###

from . import *


def setup_module(module):
    os.system("mkdir -p trash")


def teardown_module(module):
    os.system("rm -rf trash")


def test_gen_key_encrypt_decrypt():
    """
    Test if simple text can be encrypted and decrypted with the generate key, and give the same value.
    """

    key = GenKeySH(567).gen_sym_key()
    password = "Hello World !!"
    check_decrypt_encrypt(key, password)


def test_with_stored_key():
    """
    Test store generated key in text file.
    """
    GenKeySH(567).gen_sym_key(path_store="trash/key.txt")

    with open("trash/key.txt", "r") as fr:
        key = fr.read().strip()

    password = "Hello World !!"
    check_decrypt_encrypt(key, password)


def test_with_stored_key_only_file():
    """
    Test store generated key in text file.
    """
    GenKeySH(567).gen_sym_key(path_store="key.txt")

    with open("key.txt", "r") as fr:
        key = fr.read().strip()

    password = "Hello World !!"
    check_decrypt_encrypt(key, password)

    os.system("rm -rf key.txt")


def test_raise_error():
    with pytest.raises(GenKeySHException, match=r"AES key must be either.*"):
        GenKeySH().gen_sym_key(nb_bytes=17)

    with pytest.raises(GenKeySHException, match=r"path to store the key is invalid.*"):
        GenKeySH().gen_sym_key(path_store="tututu/zerze")
