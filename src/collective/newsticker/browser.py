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


class CSSLink_Viewlet(grok.Viewlet):
    grok.context(Interface)
    grok.layer(INewsTickerLayer)
    grok.name('collective.newsticker.csslink')
    grok.viewletmanager(IHtmlHeadLinks)
