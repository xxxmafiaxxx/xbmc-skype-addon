import sys
import os
import xbmc
import xbmcgui
import Skype4Py
import gui

_ = sys.modules[ "__main__" ].__language__
__scriptname__ = sys.modules[ "__main__" ].__scriptname__
__version__ = sys.modules[ "__main__" ].__version__
__settings__ = sys.modules[ "__main__" ].__settings__

STATUS_LABEL = 100
BUDDY_LIST = 120
STATUS_BAR = 102
CONNECT_STATUS = 101



class CallWindow( xbmcgui.WindowXMLDialog ):
    def __init__( self, *args, **kwargs ):
        xbmcgui.WindowXMLDialog.__init__( self, *args, **kwargs )
        self.call = kwargs.get( "call" )
	self.skype = kwargs.get( "skype" )
	

    def onInit( self ):
	if(self.call.PartnerDisplayName != ""):
        	caller = self.call.PartnerDisplayName
        else:
                caller = self.call.PartnerHandle

	self.getControl( 201 ).setLabel(caller)

    def onClick( self, controlId ):
        if(controlId == 202):
		self.call.Finish()
		self.close()
	

class AnswerWindow( xbmcgui.WindowXMLDialog ):
    def __init__( self, *args, **kwargs ):
        self.call = kwargs.get( "call" )
	self.skype = kwargs.get( "skype" )

    def onInit( self ):
        if(self.call.PartnerDisplayName != ""):
                caller = self.call.PartnerDisplayName
        else:
                caller = self.call.PartnerHandle

        self.getControl( 201 ).setLabel(caller)

    def onClick( self, controlId ):
	if(controlId == 202):
		self.call.Answer()
        elif(controlId == 203):
                self.call.Finish()
                
	self.close()	
	

class GUI( xbmcgui.WindowXMLDialog ):
##	Event Handler
##	It is called when the status of a call changes. Usually this is how we know
##	That there is an incoming call. Spawns a new window with the call details

    def CallStatus(self, Call, Status):

		self.call = Call
		if(Status ==  Skype4Py.clsUnknown):
			self.getControl(STATUS_BAR).setLabel( "Unknown status" )
		elif(Status ==   Skype4Py.clsUnplaced ):
			self.getControl(STATUS_BAR).setLabel( "Unplaced" )
		elif(Status == Skype4Py.clsRouting ):
			self.getControl(STATUS_BAR).setLabel( "Routing..." )
		elif(Status == Skype4Py.clsEarlyMedia ):
			self.getControl(STATUS_BAR).setLabel( "Early Media" )
		elif(Status == Skype4Py.clsFailed ):
			self.getControl(STATUS_BAR).setLabel( "Failed!" )
		elif(Status == Skype4Py.clsRinging ):
			if(Call.Type == Skype4Py.cltIncomingP2P or Call.Type == Skype4Py.cltIncomingPSTN):
				self.enableAnswerWin()
			elif(Call.Type == Skype4Py.cltOutgoingP2P  or Call.Type == Skype4Py.cltOutgoingPSTN):
				pass	
		elif(Status == Skype4Py.clsInProgress ):
			self.getControl(STATUS_BAR).setLabel( "In progress" )
		elif(Status == Skype4Py.clsOnHold ):
			self.getControl(STATUS_BAR).setLabel( "On Hold" )
		elif(Status == Skype4Py.clsFinished ):
			self.getControl(STATUS_BAR).setLabel( "Finished!" )
			self.disableCallWin()
			
		elif(Status == Skype4Py.clsMissed ):
			self.getControl(STATUS_BAR).setLabel( "Missed a call..." )
			self.disableAnswerWin()


    def ConnectionStatus(self, Status):
		if(Status ==  Skype4Py.conOffline):
			self.getControl(CONNECT_STATUS).setLabel( "Offline" )
		if(Status ==  Skype4Py.conConnecting):
			self.getControl(CONNECT_STATUS).setLabel( "Connecting" )
##	Event Handler
##	It is called when the status of the user changes and it changes
##	the status on the top right of the skype window

    def UserStatus(self, Status):
		if(Status ==  Skype4Py.cusOffline):
			self.getControl(CONNECT_STATUS).setLabel( "Offline" )
		if(Status ==  Skype4Py.cusOnline):
			 self.getControl(CONNECT_STATUS).setLabel( "Online" )
		if(Status ==  Skype4Py.cusAway):
			 self.getControl(CONNECT_STATUS).setLabel( "Away" )
		if(Status ==  Skype4Py.cusDoNotDisturb ):
			 self.getControl(CONNECT_STATUS).setLabel( "Do Not Disturb" )
		if(Status ==  Skype4Py.cusInvisible):
			 self.getControl(CONNECT_STATUS).setLabel( "Invisible" )
		if(Status ==  Skype4Py.cusLoggedOut ):
			 self.getControl(CONNECT_STATUS).setLabel( "Logged Out" )
		if(Status ==  Skype4Py.cusSkypeMe ):
			 self.getControl(CONNECT_STATUS).setLabel( "SkypeMe" )
		if(Status ==  Skype4Py.cusNotAvailable):
			 self.getControl(CONNECT_STATUS).setLabel( "Not Available" )
		if(Status ==  Skype4Py.cusUnknown):
			 self.getControl(CONNECT_STATUS).setLabel( "Unknown" )

    def OnlineStatus(self, User, Status):
	self.loadBuddyList()

##
##      Initializes the Skype object and attaches on skype
##
    def __init__( self, *args, **kwargs ):
    	self.skype = Skype4Py.Skype(Events=self)
    	self.skype.FriendlyName = 'xbmc_skype'
    	self.skype.Attach()


    def onInit( self ):
    		self.getControl(200).setVisible(False)
		self.getControl(300).setVisible(False)
		self.setup_all()


    def setup_all( self ):
	self.getControl( STATUS_LABEL ).setLabel(self.skype.CurrentUser.FullName)
	self.loadBuddyList()


    def loadBuddyList( self ):
	self.getControl( BUDDY_LIST ).reset()
	for F in self.skype.Friends:
	
		# Label  is always the handle and is used like a primary key on a database, as it is unique
		# label2 is used for the listItem Label so we use either Handle or the full name
		if(F.FullName == ""):
			listitem = xbmcgui.ListItem( label=F.Handle, label2=F.Handle)
		else:
			listitem = xbmcgui.ListItem( label=F.Handle, label2=F.FullName)

		# Set all the properties of each user
		listitem.setProperty("about", F.About);
		#listitem.setProperty("birthday", F.Birthday);
		listitem.setProperty("city", F.City);
		listitem.setProperty("country", F.Country);
		listitem.setProperty("countrycode", F.CountryCode);
		listitem.setProperty("displayname", F.DisplayName);
		listitem.setProperty("language", F.Language);
		listitem.setProperty("moodtext", F.MoodText);
		listitem.setProperty("phonehome", F.PhoneHome);
		listitem.setProperty("phonemobile", F.PhoneMobile);
		listitem.setProperty("phoneoffice", F.PhoneOffice);
		
		if(F.OnlineStatus == Skype4Py.olsOnline):
			listitem.setProperty( "statusIcon", "online.png")
		elif(F.OnlineStatus == Skype4Py.olsOffline):
			listitem.setProperty( "statusIcon", "offline.png")
		elif(F.OnlineStatus == Skype4Py.olsAway):
			listitem.setProperty( "statusIcon", "away.png")
		elif(F.OnlineStatus == Skype4Py.olsDoNotDisturb):
			listitem.setProperty( "statusIcon", "dnd.png")
		self.getControl( BUDDY_LIST ).addItem( listitem )

	self.setFocus( self.getControl( BUDDY_LIST ) )
	self.getControl( BUDDY_LIST ).selectItem( 0 )

    def enableAnswerWin(self):
        if(self.call.PartnerDisplayName != ""):
                caller = self.call.PartnerDisplayName
        else:
                caller = call.PartnerHandle
        self.getControl(201).setLabel(caller)

        self.getControl(200).setVisible(True)
	self.setFocusId(202)

    def disableAnswerWin(self):
        self.getControl(200).setVisible(False)
        self.setFocusId(101)

    def enableCallWin(self):
	if(self.call.PartnerDisplayName != ""):
        	caller = self.call.PartnerDisplayName
        else:
        	caller = call.PartnerHandle
        self.getControl(301).setLabel(caller)

        self.getControl(300).setVisible(True)
        self.setFocusId(302)

    def disableCallWin(self):
        self.getControl(300).setVisible(False)
        self.setFocusId(101)


##
##	Event Handler for the remote/keyboard presses
##
    def onClick( self, controlId ):
	print "in onclick"
	if(controlId == 120):
		selectedHandle = self.getControl( 120 ).getSelectedItem()
	        self.call = self.skype.PlaceCall(selectedHandle.getLabel())
        elif(controlId == 202):
                self.call.Answer()
		self.enableCallWin()
		self.disableAnswerWin()
        elif(controlId == 203):
                self.call.Finish()
		self.disableAnswerWin()
	elif(controlId == 302):
		self.call.Finish()
		self.disableCallWin()

    def onFocus( self, controlId ):

    	self.controlId = controlId


	
def onAction( self, action ):

	if ( action.getButtonCode() in CANCEL_DIALOG ):
		print "Closing"
		self.close()


