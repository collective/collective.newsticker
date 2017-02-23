# -*- coding: utf-8 -*-
from collective.newsticker.testing import INTEGRATION_TESTING
from plone import api
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

import unittest


class VocabulariesTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        with api.env.adopt_roles(['Manager']):
            api.content.create(self.portal, 'Collection', title='foo')

    def test_news_sources_vocabulary(self):
        name = 'collective.newsticker.NewsSources'
        factory = queryUtility(IVocabularyFactory, name)
        self.assertIsNotNone(factory)
        news_sources = factory(None)
        self.assertIn('/plone/foo', news_sources)
