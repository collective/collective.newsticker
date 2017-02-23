# -*- coding: utf-8 -*-
from collective.newsticker.config import PROJECTNAME
from collective.newsticker.interfaces import INewsTickerLayer
from collective.newsticker.testing import INTEGRATION_TESTING
from collective.newsticker.testing import IS_PLONE_5
from plone.browserlayer.utils import registered_layers

import unittest


JS = '++resource++collective.newsticker/jquery.ticker.js'


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer(self):
        self.assertIn(INewsTickerLayer, registered_layers())

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_jsregistry(self):
        resource_ids = self.portal['portal_javascripts'].getResourceIds()
        self.assertIn(JS, resource_ids)


class UninstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_removed(self):
        self.assertNotIn(INewsTickerLayer, registered_layers())

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_jsregistry_removed(self):
        resource_ids = self.portal['portal_javascripts'].getResourceIds()
        self.assertNotIn(JS, resource_ids)
