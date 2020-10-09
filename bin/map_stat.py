#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Report reads mapping statistics.
Example output:

 Total_alignments: 589060389
 └--Confident_alignments: 443330914

 Total_mapped_reads:     589060389
 |--Non_confidently_mapped_reads:        145729475       (24.74%)
 └--Confidently_mapped_reads:    443330914       (75.26%)
    |--PCR duplicate reads:      327447641       (73.86%)
    └--Non PCR duplicate reads:  115883273       (26.14%)

    |--Forward reads:    259474203       (58.53%)
    └--Reverse reads:    183856711       (41.47%)

    |--Reads with Error-Corrected cell barcode:  437707874       (98.73%)
    └--Reads without Error-Corrected cell barcode:       5623040 (1.27%)

    |--Reads with Error-Corrected UMI:   443184634       (99.97%)
    └--Reads without Error-Corrected UMI:        146280  (0.03%)

    |--Map_consecutively:        242755968       (54.76%)
    |--Map_with_clipping:        49473035        (11.16%)
    |--Map_with_splicing:        115086767       (25.96%)
    |--Map_with_splicing_and_clipping:   19346122        (4.36%)
    └--Others:   16669022        (3.76%)

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
	usage = __doc__
	parser = OptionParser(usage,version="%prog " + __version__)
	parser.add_option("-i","--infile",action="store",type="string", dest="bam_file",help="Input file in BAM foramt. Must have BAM alignment tags indicated below. ")
	parser.add_option("--cb-tag",action="store",type="string", dest="CB_tag", default='CB', help="BAM alignment tag. Used to indicate error-corrected cellular barcode. default=\'%default\'")
	parser.add_option("--re-tag",action="store",type="string", dest="RE_tag", default='RE', help="BAM alignment tag. Used to indicate the region type of the alignment (E = exonic, N = intronic, I = intergenic). default=\'%default\'")
	parser.add_option("--tx-tag",action="store",type="string", dest="TX_tag", default='TX', help="BAM alignment tag. Used to indicate reads aligned to the same strand as the annotated transcripts. default=\'%default\'")
	parser.add_option("--an-tag",action="store",type="string", dest="AN_tag", default='AN', help="BAM alignment tag. Used to indicate reads aligned to the antisense strand of the annotated transcripts. default=\'%default\'")
	parser.add_option("--umi-tag",action="store",type="string", dest="UMI_tag", default='UB', help="BAM alignment tag. Used to indicat the error-corrected UMI. default=\'%default\'")
	parser.add_option("--xf-tag",action="store",type="string", dest="xf_tag", default='xf', help="BAM alignment tag. Used to indicate reads confidently mapped to the feature. default=\'%default\'")
	parser.add_option("--verbose",action="store_true",dest="debug",default=False,help="Logical to determine if detailed running information is printed to screen.")

	(options,args)=parser.parse_args()
	if options.debug:
		logging.basicConfig(format = "%(asctime)s [%(levelname)s]  %(message)s",datefmt='%Y-%m-%d %I:%M:%S', level=logging.DEBUG)
	else:
		logging.basicConfig(format = "%(asctime)s [%(levelname)s]  %(message)s",datefmt='%Y-%m-%d %I:%M:%S', level=logging.INFO)

	for file in ([options.bam_file]):
		if not (file):
			parser.print_help()
			sys.exit(0)

	scbam.mapping_stat(infile = options.bam_file, CB_tag = options.CB_tag, UMI_tag = options.UMI_tag, xf_tag = options.xf_tag, RE_tag = options.RE_tag, TX_tag = options.TX_tag, AN_tag = options.AN_tag)
	logging.info ("Done.")

if __name__=='__main__':
	main()