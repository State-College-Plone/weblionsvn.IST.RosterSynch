import unittest
from Products.RosterSynch.tests.base import RosterSynchTestCase
from Products.RosterSynch.Extensions import Synch
from Products.CMFCore.utils import getToolByName

class TestSetup(RosterSynchTestCase):
    
    def test_createGroups(self):
        self.loginAsPortalOwner()
        
        Synch.createGroups(self.portal)
        self.failUnless("Instructors" in self.portal.portal_groups.getGroupIds(), "createGroups failed -- Instructors not created")
        self.failUnless("CourseEditors" in self.portal.portal_groups.getGroupIds(), "createGroups failed -- CourseEditors not created")
        self.failUnless("Students" in self.portal.portal_groups.getGroupIds(), "createGroups failed -- Students not created")
        self.logout()
    
    def test_createUserAndAddToGroup(self):
        self.loginAsPortalOwner()
        userid = 'user123'
        fname = 'first'     
        lname = 'last'
        rights = '2'
        regTool = getToolByName(self.portal,'portal_registration')
        
        Synch.createGroups(self.portal)
        Synch.createUser(userid, fname, lname, rights, regTool, self.portal) 
        self.failUnless("user123" in self.portal.acl_users.source_users.getUserIds(), "CreateUser failed -- Test student not created")
        self.failUnless("user123" in self.portal.acl_users.source_groups.getGroupMembers('Students'), "AddToGroup failed -- Test student not in student group")
        self.logout()
         
    def test_createAdditionalUsersAndAddToGroup(self):
        self.loginAsPortalOwner()
        addInstructors = ['ins123']
        addEditors = ['edi123']      
        addStudents = ['stu123'] 
        regTool = getToolByName(self.portal,'portal_registration')
        
        Synch.createGroups(self.portal)
        Synch.createAdditionalUsers(addInstructors, addEditors, addStudents, regTool, self.portal)
        self.failUnless("stu123" in self.portal.acl_users.source_users.getUserIds(), "CreateAdditionalUsers failed -- Test student not created")
        self.failUnless("edi123" in self.portal.acl_users.source_users.getUserIds(), "CreateAdditionalUsers failed -- Test editor not created")
        self.failUnless("ins123" in self.portal.acl_users.source_users.getUserIds(), "CreateAdditionalUsers failed -- Test instructor not created")
        self.failUnless("stu123" in self.portal.acl_users.source_groups.getGroupMembers('Students'), "AddToGroup failed -- Test student not in student group")
        self.failUnless("edi123" in self.portal.acl_users.source_groups.getGroupMembers('CourseEditors'), "AddToGroup failed -- Test editor not in course editors group")
        self.failUnless("ins123" in self.portal.acl_users.source_groups.getGroupMembers('Instructors'), "AddToGroup failed -- Test instructor not in Instructors group")    
        self.logout()
    
    def test_deleteUsers(self):
        self.loginAsPortalOwner()
        regTool = getToolByName(self.portal,'portal_registration')
        regTool.addMember('deleteMe','goober123','', properties={'username':'deleteMe','email':'someone@somewhere.com','fullname': 'The Maestro'})
        angelUsers=['abc123','def456']
        addInstructors = ['ins123']
        addEditors = ['edi123']
        addStudents = ['stu123']
        
        Synch.deleteUsers(angelUsers,addInstructors, addEditors, addStudents, self.portal)
        self.failUnless("deleteMe" not in self.portal.acl_users.source_users.getUserIds(), "DeleteUsers failed -- User not deleted")
        self.logout()
        
    def test_removeUserFromAllGroups(self):
        self.loginAsPortalOwner()
        Synch.createGroups(self.portal)
        ins = self.portal.portal_groups.getGroupById("Instructors")
        edi = self.portal.portal_groups.getGroupById("CourseEditors") 
        stu = self.portal.portal_groups.getGroupById("Students")     
        ins.addMember('groupmember')
        edi.addMember('groupmember')
        stu.addMember('groupmember')
        
        Synch.removeUserFromAllGroups('groupmember', self.portal)
        self.failUnless("groupmember" not in self.portal.acl_users.source_groups.getGroupMembers('Students'), "removeUserFromAllGroups failed -- Test student not removed from student group")
        self.failUnless("groupmember" not in self.portal.acl_users.source_groups.getGroupMembers('CourseEditors'), "removeUserFromAllGroups failed -- Test editor not removed from course editors group")
        self.failUnless("groupmember" not in self.portal.acl_users.source_groups.getGroupMembers('Instructors'), "removeUserFromAllGroups failed -- Test instructor not removed from Instructors group")    
        self.logout()
        
    def test_handleRoster(self):
        import urllib
        import xml.dom.minidom
        self.loginAsPortalOwner() 
        propTool = getToolByName(self.portal, 'portal_properties')
        rsProps = propTool['RosterSynch']
        rsProps.manage_changeProperties(courseID='myCourse', addInstructors='ins123',addEditors='edi456',addStudents='stu789',apiuser='some_user',apipwd='password',apiaction='some_action',apiurl='https://edtech.worldcampus.psu.edu/testCourse2.xml') 
        
        Synch.handleRoster(self.portal)
        self.failUnless("jad52" in self.portal.acl_users.source_users.getUserIds(), "handleRoster test failed -- user not created")
        self.failUnless("jad52" in self.portal.acl_users.source_groups.getGroupMembers('Instructors'), "AddToGroup failed in handleRoser test -- Test instructor not in instructor group")
        self.logout()
        
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite