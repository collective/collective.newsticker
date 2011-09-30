# -*- coding: utf-8 -*-

from zope import schema
from zope.component.hooks import getSite
from zope.interface import Interface, provider
from zope.schema.interfaces import IContextAwareDefaultFactory

from plone.app.registry.browser import controlpanel

from collective.newsticker import _
from collective.newsticker import config


@provider(IContextAwareDefaultFactory)
def default_feed_url(context):
    site = getSite()
    # FIXME: figure out the address of the default RSS feed
    return u'%s/news/aggregator' % site.absolute_url()


class INewsTickerSettings(Interface):
    """Interface for the form on the control panel.
    """

    title_text = schema.TextLine(
        title=_(u'Title text'),
        description=_('help_title_text',
                      default=u'To remove the title set this to an empty '
                               'string.'),
        required=True,
        default=config.TITLE_TEXT,
        )

    feed_url = schema.TextLine(
        title=_(u'Feed URL'),
        description=_('help_feed_url',
                      default=u'The URL of the feed. Must be on the same '
                               'domain as the ticker.'),
        required=True,
        defaultFactory=default_feed_url,
        )

    controls = schema.Bool(
        title=_(u'Controls'),
        description=_('help_controls',
                      default=u'Whether or not to show the jQuery News Ticker '
                               'controls.'),
        required=True,
        default=config.CONTROLS,
        )


class NewsTickerSettingsEditForm(controlpanel.RegistryEditForm):
    schema = INewsTickerSettings
    label = _(u'News Ticker Settings')
    description = _(u'Here you can modify the settings for '
                     'collective.newsticker.')

    def updateFields(self):
        super(NewsTickerSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(NewsTickerSettingsEditForm, self).updateWidgets()


class NewsTickerConfiglet(controlpanel.ControlPanelFormWrapper):
    form = NewsTickerSettingsEditForm
