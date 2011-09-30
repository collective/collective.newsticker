# -*- coding: utf-8 -*-

PROJECTNAME = 'collective.newsticker'

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from collective.newsticker import _

# based on jQuery News Ticker v1.7 (http://www.jquerynewsticker.com/)
SPEED = 0.10        # The speed of the reveal
AJAX_FEED = True    # Populate jQuery News Ticker via a feed
#FEED_URL = ''      # The URL of the feed (look in controlpanel.py)
                    # **Must be on the same domain as the ticker**
FEED_TYPE = 'xml'   # Currently only XML
HTML_FEED = not AJAX_FEED  # Populate jQuery News Ticker via HTML
DEBUG_MODE = True   # Show some helpful errors in the console or as alerts
                    # **Should be set to False for production sites**
CONTROLS = True     # Whether or not to show the jQuery News Ticker controls
TITLE_TEXT = _(u'Latest')  # To remove the title set this to an empty string

DISPLAY_TYPE = SimpleVocabulary([  # Animation type
    SimpleTerm(value='reveal', title=_(u'Reveal')),
    SimpleTerm(value='fade', title=_(u'Fade')),
    ])

DIRECTION = SimpleVocabulary([  # Ticker direction
    SimpleTerm(value='ltr', title=_(u'Left-to-Right')),
    SimpleTerm(value='rtl', title=_(u'Right-to-Left')),
    ])

PAUSE_ON_ITEMS = 2000   # The pause on a news item before being replaced
FADE_IN_SPEED = 600     # Speed of fade in animation
FADE_OUT_SPEED = 300    # Speed of fade out animation
