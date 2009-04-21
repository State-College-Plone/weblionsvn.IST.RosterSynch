import urllib
import xml.dom.minidom
from operator import itemgetter
from Products.CMFCore.utils import getToolByName

addInstructors = []
addEditors = []
addStudents = []
apiaction =""
apiuser = ""
apipwd = ""
courseID = ""
context = ""

# hit the api and get the xml object
def getRoster(courseID, apiurl):
    data = urllib.urlencode({"strcourse_id":courseID,"apiaction":apiaction,"apiuser":apiuser,"apipwd":apipwd})
    f = urllib.urlopen(apiurl, data)   
    thexml = f.read()
    f.close
    return thexml

# the main function that return either the roster as a list of dictionaries or an error message
def handleRoster(self):
    context = self    
    # create the prop tool to extract values from the site properties
    propTool = getToolByName(context, 'portal_properties')
    rsProps = propTool['RosterSynch']    
    courseID = rsProps.getProperty('courseID')
    apiurl = rsProps.getProperty('apiurl')
    #populate the global variables from the site properties
    global apiaction, apiuser, apipwd, regTool
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
        createAdditionalUsers(addInstructors, addEditors, addStudents, context)
        members = src.getElementsByTagName("member")
        roster = handleMembers(members, src, regTool, addInstructors, addEditors, addStudents, context)
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
# while we're at it create a list of users to pass to the writeTheACL function to create the groups file
def handleMembers(members, src, regTool, addInstructors, addEditors, addStudents, context):
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
        createUser(userid, fname, lname, rights, context)
        i=i+1
    userDicts = sorted(userDicts, key=itemgetter('lname'))
    #writeTheACL(userList)
    #deleteUsers(userList, rights, context)
    return userDicts

# deals with an error message if one is returned from the xml  
def handleError(messages):
    msg = ""
    for message in messages:
        msg = getText(message.childNodes)
    return msg  

def createAdditionalUsers(addInstructors, addEditors, addStudents, context):  
    #import pdb; pdb.set_trace()
    addInstructors=[addInstructors]
    addEditors=[addEditors]
    addStudents=[addStudents]
    for userid in addInstructors:
        createUser(userid, '', '', '32', context)
    for userid in addEditors:
        createUser(userid, '', '', '16', context)
    for userid in addStudents:
        createUser(userid, '', '', '2', context)   

def createUser(userid, fname, lname, rights, context):  
    if rights == '32':
        groupname = 'Instructors'
    elif rights == '16':
        groupname = 'Course Editors'
    else:
        groupname = 'Students'
    try:
        regTool.addMember(userid,'goober123','', properties={'username':userid,'email':userid+'@psu.edu','fullname': fname +' '+lname})    
        group = context.portal_groups.getGroupById(groupname)
        group.addMember(userid)
    except:
       pass

def deleteUsers(angelUsers, rights, context):
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
   
