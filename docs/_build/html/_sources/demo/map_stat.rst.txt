map_stat.py
===========

Description
------------

Report reads mapping statistics


Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i BAM_FILE, --infile=BAM_FILE
                        Input file in BAM foramt. Must have BAM alignment tags
                        indicated below.
  --cb-tag=CB_TAG       BAM alignment tag. Used to indicate error-corrected
                        cellular barcode. default='CB'
  --re-tag=RE_TAG       BAM alignment tag. Used to indicate the region type of
                        the alignment (E = exonic, N = intronic, I =
                        intergenic). default='RE'
  --tx-tag=TX_TAG       BAM alignment tag. Used to indicate reads aligned to
                        the same strand as the annotated transcripts.
                        default='TX'
  --an-tag=AN_TAG       BAM alignment tag. Used to indicate reads aligned to
                        the antisense strand of the annotated transcripts.
                        default='AN'
  --umi-tag=UMI_TAG     BAM alignment tag. Used to indicat the error-corrected
                        UMI. default='UB'
  --xf-tag=XF_TAG       BAM alignment tag. Used to indicate reads confidently
                        mapped to the feature. default='xf'
  --chrM-id=MIT_CONTIG_NAME
                        The name of mitochondrial chromosome in BAM file.
                        default='chrM'
  --verbose             Logical to determine if detailed running information
                        is printed to screen.

Example
-------

::
 
 
 $ python3 map_stat2.py -i normal_possorted_genome_bam.bam
 
 2020-10-08 10:06:41 [INFO]  Reading BAM file "normal_possorted_genome_bam.bam" ...
 2020-10-08 10:06:41 [INFO]  Processing "chr1" ...
 2020-10-08 10:11:50 [INFO]  Processed 24729033 alignments mapped to: "chr1"
 2020-10-08 10:12:16 [INFO]  Processing "chr10" ...
 2020-10-08 10:17:57 [INFO]  Processed 26004376 alignments mapped to: "chr10"
 2020-10-08 10:18:27 [INFO]  Processing "chr11" ...
 2020-10-08 10:26:59 [INFO]  Processed 37558210 alignments mapped to: "chr11"
 ...
 ...
 
 Total_alignments: 589060389
 └--Confident_alignments: 443330914
 
 Total_mapped_reads:     589060389
 |--Non_confidently_mapped_reads:        145729475       (24.74%)
 └--Confidently_mapped_reads:    443330914       (75.26%)
    |--Reads_with_PCR_duplicates:        327447641       (73.86%)
    └--Reads_no_PCR_duplicates:  115883273       (26.14%)
 
    |--Reads_map_to_forward(Waston)_strand:      259474203       (58.53%)
    └--Reads_map_to_Reverse(Crick)_strand:       183856711       (41.47%)
 
    |--Reads_map_to_sense_strand:        443330914       (100.00%)
    └--Reads_map_to_antisense_strand:    0       (0.00%)
    └--Other:    0       (0.00%)
 
    |--Reads_map_to_exons:       443330914       (100.00%)
    └--Reads_map_to_introns:     0       (0.00%)
    └--Reads_map_to_intergenic:  0       (0.00%)
    └--Other:    0       (0.00%)
 
    |--Reads_with_Error-Corrected_barcode:       437707874       (98.73%)
    └--Reads_no_Error-Corrected_barcode: 5623040 (1.27%)
 
    |--Reads_with_Error-Corrected_UMI:   443184634       (99.97%)
    └--Reads_no_Error-Corrected_UMI:     146280  (0.03%) 
 
    |--Reads_map_to_mitochonrial_genome: 56744099        (12.80%)
    └--Reads_map_to_nuclear_genome:      386586815       (87.20%)
 
    |--Map_consecutively:        242755968       (54.76%)
    |--Map_with_clipping:        49473035        (11.16%)
    |--Map_with_splicing:        115086767       (25.96%)
    |--Map_with_splicing_and_clipping:   19346122        (4.36%)
    └--Others:   16669022        (3.76%)
   
   
.. Note::
   Except the header section, each row in a BAM file represents an *alignment*.
   One read can have multiple alignments. 
