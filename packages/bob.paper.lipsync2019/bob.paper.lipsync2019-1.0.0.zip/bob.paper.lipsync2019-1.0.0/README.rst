.. vim: set fileencoding=utf-8 :
.. Thu 23 Jun 13:43:22 2016
.. image:: http://img.shields.io/badge/docs-v1.0.0-yellow.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.paper.lipsync2019/v1.0.0/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.paper.lipsync2019/master/index.html
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.paper.lipsync2019
.. image:: http://img.shields.io/pypi/v/bob.paper.lipsync2019.svg
   :target: https://pypi.python.org/pypi/bob.paper.lipsync2019


===================================================
 Speaker Inconsistency Detection in Tampered Video
===================================================

This package is part of the Bob_ toolkit and it allows to reproduce the experimental results published in the following paper::

    @inproceedings{KorshunovICML2019,
         author = {Korshunov, Pavel and Halstead, Michael and Castan, Diego and Graciarena, Martin and McLaren, Mitchell and Burns, Brian and Lawson, Aaron and Marcel, S{\'{e}}bastien},
       keywords = {inconsistencies detection, lip-syncing, Video tampering},
          month = jul,
          title = {Tampered Speaker Inconsistency Detection with Phonetically Aware Audio-visual Features},
      booktitle = {International Conference on Machine Learning},
         series = {Synthetic Realities: Deep Learning for Detecting AudioVisual Fakes},
           year = {2019},
    }

If you use this package and/or its results, please cite the paper.


Installation
------------

The installation instructions are based on conda_ and works on **Linux** and **Mac OS** systems
only. `Install conda`_ before continuing.

Once you have installed conda_, download the source code of this paper and
unpack it or checkout from Gitlab.  Then, you can create a conda environment with the following
command::

    $ cd bob.paper.lipsync2019
    $ conda env create -f environment.yml
    $ source activate bob.paper.lipsync2019  # activate the environment
    $ python -c "import bob.io.base"  # test the installation
    $ buildout

This will install all the required software to reproduce this paper.


Documentation
-------------

  * `Download databases and generate tampered videos <https://gitlab.idiap.ch/bob/bob.paper.lipsync2019/tree/v1.0.0/doc/databases.rst>`_
  * `Reproduce the experiments <https://gitlab.idiap.ch/bob/bob.paper.lipsync2019/tree/v1.0.0/doc/guide.rst>`_

Contact
-------

For questions or reporting issues to this software package, contact Pavel Korshunov (pavel.korshunov@idiap.ch).


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://www.idiap.ch/software/bob/install
.. _mailing list: https://www.idiap.ch/software/bob/discuss
.. _idiap: https://www.idiap.ch
.. _conda: https://conda.io
.. _install conda: https://conda.io/docs/install/quick.html#linux-miniconda-install

