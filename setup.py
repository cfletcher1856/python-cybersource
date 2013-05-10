#!/usr/bin/env python
from distutils.core import setup
import cybersource

LONG_DESCRIPTION = open('README.md').read()

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

KEYWORDS = 'cybersource soap suds wrapper'

setup(name='cybersource',
      version=cybersource.VERSION,
      description='Cyber Source API wrapper.',
      long_description=LONG_DESCRIPTION,
      author='Colin Fletcher',
      author_email='cfletcher1856@gmail.com',
      url='https://github.com/cfletcher1856/python-cybersource/',
      download_url='http://pypi.python.org/pypi/cybersource/',
      packages=['cybersource'],
      package_dir={'cybersource': 'cybersource'},
      platforms=['Platform Independent'],
      license='BSD',
      classifiers=CLASSIFIERS,
      keywords=KEYWORDS,
      requires=['suds'],
      install_requires=['suds'],
)
