=============================
eras
=============================

.. image:: https://badge.fury.io/py/django-eras.svg
    :target: https://badge.fury.io/py/django-eras

.. image:: https://travis-ci.org/rob-metalinkage/django-eras.svg?branch=master
    :target: https://travis-ci.org/rob-metalinkage/django-eras

.. image:: https://codecov.io/gh/rob-metalinkage/django-eras/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/rob-metalinkage/django-eras

An extension to django-skosxl to describe ordered temportal eras as SKOS Concept Schemes with additional temporal boundary and ordering relationships.

Documentation
-------------

The full documentation is at https://django-eras.readthedocs.io.

Quickstart
----------

Install eras::

    pip install django-eras

Add it to your `INSTALLED_APPS`:

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

Features
--------

* TODO

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
