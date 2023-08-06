# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, '', 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='BatchAdapt',
    version='1.1',
    python_requires='>3.7',
    description='Dynamic multi-loci/multi-repeat tract microsatellite reference sequence generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/helloabunai/Batchadapt',
    author='Alastair Maxwell/University of Glasgow',
    author_email='alastair.maxwell@glasgow.ac.uk',
    license='GPLv3',
    keywords='XML FASTA Genetic-references Bioinformatics Data-analysis',
    packages=find_packages(exclude=['input',
									'lib',
									'batchadapt.egg-info',
									'build',
									'dist',
									'logs'
									]),
    classifiers=[
		'Development Status :: 2 - Pre-Alpha',

		# Indicate who your project is intended for
		'Intended Audience :: Education',
		'Intended Audience :: End Users/Desktop',
		'Intended Audience :: Science/Research',

		# Classifier matching license flag from above
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

		# Specific version of the python interpreter that are supported
		# by this package. Python 3 not support at this time.
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',

		## And so on
		'Environment :: Console',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: POSIX'
	],
    install_requires=['progressbar2'],
    entry_points={
        'console_scripts': ['batchadapt=batchadapt.batchadapt:main',],
    },
)
