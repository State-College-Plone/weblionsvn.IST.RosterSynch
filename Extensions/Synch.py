import urllib
import xml.dom.minidom
from operator import itemgetter
from Products.CMFCore.utils import getToolByName

addUsers = []
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
    context = self    
    # create the prop tool to extract values from the site properties
    propTool = getToolByName(context, 'portal_properties')
    regTool = getToolByName(context,'portal_registration')
    rsProps = propTool['RosterSynch']    
    courseID = rsProps.getProperty('courseID')
    apiurl = rsProps.getProperty('apiurl')
    #populate the global variables from the site properties
    global addUsers, apiaction, apiuser, apipwd
    addUsers = rsProps.getProperty('addUsers')
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
        members = src.getElementsByTagName("member")
        roster = handleMembers(members, src, regTool, context)
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
def handleMembers(members, src, regTool, context):
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
        createUser(userid, fname, lname, rights, regTool)
        i=i+1
    userDicts = sorted(userDicts, key=itemgetter('lname'))
    #writeTheACL(userList)
    deleteUsers(userList, rights, context)
    return userDicts

# deals with an error message if one is returned from the xml  
def handleError(messages):
    msg = ""
    for message in messages:
        msg = getText(message.childNodes)
    return msg  

def createUser(userid, fname, lname, rights, regTool):  
    if rights == '32':
        role = 'Instructor'
    elif rights == '16':
        role = 'Editor'
    else:
        role = 'Student'
    try:
        #import pdb; pdb.set_trace()
        regTool.addMember(userid,'goober123',(role,), properties={'username':userid,'email':userid+'@psu.edu','fullname': fname +' '+lname})
    except:
       pass

def deleteUsers(angelUsers, rights, context):
    mtool = getToolByName(context,'portal_membership')
    siteUsers = context.acl_users.getUserIds()
    for user in siteUsers:
        if user not in angelUsers:
            mtool.deleteMembers(user)
            
# opens the "groups" file and replaces its contents with the users returned from handleUserIds       
def writeTheACL(users):     
    myfile = open(groupsFile, 'w')
    if admins != "":
        aclString = groupName+": " +" ".join(users).lower()+" " + addUsers.lower()+"\nadmins: " +admins
    else:
         aclString = groupName+": " +" ".join(users).lower()+" " + addUsers.lower()
    myfile.write(aclString)
   
