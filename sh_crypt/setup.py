# -*- coding:utf-8 -*-
###
#    Author:         Steven HELLEC
#    Creation Date:  Friday, August 26th 2022, 8:17:47 pm
###

from setuptools import setup, find_packages
import sh_crypt

setup(
    name='sh-crypt',
    version=sh_crypt.__version__,
    description='Simple symmetric GPG file encryption and decryption',
    long_description=(docs_read('README.rst')),
    url='https://github.com/chrissimpkins/crypto',
    license='MIT license',
    author='Christopher Simpkins',
    author_email='git.simpkins@gmail.com',
    platforms=['any'],
    entry_points={
        'console_scripts': ['crypto = crypto.app:main', 'decrypto = crypto.decryptoapp:main'],
    },
    packages=find_packages("lib"),
    package_dir={'': 'lib'},
    install_requires=['Naked', 'shellescape'],
    keywords=
    'encryption,decryption,gpg,pgp,openpgp,cipher,AES256,crypto,cryptography,security,privacy',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: End Users/Desktop', 'Topic :: Security :: Cryptography',
        'Topic :: Security', 'Development Status :: 5 - Production/Stable',
        'Natural Language :: English', 'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X', 'Operating System :: POSIX',
        'Operating System :: Unix', 'Programming Language :: Python',
        'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3'
    ],
)