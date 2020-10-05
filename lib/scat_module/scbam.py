#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analzye 10X genomics single cell BAM files.
"""

import pysam
import sys
import collections
import logging
import re
import pandas as pd

def diff_str(s1, s2):
	'''
	Comparing orignal barcode to the corrected barcode
	find the index and the nucleotide that has been corrected.


	Parameters
	----------
	s1 : str
		the original barcode
	s2 : str
		the corrrected barcode

	'''
	results = []
	if len(s1) != len(s2):
		return results
	diff_positions = [i for i in range(len(s1)) if s1[i] != s2[i]]
	for pos in diff_positions:
		results.append([pos, s1[pos], s2[pos]])
	return results

def barcode_stat(infile, outfile, step_size=10000, limit=2000000, CR_tag = 'CR', CB_tag = 'CB', UR_tag = 'UR', UB_tag = 'UB'):
	'''
	Analzye barcode in BAM file.

	Parameters
	----------
	infile : str
		Input BAM file. Must be sorted and indexed.
	outfile : str
		Prefix of output files.
	step_size: int
		Output progress report when step_size alignments have been processed.
	limit : int
		Only process this number of alignments and stop.
	'''
	logging.info("Reading BAM file \"%s\" ..." % infile)
	samfile = pysam.Samfile(infile,'rb')

	CB_miss = 0 #number of reads without cell barcode
	CB_same = 0 #number of reads whose original cell barcode same as edited barcode
	CB_diff = 0 #number of reads whose cell barcode has been edited
	CB_freq = collections.defaultdict(int) # cell barcode: raw reads
	CB_corrected_bases = collections.defaultdict(dict)


	UMI_miss = 0
	UMI_same = 0
	UMI_diff = 0
	UMI_freq = collections.defaultdict(int) # UMI : raw reads
	UMI_corrected_bases = collections.defaultdict(dict)

	total_alignments = 0
	try:
		while(1):
			total_alignments += 1
			aligned_read = next(samfile)
			tag_dict = dict(aligned_read.tags) #{'NM': 1, 'RG': 'L1'}

			original_CB = ''
			corrected_CB = ''
			if CR_tag in tag_dict and CB_tag in tag_dict:
				original_CB = tag_dict[CR_tag].replace('-1','')
				corrected_CB = tag_dict[CB_tag].replace('-1','')
				CB_freq[corrected_CB] +=1
				if original_CB != corrected_CB:
					CB_diff += 1
					for diff in diff_str(original_CB, corrected_CB):
						try:
							CB_corrected_bases[diff[0]][diff[1]+ ':' + diff[2]] += 1
						except:
							CB_corrected_bases[diff[0]][diff[1]+ ':' + diff[2]] = 1
				else:
					CB_same +=1
			else:
				CB_miss += 1

			original_UMI = ''
			corrected_UMI = ''
			if UR_tag in tag_dict and UB_tag in tag_dict:
				original_UMI = tag_dict[UR_tag].replace('-1','')
				corrected_UMI = tag_dict[UB_tag].replace('-1','')
				UMI_freq[corrected_UMI] += 1
				if original_UMI != corrected_UMI:
					UMI_diff += 1
					for diff in diff_str(original_UMI, corrected_UMI):
						try:
							UMI_corrected_bases[diff[0]][diff[1]+ ':' + diff[2]] += 1
						except:
							UMI_corrected_bases[diff[0]][diff[1]+ ':' + diff[2]] = 1
				else:
					UMI_same += 1
			else:
				UMI_miss += 1

			if total_alignments % step_size == 0:
				print("%d alignments processed.\r" % total_alignments, end=' ', file=sys.stderr)
			if limit is not None:
				if total_alignments >= limit:
					break

	except StopIteration:
		pass
	logging.info ("Total alignments processed: %d" % total_alignments)

	logging.info("Number of alignmenets with <cell barcode> kept AS IS: %d" % CB_same)
	logging.info("Number of alignmenets with <cell barcode> edited: %d" % CB_diff)
	logging.info("Number of alignmenets with <cell barcode> missing: %d" % CB_miss)
	logging.info("Number of alignmenets with UMI kept AS IS: %d" % UMI_same)
	logging.info("Number of alignmenets with UMI edited: %d" % UMI_diff)
	logging.info("Number of alignmenets with UMI missing: %d" % UMI_miss)

	# writing cell barcode
	logging.info ("Writing cell barcode frequencies to \"%s\"" % (outfile + '.CB_freq.tsv'))
	with open(outfile + '.CB_freq.tsv','w') as CB_OUT:
		for bc,count in sorted(CB_freq.items(), key=lambda item: item[1], reverse=True):
			CB_OUT.write(bc + '\t' + str(count) + '\n')

	# writing UMI
	logging.info ("Writing UMI frequencies to \"%s\"" % (outfile + '.UMI_freq.tsv'))
	with open(outfile + '.UMI_freq.tsv','w') as UMI_OUT:
		for bc,count in sorted(UMI_freq.items(), key=lambda item: item[1], reverse=True):
			UMI_OUT.write(bc + '\t' + str(count) + '\n')

	CB_mat_file = outfile + '.CB_edits_count.csv'
	logging.info ("Writing the nucleotide editing matrix (count) of cell barcode to \"%s\"" % CB_mat_file)
	CB_diff_mat = pd.DataFrame.from_dict(CB_corrected_bases)
	CB_diff_mat = CB_diff_mat.fillna(0)
	#CB_diff_mat = CB_diff_mat.T
	CB_diff_mat.sort_index(inplace=True)
	CB_diff_mat = CB_diff_mat.sort_index(axis=1)
	CB_diff_mat.index.name='Edits'
	CB_diff_mat.to_csv(CB_mat_file, index=True, index_label="Index")

	UMI_mat_file = outfile + '.UMI_edits_count.csv'
	logging.info ("Writing the nucleotide editing matrix of molecular barcode (UMI) to \"%s\"" % UMI_mat_file)
	UMI_diff_mat = pd.DataFrame.from_dict(UMI_corrected_bases)
	UMI_diff_mat = UMI_diff_mat.fillna(0)
	#UMI_diff_mat = UMI_diff_mat.T
	UMI_diff_mat.sort_index(inplace=True)
	UMI_diff_mat = UMI_diff_mat.sort_index(axis=1)
	UMI_diff_mat.index.name='Edits'
	UMI_diff_mat.to_csv(UMI_mat_file, index=True, index_label="Index")



def reads_stat(infile, step_size=10000, limit=1000000):
	'''
	Reads mapping statistics

	Parameters
	----------
	infile : str
		Input BAM file. Must be sorted and indexed.
	outfile : str
		Prefix of output files.
	step_size: int
		Output progress report when step_size alignments have been processed.
	limit : int
		Only process this number of alignments and stop.
	'''
	logging.info("Reading BAM file \"%s\" ..." % infile)
	samfile = pysam.AlignmentFile(infile,'rb')

	#exon_count + intron_count + intergenic_count == total
	unknown_count = 0 #reads with unknown mapping information
	exon_count = 0
	exon_count_tx = 0 # read aligned to same strand as the transcripts
	exon_count_an = 0 #read aligned to antisense strand of the transcripts
	exon_count_other = 0 #reads aligned to other (e.g., exon-intron boundaries)
	intron_count = 0
	intergenic_count = 0


	confid_mapped = 0 #read confidently mapped to feature
	UMI_read = 0 #This read is representative for the molecule and can be treated as a UMI count
	alien_read = 0 # The read maps to a feature that the majority of other reads with this UMI did not
	targeted_UM_fil = 0 #This read was removed by targeted UMI filtering.

	total_alignments = 0
	unique_reads = collections.defaultdict(int)
	try:
		while(1):
			total_alignments += 1
			aligned_read = next(samfile)
			unique_reads[aligned_read.query_name] += 1
			tag_dict = dict(aligned_read.tags) #{'NM': 1, 'RG': 'L1'}
			if 'xf' in tag_dict:
				flag_value = tag_dict['xf']
				if flag_value & 0x1 != 0:
					confid_mapped += 1
				if flag_value & 0x2 != 0:
					alien_read += 1
				if flag_value & 0x8 != 0:
					UMI_read += 1
				if flag_value & 0x20 != 0:
					targeted_UM_fil += 1

			if 'RE' in tag_dict:
				if tag_dict['RE'] == "E":
					exon_count += 1
					if 'TX' in tag_dict:
						exon_count_tx += 1
					elif 'AN' in tag_dict:
						exon_count_an += 1
					else:
						exon_count_other += 1
				elif tag_dict['RE'] == "I":
					intron_count += 1
				elif tag_dict['RE'] == "N":
					intergenic_count += 1
			else:
				unknown_count += 1
				continue
			if total_alignments % step_size == 0:
				print("%d alignments processed.\r" % total_alignments, end=' ', file=sys.stderr)

			if limit is not None:
				if total_alignments >= limit:
					break
	except StopIteration:
		pass
	logging.info ("\nTotal alignments processed: %d" % total_alignments)

	total_reads = len(unique_reads)
	print ("\nGenomic distribution of mapped reads:")
	print ("Total_reads:\t%d\t(100%%)" % total_reads)
	print ("  *Exonic_reads:\t%d\t(%.2f%%)" % (exon_count, exon_count*100.0/total_reads))
	print ("    #Exonic_transcript:\t%d\t(%.2f%%)" % (exon_count_tx,exon_count_tx*100.0/total_reads))
	print ("    #Exonic_antisense:\t%d\t(%.2f%%)" % (exon_count_an, exon_count_an*100.0/total_reads))
	print ("    #Exonic_other:\t%d\t(%.2f%%)" % (exon_count_other, exon_count_other*100.0/total_reads))
	print ("  *Intronic_reads:\t%d\t(%.2f%%)" % (intron_count,intron_count*100.0/ total_reads))
	print ("  *Intergenic_reads:\t%d\t(%.2f%%)" % (intergenic_count, intergenic_count*100.0/total_reads))
	print ("  *Unknown_reads:\t%d\t(%.2f%%)" % (unknown_count, unknown_count*100.0/total_reads))
	print ('\n')

	print ("Other statistics:")
	print ("  *Confidently_mapped_reads:\t%d\t(%.2f%%)" % (confid_mapped, confid_mapped*100.0/total_reads))
	print ("  *UMI counting_eligible_reads:\t%d\t(%.2f%%)" % (UMI_read, UMI_read*100.0/total_reads))
	print ("  *Alien_reads:\t%d\t(%.2f%%)" % (alien_read, alien_read*100.0/total_reads))
	print ("  *Targeted_UMI_filtered_reads:\t%d\t(%.2f%%)" % (targeted_UM_fil, targeted_UM_fil*100.0/total_reads))


def read_match_type(cigar_str):
	'''return the matching type between read and ref'''
	match_type = ''
	if bool(re.search(r'\A\d+M\Z', cigar_str)):
		match_type ='Map_consecutively'
	elif bool(re.search(r'\A\d+M\d+N\d+M\Z', cigar_str)):
		match_type = 'Map_with_splicing'
	elif bool(re.search(r'\A\d+S\d+M\Z', cigar_str)):
		match_type = 'Map_with_clipping'
	elif bool(re.search(r'\A\d+M\d+S\Z', cigar_str)):
		match_type = 'Map_with_clipping'
	elif bool(re.search(r'\A\d+M\d+N\d+M\d+S\Z', cigar_str)):
		match_type = 'Map_with_splicing_and_clipping'
	elif bool(re.search(r'\A\d+S\d+M\d+N\d+M\Z', cigar_str)):
		match_type = 'Map_with_splicing_and_clipping'
	else:
		match_type = 'Others'
	return match_type

def list2str (lst):
	'''
	translate samtools returned cigar_list into cigar_string
	'''
	code2Char={'0':'M','1':'I','2':'D','3':'N','4':'S','5':'H','6':'P','7':'=','8':'X'}
	cigar_str=''
	for i in lst:
		cigar_str += str(i[1]) + code2Char[str(i[0])]
	return cigar_str

def mapping_stat(infile, outfile, step_size=10000, limit=1000000):
	'''
	1) mapping statistics
	2) split reads into confidently mapped and non-confidently mapped, and save into seprate BAM files.
	Parameters
	----------
	infile : str
		Input BAM file. Must be sorted and indexed.
	outfile : str
		Prefix of output files. If outfile is None, only do counting and do not generate BAM files.
	step_size: int
		Output progress report when step_size alignments have been processed.
	limit : int
		Only process this number of alignments and stop.
	'''
	logging.info("Reading BAM file \"%s\" ..." % infile)
	samfile = pysam.AlignmentFile(infile,'rb')


	if outfile is not None:
		logging.info("Counting reads and generating BAM files ...")
		logging.info("  Saving reads confidently mapped to transcriptome to \"%s\" ..." % (outfile + '.confident_alignments.bam'))
		OUTC = pysam.Samfile((outfile + '.confident_alignments.bam'),'wb',template=samfile)
		logging.info("  Saving reads not confidently mapped to transcriptome to \"%s\" ..." % (outfile + '.non_confident_alignments.bam'))
		OUTN = pysam.Samfile((outfile + '.non_confident_alignments.bam'),'wb',template=samfile)
	else:
		logging.info("Counting reads without generating BAM files ...")
	total_alignments = 0
	confi_alignments = 0
	total_reads = collections.defaultdict(int) #total reads in BAM file
	confi_reads = collections.defaultdict(int) #reads marked as confidently mapped to transcriptome by xf:i:1 tag

	#PCR duplicate or not
	confi_reads_dup = 0
	confi_reads_nondup = 0

	#Reverse or forward
	confi_reads_rev = 0
	confi_reads_fwd = 0

	# with error-corrected CB
	confi_CB = 0

	# with error-corrected UMI
	confi_UB = 0

	#read match type
	read_type = collections.defaultdict(int)
	try:
		while(1):
			aligned_read = next(samfile)
			read_id = aligned_read.query_name
			tag_dict = dict(aligned_read.tags) #{'NM': 1, 'RG': 'L1'}
			cigar_str = list2str( aligned_read.cigar)
			total_reads[read_id] +=1

			#confident alignments
			if 'xf' in tag_dict and tag_dict['xf']& 0x1 != 0:
				if aligned_read.is_duplicate:
					confi_reads_dup += 1
				else:
					confi_reads_nondup += 1
				if aligned_read.is_reverse:
					confi_reads_rev += 1
				else:
					confi_reads_fwd += 1

				if 'CB' in tag_dict:
					confi_CB += 1
				if 'UB' in tag_dict:
					confi_UB += 1

				cigar_str = list2str( aligned_read.cigar)
				tmp = read_match_type(cigar_str)
				read_type[tmp] += 1
				confi_alignments += 1
				confi_reads[read_id] += 1
				if outfile is not None:
					OUTC.write(aligned_read)
			else:
				if outfile is not None:
					OUTN.write(aligned_read)


			total_alignments += 1
			if total_alignments % step_size == 0:
				print("%d alignments processed.\r" % total_alignments, end=' ', file=sys.stderr)
			if limit is not None:
				if total_alignments >= limit:
					break

	except StopIteration:
		pass
	total_reads_n = len (total_reads)
	confi_reads_n = len (confi_reads)
	non_confi_reads = total_reads_n - confi_reads_n
	print ('')
	print("\nTotal_alignments: %d" % total_alignments)
	print ("└--Confident_alignments: %d" % confi_alignments)
	print ('')
	print ("Total_reads:\t%d" % total_reads_n)
	print ("|--Non_confidently_mapped_reads:\t%d\t(%.2f%%)" % (non_confi_reads, non_confi_reads*100.0/total_reads_n))
	print ("└--Confidently_mapped_reads:\t%d\t(%.2f%%)" % (confi_reads_n, confi_reads_n*100.0/total_reads_n))

	print ("   |--PCR duplicate reads:\t%d\t(%.2f%%)" % (confi_reads_dup, confi_reads_dup*100.0/confi_reads_n))
	print ("   └--Non PCR duplicate reads:\t%d\t(%.2f%%)" % (confi_reads_nondup, confi_reads_nondup*100.0/confi_reads_n))
	print ('')

	print ("   |--Forward reads:\t%d\t(%.2f%%)" % (confi_reads_fwd, confi_reads_fwd*100.0/confi_reads_n))
	print ("   └--Reverse reads:\t%d\t(%.2f%%)" % (confi_reads_rev, confi_reads_rev*100.0/confi_reads_n))
	print ('')

	print ("   |--Reads with Error-Corrected cell barcode:\t%d\t(%.2f%%)" % (confi_CB, confi_CB*100.0/confi_reads_n))
	print ("   └--Reads without Error-Corrected cell barcode:\t%d\t(%.2f%%)" % ((confi_reads_n - confi_CB), (confi_reads_n - confi_CB)*100.0/confi_reads_n))
	print ('')
	print ("   |--Reads with Error-Corrected UMI:\t%d\t(%.2f%%)" % (confi_UB, confi_UB*100.0/confi_reads_n))
	print ("   └--Reads without Error-Corrected UMI:\t%d\t(%.2f%%)" % ((confi_reads_n - confi_UB), (confi_reads_n - confi_UB)*100.0/confi_reads_n))
	print ('')

	for i in sorted(read_type):
		if i == 'Others':continue
		print ("   |--%s:\t%d\t(%.2f%%)" % (i, read_type[i], read_type[i]*100.0/confi_reads_n))
	print ("   └--%s:\t%d\t(%.2f%%)" % ('Others', read_type['Others'], read_type['Others']*100.0/confi_reads_n))
	print ('')
	##add with/without CB

def readCount(infile, outfile, step_size=10000, limit=1000000, csv_out=False):
	'''
	Save reads that confidenlty mapped to transcriptome to a BAM file.

	Parameters
	----------
	infile : str
		Input BAM file. Must be sorted and indexed.
	outfile : str
		Prefix of output files.
	step_size: int
		Output progress report when step_size alignments have been processed.
	limit : int
		Only process this number of alignments and stop.
	'''
	logging.info("Reading BAM file \"%s\" ..." % infile)
	samfile = pysam.AlignmentFile(infile,'rb')

	#OUT = open(outfile,'w')
	total_alignments = 0
	CB_GN_READ = collections.defaultdict(dict)
	#CB_GN_UMI = collections.defaultdict(list)
	try:
		while(1):
			aligned_read = next(samfile)
			read_id = aligned_read.query_name
			tag_dict = dict(aligned_read.tags) #{'NM': 1, 'RG': 'L1'}
			if 'xf' in tag_dict and tag_dict['xf']& 0x1 == 0:
				continue
			if 'CB' in tag_dict:
				CB = tag_dict['CB'].replace('-1','')
			else:
				logging.debug('%s has no cell barcode!' % read_id)
			#if 'UB' in tag_dict:
			#	UMI = tag_dict['UB'].replace('-1','')
			if 'GX' in tag_dict:
				geneID = tag_dict['GX']
			else:
				geneID = 'NA'
			if 'GN' in tag_dict:
				geneSymbol = tag_dict['GN']
			else:
				geneSymbol="NA"

			if geneID == 'NA':
				continue

			try:
				CB_GN_READ[CB][geneID + '|' + geneSymbol] += 1
			except KeyError:
				CB_GN_READ[CB][geneID + '|' + geneSymbol] = 1

			#CB_GN_UMI[CB + ':' + geneID].append(UMI)

			total_alignments += 1
			if total_alignments % step_size == 0:
				print("%d alignments processed.\r" % total_alignments, end=' ', file=sys.stderr)
			if limit is not None:
				if total_alignments >= limit:
					break

	except StopIteration:
		pass
	"""
	logging.info('Total %d alignments processed' % total_alignments)
	logging.info('Convert dict of dict to pandas data frame')
	count_mat = pd.DataFrame(CB_GN_READ)
	(gene_num, CB_num) = count_mat.shape
	logging.info('Data frame contains %d genes (rows) and %d cell barcodes (columns)' % (gene_num, CB_num))

	if csv_out is True:
		logging.info('Save data frame to \"%s\"' % (outfile + '.csv'))
		count_mat.to_csv(outfile + '.csv', index=True, index_label="Gene")


	logging.info('Save data frame to \"%s\"' % (outfile + '.h5'))
	count_mat.to_hdf(outfile + '.h5',key='df',mode='w',complevel=6)
	"""


def CBC_UMIcount(infile, outfile, step_size=10000, CB_tag = 'CB', UMI_tag = 'UB', CB_num = 100000, read_num=200):
	'''
	Calculate UMI count for each cell barcode.

	Parameters
	----------
	infile : str
		Input BAM file. Must be sorted and indexed.
	outfile : str
		Prefix of output files.
	step_size: int
		Print progress report when step_size alignments have been processed.
	CB_tag : str
		Tag for cell barcode in the input BAM file.
	UMI_tag : str
		Tag for UMI in the input BAM file.
	CB_num : int
		Number of cell barcodes to be considered.
	read_num : int
		Read number threshold to filter invalid cell barcode.
		Cell barcode with reads less than this value will be skipped.
	'''


	CB_read_freq = collections.defaultdict(int) # cell_barcode:read_frequency
	CB_UMI_freq = {} # cell_barcode:UMI
	CB_cutoff = CB_num
	logging.info("Top %d cell barcodes (ranked by associated UMI frequency) will be analyzed." % CB_cutoff)
	read_cutoff = read_num
	logging.info("Only count UMIs for cell barcodes with more than %d reads." % read_cutoff)

	#count read number for each cell barcode
	logging.info("Reading BAM file \"%s\". Count reads for each cell barcode ..." % infile)
	samfile = pysam.AlignmentFile(infile,'rb')
	total_alignments = 0
	try:
		while(1):
			aligned_read = next(samfile)
			tag_dict = dict(aligned_read.tags) #{'NM': 1, 'RG': 'L1'}
			if 'xf' in tag_dict and tag_dict['xf']& 0x1 == 0:
				continue

			#count reads
			if CB_tag in tag_dict:
				CB = tag_dict[CB_tag].replace('-1','')
			else:
				continue
			CB_read_freq[CB] += 1
			total_alignments += 1
			if total_alignments % step_size == 0:
				print("%d alignments processed.\r" % total_alignments, end=' ', file=sys.stderr)
	except StopIteration:
		pass
	logging.info('Total %d alignments processed' % total_alignments)

	logging.info("Filtering cell barcodes ...")
	CB_usable = set()
	for k,v in CB_read_freq.items():
		if v >= read_cutoff:
			CB_usable.add(k)
	logging.info("Total cell barcode: %d" % len(CB_read_freq))
	logging.info("Cell barcode with more than %d reads: %d" % (read_cutoff, len(CB_usable)))


	#count UMI for each cell barcode
	logging.info("Reading BAM file \"%s\". Count UMIs for each cell barcode ..." % infile)
	samfile = pysam.AlignmentFile(infile,'rb')
	CB_freq_list = {} #cell_barcode:UMI_list
	total_alignments = 0
	try:
		while(1):
			aligned_read = next(samfile)
			read_id = aligned_read.query_name
			#chrom = samfile.get_reference_name(aligned_read.reference_id)
			#if aligned_read.is_duplicate:continue
			tag_dict = dict(aligned_read.tags) #{'NM': 1, 'RG': 'L1'}
			if 'xf' in tag_dict and tag_dict['xf']& 0x1 == 0:
				continue

			if CB_tag in tag_dict:
				CB = tag_dict[CB_tag].replace('-1','')
				if CB not in CB_usable: #filter out CB with low number of reads
					continue
			else:
				logging.debug('%s has no cell barcode!' % read_id)
				continue

			if UMI_tag in tag_dict:
				UMI = tag_dict[UMI_tag].replace('-1','')
			else:
				logging.debug('%s has no UMI!' % read_id)
				continue

			if 	CB not in CB_freq_list:
				CB_freq_list[CB] = set(UMI)
			else:
				CB_freq_list[CB].add(UMI)

			total_alignments += 1
			if total_alignments % step_size == 0:
				print("%d alignments processed.\r" % total_alignments, end=' ', file=sys.stderr)
	except StopIteration:
		pass
	logging.info('Total %d alignments processed' % total_alignments)

	for k,v in CB_freq_list.items():
		CB_UMI_freq[k] = len(v)

	OUT = open(outfile + '.Read_UMI_freq.tsv','w')
	logging.info ("Writing cell barcodes' reads and UMI frequencies to \"%s\"" % (outfile + '.Read_UMI_freq.tsv'))
	print ('\t'.join(['Serial#','Cell_barcode', 'read_count', 'UMI_count']), file=OUT) #do NOT change the header
	count = 0
	for k in sorted(CB_UMI_freq, key=CB_UMI_freq.get, reverse=True):
		count += 1
		print ('\t'.join([str(count), k, str(CB_read_freq[k]), str(CB_UMI_freq[k])]), file=OUT)
		if count > CB_cutoff:
			break
	OUT.close()
	logging.info ("Done.")




