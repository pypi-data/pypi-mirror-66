from setuptools import setup

with open("README.rst", "r") as fh:
	long_description = fh.read()

setup(
		name="domdf_spreadsheet_tools",
		version="0.1.4",
		author='Dominic Davis-Foster',
		author_email="dominic@davis-foster.co.uk",
		py_modules=["domdf_spreadsheet_tools"],
		url="https://github.com/domdfcoding/domdf_spreadsheet_tools",
		description='Tools for creating and formatting spreadsheets with Python and OpenPyXL',
		long_description=long_description,
		long_description_content_type="text/markdown",
		classifiers=[
				"Programming Language :: Python :: 3.6",
				"Programming Language :: Python :: 3.7",
				"Programming Language :: Python :: 3.8",
				"License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
				"Operating System :: OS Independent",
				"Development Status :: 4 - Beta",
				],
		install_requires=[
				"openpyxl >= 2.6.0",
				"domdf_python_tools >= 0.1.5"
				],
		)
