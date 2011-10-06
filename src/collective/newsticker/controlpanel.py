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
from collective.newsticker import config


@provider(IContextAwareDefaultFactory)
def default_title_text(context):
    site = getSite()
    # HACK: to avoid "AttributeError: translate" on tests
    if hasattr(site, 'translate'):  # runtime
        return site.translate(config.TITLE_TEXT)
    else:  # tests
        return config.TITLE_TEXT


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
        vocabulary=u'collective.newsticker.Collections',
        )

    title_text = schema.TextLine(
        title=_(u'Title text'),
        description=_('help_title_text',
                      default=u'To remove the title set this to an empty '
                               'string.'),
        required=True,
        defaultFactory=default_title_text,
        )

    controls = schema.Bool(
        title=_(u'Controls'),
        description=_('help_controls',
                      default=u'Whether or not to show the jQuery News '
                               'Ticker controls.'),
        required=True,
        default=config.CONTROLS,
        )


class CollectionsVocabulary(object):
    """Creates a vocabulary with all the collections (topics) available on the
    site.
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
            items.append(SimpleVocabulary.createTerm(title, path, title))
        return SimpleVocabulary(items)

grok.global_utility(CollectionsVocabulary,
                    name=u'collective.newsticker.Collections')


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
