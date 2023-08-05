#!/usr/bin/env python
"""Setup script"""

from __pkginfo__ import (
	author, author_email,  # install_requires,
	license, long_description, classifiers,
	entry_points, modname, py_modules,
	short_desc, VERSION, web, data_files
	)

from setuptools import setup


# Create .desktop file
with open("wxIconSaver.desktop", "w") as desktop:
	desktop.write(f"""[Desktop Entry]
Version={VERSION}
Name={modname}
Comment=A GUI utility for saving wxPython icons to files
Exec=wxIconSaver
Icon=document-save
Terminal=false
Type=Application
Categories=Utility;Application;
""")


setup(
		author=author,
		author_email=author_email,
		classifiers=classifiers,
		description=short_desc,
		entry_points=entry_points,
		# install_requires=install_requires,
		license=license,
		long_description=long_description,
		name=modname,
		# packages           = find_packages(),
		py_modules=py_modules,
		url=web,
		version=VERSION,
		data_files=data_files,
		)
