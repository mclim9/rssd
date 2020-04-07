### Reference: https://github.com/Terrabits/rohdeschwarz/blob/master/setup.py
### Reference: https://python-packaging.readthedocs.io/en/latest/minimal.html
###
### python setup.py register #Reserve name in pypi
### python setup.py --help-commands #Help
### python setup.py bdist           #Creates <pkg>.zip
### python setup.py install         #Installs package
### python setup.py install_scripts
### pip install .                   #Installs package in directory
### pip install -e .                #Install editable package
##########################################################
### Upload to PyPi
### python setup.py sdist           #Creates <pkg>.tar.gz
### twine upload .\dist\rssd-0.1.8.tar.gz 

import os
from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(name='rssd',
    version='2020.04.0',
    description='Rohde & Schwarz SCPI Driver',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',      #3:Alpha 4:Beta 5:Production/Stable
        'License :: Freely Distributable',
        'License :: Other/Proprietary License',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
        'Topic :: System :: Hardware :: Hardware Drivers',
    ],
    keywords='Rohde Schwarz test equipment FSW FSV NRP NRQ OSP SGT SMA SMB SMBV SMW SCPI VSA VSG VST',
    url='https://github.com/mclim9/rssd',
    author='Martin Lim',
    author_email='martin.lim@rsa.rohde-schwarz.com',
    license='R&S Terms and Conditions for Royalty-Free Products',
    packages=find_packages(exclude=['test','proto']),
    #packages=['rssd'],
    install_requires=[
        'pyvisa>=1.9.0',
        'future_fstrings>=1.0.0',
    ],
    test_suite = 'test',
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
          'rssd=rssd.bin.cli:main'
        ],
    },
)