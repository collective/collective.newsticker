# -*- coding: utf-8 -*-
from collective.newsticker.browser import NewsTicker_Viewlet
from collective.newsticker.controlpanel import INewsTickerSettings
from collective.newsticker.interfaces import INewsTickerLayer
from collective.newsticker.testing import INTEGRATION_TESTING
from plone import api
from plone.app.layout.viewlets.interfaces import IAboveContent
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory

import unittest


class BrowserTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, INewsTickerLayer)  # noqa: D001

        registry = getUtility(IRegistry)
        vocab_util = getUtility(
            IVocabularyFactory, name='collective.newsticker.NewsSources')

        with api.env.adopt_roles(['Manager']):
            self.newsitem = api.content.create(
                self.portal, 'Document', title=u'Lorem Ipsum')
            self.collection = api.content.create(
                self.portal, 'Collection', title=u'News Items')

        query = [{
            'i': 'portal_type',
            'o': 'plone.app.querystring.operation.selection.is',
            'v': ['Document'],
        }]
        self.collection.setQuery(query)
        self.collection.setLayout('folder_summary_view')
        self.collection.reindexObject()

        self.settings = registry.forInterface(INewsTickerSettings)  # noqa: P001
        self.vocabulary = vocab_util(self.portal)
        self.settings.html_source = self.collection.absolute_url_path()

    def test_newsticker_api_view(self):
        view = api.content.get_view('newsticker_api', self.portal, self.request)
        self.assertFalse(view.settings.controls)
        self.assertEqual(view.settings.html_source, '/plone/news-items')
        speed = '%d.1' % view.settings.speed  # noqa: S001
        self.assertEqual(speed, '0.1')
        self.assertEqual(view.settings.pauseOnItems, 2000)
        self.assertEqual(view.settings.titleText, u'Latest')
        self.assertTrue(self.vocabulary.getTerm(view.settings.html_source))

    def test_newsticker_js_view(self):
        view = api.content.get_view('newsticker.js', self.portal, self.request)

        self.assertTrue(view())
        default_js = u'$(document).ready(function() {' + \
                     u'\n        var config_data = {' + \
                     u'\n"controls": false, ' + \
                     u'\n"feedType": "xml", ' + \
                     u'\n"htmlFeed": true, ' + \
                     u'\n"pauseOnItems": 2000, ' + \
                     u'\n"speed": 0.1, ' + \
                     u'\n"titleText": "Latest"' + \
                     u'\n}' + \
                     u'\n        $("#js-news").ticker(config_data);' + \
                     u'\n        });\n'
        self.assertEqual(default_js, view())

    @unittest.expectedFailure
    def test_newsticker_viewlet(self):
        view = api.content.get_view('view', self.portal, self.request)
        viewlet = NewsTicker_Viewlet(
            self.portal, self.request, view, IAboveContent)
        self.assertTrue(viewlet.render())
        self.assertIn(self.newsitem.title, viewlet.render())
        self.assertIn(self.collection.title, viewlet.render())
