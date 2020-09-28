import sys, os, platform, glob
from distutils.core import setup
from setuptools import *

"""
Setup script for bhive  -- python package for single cell RNA-seq data analysis
"""

def main():
	setup(  name = "bhive",
			version = "1.0.0",
			py_modules = [ 'psyco_full' ],
			python_requires='>=3.5',
			packages = find_packages( 'lib' ),
			package_dir = { '': 'lib' },
			package_data = { '': ['*.ps'] },
			scripts = glob.glob( "bin/*.py"),
			ext_modules = [],
			test_suite = 'nose.collector',
			setup_requires = ['nose>=0.10.4'],
			author = "Liguo Wang",
			author_email ="wangliguo78@gmail.com",
			platforms = ['Linux','MacOS'],
			requires = ['cython (>=0.17)'],
			install_requires = ['numpy','pysam', 'pandas', 'sklearn','logomaker','matplotlib'], 
			description = "SCAT (Single Cell data Analysis Tool)",
			long_description = "Single Cell data Analysis Tool",
			license='MIT License',
			url = "",
			zip_safe = False,
			dependency_links = [],
			classifiers=[
				'Development Status :: 5 - Production/Stable',
				'Environment :: Console',
				'Intended Audience :: Science/Research',
				'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
				'Operating System :: MacOS :: MacOS X',
				'Operating System :: POSIX',
				'Programming Language :: Python',
				'Topic :: Scientific/Engineering :: Bio-Informatics',
			],
			
			keywords='bhive, single cell RNA-seq, scRNA-seq, QC, analysis, visualization',
             )


if __name__ == "__main__":
	main()
