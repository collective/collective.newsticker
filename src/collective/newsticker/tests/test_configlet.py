# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter, getUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles

from plone.registry.interfaces import IRegistry

from collective.newsticker.config import PROJECTNAME, TITLE_TEXT
from collective.newsticker.controlpanel import INewsTickerSettings
from collective.newsticker.testing import INTEGRATION_TESTING


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']

    def test_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name='newsticker-settings')
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                         '@@newsticker-settings')

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertTrue('NewsTickerSettings' in actions)

    def test_controlpanel_removed_on_uninstall(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertTrue('NewsTickerSettings' not in actions)


class RegistryTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(INewsTickerSettings)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_html_source_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'html_source'))
        self.assertEqual(self.settings.html_source, None)

    def test_titleText_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'titleText'))
        self.assertEqual(self.settings.titleText, TITLE_TEXT)

    def test_controls_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'controls'))
        self.assertEqual(self.settings.controls, False)

    def test_pauseOnItems_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'pauseOnItems'))
        self.assertEqual(self.settings.pauseOnItems, 2000)

    def test_speed_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'speed'))
        self.assertEqual(self.settings.speed, 0.1)

    def get_record(self, record):
        """ Helper function; it raises KeyError if the record is not in the
        registry.
        """
        prefix = 'collective.newsticker.controlpanel.INewsTickerSettings.'
        return self.registry[prefix + record]

    def test_records_removed_on_uninstall(self):
        # XXX: I haven't found a better way to test this; anyone?
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        self.assertRaises(KeyError, self.get_record, 'html_source')
        self.assertRaises(KeyError, self.get_record, 'titleText')
        self.assertRaises(KeyError, self.get_record, 'controls')
        self.assertRaises(KeyError, self.get_record, 'pauseOnItems')
        self.assertRaises(KeyError, self.get_record, 'speed')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
