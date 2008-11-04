from cStringIO import StringIO

from OFS.Folder import manage_addFolder
from Products.CMFCore.utils import getToolByName
from Products.ExternalMethod.ExternalMethod import manage_addExternalMethod
#from Products.WebLionLibrary.skins import deleteLayers
from Products.RosterSynch.config import *
try:
    from Products.CMFCore.permissions import ManagePortal
except:
    from Products.CMFCore.CMFCorePermissions import ManagePortal
    
_externalMethodsFolderId = 'rostersynch_external_methods'

def _skinsTool(portal):
    return getToolByName(portal, 'portal_skins')

def _importProfile(portal, profile):
    setupTool = getToolByName(portal, 'portal_setup')
    
    if hasattr(setupTool, 'runAllImportStepsFromProfile'):  # Plone 3.0
        setupTool.runAllImportStepsFromProfile(profile)
    else:  # Plone 2.5
        oldContextId = setupTool.getImportContextID()
        setupTool.setImportContext(profile)
        setupTool.runAllImportSteps()
        setupTool.setImportContext(oldContextId)

def install(portal):
    out = StringIO()
    print >>out, "Creating RosterSynch External Method..."
    skinsTool = _skinsTool(portal)
    manage_addFolder(skinsTool, _externalMethodsFolderId)
    manage_addExternalMethod(skinsTool[_externalMethodsFolderId], 'RosterSynch', 'RosterSynch', 'RosterSynch.Synch', 'handleRoster')
   
     # Add Configlet - Delete old version before adding, if exist one.
    controlpanel_tool = getToolByName(portal, 'portal_controlpanel')
    controlpanel_tool.unregisterConfiglet(CONFIGLET_ID)
    controlpanel_tool.registerConfiglet(id=CONFIGLET_ID, name=CONFIGLET_NAME, category='Products',
                                        action='string:${portal_url}/%s' % CONFIGLET_ID,
                                        appId=PRODUCT_NAME, permission=ManagePortal, imageUrl='group.gif')
   
   
    # add Property sheet to portal_properies
    pp = getToolByName(portal, 'portal_properties')
    if not 'RosterSynch' in pp.objectIds():
        pp.addPropertySheet(id='RosterSynch', title= '%s Properties' % 'RosterSynch')
        out.write("Adding %s property sheet to portal_properies\n" % 'RosterSynch' )
    props_sheet = pp['RosterSynch']
    updateProperties(props_sheet, out, PROPERTIES) 
       
    print >>out, "Importing GenericSetup profile..."
    _importProfile(portal, 'profile-Products.RosterSynch:default')
    print >>out, "Successfully installed RosterSynch."
    return out.getvalue()


def updateProperties(pp_ps, out, *args):
    for prop in args:
        for prop_id, prop_value, prop_type in prop:
            if not pp_ps.hasProperty(prop_id):
                pp_ps.manage_addProperty(prop_id, prop_value, prop_type)
                out.write("Adding %s property to %s property sheet\n" % (prop_id, 'RosterSynch'))

def deleteLayers(skinsTool, layersToDelete):
    """ 
        Taken directly from WebLionLibrary to remove that dependency.  
        This was the only function being used from WLL.
    """
    # Thanks to SteveM of PloneFormGen for a good example.
    for skinName in skinsTool.getSkinSelections():
        layers = [x.strip() for x in skinsTool.getSkinPath(skinName).split(',')]
        try:
            for curLayer in layersToDelete:
                layers.remove(curLayer)
        except ValueError:  # thrown if a layer ain't in there
            pass
        skinsTool.addSkinSelection(skinName, ','.join(layers))  # more like "set" than "add"

def uninstall(portal):
    out = StringIO()

    print >>out, "Running 'uninstall' GenericSetup profile..."
    _importProfile(portal, 'profile-Products.RosterSynch:uninstall')
    
    # Remove layers, since GenericSetup doesn't support doing it through a profile yet:
    print >>out, "Removing layers from portal_skins..."
    deleteLayers(_skinsTool(portal), ['rostersynch_templates', _externalMethodsFolderId])
    
    # Remove configlet
    controlpanel_tool = getToolByName(portal, 'portal_controlpanel')
    controlpanel_tool.unregisterConfiglet(CONFIGLET_ID)
    # Remove Product's property sheet from portal_properties
    pp = getToolByName(portal, 'portal_properties')
    if 'RosterSynch' in pp.objectIds():
        pp.manage_delObjects(ids=['RosterSynch'])
       
    print >>out, "Successfully uninstalled RosterSynch."
    return out.getvalue()
