BC_edit_matrix.py
=================

Description
-------------
This program generates heatmaps to visualize the **positions** (X-axis),
type of edits (Y-axis, such as "C" to "T") and  **frequencies** (color) 
of error-corrected nucleotides in cell barcodes and UMIs.

Options
-------
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i IN_FILE, --infile=IN_FILE
                        Input file in BAM foramt.
  -o OUT_FILE, --outfile=OUT_FILE
                        The prefix of output files.
  --limit=READS_NUM     Number of alignments to process. default=none
  --cr-tag=CR_TAG       Tag of cellular barcode reported by the sequencer in
                        BAM file. default='CR'
  --cb-tag=CB_TAG       Tag of error-corrected cellular barcode in BAM file.
                        default='CB'
  --ur-tag=UR_TAG       Tag of UMI reported by the sequencer in BAM file.
                        default='UR'
  --ub-tag=UB_TAG       Tag of error-corrected UMI in BAM file. default='UB'
  --cell-width=CELL_WIDTH
                        Points of cell width in the heatmap. default=15
  --cell-height=CELL_HEIGHT
                        Points of cell height in the heatmap. default=10
  --font-size=FONT_SIZE
                        Font size. If --display-num was set, fontsize_number =
                        0.8 * font_size. default=8
  --angle=COL_ANGLE     The angle (must be 0, 45, 90, 270, 315) of column text
                        lables under the heatmap. default=45
  --text-color=TEXT_COLOR
                        The color of numbers in each cell. default=black
  --file-type=FILE_TYPE
                        The file type of heatmap. Choose one of 'pdf', 'png',
                        'tiff', 'bmp', 'jpeg'. default=pdf
  --verbose             If set, detailed running information is printed to
                        screen.
  --no-num              If set, will not print numerical values to cells.
                        default=False                        

Input file format
------------------
BAM file with the following tags:

- CB : cellular barcode sequence that is error-corrected
- CR : cellular barcode sequence as reported by the sequencer.
- UB : molecular barcode sequence that is error-corrected
- UR : molecular barcode sequence as reported by the sequencer. 
 
Example (Visualize sample barcode)
--------------------------------------

::
 
 $ python3 BC_edit_matrix.py -i normal_possorted_genome_bam.bam --limit 5000000 -o output
 
 2020-09-30 08:59:21 [INFO]  Reading BAM file "normal_possorted_genome_bam.bam" ...
 2020-09-30 09:00:03 [INFO]  Total alignments processed: 5000000
 2020-09-30 09:00:03 [INFO]  Number of alignmenets with <cell barcode> kept AS IS: 4876615
 2020-09-30 09:00:03 [INFO]  Number of alignmenets wiht <cell barcode> edited: 47377
 2020-09-30 09:00:03 [INFO]  Number of alignmenets with <cell barcode> missing: 76008
 2020-09-30 09:00:03 [INFO]  Number of alignmenets with UMI kept AS IS: 4973597
 2020-09-30 09:00:03 [INFO]  Number of alignmenets wiht UMI edited: 24842
 2020-09-30 09:00:03 [INFO]  Number of alignmenets with UMI missing: 1561
 2020-09-30 09:00:03 [INFO]  Writing cell barcode frequencies to "output.CB_freq.tsv"
 2020-09-30 09:00:03 [INFO]  Writing UMI frequencies to "output.UMI_freq.tsv"
 2020-09-30 09:00:04 [INFO]  Writing the nucleotide editing matrix (count) of cell barcode to "output.CB_edits_count.csv"
 2020-09-30 09:00:04 [INFO]  Writing the nucleotide editing matrix of molecular barcode (UMI) to "output.UMI_edits_count.csv"
 2020-09-30 09:00:04 [INFO]  Writing R code to "output.CB_edits_heatmap.r"
 2020-09-30 09:00:04 [INFO]  Displayed numerical values on heatmap
 2020-09-30 09:00:04 [INFO]  Numbers will be displayed on log2 scale
 2020-09-30 09:00:04 [INFO]  Running R script file "output.CB_edits_heatmap.r"
 Loading required package: Matrix
 Loading required package: SPAtest
 Loading required package: pheatmap
 2020-09-30 09:00:07 [INFO]  Writing R code to "output.UMI_edits_heatmap.r"
 2020-09-30 09:00:07 [INFO]  Displayed numerical values on heatmap
 2020-09-30 09:00:07 [INFO]  Numbers will be displayed on log2 scale
 2020-09-30 09:00:07 [INFO]  Running R script file "output.UMI_edits_heatmap.r"
 Loading required package: Matrix
 Loading required package: SPAtest
 Loading required package: pheatmap

out put files
-------------
- output.CB_edits_count.csv : editing matrix of cellular barcodes in CSV format.
- output.CB_freq.tsv : corrected cell barcodes and their frequencies.
- output.CB_edits_heatmap.pdf : heatmap showing the positions, types and frequencies of nucleotides that have been corrected.  
- output.CB_edits_heatmap.r : R script for the above heatmap.
- 
- output.UMI_edits_count.csv : editing matrix of UMIs in CSV format.
- output.UMI_freq.tsv : corrected UMIs and their frequencies.
- output.UMI_edits_heatmap.pdf :  heatmap showing the positions, types and frequencies of nucleotides that have been corrected.  
- output.UMI_edits_heatmap.r : R script for the above heatmap.



Three files were generated.

- I1.count_matrix.csv
- I1.logo.pdf
- I1logo.mean_centered.pdf

output.CB_edits_heatmap.pdf

.. image:: ../_static/CB_edits_heatmap.png
   :height: 600 px
   :width: 800 px
   :scale: 100 %  

output.UMI_edits_heatmap.pdf

.. image:: ../_static/UMI_edits_heatmap.png
   :height: 600 px
   :width: 800 px
   :scale: 100 %  



