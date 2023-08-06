import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()


setuptools.setup(name='deep_genome',
	version='0.1.1',
	description='Synthetic Protein Generation',
	url='https://github.com/nitinnairk/deep_genome',
	long_description=long_description,
	long_description_content_type="text/markdown",
	author='Nitin Nair',
	author_email='nitinnair@vt.edu',
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
		"Operating System :: Unix",
	],
	python_requires='>=3.6',
	zip_safe=False)