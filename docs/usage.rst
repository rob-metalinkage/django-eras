=====
Usage
=====

To use eras in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'eras.apps.ErasConfig',
        ...
    )

Add eras's URL patterns:

.. code-block:: python

    from eras import urls as eras_urls


    urlpatterns = [
        ...
        url(r'^', include(eras_urls)),
        ...
    ]
