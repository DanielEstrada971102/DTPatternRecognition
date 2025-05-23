NTuple
========

The ``NTuple`` class serves as a simple gateway to access information from single or multiple ``.root`` 
Ntuples located in the specified input path. It represents an interface to build ``Event`` instances
directly from the TTree event entries automatically. This class is capable of preprocessing, filtering and building ``Event`` 
instances according to the **preprocessors**, and **selectors** passed.

A **preprocessor** refers to a function that takes an ``Event`` instance as input and applies 
any necessary modifications or additions. A **selector** refers to a function that returns a 
boolean based on the information of an ``Event`` passed as input.

The ``NTuple`` class is designed to be generic and handle many types of NTuple formats since ``Event`` creation can be
controlled through a **configuration** ``YAML`` **file**. Internally, the ``NTuple`` class just loads
the ROOT TTrees in a TChain (accessible through the attribute ``tree``), and generates ``Event`` instances
on the fly by demand (accessible through the attribute ``events``), applying the preprocessors
and selectors methods before returning to perform any necessary processing and selecting steps.

The preprocessing feature was implemented in that way to allow creating selectors based on properties that by default
do not come directly from the input NTuples, but can be computed with extra preprocessing functions
steps before applying the selection methods.

The ``NTuple`` class admits specifying the following maps into the configuration file:

- ``ntuple-tree-name``: The name of the TTree to be used. It is supposed to be the same for all the files in the input folder.
- ``ntuple_preprocessors``:  A map containing the preprocessors to be used in the NTuple.
- ``ntuple_selectors``: A map containing the selectors to be used in the NTuple.

Both, preprocessors and selectors maps should contains a ``src`` key that specifies the path to the function
to be used, and optionally, a ``kwargs`` map for additional parameters of the preprocessor.  

.. rubric:: example

.. code-block:: yaml

    #...
    ntuple_tree_name: '/dtNtupleProducer/DTTREE'

    ntuple_preprocessors:
        prepocessor_name: # Any name, not relevant to the codes
            src: 'path.to.preprocessor'
            kwargs: # optional arguments to be passed to the preprocessor
                arg1: value1
            #...

    ntuple_selectors:
        selector_name: # Any name, not relevant to the codes
            src: 'path.to.selector' 
            kwargs: # optional arguments to be passed to the selector
                arg1: value1
        #...

The following example shows how to use the ``NTuple`` class to read DT Ntuples and access events.

.. literalinclude:: ../../../dtpr/base/ntuple.py
    :language: python
    :dedent:
    :start-after: [start-example-1]

.. rubric:: Output

.. code-block:: text

    + Opening input file /root/DTPatternRecognition/test/ntuples/DTDPGNtuple_12_4_2_Phase2Concentrator_thr6_Simulation_99.root
    >> ------ Event 39954 info ------
    + Index: 9
    + Digis
        * Number of digis: 167
    + Segments
        * Number of segments: 21
        * AM-Seg matches:
        --> Segment 1 info -->
            - Wh: -2, Sc: 5, St: 1, Phi: 2.2211668491363525, Eta: -0.9381515979766846
        --> Segment 2 info -->
            - Wh: -2, Sc: 5, St: 1, Phi: 2.2211666107177734, Eta: -0.9440188407897949
        --> Segment 8 info -->
            - Wh: -2, Sc: 5, St: 2, Phi: 2.221505880355835, Eta: -0.9430407881736755
        --> Segment 9 info -->
            - Wh: -2, Sc: 5, St: 2, Phi: 2.2215068340301514, Eta: -0.9163724184036255
        --> Segment 10 info -->
            - Wh: -2, Sc: 12, St: 2, Phi: -0.6958962082862854, Eta: -0.8441917300224304
    + Tps
        * Number of tps: 32
    + Genmuons
        * Number of genmuons: 2
        * GenMuon 1 info -->
        --> Pt: 548.1250610351562, Eta: -0.8365859985351562, Phi: -0.6915670037269592, Charge: 1, Matched_segments_stations: [(2, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (1, 5, -2), (1, 5, -2), (2, 5, -2), (2, 5, -2)], Showered: True
        * GenMuon 0 info -->
        --> Pt: 511.7483215332031, Eta: -0.9357022643089294, Phi: 2.2167818546295166, Charge: -1, Matched_segments_stations: [(2, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (1, 5, -2), (1, 5, -2), (2, 5, -2), (2, 5, -2)], Showered: True
    + Emushowers
        * Number of emushowers: 1
    + Simhits
        * Number of simhits: 188
    + Realshowers
        * Number of realshowers: 3
    <generator object EventList.__getitem__.<locals>.<genexpr> at 0x7ff5a640a740>
    >> ------ Event 39956 info ------
    + Index: 0
    + Digis
        * Number of digis: 81
    + Segments
        * Number of segments: 8
        * AM-Seg matches:
        --> Segment 5 info -->
            - Wh: 0, Sc: 8, St: 1, Phi: -2.5716519355773926, Eta: -0.2304154634475708
        --> Segment 7 info -->
            - Wh: -1, Sc: 8, St: 4, Phi: -2.5743513107299805, Eta: -0.36347508430480957
    + Tps
        * Number of tps: 21
    + Genmuons
        * Number of genmuons: 2
        * GenMuon 0 info -->
        --> Pt: 258.0812683105469, Eta: -1.9664770364761353, Phi: 0.5708979964256287, Charge: -1, Matched_segments_stations: [(2, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (1, 5, -2), (1, 5, -2), (2, 5, -2), (2, 5, -2), (1, 8, 0), (4, 8, -1)], Showered: True
        * GenMuon 1 info -->
        --> Pt: 190.72511291503906, Eta: -0.2504693865776062, Phi: -2.558511257171631, Charge: 1, Matched_segments_stations: [(2, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (3, 12, -2), (1, 5, -2), (1, 5, -2), (2, 5, -2), (2, 5, -2), (1, 8, 0), (4, 8, -1)], Showered: True
    + Emushowers
        * Number of emushowers: 0
    + Simhits
        * Number of simhits: 50
    + Realshowers
        * Number of realshowers: 0
    Event orbit number: -1

.. important::
    
    The ``NTuple.events`` attribute is not a simple list, but an instance of the :doc:`event_list` class.
    This design prevents loading all events into memory simultaneously. Instead, it allows iteration and access by index and slice,
    while internally iterating over the root tree entries to create the required event on the fly.
