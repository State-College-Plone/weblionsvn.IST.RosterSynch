import urllib
import xml.dom.minidom
from operator import itemgetter
from Products.CMFCore.utils import getToolByName

# hit the api and get the xml object
def getRoster(courseID, apiurl, apiaction, apiuser, apipwd):
    """Return the xml retrieved from the ANGEL API"""
    data = urllib.urlencode({"strcourse_id":courseID,"apiaction":apiaction,"apiuser":apiuser,"apipwd":apipwd})
    f = urllib.urlopen(apiurl, data)   
    thexml = f.read()
    f.close
    return thexml

# the main function that return either the roster as a list of dictionaries or an error message
def handleRoster(self):
    """Return a dictionary of course roster as found in ANGEL"""
    #set some global vars that all functions will need
    context = self    
    # create the prop tool to extract values from the site properties
    propTool = getToolByName(context, 'portal_properties')
    rsProps = propTool['RosterSynch']    
    courseID = rsProps.getProperty('courseID')
    apiurl = rsProps.getProperty('apiurl')
    regTool = getToolByName(context,'portal_registration')
    apiaction = rsProps.getProperty('apiaction')
    apiuser = rsProps.getProperty('apiuser')
    apipwd = rsProps.getProperty('apipwd')
    # get additional users, strip spaces and turn 'em into lists
    addInstructors = rsProps.getProperty('addInstructors')
    addInstructors = addInstructors.replace(' ','')
    addInstructors = addInstructors.split(',')
    addEditors = rsProps.getProperty('addEditors')
    addEditors = addEditors.replace(' ','')
    addEditors=addEditors.split(',')
    addStudents = rsProps.getProperty('addStudents')
    addStudents = addStudents.replace(' ','')
    addStudents=addStudents.split(',')
    # check for errors from the api and to make sure that the user has completed RosterSynch Setup, if none, get parsing
    errorMessage = ""
    if apiurl == "" or apiuser == "" or apipwd == "" or courseID == "":
        errorMessage = "Please complete the RosterSynch setup form in Site Setup."
    else:
        # we've got the values we need, let's see what the api returned
        # if an error message, display that.  otherwise get on with it
        src = xml.dom.minidom.parseString(getRoster(courseID, apiurl, apiaction, apiuser, apipwd))
        error = src.getElementsByTagName("error") 
        errorMessage = handleError(error)
    if errorMessage != "":
        return  errorMessage
    else: 
        createGroups(context)
        members = src.getElementsByTagName("member")
        roster = handleMembers(members, src, addInstructors, addEditors, addStudents, regTool, context)
        createAdditionalUsers(addInstructors, addEditors, addStudents, regTool, context)
        return roster

# this function extracts and returns the actual text from the xml text node        
def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

#Parse the xml and create a list of user dictionaries with the keys userid, fname and lname 
# sort the dictionaries by last name
# while we're at it create the user if he or she is not already present
def handleMembers(members, src, addInstructors, addEditors, addStudents,regTool, context):
    """Create a dictionary of users found in the ANGEL roster."""
    person = {}
    userDicts = []
    userList = []
    for member in members:
        #import pdb; pdb.set_trace()
        userid = member.getElementsByTagName("user_id")[0].firstChild.data.lower()
        fname = member.getElementsByTagName("fname")[0].firstChild.data.upper()
        lname = member.getElementsByTagName("lname")[0].firstChild.data.upper()
        rights = member.getElementsByTagName("course_rights")[0].firstChild.data
        person = {"userid":userid,"fname":fname,"lname":lname}
        userid = userid.encode('ascii','ignore')
        userList.append(userid)
        userDicts.append(person)
        #create this user
        createUser(userid, fname, lname, rights, regTool, context)
    userDicts = sorted(userDicts, key=itemgetter('lname'))
    #delete any users who are not in ANGEL or additional users
    deleteUsers(userList, addInstructors, addEditors, addStudents, context)
    return userDicts

# deals with an error message if one is returned from the xml  
def handleError(messages):
    """Return the error message received from the ANGEL API"""
    msg = ""
    for message in messages:
        msg = getText(message.childNodes)
    return msg  

#inserts the users added to the Plone site who are not in ANGEL
def createAdditionalUsers(addInstructors, addEditors, addStudents, regTool, context):  
    """Create users that are added to the roster via Plone configlet."""
    #import pdb; pdb.set_trace()
    for userid in addInstructors:
        createUser(userid, '', '', '32', regTool, context)
    for userid in addEditors:
        createUser(userid, '', '', '16', regTool, context)
    for userid in addStudents:
        createUser(userid, '', '', '2', regTool, context)   

def createUser(userid, fname, lname, rights, regTool, context):  
    """Create users and put them in the appropriate groups."""   
    if rights == '32':
        groupname = 'Instructors'
    elif rights == '16':
        groupname = 'CourseEditors'
    else:
        groupname = 'Students'
    allUsers = context.acl_users.source_users.getUserNames()
    groupMembers = context.portal_groups.getGroupMembers(groupname)
    if userid not in allUsers and userid != '' and userid != None:
        regTool.addMember(userid,'goober123','', properties={'username':userid,'email':userid+'@psu.edu','fullname': fname +' '+lname})    
    if userid not in groupMembers and userid != None:
        addUserToGroup(groupname, userid, context)
        
def addUserToGroup(groupname, userid, context):
    group = context.portal_groups.getGroupById(groupname)    
    group.addMember(userid)

# removes a user from all groups (called when a user is deleted)
def removeUserFromAllGroups(userid, context):
    """Remove a user from all groups (called when a user is deleted)"""
    groups=context.portal_groups.getGroupIds()
    for group in groups:
        groupname = context.portal_groups.getGroupById(group)
        groupname.removeMember(userid)
        
# create groups if for some reason they don't exist
def createGroups(context):
    """Create groups required by the ANGEL API"""
    if not context.portal_groups.getGroupById('Instructors'):
        context.portal_groups.addGroup('Instructors',)
    if not context.portal_groups.getGroupById('CourseEditors'):
        context.portal_groups.addGroup('CourseEditors',properties={'title':'Course Editors'})
    if not context.portal_groups.getGroupById('Students'):
        context.portal_groups.addGroup('Students',)
                
def deleteUsers(angelUsers, addInstructors, addEditors, addStudents, context):
    """Remove users who are not in the ANGEL API or explicitley added by the portal roster synch properties."""
    #create a list of all users to compare with site users
    #if in site users, but not in the list nuke 'em
    allUsers = angelUsers
    allUsers.extend(addInstructors)
    allUsers.extend(addEditors)
    allUsers.extend(addStudents)
    mtool = getToolByName(context,'portal_membership')
    siteUsers = context.acl_users.getUserIds()
    for userid in siteUsers:
        if userid not in allUsers:
            mtool.deleteMembers(userid)
            removeUserFromAllGroups(userid, context)

   
