# -*- coding: utf-8 -*-
from plone import api
from zope.schema.vocabulary import SimpleVocabulary


def NewsSourcesVocabulary(context):
    """Vocabulary with all the collections available on the site.
    We use object path to avoid duplicated tokens.
    """
    # use portal_type instead of object_provides to simplify
    # as we need to suport both, Archetypes and Dexterity
    results = api.content.find(
        portal_type='Collection',
        sort_on='getObjPositionInParent',
    )
    items = []
    for brain in results:
        path = brain.getPath()
        title = brain.Title
        items.append(SimpleVocabulary.createTerm(path, path, title))
    return SimpleVocabulary(items)
