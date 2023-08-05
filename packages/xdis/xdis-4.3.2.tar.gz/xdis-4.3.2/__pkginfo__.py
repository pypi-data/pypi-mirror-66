"""xdis packaging information"""

# To the extent possible we make this file look more like a
# configuration file rather than code like setup.py. I find putting
# configuration stuff in the middle of a function call in setup.py,
# which for example requires commas in between parameters, is a little
# less elegant than having it here with reduced code, albeit there
# still is some room for improvement.

# Things that change more often go here.
copyright = """
Copyright (C) 2015-2020 Rocky Bernstein <rb@dustyfeet.com>.
"""

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.4",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Topic :: Software Development :: Debuggers",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

_six = "six >= 1.10.0"

# The rest in alphabetic order
author = "Rocky Bernstein, Hartmut Goebel and others"
author_email = "rb@dustyfeet.com"
entry_points = {"console_scripts": ["pydisasm=xdis.bin.pydisasm:main"]}
ftp_url = None
install_requires = [_six, "click"]
license = "GPL-2.0"
mailing_list = "python-debugger@googlegroups.com"
modname = "xdis"
py_modules = None
# setup_requires     = ['pytest-runner']
scripts = ["bin/pydisasm.py"]
short_desc = "Python cross-version byte-code disassembler and marshal routines"
tests_require = ["pytest", _six]
web = "https://github.com/rocky/python-xdis/"

# tracebacks in zip files are funky and not debuggable
zip_safe = True

import os.path


def get_srcdir():
    filename = os.path.normcase(os.path.dirname(os.path.abspath(__file__)))
    return os.path.realpath(filename)


srcdir = get_srcdir()


def read(*rnames):
    return open(os.path.join(srcdir, *rnames)).read()


# Get info from files; set: long_description and VERSION
long_description = read("README.rst") + "\n"
exec(read("xdis/version.py"))
