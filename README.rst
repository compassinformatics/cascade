===============================
cascade
===============================

.. image:: strahler.png
   :alt: Strahler stream-ordering
   :align: right

| |Version| |Coveralls|

A Python library to assign river order to hydrometric networks. Geospatial networks can be loaded
using https://github.com/compassinformatics/wayfarer/, and then stream ordering can be applied.

* Documentation: https://compassinformatics.github.io/cascade/

Features
--------

Two stream-ordering algorithms:

* Strahler
* Shreve

Installation
------------

.. code-block:: bash

    pip install cascade-rivers

.. |Version| image:: https://img.shields.io/pypi/v/cascade-rivers.svg
   :target: https://pypi.python.org/pypi/cascade-rivers

.. |Coveralls| image:: https://coveralls.io/repos/github/compassinformatics/cascade/badge.svg?branch=main
    :target: https://coveralls.io/github/compassinformatics/cascade?branch=main

.. |Downloads| image:: http://pepy.tech/badge/cascade-rivers
    :target: http://pepy.tech/project/cascade-rivers