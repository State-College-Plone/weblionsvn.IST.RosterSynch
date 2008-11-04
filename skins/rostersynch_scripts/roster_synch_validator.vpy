## Controller Script Python "roster_synch_validator"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state  
##bind subpath=traverse_subpath
##parameters=courseID,groupName,groupsFile,apiurl='',apiuser='',apipwd=''
##title=Validate RosterSynch Preferences

if courseID != 'TR_200506S1_ALH245_001' and len(courseID) != 26:
    state.setError('SectionIDLen', '1')      

if chr(32) in groupName:
    state.setError('GroupNameSpace', '1')      

if state.getErrors(): # an error has occurred
    state.setStatus('failure')
    return state.set(portal_warning_message='Warnings:',errs = state.getErrors())

return state # no errors - always return the state