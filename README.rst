=============
Django Guitar
=============

.. image:: https://badge.fury.io/py/dj-guitar.svg
    :target: https://badge.fury.io/py/dj-guitar

.. image:: https://travis-ci.org/ppo/dj-guitar.svg?branch=master
    :target: https://travis-ci.org/ppo/dj-guitar

.. image:: https://codecov.io/gh/ppo/dj-guitar/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ppo/dj-guitar


Complementary core components for Django.


Documentation
-------------

@TODO: The full documentation is at https://dj-guitar.readthedocs.io.


Quickstart
----------

Install Django Guitar::

    pip install dj-guitar

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        "guitar.apps.GuitarConfig",
        ...
    )

Add it to the `MIDDLEWARE` list, below all other middleware:

.. code-block:: python

    MIDDLEWARE = [
        ...
        "guitar.middlewares.GuitarMiddleware",
    ]


Features
--------

* @TODO


Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
