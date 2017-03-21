# -*- coding: utf-8 -*-
from collective.newsticker.config import PROJECTNAME
from collective.newsticker.config import TITLE_TEXT
from collective.newsticker.controlpanel import INewsTickerSettings
from collective.newsticker.testing import INTEGRATION_TESTING
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']

    def test_controlpanel_view(self):
        request = self.layer['request']
        view = api.content.get_view('newsticker-settings', self.portal, request)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        from plone.app.testing import logout
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@newsticker-settings')

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertIn('collective.newsticker', actions)

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertNotIn('collective.newsticker', actions)


class RegistryTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(INewsTickerSettings)  # noqa: P001

    def test_enabled_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'enabled'))
        self.assertTrue(self.settings.enabled)

    def test_html_source_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'html_source'))
        self.assertIsNone(self.settings.html_source)

    def test_limit_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'limit'))
        self.assertEqual(self.settings.limit, 0)

    def test_titleText_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'titleText'))
        self.assertEqual(self.settings.titleText, TITLE_TEXT)

    def test_displayType_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'displayType'))
        self.assertEqual(self.settings.displayType, 'reveal')

    def test_controls_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'controls'))
        self.assertFalse(self.settings.controls)

    def test_pauseOnItems_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'pauseOnItems'))
        self.assertEqual(self.settings.pauseOnItems, 2000)

    def test_speed_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'speed'))
        self.assertEqual(self.settings.speed, 0.1)

    def test_records_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        records = [
            INewsTickerSettings.__identifier__ + '.html_source',
            INewsTickerSettings.__identifier__ + '.limit',
            INewsTickerSettings.__identifier__ + '.titleText',
            INewsTickerSettings.__identifier__ + '.displayType',
            INewsTickerSettings.__identifier__ + '.controls',
            INewsTickerSettings.__identifier__ + '.pauseOnItems',
            INewsTickerSettings.__identifier__ + '.speed',
        ]

        for r in records:
            self.assertNotIn(r, self.registry)
