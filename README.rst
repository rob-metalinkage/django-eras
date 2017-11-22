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

* Eras are extensions of SKOS Concepts, using django-skosxl to handle multi-lingual labels, hierarchies and relationships.
* Eras add start and end times, using a "frame" that defines how times translate to years - for example Geological eras use a timeframe of millions of years BC (-1000000)
* Era sources are supported files from the django-rdf_io package, and generate a new Era Scheme, and associated eras
* a view provides a JSON dump of eras as time intervals (eras with valid start dates) within start,end boundaries
* d3 is used to provide a hierarchical timeline visualisation (json + SVG in the browser)

Sourcing Era definitions
------------------------

The idea is to use externally defined schemes where possible, with URI references to deeper description with historical source materials.

Organising Era Schemes
----------------------

Each scheme supports a simple hierarchy - so if necessary overlapping schemes (such as Bronze age periods in Europe and Asia can co-exist and be visualised in combination as required.
Each scheme has its own "ConceptRank" model it will extract from source data. If URI references for these ranks are provided, then equivalence of these ranking schemes can be asserted. Each scheme may treat these as different levels safely - so there is no absolute requirement for a common top level of a scheme.



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
