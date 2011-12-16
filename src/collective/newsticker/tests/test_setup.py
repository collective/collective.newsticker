# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.browserlayer.utils import registered_layers

from collective.newsticker.config import PROJECTNAME
from collective.newsticker.testing import INTEGRATION_TESTING

JS = '++resource++collective.newsticker/jquery.ticker.js'


class InstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.failUnless(qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_installed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('INewsTickerLayer' in layers,
                        'browser layer not installed')

    def test_javascript_installed(self):
        js = getattr(self.portal, 'portal_javascripts')
        self.failUnless(JS in js.getResourceIds(), 'javascript not installed')


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.failIf(self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_installed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('INewsTickerLayer' not in layers,
                        'browser layer not removed')

    def test_javascript_installed(self):
        js = getattr(self.portal, 'portal_javascripts')
        self.failIf(JS in js.getResourceIds(), 'javascript not removed')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
