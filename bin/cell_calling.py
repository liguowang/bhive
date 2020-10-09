#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Call cells from background.
First, calculates the "read count" and "UMI count" for each barcode (i.e. cell
barcode),and generates the barcode rank plot and density plot. Then, using the
Bayesian Gaussian Mixture Model (BGMM) to classify barcodes into "cell-associated"
and "background-associated".

"""
import sys
import logging
from scat_module import mixmodel
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
	parser.add_option("-i","--infile",action="store",type="string", dest="in_file",help="Input file in BAM foramt.")
	parser.add_option("-o","--outfile",action="store",type="string", dest="out_file", help="The prefix of output files.")
	parser.add_option("--cb-tag",action="store",type="string", dest="CB_tag", default='CB', help="Tag of error-corrected cellular barcode in BAM file. default=\'%default\'")
	parser.add_option("--umi-tag",action="store",type="string", dest="UMI_tag", default='UB', help="Tag of error-corrected UMI in BAM file. default=\'%default\'")
	parser.add_option("--cb-num",action="store",type="int", dest="CB_limit", default=100000, help="Maximum cell barcodes (ranked by associated UMI frequency) analysed. default=%default")
	parser.add_option("--min-read-count",action="store",type="int", dest="min_reads",default=200, help="The minimum number of reads to filter out cell barcode. default=%default")
	parser.add_option("-r","--report",action="store_true",dest="report_summary",default=False, help="If set, generates report file for mixture models.  default=%default")
	parser.add_option("-s","--seed",action="store",type='int', dest="random_state",default=0, help="The seed used by the random number generator. default=%default")
	parser.add_option("--prob-cut",action="store",type='float', dest="probability_cutoff",default=0.5, help="The probabiilty cutoff [0.5, 1] to assign cell barcode to the \"cell\" or the \"background\" component. default=%default")
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
	if options.probability_cutoff < 0.5 or  options.probability_cutoff >1:
		logging.error ("The probability cutoff must within in [0.5, 1]")
		parser.print_help()
		sys.exit(0)
	scbam.CBC_UMIcount(infile = options.in_file,  outfile = options.out_file, CB_tag = options.CB_tag, UMI_tag = options.UMI_tag, CB_num = options.CB_limit, read_num = options.min_reads)



	#outfile + ".Read_UMI_freq.tsv"
	logging.info ("Read %s to build Bayesian Gaussian Mixture Model (BGMM)..." % (options.out_file + ".Read_UMI_freq.tsv"))
	dat = mixmodel.load_data(options.out_file + ".Read_UMI_freq.tsv")

	#step2: build BGMM models
	logging.info ("Build BGMM ...")
	GMMs = mixmodel.build_GMM(dat, rnd = options.random_state)

	#step3: Summerize BGMM models
	if options.report_summary:
		logging.info ("Summerzie the BGMM models ...")
		mixmodel.summary_GMM(GMMs, outfile = (options.out_file + '.BGMM_report.txt'))

	#step4: Classification
	logging.info ("Classify cell barcode using the BGMM models ...")
	mixmodel.dichotmize(dat, GMMs, outfile = options.out_file, prob_cutoff = options.probability_cutoff)


	ROUT = open(options.out_file + '.Read_UMI_freq.r','w')
	logging.info ("Writing R script to \"%s\"" % (options.out_file + '.Read_UMI_freq.r'))

	print (r"if(!require(ggplot2)){install.packages('ggplot2')}" , file=ROUT)
	print (r"if(!require(cowplot)){install.packages('cowplot')}" , file=ROUT)
	print (r"library(ggplot2)" , file=ROUT)
	print (r"library(cowplot)" , file=ROUT)
	print ('\n', file=ROUT)
	## read plot
	print ('read_dat <- read.table(file=\"%s\",header=T,sep=\"\\t\")' % (options.out_file + ".Read_count_classification.txt"), file=ROUT)
	print (r'read_dat <-  read_dat[order(read_dat$log10_count, decreasing=TRUE),]', file=ROUT)
	print (r'cell_num <- sum(read_dat$Assigned_lable=="cell")', file=ROUT)

	print (r'x1 <- 1:length(read_dat$log10_count)', file = ROUT)
	print ('\n', file=ROUT)
	print (r'A = ggplot(read_dat, aes(log10_count, fill=Assigned_lable, colour=Assigned_lable)) + geom_histogram(aes(y=..density..), alpha=0.6, position="identity", lwd=0.2, bins=50)  + xlab("Log10(read count)") + ylab("Cell barcode density") + geom_density(alpha=.2) + ggtitle(paste(c("Density plot,", cell_num, "cells"), collapse = " ")) + theme(legend.position=c(0.75, 0.75))', file=ROUT)
	print (r'B = ggplot(read_dat, aes(x=x1,y=log10_count)) + geom_point(aes(color = Assigned_lable), size=0.5) + xlab("Index of cell barcode") + ylab("Log10(read count)") + ggtitle(paste(c("Barcode rank plot,", cell_num, "cells"), collapse = " ")) + theme(legend.position=c(0.75, 0.75))', file=ROUT)
	print (r'C = ggplot(read_dat, aes(x=cell_prob,y=log10_count)) + geom_point(aes(color = Assigned_lable), size=0.5) + xlab("Probability") +  ylab("Log10(read count)") + ggtitle(paste(c("Probability rank plot,", cell_num, "cells"), collapse = " ")) + theme(legend.position="None")', file=ROUT)

	#UMI plot
	print ('\n', file=ROUT)
	print ('umi_dat <- read.table(file=\"%s\",header=T,sep=\"\\t\")' % (options.out_file + ".UMI_count_classification.txt"), file=ROUT)
	print (r'umi_dat <-  umi_dat[order(umi_dat$log10_count, decreasing=TRUE),]', file=ROUT)
	print (r'cell_num <- sum(umi_dat$Assigned_lable=="cell")', file=ROUT)

	print (r'x2 <- 1:length(umi_dat$log10_count)', file = ROUT)
	print ('\n', file=ROUT)
	print (r'D = ggplot(umi_dat, aes(log10_count, fill=Assigned_lable, colour=Assigned_lable)) + geom_histogram(aes(y=..density..), alpha=0.6, position="identity", lwd=0.2, bins=50)  + xlab("Log10(UMI count)") + ylab("Cell barcode density") + geom_density(alpha=.2) + ggtitle(paste(c("Density plot,", cell_num, "cells"), collapse = " ")) + theme(legend.position="None")', file=ROUT)
	print (r'E = ggplot(umi_dat, aes(x = x2, y = log10_count)) + geom_point(aes(color = Assigned_lable), size=0.5) + xlab("Index of cell barcode") + ylab("Log10(UMI count)") + ggtitle(paste(c("Barcode rank plot,", cell_num, "cells"), collapse = " ")) + theme(legend.position="None")', file=ROUT)
	print (r'F = ggplot(umi_dat, aes(x = cell_prob, y = log10_count)) + geom_point(aes(color = Assigned_lable), size=0.5) + xlab("Probability") +  ylab("Log10(UMI count)") + ggtitle(paste(c("Probability rank plot,", cell_num, "cells"), collapse = " ")) + theme(legend.position="None")', file=ROUT)
	print ('\n', file=ROUT)

	print ("pdf(\'%s\', height=8, width=10)" %  (options.out_file + '.Read_UMI_freq.pdf'), file=ROUT)
	print (r'plot_grid(A, B, C,D,E,F, labels = "AUTO")', file=ROUT)
	print (r'dev.off()', file=ROUT)



	ROUT.close()


if __name__=='__main__':
	main()
