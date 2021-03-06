GLOBALS = globals()
PRODUCT_NAME = 'RosterSynch'

TOOL_ICON = 'tool.gif'
TOOL_ID = 'portal_rostersynch'
CONFIGLET_ID = "prefs_rostersynch_setup_form"
CONFIGLET_NAME = "RosterSynch setup"

DEFAULT_API = "psu_teamlistxml2"

PROPERTIES = (('apiaction', DEFAULT_API, 'string'),
              ('apiurl','', 'string'),
              ('courseID', '', 'string'),
              ('addInstructors','','string'),
              ('addStudents','','string'),
              ('addEditors','','string'),
              ('apiuser', '', 'string'),
              ('apipwd', '', 'string'))
