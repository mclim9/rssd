""" 
Reference: https://github.com/Terrabits/rohdeschwarz/blob/master/setup.py

python setup.py --help-commands
python setup.py bdist    #Creates
python setup.py sdist    #Creates tar.gz

"""

import os
from setuptools import setup, find_packages

def readme():
    with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
        return f.read()

setup(name='rssd',
      version='0.1',
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
      url='https://bitbucket.org/mclim/rs_ate_python2',
      author='Martin Lim',
      author_email='martin.lim@rsa.rohde-schwarz.com',
      license='R&S Terms and Conditions for Royalty-Free Products',
      packages=find_packages(exclude=['test']),
      install_requires=[
          'pyvisa',
      ],
      include_package_data=True,
      zip_safe=False)
