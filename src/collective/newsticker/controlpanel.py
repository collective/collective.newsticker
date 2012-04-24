# -*- coding: utf-8 -*-

from five import grok
from zope import schema

from zope.interface import Interface, provider
from zope.schema.interfaces import IContextAwareDefaultFactory
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.site.hooks import getSite

from plone.app.registry.browser import controlpanel

from Products.ATContentTypes.interfaces import IATTopic
from Products.CMFPlone.utils import getToolByName

from collective.newsticker import _
from collective.newsticker.config import TITLE_TEXT


@provider(IContextAwareDefaultFactory)
def default_title_text(context):
    """ HACK: this method is to avoid "AttributeError: translate" on tests.
    """
    site = getSite()
    if hasattr(site, 'translate'):  # runtime
        return site.translate(TITLE_TEXT)
    else:  # tests
        return TITLE_TEXT


class INewsTickerSettings(Interface):
    """Interface for the form on the control panel.
    """
    html_source = schema.Choice(
        title=_(u'News ticker source'),
        description=_('help_html_source',
                      default=u'Select a collection from the list. Query '
                      'results will be used as the source for the news '
                      'ticker.'),
        required=True,
        vocabulary=u'collective.newsticker.NewsSources',
        )

    titleText = schema.TextLine(
        title=_(u'Title text'),
        description=_('help_title_text',
                      default=u'To remove the title set this to an empty '
                               'string.'),
        required=True,
        defaultFactory=default_title_text,
        missing_value=u'',
        )

    speed = schema.Float(
        title=_(u'Display speed'),
        description=_('help_speed',
                      u'The speed at which the ticker items appear on the '
                       'screen. Values go from 0.0 - 1.0.'),
        required=True,
        default=0.10,
        min=0.0,
        max=1.0,
        )

    pauseOnItems = schema.Int(
        title=_(u'Time items appear on screen'),
        description=_('help_pause_on_items',
                      u'The time, in miliseconds (ms), that each '
                       'ticker item appears on the screen.'),
        required=True,
        default=2000,
        min=0,
        )

    controls = schema.Bool(
        title=_(u'Controls'),
        description=_('help_controls',
                      default=u'Whether or not to show the jQuery News '
                               'Ticker controls.'),
        default=False,
        )


class NewsSourcesVocabulary(object):
    """ Creates a vocabulary with all the collections (topics) available on
    the site. We use object path to avoid duplicated tokens.
    """
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        site = getSite()
        catalog = getToolByName(site, 'portal_catalog')
        collections = catalog(object_provides=IATTopic.__identifier__,
                              sort_on='getObjPositionInParent')

        items = []
        for collection in collections:
            path = collection.getPath()
            title = collection.Title
            items.append(SimpleVocabulary.createTerm(path, path, title))
        return SimpleVocabulary(items)

grok.global_utility(NewsSourcesVocabulary,
                    name=u'collective.newsticker.NewsSources')


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
