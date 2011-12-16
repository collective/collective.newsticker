# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.registry import Registry

from Products.CMFCore.utils import getToolByName

from collective.newsticker import config
from collective.newsticker.controlpanel import INewsTickerSettings
from collective.newsticker.testing import INTEGRATION_TESTING

BASE_REGISTRY = 'collective.newsticker.controlpanel.INewsTickerSettings.%s'


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

    def test_controls_record(self):
        record_controls = self.registry.records[
            BASE_REGISTRY % 'controls']
        self.failUnless('controls' in INewsTickerSettings)
        self.assertEquals(record_controls.value, config.CONTROLS)

    def test_html_source_record(self):
        record_html_source = self.registry.records[
            BASE_REGISTRY % 'html_source']
        self.failUnless('html_source' in INewsTickerSettings)
        self.assertEquals(record_html_source.value, None)

    def test_pauseOnItems_record(self):
        record_pauseOnItems = self.registry.records[
            BASE_REGISTRY % 'pauseOnItems']
        self.failUnless('pauseOnItems' in INewsTickerSettings)
        self.assertEquals(record_pauseOnItems.value, config.PAUSE_ON_ITEMS)

    def test_speed_record(self):
        record_speed = self.registry.records[
            BASE_REGISTRY % 'speed']
        self.failUnless('speed' in INewsTickerSettings)
        self.assertEquals(record_speed.value, config.SPEED)

    def test_titleText_record(self):
        record_titleText = self.registry.records[
            BASE_REGISTRY % 'titleText']
        self.failUnless('titleText' in INewsTickerSettings)
        self.assertEquals(record_titleText.value, config.TITLE_TEXT)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
