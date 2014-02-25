|Build Status| |Coverage Status|

pyconcordion2
=============

A python implementation of the Concordion Acceptance Testing framework.

Installation
------------

``$ pip install pyconcordion2``

Usage
-----

Simply extend your python test cases from ConcordionTestCase

``from pyconcordion2 import ConcordionTestCase``

Execute as you would normal unittests.

Key Differences
---------------

This is not a 100% port of the original Concordion framework. If you
found a differing behaviour please let me know.

Differences:

-  Not possible to link to test data via CSV
-  Extensions are currently not supported.

Development Setup
-----------------

::

    $ git clone git@github.com:johnjiang/pyconcordion2.git
    $ cd pyconcordion2
    $ virtualenv env_concordion
    $ source ./env_concordion/bin/activate
    $ pip install -r requirements.txt
    $ nosetests  # to run tests

License
-------

Copyright 2013 John Jiang

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

::

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Attribution
-----------

Thanks to the `Concordion team`_ for making the original framework.

Thanks to JC Plessis for making `pyconcordion python port`_

Donate Bitcoins
---------------

1AAzqUTiRR68hN81KU3YmtJFLbcmPVM53F

.. _Concordion team: http://www.concordion.org/
.. _pyconcordion python port: https://code.google.com/p/pyconcordion/

.. |Build Status| image:: https://travis-ci.org/johnjiang/pyconcordion2.png
   :target: https://travis-ci.org/johnjiang/pyconcordion2
.. |Coverage Status| image:: https://coveralls.io/repos/johnjiang/pyconcordion2/badge.png
   :target: https://coveralls.io/r/johnjiang/pyconcordion2