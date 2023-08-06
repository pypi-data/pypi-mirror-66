========
Overview
========
.. image:: https://travis-ci.com/rorre/Yippi.svg?branch=master
    :target: https://travis-ci.com/rorre/Yippi
.. image:: https://codecov.io/gh/rorre/yippi/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/rorre/yippi

An (a)sync e621 API wrapper library.

* Free software: GNU Lesser General Public License v3 (LGPLv3)

Installation
============

::

    pip install yippi

You can also install the in-development version with::

    pip install git+ssh://git@github.com/rorre/yippi.git@master

Quickstart
==========

Sync
----

::

    >>> from yippi import YippiClient
    >>> client = YippiClient("MyProject", "1.0", "MyUsernameOnE621")
    >>> posts = client.posts("m/m zeta-haru rating:s") # or ["m/m", "zeta-haru", "rating-s"], both works.
    [Post(id=1383235), Post(id=514753), Post(id=514638), Post(id=356347), Post(id=355044)]
    >>> posts[0].tags
    {'artist': ['zeta-haru'],
     'character': ['daniel_segja', 'joel_mustard'],
     'copyright': ['patreon'],
     'general': ['5_fingers', ..., 'spooning'],
     'invalid': [],
     'lore': [],
     'meta': ['comic'],
     'species': ['bird_dog', ... ]}

Async
-----

::

    >>> from yippi import AsyncYippiClient
    >>> client = AsyncYippiClient("MyProject", "1.0", "MyUsernameOnE621")
    >>> posts = await client.posts("m/m zeta-haru rating:s") # or ["m/m", "zeta-haru", "rating-s"], both works.
    [Post(id=1383235), Post(id=514753), Post(id=514638), Post(id=356347), Post(id=355044)]
    >>> posts[0].tags
    {'artist': ['zeta-haru'],
     'character': ['daniel_segja', 'joel_mustard'],
     'copyright': ['patreon'],
     'general': ['5_fingers', ..., 'spooning'],
     'invalid': [],
     'lore': [],
     'meta': ['comic'],
     'species': ['bird_dog', ... ]}
    
Documentation
=============


Documentation is available on readthedocs: https://yippi.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
