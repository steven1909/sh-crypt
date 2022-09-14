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


def test_gen_key_encrypt_decrypt_sym():
    """
    Test if simple text can be encrypted and decrypted with the generate key, and give the same value.
    """

    key = GenKeySH(567).gen_sym_key()
    password = "Hello World !!"
    check_decrypt_encrypt_sym(key, password)


def test_gen_key_encrypt_decrypt_asym():
    """
    Test to generate asymetric keys and to load it.
    """
    key_gen = GenKeySH()

    priv_key, public_key = key_gen.gen_asym_key()

    # Loading keys directly
    crypt = AsymCryptSH()

    crypt.add_key(priv_key)
    crypt.add_key(public_key)


def test_gen_key_encrypt_decrypt_asym_with_sotred_keys():
    """
    Test to generate asymetric keys and to load it from file.
    """
    key_gen = GenKeySH(23)

    priv_key, public_key = key_gen.gen_asym_key(path_store="trash/my_keys")

    # Loading keys from file
    crypt = AsymCryptSH()

    crypt.add_key("trash/my_keys")
    crypt.add_key("trash/my_keys.pubkey")


def test_with_stored_key():
    """
    Test store generated key in text file.
    """
    GenKeySH(567).gen_sym_key(path_store="trash/key.txt")

    with open("trash/key.txt", "r") as fr:
        key = fr.read().strip()

    password = "Hello World !!"
    check_decrypt_encrypt_sym(key, password)


def test_generate_same_key_with_same_seed():
    """
    Test that with the same seed we will generate the same key
    """
    seed = rnd.randint(1, 1e12)
    assert GenKeySH(seed).gen_sym_key() == GenKeySH(seed).gen_sym_key()


def test_with_stored_key_only_file():
    """
    Test store generated key in text file.
    """
    GenKeySH(567).gen_sym_key(path_store="key.txt")

    with open("key.txt", "r") as fr:
        key = fr.read().strip()

    password = "Hello World !!"
    check_decrypt_encrypt_sym(key, password)

    os.system("rm -rf key.txt")


def test_raise_error():
    with pytest.raises(GenKeySHException, match=r"AES key must be either.*"):
        GenKeySH().gen_sym_key(nb_bytes=17)

    with pytest.raises(GenKeySHException, match=r"path to store the key is invalid.*"):
        GenKeySH().gen_sym_key(path_store="tututu/zerze")

    with pytest.raises(GenKeySHException, match=r"nb_bytes must be at least 512-bits"):
        GenKeySH().gen_asym_key(nb_bytes=17)
