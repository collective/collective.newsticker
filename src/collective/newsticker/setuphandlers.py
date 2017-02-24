# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):  # pragma: no cover
        """Do not show on Plone's list of installable profiles."""
        return [
            u'collective.newsticker:uninstall',
        ]
