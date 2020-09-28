#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1) mapping statistics
2) split reads into confidently mapped and non-confidently mapped, and save into seprate BAM files.
"""

import sys
import logging

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
__version__="1.0.0"
__maintainer__ = "Liguo Wang"
__email__ = "wangliguo78@gmail.com"
__status__ = "Production"


def main():
	usage = "\n%prog  [options]"
	parser = OptionParser(usage,version="%prog " + __version__)
	parser.add_option("-i","--infile",action="store",type="string", dest="in_file",help="Input file in BAM foramt.")
	parser.add_option("-o","--outfile",action="store",type="string", dest="out_file",default = None, help="Prefix of two output BAM files: \".confident_alignments.bam\" containing reads that were confidently mapped to transcriptome. \".non_confident_alignments.bam\" containing the remaining reads. default=%default (do not generate BAM files)")
	parser.add_option("--limit",action="store",type="int", dest="reads_num",default = None, help="Number of alignments to process. default=%default (process all alignments)")
	parser.add_option("--verbose",action="store_true",dest="debug",default=False,help="Logical to determine if detailed running information is printed to screen.")

	(options,args)=parser.parse_args()
	if options.debug:
		logging.basicConfig(format = "%(asctime)s [%(levelname)s]  %(message)s",datefmt='%Y-%m-%d %I:%M:%S', level=logging.DEBUG)
	else:
		logging.basicConfig(format = "%(asctime)s [%(levelname)s]  %(message)s",datefmt='%Y-%m-%d %I:%M:%S', level=logging.INFO)


	if not (options.in_file):
		parser.print_help()
		sys.exit(0)
	scbam.mapping_stat(infile = options.in_file,  outfile = options.out_file, limit = options.reads_num)
	logging.info ("Done.")

if __name__=='__main__':
	main()