=====================
collective.newsticker
=====================

.. contents:: Table of Contents

Life, the Universe, and Everything
----------------------------------

News ticker inspired by the one on the `BBC News`_ website.

Features
^^^^^^^^

- jQuery-based, lightweight and easy to use news ticker.

- Configurable via configlet.

- Users have full control on what items to display by using collections.

Mostly Harmless
---------------

.. Note::
   ``collective.newsticker`` is currently compatible with Plone 4.1 only.

.. image:: https://secure.travis-ci.org/collective/collective.newsticker.png?branch=master
    :target: http://travis-ci.org/collective/collective.newsticker

.. image:: https://coveralls.io/repos/collective/collective.newsticker/badge.png?branch=master
    :target: https://coveralls.io/r/collective/collective.newsticker

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

Don't Panic
-----------

Installation
^^^^^^^^^^^^

To enable this product in a buildout-based installation:

1. Edit your buildout.cfg and add ``collective.newsticker`` to the list of
   eggs to install ::

    [buildout]
    ...
    eggs =
        collective.newsticker

2. You may need to extend a five.grok known good set (KGS) to make sure that
   you get the right versions of the packages that make up five.grok ::

    [buildout]
    ...
    extends =
        http://good-py.appspot.com/release/five.grok/1.2.0-1

After updating the configuration you need to run ''bin/buildout'', which will
take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ''collective.newsticker'' and click the 'Activate'
button.

.. Note::

    You may have to empty your browser cache and save your resource registries
    in order to see the effects of the product installation.

Use
^^^

- Open 'News Ticker Settings' configlet on Plone's 'Site Setup'.

- Select the collection containing the items you want to display.

That's it! You will see the items included in the collection on a site-wide
news ticker.

You can click on any item to open it.

Screenshots
^^^^^^^^^^^

.. figure:: https://github.com/collective/collective.newsticker/raw/master/configlet.png
    :align: center
    :height: 530px
    :width: 800px

    The configlet.

.. figure:: https://github.com/collective/collective.newsticker/raw/master/newsticker.png
    :align: center
    :height: 325px
    :width: 800px

    The news ticker in action.

.. _`BBC News`: http://www.bbc.co.uk/news/
.. _`opening a support ticket`: https://github.com/collective/collective.newsticker/issues
