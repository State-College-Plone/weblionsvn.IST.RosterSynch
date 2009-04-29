RosterSynch is a Penn State specific product designed to enable integrators (or site managers) 
to control access to their sites.  It is made to work in conjunction with the PSU ANGEL API.  The developer must set up
access to this API prior to using RosterSynch.

Installation

 	In old-school Plone style, copy the RosterSynch folder to your products directory and restart your zope instance.
	Install the product in your Plone site through the Add-On Products control panel (or via the ZMI portal quick installer).
	
	**With Buildout**
	
	If you use buildout, you can use the infrae.subversion recipe to pull this directly from the WebLion repository.  See the following
	example.
	
	In buildout.cfg:
	Add a line to your [buildout] parts section.  You can call it whatever you like (I call mine externals in this example).
	<pre>'[buildout]
	parts =
	...
	externals
	...'
	</pre>
		Then add the externals section:
			
	<pre>'[externals]
	recipe = infrae.subversion
	urls =	https://weblion.psu.edu/svn/weblion/collegeOfIst/RosterSynch RosterSynch'
	</pre>		
		Finally, add a line to the products section of your [instance] 
	
	<pre>'products =
	...
	${buildout:directory}/parts/externals
	...'
	</pre>

    
    Re-run buildout and it should pull this new product.
    Install the product in your Plone site through the Add-On Products control panel (or via the ZMI portal quick installer).

Configuration

	Special Notes: 
	
		1. You will have to set up access to the ANGEL api with the PSU ANGEL team.
		
		2. Your python must be compiled with ssl support to open secure (https) urls.
	
	Setup Options:
	
		**_Required Fields_**
	
		*  **API URL** - Required.  This tells RosterSynch where to find the roster.  Some servers will have access to the production api and
		some the development api.  You also may want to just point this to a test file while you are experimenting with the product.  This property 
		allows you to change that without editing the python script.
		
		*  **API Username** - Required.  Get this from the ANGEL team.
		
		*  **API Password** - Required.  Get this from the ANGEL team.
		
		*  **Section ID** -  Required.  This number is found in ANGEL.  See the screenshot link on the setup page to see where you find this number.
		The format of this ID is very important (including the spaces), so don't edit it.
		
		**_Optional Fields_**
		
		Use the following fields to grant access to users who are not in the ANGEL Roster.
		
		**NOTE:  All additional users should be added here instead of through the standard Plone User Management tool.  Only users here
		and in the ANGEL roster are respected when RosterSynch is run.  If users are not listed in one of these two places, they will be removed from the
		the Plone users and groups.**
		
		To add users to your site, add them to the appropriate group below.  To remove users from your site, remove them from the groups below or remove
		then from your course in ANGEL.
		
		*  **Additional Instructors** -  Optional.  If you add users here, RosterSynch will create that user and add him or her to the Instructors group.  
		If you wish to remove those users, remove them from this list and re-run RosterSynch. 
		
		*  **Addtional Course Editors** - Optional.  If you add users here, RosterSynch will create that user and add him or her to the Course Editors group.  
		If you wish to remove those users, remove them from this list and re-run RosterSynch.

		*  **Addtional Course Editors** - Optional.  If you add users here, RosterSynch will create that user and add him or her to the Students group.  
		If you wish to remove those users, remove them from this list and re-run RosterSynch.
		

To Do List
	
	- Enable option to create plone users during RosterSynch.
	
	- Enable importing of ANGEL groups into plone site. 
	
	- Write some tests.
	
Credits and Contact

	Credit for inspiration and paving the way for this go to the members of the former IST Solutions Institute.  Thanks also goes to the PSU WebLion team for 
	their help and patience in answering questions.  To the degree that this product is useful, credit goes to those parties.
	 
	On the other hand, problems, bugs and other issues are the fault of Joe DeLuca, who did most of the work on this project.  If you find issues, please contact
	him at jdeluca at psu dot edu.  He would also like to hear your comments and suggestions for improvements for future versions.


License

    Copyright (c) 2008 The Pennsylvania State University.

    This program is free software; you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the Free
    Software Foundation; either version 2 of the License, or (at your option)
    any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
    more details.

    You should have received a copy of the GNU General Public License along with
    this program; if not, write to the Free Software Foundation, Inc., 59 Temple
    Place, Suite 330, Boston, MA 02111-1307 USA.

    This document is written using the Structured Text format for conversion
    into alternative formats.
