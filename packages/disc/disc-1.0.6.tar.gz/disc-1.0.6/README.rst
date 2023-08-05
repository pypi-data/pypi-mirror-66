DISC
====

|PyPI|

.. |PyPI| image:: https://img.shields.io/pypi/v/DISC.svg
    :target: https://pypi.org/project/disc

A highly scalable and accurate inference of gene expression and structure for single-cell transcriptomes using semi-supervised deep learning.

* Free software: Apache License 2.0

Requirements
------------

- Python_ >=3.6
- TensorFlow_ >=1.13.1,<2.0.0
- numpy_ >=1.14.0
- pandas_ >=0.21.0
- h5py_ >=2.9.0

Installation
------------

**Install TensorFlow**
  If you have an Nvidia GPU, be sure to install a version of TensorFlow that supports it first -- DISC runs much faster with GPU::

    pip install "tensorflow-gpu>= 1.13.1,<2.0.0"

  We typically tensorflow-gpu==1.13.1.

  Here are requirements for GPU version TensorFlow_::

    * Hardware
        * NVIDIA GPU card with CUDA Compute Capability 3.5 or higher.
    * Software
        * NVIDIA GPU drivers - CUDA 10.0 requires 410.x or higher.
        * CUDA Toolkit - TensorFlow_ supports CUDA 10.0 (TensorFlow >= 1.13.0)
        * CUPTI ships with the CUDA Toolkit.
        * cuDNN SDK (>= 7.4.1)

  see this__ for further information

      .. __: https://www.tensorflow.org/install/gpu

**Install DISC with pip**
  To install with ``pip``, run the following from a terminal::

    pip install disc

**Install DISC from GitHub**
  To clone the repository and install manually, run the following from a terminal::

    git clone git://github.com/iyhaoo/DISC.git

    cd disc

    python setup.py install

Usage
-----

Quick Start
 1. Run DISC::

     disc \
     --dataset=matrix.loom \
     --out-dir=out_dir

    where ``matrix.loom`` is a `loom-formatted`_ raw count matrix with genes in rows and cells in columns and ``out_dir`` is the path of output directory.
 2. Results:

    * ``log.tsv``: a tsv-formatted log file that records training states.
    * ``summary.pdf``: a pdf-formatted file that visualizes the fitting line and optimal point and it will be updated in real time when running.
    * ``summary.tsv``: a tsv-formatted file that shows the raw data of visualization.
    * ``result``: a directory for imputaion results as below:

      * ``imputation.loom``: a `loom-formatted`_ imputed matrix with genes in rows and cells in columns.
      * ``feature.loom``: a `loom-formatted`_ dimensionally reduced feature matrix provided by our method based on the imputed matrix above with feature in rows and cells in columns.
      * ``running_info.hdf5``: a `hdf5-formatted`_ saved some basic information about the input dataset such as library size, genes used for modelling and so on.

    * ``models``: a directory for trained models in every save interval

`Data availability`_
  We provide `loom-formatted`_ original, raw, down-sampled (DS), imputed raw/DS RNA-seq data and FISH data.

  * MELANOMA :
      8,640 cells from the melanoma WM989 cell line were sequenced using Drop-seq, where 32,287 genes were detected (`MELANOMA`_).
      In addition, RNA FISH experiment of across 7,000-88,000 cells from the same cell line was conducted and 26 genes were detected (`MELANOMA_FISH`_).

      The original, raw, DS (0.5), imputed raw/DS RNA-seq data and FISH data are provide `here`__.

        .. __: https://github.com/iyhaoo/DISC_data_availability/tree/master/MELANOMA

  * SSCORTEX :
      Mouse somatosensory cortex of CD-1 mice at age of p28 and p29 were profiled by 10X where 7,477 cells were detected (`SSCORTEX`_).
      In addition, osmFISH experiment of 4,839 cells from somatosensory cortex, hippocampus and ventricle of a CD-1 mouse at age of p22 was conducted and 33 genes were detected (`SSCORTEX_FISH`_).

      The original, raw RNA-seq data and FISH data are provide `here`__.

        .. __: https://github.com/iyhaoo/DISC_data_availability/tree/master/SSCORTEX

  * PBMC :
      2,700 freeze-thaw peripheral blood mononuclear cells (PBMC) from a healthy donor were profiled by 10X, where 32,738 genes were detect (`PBMC`_).

      The  original, raw, DS (0.3), imputed DS RNA-seq data are provide `here`__.

        .. __: https://github.com/iyhaoo/DISC_data_availability/tree/master/PBMC

  * CBMC :
      Cord blood mononuclear cells were profiled by CITE-seq, where 8,005 human cells were detected in total (`CBMC`_).

      The original and raw RNA-seq data are provide `here`__.

        .. __: https://github.com/iyhaoo/DISC_data_availability/tree/master/CBMC

  * RETINA :
      Retinas of mice at age of p14 were profiled in 7 different replicates on by Drop-seq, where 6,600, 9,000, 6,120, 7,650, 7,650, 8280, and 4000 (49,300 in total) STAMPs (single-cell transcriptomes attached to micro-particles) were collected with totally 24,658 genes detected (`RETINA`_).

      The raw RNA-seq data and the `RDS-formatted`_ cluster assignments data from the original study are provide `here`__.

        .. __: https://github.com/iyhaoo/DISC_data_availability/tree/master/RETINA

  * BRAIN_SPLiT :
      156,049 mice nuclei from developing brain and spinal cord at age of p2 or p11 mice were profiled by SPLiT-seq, where 26,894 genes were detected (`BRAIN_SPLiT`_).

      The raw RNA-seq data and the `RDS-formatted`_ cluster assignments data from the original study are provide `here`__.

        .. __: https://github.com/iyhaoo/DISC_data_availability/tree/master/BRAIN_SPLiT

  * BRAIN_1.3M :
      1,306,127 cells from combined cortex, hippocampus, and subventricular zone of 2 E18 C57BL/6 mice were profiled by 10X, where 27998 genes were detected (`BRAIN_1.3M`_).

Tutorials
 1. Data preparation and imputation

    * Data pre-processing (`MELANOMA`__, `SSCORTEX`__, `CBMC`__, `RETINA`__, `BRAIN_SPLiT`__)

      .. __: https://nbviewer.jupyter.org/github/iyhaoo/DISC/blob/master/reproducibility/data_preparation_and_imputation/data_preprocessing_MELANOMA.ipynb
      .. __: https://nbviewer.jupyter.org/github/iyhaoo/DISC/blob/master/reproducibility/data_preparation_and_imputation/data_preprocessing_SSCORTEX.ipynb
      .. __: https://raw.githack.com/iyhaoo/DISC/master/reproducibility/data_preparation_and_imputation/data_preprocessing_CBMC.nb.html
      .. __: https://raw.githack.com/iyhaoo/DISC/master/reproducibility/data_preparation_and_imputation/data_preprocessing_RETINA.nb.html
      .. __: https://nbviewer.jupyter.org/github/iyhaoo/DISC/blob/master/reproducibility/data_preparation_and_imputation/data_preprocessing_BRAIN_SPLiT.ipynb


    * `Run imputation`_

 2. Reproducing our results:

    * Gene expression structures recovery validated by FISH (`MELANOMA`__)

      .. __: https://raw.githack.com/iyhaoo/DISC/master/reproducibility/gene_expression/Gene_expression_structures_recovery_validated_by_FISH_MELANOMA.nb.html

    * Dropout event recovery (`MELANOMA`__)

      .. __: https://raw.githack.com/iyhaoo/DISC/master/reproducibility/gene_expression/Dropout_event_recovery_MELANOMA.nb.html

    * Cell type identification improvement (`PBMC`__)

      .. __: https://raw.githack.com/iyhaoo/DISC/master/reproducibility/cell_type_identification/Cell_type_identification_improvement_PBMC.nb.html

 3. Supplementary topics:

    * Use DISC compressed features for Seurat clustering (`PBMC`__)

      .. __: https://raw.githack.com/iyhaoo/DISC/master/reproducibility/cell_type_identification/Use_DISC_compressed_features_for_Seurat_clustering_PBMC.nb.html

    * Violin plots of marker genes across cell types (`script`__, `PBMC`__, `RETINA`__)

      .. __: https://github.com/iyhaoo/DISC/blob/master/reproducibility/gene_expression/violin_plot.py
      .. __: https://github.com/iyhaoo/DISC/blob/master/reproducibility/results/PBMC/violin_plot.pdf
      .. __: https://github.com/iyhaoo/DISC/blob/master/reproducibility/results/RETINA/violin_plot.pdf

References
----------
Yao He\ :sup:`#`, Hao Yuan\ :sup:`#`, Cheng Wu\ :sup:`#`, Zhi Xie\ :sup:`*`.
**"DISC: a highly scalable and accurate inference of gene expression and structure for single-cell transcriptomes using semi-supervised deep learning."**

History
-------

1.0 (2019-12-16)
^^^^^^^^^^^^^^^^^^
* First release on PyPI_.


.. _Python: https://www.python.org/downloads/
.. _TensorFlow: https://www.tensorflow.org/
.. _numpy: https://numpy.org/
.. _pandas: https://pandas.pydata.org/
.. _h5py: https://www.h5py.org/
.. _`hdf5-formatted`: https://www.hdfgroup.org/solutions/hdf5/
.. _`Data availability`: https://github.com/iyhaoo/DISC_data_availability/
.. _`loom-formatted`: http://loompy.org/
.. _`RDS-formatted`: https://stat.ethz.ch/R-manual/R-devel/library/base/html/readRDS.html
.. _`Run imputation`: https://github.com/iyhaoo/DISC/blob/master/reproducibility/data_preparation_and_imputation/run_imputation.md
.. _PyPI: https://pypi.org/project/disc/
.. _MELANOMA: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE99330
.. _MELANOMA_FISH: https://www.dropbox.com/s/ia9x0iom6dwueix/fishSubset.txt?dl=0
.. _SSCORTEX: http://loom.linnarssonlab.org/clone/Mousebrain.org.level1/L1_Cortex2.loom
.. _SSCORTEX_FISH: http://linnarssonlab.org/osmFISH/availability/
.. _PBMC: https://support.10xgenomics.com/single-cell-gene-expression/datasets/1.1.0/frozen_pbmc_donor_a
.. _CBMC: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE100866
.. _RETINA: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE63472
.. _BRAIN_SPLiT: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110823
.. _BRAIN_1.3M: https://support.10xgenomics.com/single-cell-gene-expression/datasets/1.3.0/1M_neurons
