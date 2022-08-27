# -*- coding:utf-8 -*-
###
#    Author:         Steven HELLEC
#    Creation Date:  Thursday, August 25th 2022, 7:23:21 pm
###

from . import *


def check_decrypt_encrypt(key, password, encrypt_password=None):
    crypt = CryptSH(key)

    # Encrypt password
    if encrypt_password is None:
        encrypt_password = crypt.encrypt_password(password)

    # Decrypt password
    decrypted_password = crypt.decrypt_password(encrypt_password)

    assert password == decrypted_password


def test_encrypt_decrypt():
    """
    Test if simple text can be encrypted and decrypted with the same key, and give the same value.
    """
    key = "f5e2d77631ce2d87180905881b1ca84b"
    password = "Hello World !!"

    check_decrypt_encrypt(key, password)


def test_raise_error():
    with pytest.raises(CryptSHException, match=r"key must be string.*"):
        CryptSH(123)

    with pytest.raises(CryptSHException, match=r"Non-hexadecimal number found in key.*"):
        CryptSH("jklsd")

    with pytest.raises(CryptSHException, match=r"key must have len equal to 16, 24 or 32"):
        CryptSH("f5e2")

    with pytest.raises(CryptSHException, match=r"password must be string.*"):
        key = "f5e2d77631ce2d87180905881b1ca84b"
        password = 123
        check_decrypt_encrypt(key, password)

    with pytest.raises(CryptSHException, match=r"password_encrypt must be string.*"):
        key = "f5e2d77631ce2d87180905881b1ca84b"
        password = "Hello World !!"
        check_decrypt_encrypt(key, password, encrypt_password=12334)
