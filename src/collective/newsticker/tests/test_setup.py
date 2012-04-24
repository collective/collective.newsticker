# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.browserlayer.utils import registered_layers

from collective.newsticker.config import PROJECTNAME
from collective.newsticker.testing import INTEGRATION_TESTING


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_installed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('INewsTickerLayer' in layers,
                        'Browser layer not installed')

    def test_javascript_installed(self):
        portal_javascripts = self.portal['portal_javascripts']
        js = portal_javascripts.getResourceIds()
        self.assertTrue('++resource++collective.newsticker/jquery.ticker.js' in js,
                        'JavaScript not installed')


class UninstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_uninstalled(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('INewsTickerLayer' not in layers,
                        'Browser layer not removed')

    def test_javascript_uninstalled(self):
        portal_javascripts = self.portal['portal_javascripts']
        js = portal_javascripts.getResourceIds()
        self.assertFalse('++resource++collective.newsticker/jquery.ticker.js' in js,
                        'JavaScript not removed')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
