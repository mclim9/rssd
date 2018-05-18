""" 
### Reference: https://github.com/Terrabits/rohdeschwarz/blob/master/setup.py
### Reference: https://python-packaging.readthedocs.io/en/latest/minimal.html
### 
### python setup.py --help-commands
### python setup.py sdist    #Creates tar.gz| bdist for zip
### python setup.py install  #Installs package
### pip install .            #Installs package
###
##########################################################
### Upload to PyPi
### python setup.py register #Reserve name in pypi
### python setup.py sdist    #Creates tar.gz
### python setup.py upload   #Twine? 
### twine upload 
"""
import os
from setuptools import setup, find_packages

def readme():
    with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
        return f.read()

setup(name='rssd',
      version='0.1.1',
      description='Rohde & Schwarz SCPI Driver',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',      #3:Alpha 4:Beta 5:Production/Stable
        'License :: Other/Proprietary License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
        'Topic :: System :: Hardware :: Hardware Drivers',
      ],
      keywords='Rohde Schwarz FSW SMW SCPI test equipment VSA VGA',
      url='https://bitbucket.org/mclim/RS_SCPI_Driver',
      author='Martin Lim',
      author_email='martin.lim@rsa.rohde-schwarz.com',
      license='R&S Terms and Conditions for Royalty-Free Products',
      packages=find_packages(exclude=['test']),
      #packages=['rssd'],
      install_requires=[
          'pyvisa>=1.9.0',
      ],
      test_suite = 'test',
      include_package_data=True,
      zip_safe=False)
