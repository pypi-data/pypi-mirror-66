'''Setup.py'''

from distutils.core import setup
from setuptools import find_packages

setup(
    name='phantominator',
    version='0.6.4',
    author='Nicholas McKibben',
    author_email='nicholas.bgp@gmail.com',
    packages=find_packages(),
    scripts=[],
    url='https://github.com/mckib2/phantominator',
    license='GPLv3',
    description='Generate numerical phantoms.',
    long_description=open('README.rst').read(),
    install_requires=[
        "numpy>=1.18.0",
        "scipy>=1.4.1",
        "matplotlib>=3.0.0",
        "ssfp>=0.4.2",
    ],
    python_requires='>=3.5',
)
