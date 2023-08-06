=========
fountains
=========

Python library for generating and embedding in a compact way random but reproducible data for unit testing.

.. image:: https://badge.fury.io/py/fountains.svg
   :target: https://badge.fury.io/py/fountains
   :alt: PyPI version and link.

Purpose
-------
This library makes it possible to generate random test data in a reproducible way, as well as facilities for including very concise (i.e., one-line) test definitions that nevertheless test a function on a large number of inputs.

Package Installation and Usage
------------------------------
The package is available on PyPI::

    python -m pip install fountains

The library can be imported in the usual ways::

    import fountains
    from fountains import *
