RosterSynch is a Penn State specific product designed to enable integrators (or site managers) 
to control access to their sites.  It is made to work in conjunction with apache in that it creates and 
manages a groups file that can be used for authorization.  There is no manipulation of apache configuration;
rather, the product creates a groups file from the class roster (as pulled from the ANGEL course management system) 
and puts that file in the location of the integrator's choice.  The httpd.conf file must be configured to point to
this file.  See below for more details.

Installation

 	In old-school Plone style, copy the RosterSynch folder to your products directory and restart your zope instance.
	Install the product in your Plone site through the Add-On Products control panel (or via the ZMI portal quick installer).


Configuration

	Special Notes: 
	
		1. You will have to set up access to the ANGEL api with the PSU ANGEL team.
		
		2. Your python must be compiled with ssl support to open secure (https) urls.
	
	Setup Options:
	
		1.  **API URL** - Required.  This tells RosterSynch where to find the roster.  Some servers will have access to the production api and
		some the development api.  You also may want to just point this to a test file while you are experimenting with the product.  This property 
		allows you to change that without editing the python script.
		
		2.  **API Username** - Required.  Get this from the ANGEL team.
		
		3.  **API Password** - Required.  Get this from the ANGEL team.
		
		4.  **Section ID** -  Required.  This number is found in ANGEL.  See the screenshot link on the setup page to see where you find this number.
		The format of this ID is very important (including the spaces), so don't edit it.
		
		5.  **Group Name** -  Required.  This is the name of the group that is written into the groups file and that apache will use for authorization.  
		It will appear in the file like this:  mygroup: [followed by a space-delimited list of users].  You should use no spaces in this value.
	
		6.  **Groups File** -  Required.  This is the complete path to the location of your groups file.  For example: /home/zope/sra211.conf.  Depending on how you 
		have your permissions set, you may have to create the file before RosterSynch will work.  You effective zope user has to have write permission 
		to this file and apache has to be able to read it.
		
		7.  **Additional Users** -  Optional.  If you wish to grant access to other users who are not in the ANGEL course, add them here.
		This should be a space-delimited list of any users you wish to add.  If you wish to remove those users, remove them from this 
		list and re-run RosterSynch. 
		
		8.  **Admin ID** - Optional.  If you add users here, RosterSynch will create another group called admins and add these users.
		This, by itself, does nothing to grant any special privileges; that is handled through the apache configuration.  This just gives you 
		the flexibility of having another group to work with.  If, for example, you wish to limit access to one section of your site,
		you can require group admins.
		
A (very) little about apache configuration

	The RosterSynch product is designed to work in conjunction with the apache web server and PSU Web Access (CoSign) authorization.
	Apache configuration is an extensive topic and way outside of the scope of this documentation, but here is a quick explanation of how 
	you might apply the groups file.
	
	The directory (or site) that is secured with CoSign would have a Location block in the httpd.conf file that looks something like this::
		
		<Location /mysite>
			AuthType Cosign
			AuthGroupFile /home/zope/myGroupsFile.conf
			Require group mygroup admins
			...
		</Location>
		
	More information about configuring CoSign, apache and your zope instance is available from the "PSU WebLion":http://weblion.psu.edu team.
   

To Do List
	
	- Enable option to create plone users during RosterSynch.
	
	- Enable importing of ANGEL groups into plone site. 
	
	- Write some tests.
	
Credits and Contact

	Credit for inspiration and paving the way for this go to the members of the former IST Solutions Institute.  Thanks also goes to the PSU WebLion team for 
	their help and patience in answering questions.  To the degree that this product is useful, credit goes to those parties.
	 
	On the other hand, problems, bugs and other issues are the fault of Joe DeLuca, who did most of the work on this project.  If you find issues, please contact
	him at joedeluca at psu dot edu.  He would also like to hear your comments and suggestions for improvements for future versions.


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
