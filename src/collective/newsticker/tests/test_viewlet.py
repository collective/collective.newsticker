# -*- coding: utf-8 -*-
from collective.newsticker.controlpanel import INewsTickerSettings
from collective.newsticker.interfaces import INewsTickerLayer
from collective.newsticker.testing import INTEGRATION_TESTING
from lxml import etree
from plone import api
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView as View
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager

import unittest


class BrowserTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, INewsTickerLayer)

        self.populate()
        self.viewlet = self.get_viewlet(self.portal)

    def populate(self):
        with api.env.adopt_roles(['Manager']):
            api.content.create(self.portal, 'News Item', title=u'Lorem Ipsum')
            api.content.create(self.portal, 'News Item', title=u'Neque Porro')
            self.collection = api.content.create(
                self.portal, 'Collection', title=u'News Items')

        query = [{
            'i': 'portal_type',
            'o': 'plone.app.querystring.operation.selection.is',
            'v': ['News Item'],
        }]
        self.collection.setQuery(query)
        self.collection.reindexObject()

        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(INewsTickerSettings)  # noqa: P001
        self.settings.html_source = self.collection.absolute_url_path()

    def get_viewlet_manager(self, context, name='plone.abovecontent'):
        request = self.request
        view = View(context, request)
        manager = getMultiAdapter(
            (context, request, view), IViewletManager, name)
        return manager

    def get_viewlet(self, context, name='collective.newsticker'):
        manager = self.get_viewlet_manager(context)
        manager.update()
        viewlet = [v for v in manager.viewlets if v.__name__ == name]
        assert len(viewlet) == 1
        return viewlet[0]

    def test_newsticker(self):
        html = etree.HTML(self.viewlet())
        self.assertTrue(
            html.xpath('//a')[0].attrib['href'].endswith('lorem-ipsum'))
        self.assertTrue(
            html.xpath('//a')[1].attrib['href'].endswith('neque-porro'))

        self.assertIn('"controls": false', html.xpath('//script')[0].text)
        self.assertIn('"debugMode": false', html.xpath('//script')[0].text)
        self.assertIn('"displayType": "reveal"', html.xpath('//script')[0].text)
        self.assertIn('"pauseOnItems": 2000', html.xpath('//script')[0].text)
        self.assertIn('"speed": 0.1', html.xpath('//script')[0].text)
        self.assertIn('"titleText": "Latest"', html.xpath('//script')[0].text)

    def test_newsticker_enabled(self):
        newsticker = self.viewlet
        self.assertTrue(newsticker.enabled)
        self.settings.enabled = False
        self.assertFalse(newsticker.enabled)

    def test_newsticker_get_items(self):
        newsticker = self.viewlet
        self.assertEqual(len(newsticker.get_items), 2)
        self.assertEqual(newsticker.get_items[0].Title(), 'Lorem Ipsum')
        self.assertEqual(newsticker.get_items[1].Title(), 'Neque Porro')

        # limit must be honored
        self.settings.limit = 1
        self.assertEqual(len(newsticker.get_items), 1)
        self.assertEqual(newsticker.get_items[0].Title(), 'Lorem Ipsum')

    def test_newsticker_get_settings(self):
        import json
        newsticker = self.viewlet
        settings = json.loads(newsticker.get_settings)
        self.assertFalse(settings['controls'])
        self.assertFalse(settings['debugMode'])
        self.assertEqual(settings['displayType'], 'reveal')
        self.assertEqual(settings['pauseOnItems'], 2000)
        self.assertEqual(settings['speed'], 0.1)
        self.assertEqual(settings['titleText'], 'Latest')

    def test_rendering(self):
        html = etree.HTML(self.viewlet())
        self.assertTrue(html.xpath('//div'))
        self.assertTrue(html.xpath('//script'))
        self.settings.enabled = False
        html = etree.HTML(self.viewlet())
        self.assertIsNone(html)
