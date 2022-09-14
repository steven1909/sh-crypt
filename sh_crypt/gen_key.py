# -*- coding:utf-8 -*-
###
#    Author:         Steven HELLEC
#    Creation Date:  Friday, August 26th 2022, 9:02:05 am
###

from . import *


class GenKeySHException(Exception):

    def __init__(self, raison):
        self.raison = raison

    def __str__(self):
        return self.raison


class GenKeySH:
    """
    Class to generate and store random encryption keys.
    """

    def __init__(self, seed=None):
        self.seed = seed

    @staticmethod
    def __check_store_path_validity(path_store):
        if path_store is not None:
            path, _ = os.path.split(path_store)
            if path != "":
                if not os.path.exists(path):
                    raise GenKeySHException(f"path to store the key is invalid : {path_store}")

    def gen_sym_key(self, nb_bytes=32, path_store=None):
        """
        Description :
        -----------
        Generate 16, 24 or 32 bytes key for encryption.
        
        Parameters :
        -----------     
            - nb_bytes (int) : (default : 32) Number of bytes of the keys.
            - path_store (str) : (default : None) Path to the text file which will contains the key.
                       
        Returns :
        ----------
            - key (str) : The key.
        """
        if nb_bytes not in [16, 24, 32]:
            raise GenKeySHException("AES key must be either 16, 24, or 32 bytes long")

        self.__check_store_path_validity(path_store)

        # Initialisation of the seed
        rnd.seed(self.seed)
        key = "".join([rnd.choice(string.hexdigits[:16]) for n in range(nb_bytes)])

        if path_store is not None:
            with open(path_store, "w") as fw:
                fw.writelines(key)

        return key

    def gen_asym_key(self, nb_bytes=2048, path_store=None):
        """
        Description :
        -----------
        Generate a key pair for encryption and decryption.
        
        Parameters :
        -----------     
            - nb_bytes (int) : (default : 2048) Number of bytes of the keys.
            - path_store (str) : (default : None) Path to the text file which will contains the 
                                private key. The public key will be written in a file ended with .pubkey
                       
        Returns :
        ----------
            - private_key_str (str) : The private key.
            - public_key_str (str) : The public key.        
        """

        if nb_bytes <= 512:
            raise GenKeySHException("nb_bytes must be at least 512-bits.")

        self.__check_store_path_validity(path_store)

        if self.seed is not None:
            logging.warn("The seed paramater won't be used here.")

        # Gen private key
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=nb_bytes)

        # Gen public key
        public_key = private_key.public_key()

        private_key_str = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()).decode("utf8")

        public_key_str = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo).decode("utf8")

        if path_store is not None:
            with open(path_store, "w") as fw:
                fw.writelines(private_key_str)

            with open(path_store + ".pubkey", "w") as fw:
                fw.writelines(public_key_str)

        return private_key_str, public_key_str