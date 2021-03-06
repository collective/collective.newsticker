# -*- coding: utf-8 -*-
from collective.newsticker.testing import INTEGRATION_TESTING

import unittest


class UpgradeTestCaseBase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self, from_version, to_version):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.profile_id = u'collective.newsticker:default'
        self.from_version = from_version
        self.to_version = to_version

    def get_upgrade_step(self, title):
        """Get the named upgrade step."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = [s for s in upgrades[0] if s['title'] == title]
        return steps[0] if steps else None

    def execute_upgrade_step(self, step):
        """Execute an upgrade step."""
        request = self.layer['request']
        request.form['profile_id'] = self.profile_id
        request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=request)

    @property
    def total_steps(self):
        """Return the number of steps in the upgrade."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        assert len(upgrades) > 0
        return len(upgrades[0])


class To2TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'1', u'2')

    def test_upgrade_to_2_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(version, self.to_version)
        self.assertEqual(self.total_steps, 1)

    def test_add_enabled_field_to_configlet(self):
        title = u"Add 'enabled' field to configlet"
        step = self.get_upgrade_step(title)
        self.assertIsNotNone(step)

        from collective.newsticker.controlpanel import INewsTickerSettings
        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility
        registry = getUtility(IRegistry)

        # simulate state on previous version
        record = INewsTickerSettings.__identifier__ + '.enabled'
        del registry.records[record]

        with self.assertRaises(KeyError):
            registry.forInterface(INewsTickerSettings)  # noqa: P001

        # execute upgrade step and verify changes were applied
        self.execute_upgrade_step(step)

        settings = registry.forInterface(INewsTickerSettings)  # noqa: P001
        self.assertTrue(hasattr(settings, 'enabled'))
        self.assertTrue(settings.enabled)
