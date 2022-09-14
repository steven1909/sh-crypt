# -*- coding:utf-8 -*-
###
#    Author:         Steven HELLEC
#    Creation Date:  Thursday, August 25th 2022, 7:22:53 pm
###

from . import *


class CryptSHException(Exception):

    def __init__(self, raison):
        self.raison = raison

    def __str__(self):
        return self.raison


class SymCryptSH:
    """
    Class to encrypt and decrypt with symetric key strings.
    """

    def __init__(self, key):
        """
        Setting of object attributes.
        """
        if not isinstance(key, str):
            raise CryptSHException(f"key must be string : {type(key)}")

        if not all(c in string.hexdigits for c in key):
            raise CryptSHException(f"Non-hexadecimal number found in key : {key}")

        key = bytes.fromhex(key)

        if len(key) not in [16, 24, 32]:
            raise CryptSHException(f"key must have len equal to 16, 24 or 32 : {len(key)}")

        self.cipher = Cipher(algorithms.AES(key), modes.ECB())
        self.padder = sym_padding.PKCS7(algorithms.AES(key).block_size)

    def encrypt_message(self, message):
        """
        Description :
        -----------
        Encrypt the provided message.

        Parameters :
        -----------
            - message (str) : String to encrypt.
            - key (str) : Encrypted key.

        Returns :
        ----------
            - _ (str) : Encrypted message.
        """
        if not isinstance(message, str):
            raise CryptSHException(f"message must be string : {type(message)}")

        message_bytes = self.__pad(bytes(message, encoding="utf8"))
        return binascii.hexlify(self.cipher.encryptor().update(message_bytes)).decode("utf8")

    def decrypt_message(self, message_encrypt):
        """
        Description :
        -----------
        Decrypt an encrypted message with a provided key

        Parameters :
        -----------
            - message_encrypt (str) : Encrypted string.
            - key (str) : Decrypting key.

        Returns :
        ----------
            - _ (str) : String decrypted.
        """
        if not isinstance(message_encrypt, str):
            raise CryptSHException(f"message_encrypt must be string : {type(message_encrypt)}")

        enc = bytes.fromhex(message_encrypt)
        return self.__unpad(self.cipher.decryptor().update(enc)).decode("utf8")

    def __unpad(self, s):
        """
        Description :
        -----------
        Unpad string to match with the len size of AES.

        Parameters :
        -----------
            - s (bytes) : Sequence of blocs.

        Returns :
        ----------
            - _ (str) : list of characters.
        """
        unpadder = self.padder.unpadder()
        return unpadder.update(s) + unpadder.finalize()

    def __pad(self, s):
        """
        Description :
        -----------
        Transforms a sequence of bytes into a multiple of blocks of the useful size for AES

        Parameters :
        -----------
            - s (str) : List of bytes.
        Returns :
        ----------
            - _ (bytes) : Sequence of blocs.
        """
        padder = self.padder.padder()
        return padder.update(s) + padder.finalize()


class AsymCryptSH:

    def __init__(self):
        self.dct_keys = {}

    def add_key(self, key_or_path, password=None):

        key_type, key = self.__read_key(key_or_path, password)

        self.dct_keys[key_type] = key
        logging.info(f"Add a {key_type} key")

        if "private" in self.dct_keys and "public" in self.dct_keys:
            self.__check_compatibility_private_public_key()

    def __check_compatibility_private_public_key(self):
        text_test = "Hello World !!!"

        text_test_encrypt = self.encrypt_message(text_test)

        try:
            self.decrypt_message(text_test_encrypt)
        except Exception:
            raise CryptSHException("Public key is not compatible with private key.")

    def __read_key(self, key_or_path, password):
        if key_or_path is None:
            raise CryptSHException("key_or_path cannot be None")

        if os.path.exists(key_or_path):
            with open(key_or_path) as fr:
                key_str = fr.read()
        else:
            key_str = key_or_path

        try:
            if "-----BEGIN PRIVATE KEY-----" in key_str:
                key_type = "private"
                key_serialized = serialization.load_pem_private_key(key_str.encode("utf8"),
                                                                    password=password)
            elif "-----BEGIN PUBLIC KEY-----" in key_str:
                key_type = "public"
                key_serialized = serialization.load_pem_public_key(key_str.encode("utf8"))
            else:
                raise CryptSHException("Your key is not in pem format")
        except Exception:
            raise CryptSHException("Your key is not in pem format")

        return key_type, key_serialized

    def encrypt_message(self, message):

        if isinstance(message, str):
            message = bytes(message, encoding="utf8")

        return binascii.hexlify(self.dct_keys["public"].encrypt(
            message,
            asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                              algorithm=hashes.SHA256(),
                              label=None))).decode("utf8")

    def decrypt_message(self, message_enc):

        if isinstance(message_enc, str):
            message_enc = bytes.fromhex(message_enc)

        return self.dct_keys["private"].decrypt(
            message_enc,
            asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                              algorithm=hashes.SHA256(),
                              label=None)).decode("utf8")

    def sign_message(self, message):
        if isinstance(message, str):
            message = bytes(message, encoding="utf8")

        signature = self.dct_keys["private"].sign(
            message,
            asym_padding.PSS(mgf=asym_padding.MGF1(hashes.SHA256()),
                             salt_length=asym_padding.PSS.MAX_LENGTH), hashes.SHA256())

        return binascii.hexlify(signature).decode("utf8")

    def check_sign_message(self, signature, message):

        if isinstance(message, str):
            message = bytes(message, encoding="utf8")

        signature = bytes.fromhex(signature)
        try:
            self.dct_keys["public"].verify(
                signature, message,
                asym_padding.PSS(mgf=asym_padding.MGF1(hashes.SHA256()),
                                 salt_length=asym_padding.PSS.MAX_LENGTH), hashes.SHA256())
        except InvalidSignature:
            logging.warning("Your signature is invalid.")
            return False
        return True
