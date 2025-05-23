Event
=====

The ``Event`` class is designed to represent an event entry from a ROOT TTree, facilitating access
to information by abstracting info into instances of :doc:`Particle <./particle>` class.
Each instance of the ``Event`` class allows to comfortably access those objects such as offline segments, generation-level muons,
simulation digis, showers, and more.

Thanks to how ``Particle`` class was designed, the ``Event`` class can dynamically build particles based 
on specifications from a **configuration file**. This file should contain information about the types 
of particles and how to build them, allowing for flexible and customizable event processing.

To illustrate the dynamic particle-building feature, suppose we want to extract digi information from 
the TTree event's entries when an event is instantiated. This requires specifying the following in 
a `YAML` configuration file under the ``particle_types`` map:

.. rubric:: run_config.yaml

.. code-block:: yaml

    particle_types:
        # ...
        digis:
            amount: 'digi_nDigis'
            branches:
                wh: 'digi_wheel'
                sc: 'digi_sector'
                st: 'digi_station'
                sl: 'digi_superLayer'
                w: 'digi_wire'
                l: 'digi_layer'
                time: 'digi_time'
            attributes:
                BX:
                    expr: 'time // 25 if time is not None else None'
            sorter:
                by: 'p.BX'
    # ...

The ``Event`` class creates **n** instances of the ``Particle`` class, where **n** is determined by the ``amount`` key. 
Attributes are defined using the ``branches`` map, which maps directly from TTree branches, and the ``attributes`` map, 
which allows for computed values using expressions (``expr``) or callable methods (specified via ``src`` key). 
The callable methods must accept the particle instance as an argument, and the expression can access directly to the particle 
instance attribute to any computation.

Additionally, the ``particle_types`` map can manage also the following keys:

- ``class``: Specifies the class path to be used for the particle. If not specified, it defaults to the ``Particle`` class.
- ``filter``: Allows to filter particles based on boolean conditions. These conditions can use the particle instance (referred to as ``p``) and the root event entry (referred to as ``ev``).
- ``sorter``: Sorts particles using Python's ``sorted()``. The ``by`` key specifies the sorting expression (which can also use ``p`` and ``ev``), and ``reverse`` key (default: ``False``) can reverse the order.

For example, to iterate over a TTree and create event instances with particles specified in the 
:download:`configuration file <../../_static/run_config.yaml>`, you can use the following code:

.. literalinclude:: ../../../dtpr/base/event.py
    :language: python
    :dedent:
    :start-after: [start-example-2]

.. rubric:: Output

.. code-block:: text

    >> ------ Event 39956 info ------
    + Index: 0
    + Digis
        * Number of digis: 81
    + Segments
        * Number of segments: 8
    + Tps
        * Number of tps: 21
    + Genmuons
        * Number of genmuons: 2
        * GenMuon 0 info -->
        --> Pt: 258.0812683105469, Eta: -1.9664770364761353, Phi: 0.5708979964256287, Charge: -1, Matched_segments_stations: [], Showered: False
        * GenMuon 1 info -->
        --> Pt: 190.72511291503906, Eta: -0.2504693865776062, Phi: -2.558511257171631, Charge: 1, Matched_segments_stations: [], Showered: False
    + Emushowers
        * Number of emushowers: 0
    + Simhits
        * Number of simhits: 50 

The ``Event`` class is highly flexible and not restricted to TTree data. As demonstrated above, you can
define any type of attributes mapping in the configuration file or even create an empty event instance and then add attributes manually as needed.

.. literalinclude:: ../../../dtpr/base/event.py
    :language: python
    :dedent:
    :start-after: [start-example-1]
    :end-before: [end-example-1]

.. rubric:: Output

.. code-block:: text

    >> ------ Event 1 info ------
    + Index: 1
    >> ------ Event 1 info ------
    + Index: 1
    + Showers
        * Number of showers: 5
    >> Shower 4 info -->
    + Wh: 1, Sc: 1, St: 1

.. autoclass:: dtpr.base.Event
    :members:
    :member-order: bysource
    :private-members: _build_particles
    :special-members: __str__, __getter__,__setter__