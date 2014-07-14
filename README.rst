==================
Facebook Connector
==================

This project is a Facebook module for Django Trigger Happy


Requirements :
==============
* django_th: 0.9.0
* facebook-sdk 0.4.0


Installation:
=============
to get the project, from your virtualenv, do :

.. code:: python

    pip install django-th-facebook
    
then do

.. code:: python

    python manage.py syncdb

to startup the database

Parameters :
============
As usual you will setup the database parameters.

Important parts are the settings of the available services :

Settings.py 
-----------

INSTALLED_APPS
~~~~~~~~~~~~~~

add the module th_rss to INSTALLED_APPS

.. code:: python

    INSTALLED_APPS = (
        'th_facebook',
    )    


TH_SERVICES 
~~~~~~~~~~~

TH_SERVICES is a list of the services used by Trigger Happy

.. code:: python

    TH_SERVICES = (
        'th_facebook.my_facebook.ServiceFacebook',
    )

TH_FACEBOOK
~~~~~~~~~~~
TH_FACEBOOK is the settings you will need to be able to add/read data in/from Facebook Service.

.. code:: python

    TH_FACEBOOK = {
        'app_id': '1234456576',
        'app_secret': 'abcdefghjkilmonpqert',
        'permissions': {'email','publish_actions','read_stream'}
    }


Setting up : Administration
===========================

once the module is installed, go to the admin panel and activate the service facebook. 

All you can decide here is to tell if the service requires an external authentication or not.

Once they are activated. User can use them.
