# -*- coding: utf-8 -*-
import json

from five import grok
from zope.component import queryUtility
from zope.interface import Interface

from plone.app.layout.viewlets.interfaces import IAboveContent
from plone.app.layout.viewlets.interfaces import IHtmlHeadLinks
from plone.registry.interfaces import IRegistry

from collective.newsticker.controlpanel import INewsTickerSettings
from collective.newsticker.interfaces import INewsTickerLayer

grok.templatedir("templates")


class NewsTicker_Viewlet(grok.Viewlet):
    grok.context(Interface)
    grok.layer(INewsTickerLayer)
    grok.name('collective.newsticker.viewlet')
    grok.order(0)
    grok.require('zope2.View')
    grok.viewletmanager(IAboveContent)


class NewsTicker_API(grok.View):
    grok.context(Interface)
    grok.layer(INewsTickerLayer)
    grok.require('zope2.View')

    def __call__(self):
        self.response.setHeader('Content-Type', 'text/plain')
        return super(NewsTicker_API, self).__call__()

    def __init__(self, *args, **kwargs):
        super(NewsTicker_API, self).__init__(*args, **kwargs)
        registry = queryUtility(IRegistry)
        self.settings = registry.forInterface(INewsTickerSettings)

    def render(self):
        return self.dumps(self.getSettings())

    def getSettings(self, *args, **kwargs):
        settings = dict(
                controls=self.settings.controls,
                titleText=self.settings.titleText,
                feedType='xml',
                htmlFeed=True,
                speed=self.settings.speed,
                pauseOnItems=self.settings.pauseOnItems,
                )
        return settings

    def getItems(self):
        path = self.settings.html_source
        if path:
            collection = self.context.unrestrictedTraverse(path)
            if collection:
                return collection.queryCatalog()
        return []

    def hasItems(self):
        items = self.getItems()
        return len(items) > 0

    def dumps(self, json_var=None, sort_keys=True, indent=0):
        """ """
        if json_var is None:
            json_var = {}
        return json.dumps(json_var, sort_keys=sort_keys, indent=indent)


class NewsTicker_JS(grok.View):
    grok.context(Interface)
    grok.layer(INewsTickerLayer)
    grok.name('newsticker.js')
    grok.require('zope2.View')


class HtmlLinks_Viewlet(grok.Viewlet):
    grok.context(Interface)
    grok.layer(INewsTickerLayer)
    grok.name('collective.newsticker.links')
    grok.viewletmanager(IHtmlHeadLinks)
    grok.require('zope2.View')
