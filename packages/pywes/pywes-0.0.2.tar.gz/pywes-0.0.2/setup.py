from setuptools import setup
from setuptools import find_packages
from os import path
import os

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'file/README.md'),'r') as f:
    long_description = f.read()
files=os.listdir('bin/')
files=['bin/'+i for i in files]
files.remove('bin/__init__.py')
setup(name='pywes',version='0.0.2',description='carrier and trio analysis',long_description=long_description, url='https://github.com/N-damo/exomreport',
author="Li'an Lin",author_email='21620151153308@stu.xmu.edu.cn',license='GPL3', keywords='exom', 
include_package_data=True,packages=['bin'],scripts=files,classifiers=['License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'])
