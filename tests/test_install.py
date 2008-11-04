from Products.PloneTestCase import PloneTestCase
from Products.CMFCore.utils import getToolByName


PloneTestCase.installProduct('RosterSynch')
PloneTestCase.setupPloneSite(products=['RosterSynch'])

_layerNames = {'rostersynch_portlets': ['portlet_custom_navigation_example'],
               'rostersynch_external_methods': ['customNavtree']}  # layer names pointing to the contents of their folders in portal_skins


class InstallTestCase(PloneTestCase.PloneTestCase):
    def afterSetUp(self):
        self.skinsTool = getToolByName(self.portal, 'portal_skins')
    
    def _testLayers(self, assertionCallable):
        """Make sure our layers either are (or aren't) registered with every skin (depending on `assertionCallable`)."""
        for skinName in self.skinsTool.getSkinSelections():
            layers = [x.strip() for x in self.skinsTool.getSkinPath(skinName).split(',')]
            for curLayer in _layerNames:
                assertionCallable(curLayer in layers)


class TestInstall(InstallTestCase):
    def testPortalSkinsContents(self):
        """Make sure rostersynch_portlets, portlet_custom_navigation_example, etc. got into portal_skins."""
        for curLayer, curContents in _layerNames.iteritems():
            for curContainedItem in curContents:
                try:
                    self.skinsTool[curLayer][curContainedItem]
                except KeyError:
                    self.fail(msg="%s wasn't in portal_skins/%s." % (curContainedItem, curLayer))
    
    def testLayers(self):
        """Make sure our skin layers got registered."""
        self._testLayers(self.failUnless)


class TestUninstall(InstallTestCase):
    def afterSetUp(self):
        InstallTestCase.afterSetUp(self)
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(products=['RosterSynch'])
    
    def testPortalSkinsContents(self):
        """Make sure rostersynch_templates, rostersynch_scripts, etc. are no longer in portal_skins."""
        for curLayer in _layerNames:
            self.failUnlessRaises(KeyError, lambda: self.skinsTool[curLayer])
    
    def testLayers(self):
        """Make sure our skin layers got unregistered."""
        self._testLayers(self.failIf)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstall))
    suite.addTest(makeSuite(TestUninstall))
    return suite
