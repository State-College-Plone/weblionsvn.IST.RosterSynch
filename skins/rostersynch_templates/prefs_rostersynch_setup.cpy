## Controller Script (Python) "prefs_rostersynch_setup"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.CMFCore.utils import getToolByName
import string

form = context.REQUEST.form
request_ids = form.keys()
skinstool = getToolByName(context, 'portal_skins')

rostersynch_props = getToolByName(context, 'portal_properties')['RosterSynch']

property_map=[(m['id'], m['type']) for m in rostersynch_props.propertyMap() if not m['id']=='title']
kw={}
for id,type in property_map:
    if type == 'boolean':
        if id in request_ids:
            kw[id] = True
        else:
            kw[id] = False
    else:
        if id in request_ids:
            kw[id] = form[id]

rostersynch_props.manage_changeProperties(**kw)

return state.set(portal_status_message = 'Changes Saved')