from setuptools import setup, find_packages
setup(
  name = 'datamotion_securemessaging',
  packages = find_packages(),
  version = '1.0.0',
  license= 'MIT',
  description = 'This is a Python Software Development Kit (SDK) for DataMotion SecureMail Messaging. This SDK is a wrapper providing helper functions for our Messaging RESTful APIs. This code is simple in nature, and is present to provide a complete yet basic implementation.',
  author = 'DataMotion Inc.',
  author_email = 'plmvas@datamotion.com',
  url = 'https://gitlab.com/datamotion/DMWeb/SecureMail/Python/Messaging/REST/Python-Messaging-Library',
  keywords = ['python', 'messaging', 'library', 'datamotion', 'securemail', 'rest', 'api', 'secure'],
  install_requires=['requests'],
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
  ],
)
