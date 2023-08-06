from setuptools import setup
from setuptools import find_packages

setup(name='distributions_mwi',
      version='0.1',
      description='Gaussian and binomial distributions',
      packages=['distributions_mwi'],
      install_requires=find_packages(),
      author='Marcus Winter',
      author_email='marcus.winter.privat@gmail.com',
      url='https://github.com/mwinterde/Putting-Code-On-PiPy',
      zip_safe=False)