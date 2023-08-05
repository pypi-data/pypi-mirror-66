.. -*- mode: rst -*-

|Travis|_ |PyPi|_

.. |Travis| image:: https://travis-ci.com/ocampor/image-quality.svg?branch=master
.. _Travis: https://travis-ci.com/ocampor/image-quality

.. |PyPi| image:: https://img.shields.io/pypi/dm/image-quality?color=blue   :alt: PyPI - Downloads
.. _PyPi: https://pypi.org/project/image-quality/

Image Quality
=============

Description
-----------

Image quality is an open source software library for Automatic Image
Quality Assessment (IQA).

Dependencies
------------

-  Python 3.7
-  LibSVM
-  (Optional) Docker

Installation
------------

The package is public and is hosted in PyPi repository. To install it in
your machine run

::

   pip install image-quality

Example
-------

After installing ``image-quality`` package, you can test that it was
successfully installed running the following commands in a python
terminal.

::

   >>> import imquality.brisque as brisque
   >>> import PIL.Image

   >>> path = 'path/to/image'
   >>> img = PIL.Image.open(path)
   >>> brisque.score(img)
   4.9541572815704455

Report Bugs
-----------

Maintainer
----------

-  Ricardo Ocampo - `me@ocampor.ai`_

.. _me@ocampor.ai: me@ocampor.ai
