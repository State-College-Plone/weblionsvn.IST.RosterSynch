import urllib
import xml.dom.minidom
from operator import itemgetter
from Products.CMFCore.utils import getToolByName

apiaction =""
apiuser = ""
apipwd = ""
courseID = ""

# hit the api and get the xml object
def getRoster(courseID, apiurl):
    data = urllib.urlencode({"strcourse_id":courseID,"apiaction":apiaction,"apiuser":apiuser,"apipwd":apipwd})
    f = urllib.urlopen(apiurl, data)   
    thexml = f.read()
    f.close
    return thexml

# the main function that return either the roster as a list of dictionaries or an error message
def handleRoster(self):
    #set some global vars that all functions will need
    global apiaction, apiuser, apipwd, regTool, context
    context = self    
    # create the prop tool to extract values from the site properties
    propTool = getToolByName(context, 'portal_properties')
    rsProps = propTool['RosterSynch']    
    courseID = rsProps.getProperty('courseID')
    apiurl = rsProps.getProperty('apiurl')
    #write the site properties to the global variables
    regTool = getToolByName(context,'portal_registration')
    addInstructors = rsProps.getProperty('addInstructors')
    addEditors = rsProps.getProperty('addEditors')
    addStudents = rsProps.getProperty('addStudents')
    apiaction = rsProps.getProperty('apiaction')
    apiuser = rsProps.getProperty('apiuser')
    apipwd = rsProps.getProperty('apipwd')
    # check for errors from the api and to make sure that the user has completed RosterSynch Setup, if none, get parsing
    errorMessage = ""
    if apiurl == "" or apiuser == "" or apipwd == "" or courseID == "":
        errorMessage = "Please complete the RosterSynch setup form in Site Setup."
    else:
        # we've got the values we need, get the roster
        src = xml.dom.minidom.parseString(getRoster(courseID, apiurl))
        error = src.getElementsByTagName("error") 
        errorMessage = handleError(error)
    if errorMessage != "":
        return  errorMessage
    else: 
        createGroups()
        createAdditionalUsers(addInstructors, addEditors, addStudents)
        members = src.getElementsByTagName("member")
        roster = handleMembers(members, src, addInstructors, addEditors, addStudents)
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
def handleMembers(members, src, addInstructors, addEditors, addStudents):
    person = {}
    userDicts = []
    userList = []
    i = 0
    for member in members:
        userid = src.getElementsByTagName("user_id")[i].firstChild.data.lower()
        fname = src.getElementsByTagName("fname")[i].firstChild.data.upper()
        lname = src.getElementsByTagName("lname")[i].firstChild.data.upper()
        rights = src.getElementsByTagName("course_rights")[i].firstChild.data
        person = {"userid":userid,"fname":fname,"lname":lname}
        userList.append(userid.encode('ascii','ignore'))
        userDicts.append(person)
        createUser(userid, fname, lname, rights)
        i=i+1
    userDicts = sorted(userDicts, key=itemgetter('lname'))
    #deleteUsers(userList, rights)
    return userDicts

# deals with an error message if one is returned from the xml  
def handleError(messages):
    msg = ""
    for message in messages:
        msg = getText(message.childNodes)
    return msg  

def createAdditionalUsers(addInstructors, addEditors, addStudents):  
    #import pdb; pdb.set_trace()
    addInstructors=addInstructors.split(',')
    addEditors=addEditors.split(',')
    addStudents=addStudents.split(',')
    for userid in addInstructors:
        createUser(userid.strip(), '', '', '32')
    for userid in addEditors:
        createUser(userid.strip(), '', '', '16')
    for userid in addStudents:
        createUser(userid.strip(), '', '', '2')   

# creates the user AND puts her in the correct group
# need to split of group add to another function
def createUser(userid, fname, lname, rights):     
    if rights == '32':
        groupname = 'Instructors'
    elif rights == '16':
        groupname = 'Course Editors'
    else:
        groupname = 'Students'
    allUsers = context.acl_users.source_users.getUserNames()
    groupMembers = context.portal_groups.getGroupMembers(groupname)
    try:
        if userid not in allUsers:
            regTool.addMember(userid,'goober123','', properties={'username':userid,'email':userid+'@psu.edu','fullname': fname +' '+lname})    
    except:
        pass
    try:
        if userid not in groupMembers:
            group = context.portal_groups.getGroupById(groupname)    
            group.addMember(userid)
    except:
        pass
    
def createGroups():
    if not context.portal_groups.getGroupById('Instructors'):
        context.portal_groups.addGroup('Instructors',)
    if not context.portal_groups.getGroupById('Course Editors'):
        context.portal_groups.addGroup('Course Editors',)
    if not context.portal_groups.getGroupById('Students'):
        context.portal_groups.addGroup('Students',)
                
def deleteUsers(angelUsers, rights):
    if rights == '32':
        groupname = 'Instructors'
    elif rights == '16':
        groupname = 'Course Editors'
    else:
        groupname = 'Students'
    mtool = getToolByName(context,'portal_membership')
    siteUsers = context.acl_users.getUserIds()
    for user in siteUsers:
        if user not in angelUsers:
            mtool.deleteMembers(user)
            group = context.portal_groups.getGroupById(groupname)
            group.removeMember(user)
   
