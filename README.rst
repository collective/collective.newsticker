.. image:: https://raw.githubusercontent.com/collective/collective.newsticker/master/docs/newsticker.png
    :align: left
    :alt: News Ticker
    :height: 128px
    :width: 128px

***********
News Ticker
***********

.. contents:: Table of Contents

Life, the Universe, and Everything
==================================

A horizontal, text-based display dedicated to presenting headlines on a site.

Features
--------

- jQuery-based, lightweight and easy to use

- Configurable via configlet

- Users have full control on what items to display by using collections

Mostly Harmless
===============

.. image:: http://img.shields.io/pypi/v/collective.newsticker.svg
   :target: https://pypi.python.org/pypi/collective.newsticker

.. image:: https://img.shields.io/travis/collective/collective.newsticker/master.svg
    :target: http://travis-ci.org/collective/collective.newsticker

.. image:: https://img.shields.io/coveralls/collective/collective.newsticker/master.svg
    :target: https://coveralls.io/r/collective/collective.newsticker

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/collective/collective.newsticker/issues

Don't Panic
===========

Installation
------------

To enable this product in a buildout-based installation:

1. Edit your buildout.cfg and add ``collective.newsticker`` to the list of eggs to install:

.. code-block:: ini

    [buildout]
    ...
    eggs =
        collective.newsticker

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ''News Ticker'' and click the 'Activate' button.

Usage
-----

- Open 'News Ticker' configlet on Plone's 'Site Setup'.

- Select the collection containing the items you want to display.

That's it! You will see the items included in the collection on a site-wide news ticker.

You can click on any item to open it.

Screenshots
-----------

.. figure:: https://github.com/collective/collective.newsticker/raw/master/configlet.png
    :align: center
    :height: 530px
    :width: 800px

    The configlet.

.. figure:: https://github.com/collective/collective.newsticker/raw/master/newsticker.png
    :align: center
    :height: 325px
    :width: 800px

    The News Ticker in action.

.. _`BBC News`: http://www.bbc.co.uk/news/
