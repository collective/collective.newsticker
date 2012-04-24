# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter, getUtility
from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory

from plone.app.layout.viewlets.interfaces import IAboveContent
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

from collective.newsticker.interfaces import INewsTickerLayer
from collective.newsticker.browser import NewsTicker_Viewlet
from collective.newsticker.controlpanel import INewsTickerSettings
from collective.newsticker.testing import INTEGRATION_TESTING


class BrowserTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, INewsTickerLayer)

        registry = getUtility(IRegistry)
        vocab_util = getUtility(IVocabularyFactory,
                          name='collective.newsticker.NewsSources')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', id='doc',
                                  title=u"Document Lorem Ipsum")
        self.doc = self.portal['doc']
        self.doc.reindexObject()
        self.portal.invokeFactory('Topic', id='news',
                                  title=u"News Collection Lorem Ipsum")
        self.news = self.portal['news']
        type_crit = self.news.addCriterion('Type', 'ATPortalTypeCriterion')
        type_crit.setValue(['Page', 'Collection'])
        self.news.setLayout('folder_summary_view')
        self.news.reindexObject()

        self.settings = registry.forInterface(INewsTickerSettings)
        self.vocabulary = vocab_util(self.portal)

        catalog = getToolByName(self.portal, 'portal_catalog')
        results = catalog({'Type': 'Collection'})
        self.settings.html_source = results[0].getPath()

    def test_newsticker_api_view(self):
        view = getMultiAdapter((self.portal, self.request),
                               name='newsticker_api')
        self.assertEqual(view.settings.controls, False)
        self.assertEqual(view.settings.html_source, '/plone/news')
        speed = "%d.1" % view.settings.speed
        self.assertEqual(speed, "0.1")
        self.assertEqual(view.settings.pauseOnItems, 2000)
        self.assertEqual(view.settings.titleText, u"Latest")

        self.assertTrue(self.vocabulary.getTerm(view.settings.html_source))

    def test_newsticker_js_view(self):
        view = getMultiAdapter((self.portal, self.request),
                               name='newsticker.js')
        self.assertTrue(view())
        default_js = u'jq(document).ready(function() {' + \
                     u'\n        var config_data = {' + \
                     u'\n"controls": false, ' + \
                     u'\n"feedType": "xml", ' + \
                     u'\n"htmlFeed": true, ' + \
                     u'\n"pauseOnItems": 2000, ' + \
                     u'\n"speed": 0.10000000000000001, ' + \
                     u'\n"titleText": "Latest"' + \
                     u'\n}' + \
                     u'\n        jq("#js-news").ticker(config_data);' + \
                     u'\n        });\n'
        self.assertEqual(default_js, view())

    def test_newsticker_viewlet(self):
        view = getMultiAdapter((self.portal, self.request), name='view')
        viewlet = NewsTicker_Viewlet(self.portal, self.request, view,
                                     IAboveContent)
        self.assertTrue(viewlet.render())
        self.assertTrue(self.doc.title in viewlet.render())
        self.assertTrue(self.news.title in viewlet.render())


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
