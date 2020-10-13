#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Do automatic K-means clustering.

"""
import sys
import logging
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from scat_module import scbam

from optparse import OptionParser

__author__ = "Liguo Wang"
__contributor__="Liguo Wang"
__copyright__ = "Copyright 2020, Mayo Clinic"
__credits__ = []
__license__ = "GPLv2"
__version__="1.0.0"
__maintainer__ = "Liguo Wang"
__email__ = "wangliguo78@gmail.com"
__status__ = "Development"



def main():
	usage= __doc__
	parser = OptionParser(usage,version="%prog " + __version__)
	parser.add_option("-i","--infile",action="store",type="string", dest="in_file",help="CSV file containing tSNE coordinates. ")
	parser.add_option("-o","--outfile",action="store",type="string", dest="out_file", help="The prefix of output files.")
	parser.add_option("--verbose",action="store_true",dest="debug",default=False,help="If set, print detailed information for debugging.")

	(options,args)=parser.parse_args()

	if options.debug:
		logging.basicConfig(format = "%(asctime)s [%(levelname)s]  %(message)s",datefmt='%Y-%m-%d %I:%M:%S', level=logging.DEBUG)
	else:
		logging.basicConfig(format = "%(asctime)s [%(levelname)s]  %(message)s",datefmt='%Y-%m-%d %I:%M:%S', level=logging.INFO)



	if not (options.in_file):
		parser.print_help()
		sys.exit(0)
	if not (options.out_file):
		parser.print_help()
		sys.exit(0)

	d =pd.read_csv('projection.csv',index_col=0)
