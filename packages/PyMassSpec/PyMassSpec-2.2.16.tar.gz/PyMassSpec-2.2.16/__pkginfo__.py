# Copyright (C) 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This script based on https://github.com/rocky/python-uncompyle6/blob/master/__pkginfo__.py

import pathlib

copyright = """
2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
"""

VERSION = "2.2.16"

modname = "pyms"
py_modules = None
entry_points = None


license = 'GPL2'

short_desc = 'Python Toolkit for Mass Spectrometry'

author = "Dominic Davis-Foster"
author_email = "dominic@davis-foster.co.uk"
github_username = "domdfcoding"
web = github_url = f"https://github.com/{github_username}/PyMassSpec"

# Original Author Sean O'Callaghan <spoc@unimelb.edu.au>,

# Get info from files; set: long_description
if pathlib.Path.cwd().name == "doc-source":
	print(pathlib.Path.cwd().parent / "README.rst")
	install_requires = (pathlib.Path.cwd().parent / "requirements.txt").read_text().split("\n")
	long_description = (pathlib.Path.cwd().parent / "README.rst").read_text() + '\n'
else:
	print(pathlib.Path("README.rst"))
	install_requires = pathlib.Path("requirements.txt").read_text().split("\n")
	long_description = pathlib.Path("README.rst").read_text() + '\n'

long_description = long_description.replace(":ref:`here <pyms-demo>`.", "`here <pyms_demo_>`__.")
long_description = long_description.replace(":ref:`here <pyms-demo/data-files>`.", "`here <datafiles_>`__.")
long_description = long_description.replace(":ref:`Demos and Examples <pyms-demo>`",
											"`Demos and Examples <pyms_demo_>`__")
long_description = long_description.replace(":ref:`pyms-demo/20a/`", "`pyms-demo/20a/`")
long_description += """

.. _pyms_demo: https://pymassspec.readthedocs.io/en/master/pyms-demo/introduction.html#pyms-demo
.. _datafiles: https://pymassspec.readthedocs.io/en/master/pyms-demo/data-files.html

"""

classifiers = [
		# "Development Status :: 4 - Beta",
		"Development Status :: 5 - Production/Stable",
		# "Development Status :: 6 - Mature",
		# "Development Status :: 7 - Inactive",
		
		"Operating System :: OS Independent",
		
		"Intended Audience :: Developers",
		"Intended Audience :: Education",
		"Intended Audience :: End Users/Desktop",
		"Intended Audience :: Science/Research",
		
		"License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
		
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: Implementation :: CPython",
		
		"Topic :: Education",
		"Topic :: Scientific/Engineering :: Bio-Informatics",
		"Topic :: Scientific/Engineering :: Chemistry",
		"Topic :: Software Development :: Libraries :: Python Modules",
		]
