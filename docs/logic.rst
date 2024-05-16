Stream Ordering Logic
=====================

Cascade uses an algorithm based on the academic paper *A Fast Recursive Gis Algorithm For Computing Strahler 
Stream Order In Braided And Nonbraided Networks.* This can be downloaded from :download:`here</files/JAWRA_Paper_03043.pdf>`.

It is based on the second pseudo-code example which takes into account braided networks.

Strahler
--------

Full details of the Strahler algorithm (written in 1957) can be found at http://en.wikipedia.org/wiki/Strahler_number.
In summary all streams start with an order of 1, and will only increase in order when they meet a stream with the
same magnitude. For example if a second order stream meets a third order stream there is no change. 

.. raw:: html

    <div id='map1' class='map'></div>
    <script>
        var options = {
            divName: 'map1',
            permalink: '#map=15/616346.7/939815.8/0',
            layerVisibilities: { 
                'Strahler': true,
                'StrahlerLabels': true
                }
        };
        var widget = MapWidget(options);
    </script>

..
    python -c "import mapscript;r=mapscript.pointObj(-7.7432,55.2053);r.project(mapscript.projectionObj('epsg:4326'), mapscript.projectionObj('epsg:2157'));print(r.toString())"

Shreve
------

The Shreve algorithm (1966) again starts with an order of 1 for each stream, but whenever two streams meet the outflowing stream's order
is the sum of the two input streams.

.. raw:: html

    <div id='map2' class='map'></div>
    <script>
        var options = {
            divName: 'map2',
            permalink: '#map=15/616346.7/939815.8/0',
            layerVisibilities: { 
                'Shreve': true,
                'ShreveLabels': true
                }
        };
        var widget = MapWidget(options);
    </script>

Lakes and Estuaries
-------------------

River networks in Ireland contain features referred to as CONTINUA. These are lines drawn through water bodies, such as 
lakes and estuaries, that allow the river network to remain fully connected. Both the Shreve and Strahler algorithms
treat these lines as any other river segment, so if two continua of the same order join within the waterbody, the resulting 
stream will increase in order. 

.. raw:: html

    <div id='map3' class='map'></div>
    <script>
        var options = {
            divName: 'map3',
            permalink: '#map=16/557782.2/888159.95/0',
            layerVisibilities: { 
                'Shreve': true,
                'ShreveLabels': true
                }
        };
        var widget = MapWidget(options);
    </script>

Below as an example of an estuary (a transitional waterbody):

.. raw:: html

    <div id='map3b' class='map'></div>
    <script>
        var options = {
            divName: 'map3b',
            permalink: '#map=15/576084.42/900358.28/0',
            layerVisibilities: { 
                'Shreve': true,
                'ShreveLabels': true
                }
        };
        var widget = MapWidget(options);
    </script>

Braided Rivers
--------------

Braided rivers, where a stream can split into two downstream segments, can be handled by the stream ordering algorithm. 
For reference two loops were found in the latest river networks. In the example below a segment (``36_2270a``)
splits in two directions. This is handled by the ordering algorithms - both Shreve and Strahler order remain the same. 

.. raw:: html

    <div id='map4' class='map'></div>
    <script>
        var options = {
            divName: 'map4',
            permalink: '#map=15/602518.4/865762.4/0',
            layerVisibilities: { 
                'Shreve': true,
                'ShreveLabels': true,
                'Flow': true
                }
        };
        var widget = MapWidget(options);
    </script>
