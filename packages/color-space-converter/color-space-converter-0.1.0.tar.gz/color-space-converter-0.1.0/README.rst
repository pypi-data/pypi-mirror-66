=====================
color-space-converter
=====================

Description
-----------

*color-space-converter* enables fast image color space conversion via vectorization from numpy arrays.

|release| |build| |pypi|

Installation
------------

* via pip:
    1. install with ``pip3 install color-space-converter``
    2. type ``color-space-converter -h`` to the command line once installation finished

* from source:
    1. install Python from https://www.python.org/
    2. download the source_ using ``git clone https://github.com/hahnec/color-space-converter.git``
    3. go to the root directory ``cd color_space_converter``
    4. load dependencies ``$ pip3 install -r requirements.txt``
    5. install with ``python3 setup.py install``
    6. if installation ran smoothly, enter ``color-space-converter -h`` to the command line

Command Line Usage
==================

From the root directory of your downloaded repo, you can run the tool by

``color-space-converter -s '../your_path/yourimage.png' -m 'gry'``

on a UNIX system where the result is found at ``../your_path/``. A windows equivalent of the above command is

``color-space-converter --src=".\\your_path\\your_image.png" --method="gry"``

Alternatively, you can specify the method or select your images manually with

``color-space-converter --win --method='yuv'``

More information on optional arguments, can be found using the help parameter

``color-space-converter -h``

Author
------

`Christopher Hahne <http://www.christopherhahne.de/>`__

.. Hyperlink aliases

.. _source: https://github.com/hahnec/color-space-converter/archive/master.zip

.. |vspace| raw:: latex

   \vspace{1mm}

.. Image substitutions

.. |release| image:: https://img.shields.io/github/v/release/hahnec/color-space-converter?style=flat-square
    :target: https://github.com/hahnec/color-space-converter/releases/
    :alt: release

.. |build| image:: https://img.shields.io/travis/com/hahnec/color-space-converter?style=flat-square
    :target: https://travis-ci.com/github/hahnec/color-space-converter

.. |pypi| image:: https://img.shields.io/pypi/dm/color-space-converter?label=PyPI%20downloads&style=flat-square
    :target: https://pypi.org/project/color-space-converter/
    :alt: PyPI Downloads