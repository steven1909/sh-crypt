# -*- coding:utf-8 -*-
###
#    Author:         Steven HELLEC
#    Creation Date:  Thursday, August 25th 2022, 7:23:21 pm
###

from . import *


def check_decrypt_encrypt_sym(key, message, encrypt_message=None):
    crypt = SymCryptSH(key)

    # Encrypt message
    if encrypt_message is None:
        encrypt_message = crypt.encrypt_message(message)

    # Decrypt message
    decrypted_message = crypt.decrypt_message(encrypt_message)

    assert message == decrypted_message


def check_decrypt_encrypt_asym(message,
                               encrypt_message=None,
                               public_key_provided=None,
                               add_key_none=False):

    key_gen = GenKeySH()

    priv_key, public_key = key_gen.gen_asym_key()

    if public_key_provided is not None:
        public_key = public_key_provided

    crypt = AsymCryptSH()

    crypt.add_key(priv_key)
    crypt.add_key(public_key)

    if add_key_none:
        crypt.add_key(None)

    # Encrypt / Decrypt Message
    encrypt_message = crypt.encrypt_message(message)

    assert message == crypt.decrypt_message(encrypt_message)


def check_sign(message):

    key_gen = GenKeySH()

    priv_key, public_key = key_gen.gen_asym_key()

    crypt = AsymCryptSH()

    crypt.add_key(priv_key)
    crypt.add_key(public_key)

    # Sign / Check signature with message
    signature = crypt.sign_message(message)

    assert crypt.check_sign_message(signature, message) is True

    assert crypt.check_sign_message(signature, message + "toto") is False


def test_encrypt_decrypt_sym():
    """
    Test if simple text can be encrypted and decrypted with the same key, and give the same value.
    """
    key = "f5e2d77631ce2d87180905881b1ca84b"
    message = "Hello World !!"

    check_decrypt_encrypt_sym(key, message)


def test_encrypt_decrypt_asym():
    """
    Test if simple text can be encrypted and decrypted with asymetric keys, and give the same value.
    """
    message = "Hello World !!"

    check_decrypt_encrypt_asym(message)


def test_check_sign():
    """
    Test if simple text can be signed and check the signature.
    """
    message = "Hello World !!"

    check_sign(message)


def test_raise_error_sym():
    with pytest.raises(CryptSHException, match=r"key must be string.*"):
        SymCryptSH(123)

    with pytest.raises(CryptSHException, match=r"Non-hexadecimal number found in key.*"):
        SymCryptSH("jklsd")

    with pytest.raises(CryptSHException, match=r"key must have len equal to 16, 24 or 32"):
        SymCryptSH("f5e2")

    with pytest.raises(CryptSHException, match=r"message must be string.*"):
        key = "f5e2d77631ce2d87180905881b1ca84b"
        message = 123
        check_decrypt_encrypt_sym(key, message)

    with pytest.raises(CryptSHException, match=r"message_encrypt must be string.*"):
        key = "f5e2d77631ce2d87180905881b1ca84b"
        message = "Hello World !!"
        check_decrypt_encrypt_sym(key, message, encrypt_message=12334)


def test_raise_error_asym():
    with pytest.raises(CryptSHException, match=r"Your key is not in pem format"):
        message = "Hello world !!!"
        public_key_provided = "FakE_Keys"
        check_decrypt_encrypt_asym(message, public_key_provided=public_key_provided)

    with pytest.raises(CryptSHException, match=r"Your key is not in pem format"):
        message = "Hello world !!!"
        public_key_provided = "-----BEGIN PRIVATE KEY-----FakE_Keys"
        check_decrypt_encrypt_asym(message, public_key_provided=public_key_provided)

    with pytest.raises(CryptSHException, match=r"Public key is not compatible with private key"):
        message = "Hello world !!!"
        public_key_provided = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAssPIa+LgHutWevLAbeen
BjnUSHWdctzF3IlqI1X5DChwsgfx6P7T/gmxa2mFtj+0RHKGKBM1vjxn+aQn/SQv
m1cHfgXn3v4yDpXMffb8bdBiG8efOJ6tI6Bsoqmp63/cf9Kq/bPf2Yfcell6bHuE
YrcyR4AKYfPDhXVprJQ7WcPmJWf2gV5owXZ1qa1gpOBmfrXyNsOZFui+xcllMWfJ
uPXpvIH2TbCAURMfO6b85grKRZUjRAui3AKxykH8giIJMeq12H623ll2ljJaJAes
YvMMreViokCo+zd1aATAK2qt3mGDHWYnt2e4zGHVmsDqZ645CRJegM8y5MAn5bL6
7QIDAQAB
-----END PUBLIC KEY-----
        """
        check_decrypt_encrypt_asym(message, public_key_provided=public_key_provided)

    with pytest.raises(CryptSHException, match=r"key_or_path cannot be None"):
        message = "Hello world !!!"
        check_decrypt_encrypt_asym(message, add_key_none=True)
