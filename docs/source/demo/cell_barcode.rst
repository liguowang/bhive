cell_barcode.py
===============

Description
------------

First, calculates the "read count" and "UMI count" for each cell barcode, and generates the
barcode rank plot and density plot. Then, using the Bayesian Gaussian Mixture Model (BGMM)
to classify cell barcode into "valid" and "background" groups.



Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i IN_FILE, --infile=IN_FILE
                        Input file in BAM foramt.
  -o OUT_FILE, --outfile=OUT_FILE
                        The prefix of output files.
  --cb-tag=CB_TAG       Tag of error-corrected cellular barcode in BAM file.
                        default='CB'
  --umi-tag=UMI_TAG     Tag of error-corrected UMI in BAM file. default='UB'
  --cb-num=CB_LIMIT     Maximum cell barcodes (ranked by associated UMI frequency)
                        analysed. default=100000
  --min-read-count=MIN_READS
                        The minimum number of reads to filter out cell
                        barcode. default=200
  -r, --report          If set, generates report file for mixture models.
                        default=False
  -s RANDOM_STATE, --seed=RANDOM_STATE
                        The seed used by the random number generator.
                        default=0
  --prob-cut=PROBABILITY_CUTOFF
                        The probabiilty cutoff [0.5, 1] to assign cell barcode
                        to the "cell" or the "background" component.
                        default=0.5
  --verbose             If set, print detailed information for debugging.                      


Example
-------

::
 
 
 $ python3 seq_qual.py -i  ../normal_dat/indepth_C05_MissingLibrary_1_HL5G3BBXX/bamtofastq_S1_L004_R1_001.fastq.gz -n  5000000 -o R1_qual
 
 2020-09-29 04:34:40 [INFO]  Reading FASTQ file "../normal_dat/indepth_C05_MissingLibrary_1_HL5G3BBXX/bamtofastq_S1_L004_R1_001.fastq.gz" ...
 2020-09-29 04:35:30 [INFO]  5000000 quality sequences finished
 2020-09-29 04:35:30 [INFO]  Make data frame from dict of dict ...
 2020-09-29 04:35:30 [INFO]  Filling NA as zero ...
 2020-09-29 04:35:30 [INFO]  Writing R code to "R1_qual.qual_heatmap.r"
 2020-09-29 04:35:30 [INFO]  Displayed numerical values on heatmap
 2020-09-29 04:35:30 [INFO]  Running R script file "R1_qual.qual_heatmap.r"
 Loading required package: Matrix
 Loading required package: SPAtest
 Loading required package: pheatmap


Output files
-------------

- R1_qual.qual_count.csv
- R1_qual.qual_heatmap.pdf
- R1_qual.qual_heatmap.r
- R1_qual.qual_percent.csv



R1_qual.qual_heatmap.pdf

.. image:: ../_static/R1_qual.qual_heatmap.png
   :height: 250 px
   :width: 900 px
   :scale: 100 %     

