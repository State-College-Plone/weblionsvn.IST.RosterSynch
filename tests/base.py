from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_RosterSynch():
    """Set up the additional products required for the World Campus course policy.
    
    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    
    # Load the ZCML configuration for the RosterSynch package.
    
    fiveconfigure.debug_mode = True
    import Products.RosterSynch
    zcml.load_config('configure.zcml', Products.RosterSynch)
    fiveconfigure.debug_mode = False
    
    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML.
    
    ztc.installPackage('RosterSynch')
    
# The order here is important: We first call the (deferred) function which
# installs the products we need for the RosterSynch package. Then, we let 
# PloneTestCase set up this product on installation.

setup_RosterSynch()
ptc.setupPloneSite(products=['RosterSynch'])

class RosterSynchTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """