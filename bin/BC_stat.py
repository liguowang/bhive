#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 14:54:42 2020

@author: m102324
"""

import sys
try:
	from scat_module import scbam
except:
	import scbam
	
from optparse import OptionParser

__author__ = "Liguo Wang"
__contributor__="Liguo Wang"
__copyright__ = "Copyright 2020, Mayo Clinic"
__credits__ = []
__license__ = "GPLv2"
__version__="3.0.0"
__maintainer__ = "Liguo Wang"
__email__ = "wangliguo78@gmail.com"
__status__ = "Production"

	
def main():
	usage = "\n%prog  [options]"
	parser = OptionParser(usage,version="%prog " + __version__)
	parser.add_option("-i","--infile",action="store",type="string", dest="in_file",help="Input file in BAM foramt.")
	parser.add_option("-o","--outfile",action="store",type="string", dest="out_file",help="The prefix of output files.")
	(options,args)=parser.parse_args()
	#print ("excludeN is set to:", options.exclude_N)
	for file in ([options.in_file, options.out_file]):
		if not (file):
			parser.print_help()
			sys.exit(0)
	
	scbam.barcode_stat(infile = options.in_file, outfile = options.out_file)	
if __name__=='__main__':
	main()	
	
