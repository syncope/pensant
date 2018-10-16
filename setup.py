from setuptools import setup, find_packages

from codecs import open
from os import path

with open(path.join('.', 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

name='pensant'
version='0'
release='0.0.5'

setup(
    name='pensant',
    version='0.0.5',

    description='Library to simplify handling parameter estimation, also providing GUI elements within pyqt.', 
    long_description=long_description,

    url='https://github.com/syncope/pensant',

    author='Ch.Rosemann',
    author_email='christoph.rosemann@desy.de',
    
    license='GPLv2',
    
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='pensant parameter estimation lmfit',
    
    packages=['pensant'],
    
    package_dir = { 'pensant':'pensant',},
    include_package_data=True,
    
)

