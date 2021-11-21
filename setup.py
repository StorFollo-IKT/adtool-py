import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

if not os.path.exists('VERSION'):
    version = '0'
else:
    with open('VERSION', 'r') as fp:
        version = fp.read().strip()
        version = version[1:]  # Remove v before version number

setup(
    name='adtools',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    license='GPL',
    description='A module to work with Active Directory from Python',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/StorFollo-IKT/django-stamdata3',
    author='Anders Birkenes',
    author_email='anders.birkenes@storfolloikt.no',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ], install_requires=['ldap3']
)
