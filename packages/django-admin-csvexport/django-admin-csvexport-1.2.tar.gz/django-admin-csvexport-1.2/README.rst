=================================
Welcome to django-admin-csvexport
=================================

.. image:: https://travis-ci.com/thomst/django-admin-csvexport.svg?branch=master
   :target: https://travis-ci.com/thomst/django-admin-csvexport

.. image:: https://coveralls.io/repos/github/thomst/django-admin-csvexport/badge.svg?branch=master
   :target: https://coveralls.io/github/thomst/django-admin-csvexport?branch=master


Description
===========
Django-admin-csvexport is a django-admin-action, that allows you to export a
selection of the fields of your models as csv-formatted data.


Features
========
* selectable model-fields
* related models included
* customizable csv-format
* view or download csv-data


Supported Django-versions
=========================
* Django-1.11
* Django-2.0
* Django-2.1
* Django-2.2


Installation
============
Install from pypi.org::

    pip install django-admin-csvexport

Add csvexport to your installed apps::

    INSTALLED_APPS = [
        'csvexport',
        ...
    ]

Add csvexport to the actions of your modeladmin::

    from csvexport.actions import csvexport

    class MyModelAdmin(admin.ModelAdmin):
        ...
        actions = [csvexport]

Configuration
=============
The following settings determine the depth of the model references that will be
regarded and the value to display for empty fields::

    CSV_EXPORT_REFERENCE_DEPTH = 3
    CSV_EXPORT_EMPTY_VALUE = ''
