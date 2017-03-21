# -*- coding: utf-8 -*-
from collective.newsticker import _
from collective.newsticker.config import TITLE_TEXT
from plone.app.registry.browser import controlpanel
from zope import schema
from zope.interface import Interface


class INewsTickerSettings(Interface):
    """Interface for the form on the control panel."""

    enabled = schema.Bool(
        title=_(u'Enabled?'),
        description=_(
            'help_enabled',
            default=u'Control whether or not the ticker will be shown.'),
        default=True,
    )

    html_source = schema.Choice(
        title=_(u'News Ticker Source'),
        description=_(
            'help_html_source',
            default=u'Select a collection from the list. '
                    u'Results will be used as the source for the News Ticker.'),
        required=True,
        vocabulary=u'collective.newsticker.NewsSources',
    )

    limit = schema.Int(
        title=_(u'Limit Results'),
        description=_(
            'help_limit',
            default=u'Specify the maximum number of items to show. '
                    u'Set to 0 to show all items in the collection.'),
        required=True,
        default=0,
        min=0,
    )

    titleText = schema.TextLine(
        title=_(u'Title Text'),
        description=_(
            'help_title_text',
            default=u'To remove the title set this to an empty string.'),
        required=False,
        default=TITLE_TEXT,
    )

    displayType = schema.Choice(
        title=_(u'Animation Type'),
        description=_(
            'help_display_type',
            default=u'Current options are "reveal" or "fade".'),
        required=True,
        default='reveal',
        values=['reveal', 'fade'],
    )

    speed = schema.Float(
        title=_(u'Display Speed'),
        description=_(
            'help_speed',
            default=u'The speed at which ticker items appear on the screen. '
                    u'Values go from 0.0 - 1.0.'),
        required=True,
        default=0.10,
        min=0.0,
        max=1.0,
    )

    pauseOnItems = schema.Int(
        title=_(u'Time items appear on screen'),
        description=_(
            'help_pause_on_items',
            default=u'The time, in miliseconds (ms), '
                    u'that each ticker item appears on the screen.'),
        required=True,
        default=2000,
        min=0,
    )

    controls = schema.Bool(
        title=_(u'Show Controls?'),
        description=_(
            'help_controls',
            default=u'Whether or not to show the ticker controls.'),
        default=False,
    )


class NewsTickerSettingsEditForm(controlpanel.RegistryEditForm):

    schema = INewsTickerSettings
    label = _(u'News Ticker')
    description = _(u'Here you can modify the settings for collective.newsticker.')


class NewsTickerConfiglet(controlpanel.ControlPanelFormWrapper):

    form = NewsTickerSettingsEditForm
