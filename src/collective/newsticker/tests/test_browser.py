# -*- coding: utf-8 -*-
from collective.newsticker.browser import NewsTicker_Viewlet
from collective.newsticker.controlpanel import INewsTickerSettings
from collective.newsticker.interfaces import INewsTickerLayer
from collective.newsticker.testing import INTEGRATION_TESTING
from plone import api
from plone.app.layout.viewlets.interfaces import IAboveContent
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory

import unittest


class BrowserTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.pt = self.portal['portal_types']
        directlyProvides(self.request, INewsTickerLayer)  # noqa: D001

        registry = getUtility(IRegistry)
        vocab_util = getUtility(
            IVocabularyFactory, name='collective.newsticker.NewsSources')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(  # noqa: P001
            'Document', id='doc', title=u'Document Lorem Ipsum')
        self.doc = self.portal['doc']
        self.doc.reindexObject()
        self.portal.invokeFactory(  # noqa: P001
            'Collection', id='news', title=u'News Collection Lorem Ipsum')
        self.news = self.portal['news']
        query = [{
            'i': 'portal_type',
            'o': 'plone.app.querystring.operation.selection.is',
            'v': ['Document', 'Collection'],
        }]
        self.news.setQuery(query)
        self.news.setLayout('folder_summary_view')
        self.news.reindexObject()

        self.settings = registry.forInterface(INewsTickerSettings)  # noqa: P001
        self.vocabulary = vocab_util(self.portal)

        catalog = api.portal.get_tool('portal_catalog')
        results = catalog({'Type': 'Collection'})
        self.settings.html_source = results[0].getPath()

    def test_newsticker_api_view(self):
        view = getMultiAdapter((self.portal, self.request),
                               name='newsticker_api')
        self.assertEqual(view.settings.controls, False)
        self.assertEqual(view.settings.html_source, '/plone/news')
        speed = '%d.1' % view.settings.speed  # noqa: S001
        self.assertEqual(speed, '0.1')
        self.assertEqual(view.settings.pauseOnItems, 2000)
        self.assertEqual(view.settings.titleText, u'Latest')

        self.assertTrue(self.vocabulary.getTerm(view.settings.html_source))

    def test_newsticker_js_view(self):
        view = getMultiAdapter((self.portal, self.request),
                               name='newsticker.js')
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
        view = getMultiAdapter((self.portal, self.request), name='view')
        viewlet = NewsTicker_Viewlet(self.portal, self.request, view,
                                     IAboveContent)
        self.assertTrue(viewlet.render())
        self.assertTrue(self.doc.title in viewlet.render())
        self.assertTrue(self.news.title in viewlet.render())
