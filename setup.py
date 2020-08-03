# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in excel_erpnext/__init__.py
from excel_erpnext import __version__ as version

setup(
	name='excel_erpnext',
	version=version,
	description='Extensions for Excel Technologies',
	author='Castlecraft Ecommerce Pvt. Ltd.',
	author_email='support@castlecraft.in',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
