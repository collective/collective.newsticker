Changelog
=========

2.1b3 (unreleased)
------------------

- Nothing changed yet.


2.1b2 (2018-04-23)
------------------

- Fix issue with upgrade step rising ``ConfigurationConflictError`` (fixes `#29`_).
  [hvelarde]

- Update screenshots.
  [tkimnguyen]

- Viewlet rendering performance was enhanced.
  [hvelarde]


2.1b1 (2017-03-21)
------------------

- Remove needless default factory for ``titleText`` field.
  [hvelarde]

- Add new field to configlet to control whether or not the ticker will be shown.
  [hvelarde]


2.0b1 (2017-03-06)
------------------

.. Warning::
    This version is not compatible with previous ones.
    If you want to upgrade, uninstall the previous version before installing this one.

- Make package compatible with Plone 5.
  [rodfersou, agnogueira]

- Add support to control animation type.
  [hvelarde]

- Register CSS on resource registry.
  [hvelarde]

- Update Brazilian Portuguese and Spanish translations.
  [hvelarde]

- Make control panel configlet accesible to Site Administrator role.
  [hvelarde]

- Allow limiting collection results (closes `#6`_).
  [hvelarde]

- Remove dependency on five.grok.
  [hvelarde]

- Drop support for Python 2.6 and Plone 4.1;
  Remove dependency on unittest2.
  [hvelarde]

- Miscelaneous fixes.
  [lepri]


1.0rc1 (2012-04-24)
-------------------

- Initial release.

.. _`#6`: https://github.com/collective/collective.newsticker/issues/6
.. _`#29`: https://github.com/collective/collective.newsticker/issues/29
