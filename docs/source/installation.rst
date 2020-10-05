Installation
============================

*bhive* is written in Python. Python3 is required to run all programs. Some programs also need R and R libraries to generate graphs. 

Prerequisites
--------------
You need to install these tools if they are not available from your computer. 

- `Python3 <https://www.python.org/downloads/>`_
- `pip3 <https://pip.pypa.io/en/stable/installing/>`_
- `R <https://www.r-project.org/>`_

R libraries required
------------------------

- R library `ggplot2 <https://cran.r-project.org/web/packages/ggplot2/index.html>`_
- R library `cowplot <https://cran.r-project.org/web/packages/cowplot/index.html>`_
- R library `pheatmap <https://www.rdocumentation.org/packages/pheatmap/versions/1.0.12/topics/pheatmap>`_

.. note::

   These R libraries will be automatically installed the first time they are used. Please manually 
   install them if you encounter error like: Error in library(XYZ) : there is no package called ‘XYZ’

Python packages required
------------------------

- `pandas <https://pandas.pydata.org/>`_
- `numpy <http://www.numpy.org/>`_
- `sklearn <https://www.scilearn.com/>`_
- `logomaker <https://logomaker.readthedocs.io/en/latest/>`_
- `pysam <https://github.com/pysam-developers/pysam>`_

.. note::
   Note: These Python packages will be automatically installed if you use
   `pip3 <https://pip.pypa.io/en/stable/installing/>`_ to install bhive.

Install bhive
------------------------------------------------------------------------------------------------------------------------------------
::

 $ pip3 install bhive
 or 
 $ pip3 install git+https://github.com/liguowang/bhive.git
 
Upgrade bhive
-----------------
::

 $ pip3 install bhive --upgrade	
