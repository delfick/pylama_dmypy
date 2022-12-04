Pylama dmypy
============

A linter plugin for pylama that makes it aware of dmypy

https://mypy.readthedocs.io/en/stable/mypy_daemon.html

Installation
------------

Install it into your environment::

    > python -m pip install pylama-dmypy

Then configure your pylama to use the ``dmypy`` linter.

Changelog
---------

.. _release-0.4:

0.4 - 4 December 2022
    * Increase speed using a results cache. Now dmypy runs only once and each
      file will get warnings/errors from that cached result

.. _release-0.3:

0.3 - 2 April 2022
    * Updated pylama and mypy

.. _release-0.2:

0.2 - 27 January 2022
    * fixed the setup.py

.. _release-0.1:

0.1 - 27 January 2022
    * Creation
