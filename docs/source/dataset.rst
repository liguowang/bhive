Testing dataset
===============

We use the same example dataset as used by `10X Genomics <https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/tutorials/gex-analysis-nature-publication>`_.
Raw data (in BAM format) were downloaded from the NCBI Sequence Read Archive (SRA). The study was published in [1]_.

Download raw data
------------------

+----------------------------------------------------------------------------+---------------+---------------+-----------+------------+----------------------------------+
| File_name                                                                  | GSM_accession | SRR_accession | File_size | Treatment  | MD5                              |
+----------------------------------------------------------------------------+---------------+---------------+-----------+------------+----------------------------------+
| `C05.bam.1 <https://sra-pub-src-1.s3.amazonaws.com/SRR7611046/C05.bam.1>`_ | GSM3308718    | SRR7611046    | 70 Gb     | normal     | 97b87c87b539e69dad7dcb04e8f03132 |
+----------------------------------------------------------------------------+---------------+---------------+-----------+------------+----------------------------------+
| `C07.bam.1 <https://sra-pub-src-1.s3.amazonaws.com/SRR7611048/C07.bam.1>`_ | GSM3308720    | SRR7611048    | 64 Gb     | irradiated | 064669deb6be22e5f82fe58679f7e394 |
+----------------------------------------------------------------------------+---------------+---------------+-----------+------------+----------------------------------+

Convert BAM to FASTQ
---------------------
Download ``bamtofastq`` from `here <https://cf.10xgenomics.com/misc/bamtofastq-1.2.0>`_. Convert BAM into FASTQ files.
::

 $ bamtofastq C05.bam.1 normal_dat
 $ bamtofastq C07.bam.1 irradiated_dat

After this step, you will get two subdirectories (``./normal_dat`` and ``./irradiated_dat``) under your current directory. And within ``./normal_dat`` and ``./irradiated_dat``, there are 
subdirectories and fastq files, for example

::

 $ cd ./normal_dat
 $ tree 
 .
 ├── indepth_C05_MissingLibrary_1_HL5G3BBXX
 │   ├── bamtofastq_S1_L003_I1_001.fastq.gz
 │   ├── bamtofastq_S1_L003_I1_002.fastq.gz
 │   ├── bamtofastq_S1_L003_R1_001.fastq.gz
 │   ├── bamtofastq_S1_L003_R1_002.fastq.gz
 │   ├── bamtofastq_S1_L003_R2_001.fastq.gz
 │   ├── bamtofastq_S1_L003_R2_002.fastq.gz
 │   ├── bamtofastq_S1_L004_I1_001.fastq.gz
 │   ├── bamtofastq_S1_L004_I1_002.fastq.gz
 │   ├── bamtofastq_S1_L004_I1_003.fastq.gz
 │   ├── bamtofastq_S1_L004_I1_004.fastq.gz
 │   ├── bamtofastq_S1_L004_I1_005.fastq.gz
 │   ├── bamtofastq_S1_L004_I1_006.fastq.gz
 │   ├── bamtofastq_S1_L004_R1_001.fastq.gz
 │   ├── bamtofastq_S1_L004_R1_002.fastq.gz
 │   ├── bamtofastq_S1_L004_R1_003.fastq.gz
 │   ├── bamtofastq_S1_L004_R1_004.fastq.gz
 │   ├── bamtofastq_S1_L004_R1_005.fastq.gz
 │   ├── bamtofastq_S1_L004_R1_006.fastq.gz
 │   ├── bamtofastq_S1_L004_R2_001.fastq.gz
 │   ├── bamtofastq_S1_L004_R2_002.fastq.gz
 │   ├── bamtofastq_S1_L004_R2_003.fastq.gz
 │   ├── bamtofastq_S1_L004_R2_004.fastq.gz
 │   ├── bamtofastq_S1_L004_R2_005.fastq.gz
 │   └── bamtofastq_S1_L004_R2_006.fastq.gz
 └── indepth_C05_MissingLibrary_1_HNNWNBBXX
     ├── bamtofastq_S1_L002_I1_001.fastq.gz
     ├── bamtofastq_S1_L002_I1_002.fastq.gz
     ├── bamtofastq_S1_L002_I1_003.fastq.gz
     ├── bamtofastq_S1_L002_I1_004.fastq.gz
     ├── bamtofastq_S1_L002_I1_005.fastq.gz
     ├── bamtofastq_S1_L002_R1_001.fastq.gz
     ├── bamtofastq_S1_L002_R1_002.fastq.gz
     ├── bamtofastq_S1_L002_R1_003.fastq.gz
     ├── bamtofastq_S1_L002_R1_004.fastq.gz
     ├── bamtofastq_S1_L002_R1_005.fastq.gz
     ├── bamtofastq_S1_L002_R2_001.fastq.gz
     ├── bamtofastq_S1_L002_R2_002.fastq.gz
     ├── bamtofastq_S1_L002_R2_003.fastq.gz
     ├── bamtofastq_S1_L002_R2_004.fastq.gz
     ├── bamtofastq_S1_L002_R2_005.fastq.gz
     ├── bamtofastq_S1_L003_I1_001.fastq.gz
     ├── bamtofastq_S1_L003_I1_002.fastq.gz
     ├── bamtofastq_S1_L003_R1_001.fastq.gz
     ├── bamtofastq_S1_L003_R1_002.fastq.gz
     ├── bamtofastq_S1_L003_R2_001.fastq.gz
     └── bamtofastq_S1_L003_R2_002.fastq.gz

Run CellRanger *count* workflow
-------------------------------
Download ``cellranger`` and **Mouse reference dataset** from `here <https://support.10xgenomics.com/single-cell-gene-expression/software/downloads/latest>`_
::

 $ cellranger --version
 cellranger 4.0.0
 
 # run cellranger for normal sample
 $ cd ./normal_dat
 $ cellranger count  --id=normal        --transcriptome=/XYZ/CellRanger/refdata-gex-mm10-2020-A  --fastqs=./indepth_C05_MissingLibrary_1_HL5G3BBXX,./indepth_C05_MissingLibrary_1_HNNWNBBXX
 
 # run cellranger for irradiated sample
 $ cd ./irradiated_dat
 $ cellranger count  --id=irradiated    --transcriptome=/XYZ/CellRanger/refdata-gex-mm10-2020-A  --fastqs=./indepth_C07_MissingLibrary_1_HL5G3BBXX,./indepth_C07_MissingLibrary_1_HNNWNBBXX
 
After each ``cellranger count`` workflow is finished successfully. Subdirectories ``normal`` and ``irradiated`` will be created, which contain the cellranger outputs. For example,
::

 $ cd normal
 $ ls -F
 _cmdline     _invocation  _mrosource	  _perf		      _tags	  _vdrkill
 _filelist    _jobmode	  normal.mri.tgz  SC_RNA_COUNTER_CS/  _timestamp  _versions
 _finalstate  _log	  outs/		  _sitecheck	      _uuid
 
.. note::
   Replace /XYZ/ with the actual path on your system.

Run CellRanger *aggr* workflow
-------------------------------

First, make the ``library.csv`` file. This CSV file has two columns which define the **ID** and the location of the **molecule_info.h5** file from each run.
::
 
 $ cat  library.csv
 
 library_id,molecule_h5
 normal,/ABC/normal_dat/normal/outs/molecule_info.h5
 irradiated,/ABC/irradiated_dat/irradiated/outs/molecule_info.h5

.. note::
   Replace /ABC/ with the actual path on your system.
   
Then, run ``cellranger aggr`` workflow. The ``cellranger aggr`` workflow aggregates outputs from multiple runs of the ``cellranger count`` workflow
::

 $ cellranger aggr --id=aggr --csv=libraries.csv
 
After each ``cellranger aggr`` workflow is finished successfully. A subdirectory ``aggr`` will be created, which contain the cellranger outputs. For example,
::

 $ cd aggr
 $ ls -F
 aggr.mri.tgz  _finalstate  _log        _perf		      _tags	  _vdrkill
 _cmdline      _invocation  _mrosource  SC_RNA_AGGREGATOR_CS/  _timestamp  _versions
 _filelist     _jobmode	   outs/       _sitecheck	      _uuid 

References
----------	

.. [1] Ayyaz A, Kumar S, Sangiorgi B, Ghoshal B, Gosio J, Ouladan S, Fink M, Barutcu S, Trcka D, Shen J, Chan K, Wrana JL, Gregorieff A. Single-cell transcriptomes of the regenerating intestine reveal a revival stem cell. Nature. 2019 May;569(7754):121-125. doi: 10.1038/s41586-019-1154-y. Epub 2019 Apr 24. PMID: 31019301.