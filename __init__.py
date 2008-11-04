"""RosterSynch will hit the PSU ANGEL API and pull a list of userids based on a course code
This list is written into a file designed to be used by apache's group authorization
"""

from Products.CMFCore.DirectoryView import registerDirectory

registerDirectory('skins', globals())  # Without this, portal_skins/weblionlibrary_portlets shows up, but it's empty.

marker = object()  # a sentinel value for customNavTree(). We can't define it in nav.py, because External Methods are apparently loaded more than once or some weird thing. At any rate, the sentinel ends up with more than one value throughout the lifetime of customNavTree(), so the "currentItem is marker" test doesn't work right.