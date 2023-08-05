py-spy-kw: Sampling profiler for Python programs
================================================

py-spy-kw is a project forked from benfred/py-spy
(https://github.com/Rosyuku/py-spy/releases/tag/v0.3.3).

Installation
------------

Prebuilt binary wheels can be installed from PyPI with:

::

    pip install py-spy-kw

Usage
-----

py-spy-kw supports additional one subcommand ``log`` which can output
stack trace jsonfiles of python process automatically every sampling.
Following code is a sample command that launches myprogram.py and
outputs stack trace jsonfiles to ./log 10 times per second until the
process ends.

.. code:: bash

    py-spy-kw log -o ./log -r 10 -- python myprogram.py

.. figure:: ./images/log.png
   :alt: log output

   log output


