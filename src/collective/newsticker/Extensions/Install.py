# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import getToolByName


def uninstall(portal):
    profile = 'profile-collective.newsticker:uninstall'
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile(profile)
    return "Ran all uninstall steps."
