#!/usr/bin/env python3

from distutils.core import setup


################################################################################
# Git version
try:
	import subprocess
	rv = subprocess.check_output(["git", "describe", "--always", "--dirty", "--long", "--tags"]).strip().decode()
except Exception:
	rv = "v0.0.0"

if "dirty" in rv:
	print("Repository is dirty... Try to clean it!")
	exit(0)

label = rv.split("-")
majorDotMinor = label[0]
build = label[1]
version = majorDotMinor + "." + build

################################################################################
# Long description
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


################################################################################
# Setup config
setup(
	name = 'virtualbus',
	packages = ['virtualbus'],
	version = version,
	license='MIT',
	description = 'Virtual bus',
	long_description = long_description,
	author = 'Kanelis Elias',
	author_email = 'hkanelhs@yahoo.gr',
	url = 'https://github.com/tedicreations/virtualbus',
	download_url = 'https://github.com/TediCreations/virtualbus/archive/' + str(majorDotMinor) + '.tar.gz',
	keywords = ['virtual', 'bus', 'socket', 'networking'],
	#install_requires=[],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
	],
)
