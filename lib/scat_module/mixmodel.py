import collections
import numpy as np
from sklearn import mixture
import logging
import pandas as pd

__author__ = "Liguo Wang"
__copyright__ = "Copyleft"
__credits__ = []
__license__ = "GPL"
__version__="1.0.7"
__maintainer__ = "Liguo Wang"
__email__ = "wang.liguo@mayo.edu"
__status__ = "Development"


def load_data(infile):
	"""
	Example of infile:
	Serial# Cell_barcode    read_count      UMI_count
	1       AACAACCCAGTTCTAG        484049  202124
	2       CTATCCGCATGGATCT        408462  184155
	3       AATCGTGTCTTTGATC        355937  165832
	4       CTTCTCTGTTGTCCCT        349352  159697
	"""
	UMI_freq_cut = 1
	read_freq_cut =1
	dat = {}
	logging.info("Reading input file: \"%s\"" % infile)
	for l in open(infile,'r'):
		l = l.strip()
		if l.startswith('Serial#'):
			continue
		f = l.split()
		read_freq = int(f[2])
		UMI_freq = int(f[3])
		if UMI_freq < UMI_freq_cut:continue
		if read_freq < read_freq_cut:continue
		try:
			dat[f[1]] = [np.log10(read_freq), np.log10(UMI_freq)]
		except:
			continue

	df1 = pd.DataFrame.from_dict(dat,orient='index',columns=['read_count', 'UMI_count'])
	df2 = df1.dropna(axis=0, how='any')
	logging.debug("%d rows with missing values were removed." % (len(df1) - len(df2)))

	#print ("\tTotal samples: %d" % (len(df2.columns)), file=sys.stderr)
	logging.info ("\tTotal analyzed barcodes: %d" % len(df2))
	return df2

def build_GMM(d,rnd):
	"""
	Return means of components of Gaussian Mixture Model.
	d is data frame returned by "load_data" function.
	rnd is a random number. You get exactly the same results when running multiple times using the same random number. Must be integer.
	"""

	bgmm_models = collections.defaultdict(list)
	for s_id in sorted(d.columns):
		logging.info ("Building Bayesian Gaussian Mixture model for subject: %s ...\r" % s_id)
		bgmm = mixture.BayesianGaussianMixture(n_components=2, covariance_type='full',max_iter=50000,tol=0.001,random_state=rnd)
		bgmm_models[s_id] = bgmm.fit(d[s_id].values.reshape(-1,1))
	#print (bgmm_models)
	return bgmm_models


def summary_GMM(m, outfile):
	"""
	Summarize BGMM models returned by "build_GMM"
	"""

	FOUT = open(outfile,'w')

	print ("\n\n#means of components", file=FOUT)
	print ("Subject_ID\tUMI_background\tUMI_valid",file=FOUT)
	for k,v in m.items():
		print (str(k) + '\t' + '\t'.join([str(i) for i in sorted(v.means_[:,0])]),file=FOUT)


	print ("\n\n#Weights of components", file=FOUT)
	print ("Subject_ID\tUMI_background\tUMI_valid",file=FOUT)
	for k,v in m.items():
		print (str(k) + '\t' + '\t'.join([str(i) for i in sorted(v.weights_)]), file=FOUT)


	print ("\n\n#Converge status and n_iter", file=FOUT)
	print ("Subject_ID\tConverged\tn_iter", file=FOUT)
	for k,v in m.items():
		print (str(k) + '\t' + '\t'.join([str(i) for i in (v.converged_, v.n_iter_)]), file=FOUT)
	FOUT.close()

	logging.info ("Reports were saved into \"%s\"" % outfile)

def dichotmize(d, m, outfile, prob_cutoff = 0.5):
	"""
	dichotmize cell barcode into "cells" and "background"
	d is data frame returned by "load_data" function
	m is BGMM models returned by 'build_GMM' function

	"""
	probe_IDs = list(d.index)


	for s_id in sorted(m.keys()):
		#if s_id =='read_count':continue
		logging.info ("Writing to \"%s\" ..." % (outfile + '.' + s_id + "_classification.txt"))
		FOUT = open((outfile + '.' + s_id + "_classification.txt"),'w')
		component_means = m[s_id].means_[:,0]	# list of component means
		log_counts = d[s_id]

		probs = m[s_id].predict_proba(d[s_id].values.reshape(-1,1))	# list of probabilities of components: [[  4.33638063e-035   9.54842259e-001   4.51577411e-002],...]

		print ("\t".join(["Barcode", "log10_count", 'background_prob','cell_prob', 'Assigned_lable']), file=FOUT)
		for probe_ID, log_count, p in zip(probe_IDs, log_counts, probs):
			#print (probe_ID, log_count, p)
			p_list = list(p)

			# make sure the first prob is the prob of "smaller mean" (i.e., background), and the 2nd prob is prob of "larger mean" (i.e., cell)
			if component_means[0] > component_means[1]:
				p_list = p_list[::-1]

			#if p_list[0] >= prob_cutoff and (abs(log_count - smaller_mean) < abs(log_count - bigger_mean)):
			if p_list[0] >= prob_cutoff:
				label = 'background'
			#elif p_list[1] >= prob_cutoff and (abs(log_count - smaller_mean) > abs(log_count - bigger_mean)):
			elif p_list[1] >= prob_cutoff:
				label = 'cell'
			else:
				label='unknown'
			print (probe_ID + '\t' + str(log_count) + '\t' + '\t'.join([str(i) for i in p_list]) + '\t' + label, file=FOUT)
		FOUT.close()

