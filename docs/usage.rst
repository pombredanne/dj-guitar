=====
Usage
=====

To use Django Guitar in a project, add it to your `INSTALLED_APPS`:

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
