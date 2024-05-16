Cascade - a Stream Ordering Library
===================================

.. raw:: html

    <div id='map1' class='map'></div>
    <script>
        var options = {
            divName: 'map1',
            permalink: '#map=15/602518.4/865762.4/0',
            layerVisibilities: { 
                'Strahler': true,
                'StrahlerLabels': true
                }
        };
        var widget = MapWidget(options);
    </script>

Cascade is a Python library to assign stream orders to river networks. Classification of streams using orders give an 
indication of the size and strength of rivers, likelihood of flooding, and to help to determine what wildlife may be present.

Stream ordering can be used to:

* sort upstream features based on stream by order, ensuring results along a main channel are given
  priority
* symbolise rivers and to allow subsets of rivers to be shown at different zoom levels
* give a rough indicator of river capacity
* provide categories when reporting on water quality

Installation
------------

.. code-block:: bash

    pip install cascade-rivers


Contents:

.. toctree::
   :maxdepth: 2

   logic
   usage
   output
   recursion
   authors
   code
   history

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

