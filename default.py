
import os
import sys
import xbmcaddon
__scriptname__ = "Skype"
__author__ = "alxnik"
__url__ = ""
__svn_url__ = ""
__credits__ = ""
__version__ = "0.0.1"
__XBMC_Revision__ = "22240"


BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )

sys.path.append (BASE_RESOURCE_PATH)
sys.path.append ("/usr/local/lib/python2.6/dist-packages/")

__settings__ = xbmcaddon.Addon(id='script.skype')

__language__ = __settings__.getLocalizedString



if __name__ == "__main__":
    import gui
    ui = gui.GUI( "ui.xml" , os.getcwd(), "Default")
    ui.doModal()
    del ui
    sys.modules.clear()
            
