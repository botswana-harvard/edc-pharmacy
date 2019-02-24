import os
from setuptools import find_packages
from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as f:
    VERSION = f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='edc-pharmacy',
    version=VERSION,
    author='Tshepiso Setsiba',
    maintainer='Erik van Widenfelt',
    author_email='ew2789@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='http://github.com/clinicedc/edc-pharmacy',
    license='GPL license, see LICENSE',
    description='Pharmacy module for clinicedc/edc projects',
    long_description=README,
    zip_safe=False,
    keywords='edc edc-pharmacy',
    install_requires=[
        'edc-base',
        'edc-appointment',
        'edc-label',
        'edc-model-admin',
        'edc-search',
        'holidays'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
