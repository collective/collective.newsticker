# -*- coding: utf-8 -*-
from collective.newsticker.controlpanel import INewsTickerSettings
from plone.app.layout.viewlets.common import ViewletBase
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility

import json


class NewsTickerViewlet(ViewletBase):
    """The News Ticker."""

    def update(self):
        registry = queryUtility(IRegistry)
        self.settings = registry.forInterface(INewsTickerSettings)  # noqa: P001

    @property
    def get_settings(self):
        settings = dict(
            controls=self.settings.controls,
            displayType=self.settings.displayType,
            debugMode=False,
            pauseOnItems=self.settings.pauseOnItems,
            speed=self.settings.speed,
            titleText=self.settings.titleText,
        )
        return json.dumps(settings, indent=2)

    @property
    def get_items(self):
        path = self.settings.html_source
        if path:
            collection = self.context.unrestrictedTraverse(path)
            if collection:
                limit = self.settings.limit
                results = collection.results(batch=False)
                if limit:
                    return results[:limit]
                return results
        return []

    @property
    def enabled(self):
        return self.settings.enabled and len(self.get_items) > 0
