from setuptools import setup

README = open("pypi_readme.md","r").read()
setup(
	name="nsmpy",
	version="1.0.2",
	long_description=README,
	long_description_content_type="text/markdown",
	author="SciencePi",
	license="MIT",
	scripts=['nsmpy.py'])
