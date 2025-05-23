DT Pattern Recognition Package
==============================
This package provides a set of base tools for implementing pattern recognition algorithms for the CMS DT system
using input data in NTuples format. It also includes visualization tools for DT Ntuples, taking into account
the geometrical features of the CMS DT system by using another auxiliary package `mplDTs <https://github.com/DanielEstrada971102/mplDTs>`_.

The core idea of this framework is to simplify the analysis of input data by adopting an event-by-event approach 
using Python classes. This approach makes the code more intuitive and readable. For example:

.. code-block:: python

   for muon in events.genmuons:
      if muon.pt > 5:
         print(muon.eta)

is much clearer compared to the traditional method:

.. code-block:: python

   for i in range(len(tree.gen_pdgID)):
      if tree.gen_pt[i] > 5:
         print(tree.gen_eta[i])

In addition to the event-by-event approach, the framework is designed to be highly flexible, aiming to support various 
data formats since the mapping of input data into Python classes is configurable through a ``YAML`` :download:`configuration file <./_static/run_config.yaml>`, as you will 
see along the different sections. The idea is that this allows users to adapt the framework to their specific needs.

Some useful, and as general as possible, tools using the framework have been implemented to facilitate some common tasks 
such as fill ROOT histograms, or inspect or visualize information from the NTuples. They are accessible through the 
`dtpr` CLI command and are described in the :doc:`src/analysis/main` section. But, reading, manipulating, and mapping
the information from the input files into the respective classes are handled
by central classes, just go around the :doc:`src/base/main` section to know more about them.

Bear in mind that the package is just in its early stages, so feel free to contribute, report bugs, or suggest improvements.
Take a look at the :`Contributors <https://github.com/DanielEstrada971102/DTPatternRecognition/CONTRIBUTING.md>`_ and 
`Developers <https://github.com/DanielEstrada971102/DTPatternRecognition/DEVELOPERS.md>`_ guides.


Installation
------------

First, download the source files or clone the repository:

.. code-block:: shell

   git clone https://github.com/DanielEstrada971102/DTPatternRecognition.git
   cd DTPatternRecognition

You can then install the package with pip by running:

.. code-block:: shell

   pip install .

To check if the package was installed successfully, run:

.. code-block:: shell

   pip show DTPatternRecognition

.. important::
   Be aware that the package requires PyROOT, so you should have it installed. If you are working in
   a Python virtual environment, ensure to include ROOT in it. To do this, use the command:

   .. code-block:: shell

      python -m venv --system-site-packages ROOT ENV_DIR[ENV_DIR ...]


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   src/analysis/main
   src/base/main
   src/particles/main
   src/utils/main