# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.registry import Registry
from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

from collective.newsticker import config
from collective.newsticker.controlpanel import INewsTickerSettings
from collective.newsticker.testing import INTEGRATION_TESTING


class RegistryTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        # set up settings registry
        self.registry = Registry()
        self.registry.registerInterface(INewsTickerSettings)

    def test_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name='newsticker-settings')
        view = view.__of__(self.portal)
        self.failUnless(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                          '@@newsticker-settings')

    def test_action_in_controlpanel(self):
        cp = getToolByName(self.portal, 'portal_controlpanel')
        actions = [a.getAction(self)['id'] for a in cp.listActions()]
        self.failUnless('newsticker' in actions)

    def test_html_source_record(self):
        record_html_source = self.registry.records[
            'collective.newsticker.controlpanel.INewsTickerSettings.html_source']
        self.failUnless('html_source' in INewsTickerSettings)
        self.assertEquals(record_html_source.value, None)

    def test_title_text_record(self):
        record_title_text = self.registry.records[
            'collective.newsticker.controlpanel.INewsTickerSettings.title_text']
        self.failUnless('title_text' in INewsTickerSettings)
        self.assertEquals(record_title_text.value, config.TITLE_TEXT)

    def test_controls_record(self):
        record_controls = self.registry.records[
            'collective.newsticker.controlpanel.INewsTickerSettings.controls']
        self.failUnless('controls' in INewsTickerSettings)
        self.assertEquals(record_controls.value, config.CONTROLS)


from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login


class RegistryUninstallTest(unittest.TestCase):
    """ensure registry is properly uninstalled"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.registry = getUtility(IRegistry)
        # uninstall the package
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[config.PROJECTNAME])
        # run manually uninstall step on registry as this is not yet
        # implemented in the uninstaller
        setup_tool = getToolByName(self.portal, 'portal_setup')
        setup_tool.runImportStepFromProfile('profile-collective.newsticker:uninstall', 'plone.app.registry')

    def test_records_uninstalled(self):
        # Test that the records were removed from the control panel
        records = [
            'collective.nesticker.controlpanel.INewsTickerSettings.html_source'
            'collective.nesticker.controlpanel.INewsTickerSettings.title_text'
            'collective.nesticker.controlpanel.INewsTickerSettings.controls'
            ]
        for r in records:
            self.failIf(r in self.registry)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
