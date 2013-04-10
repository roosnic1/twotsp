import wx
import wx.xrc
import subprocess

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"two TSP problem", pos = wx.DefaultPosition, size = wx.Size( 600,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		boxsizer = wx.BoxSizer( wx.VERTICAL )
		
		self.btnStart = wx.Button( self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
		boxsizer.Add( self.btnStart, 0, wx.ALL, 5 )
		
		self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 500,400 ), 0 )
		boxsizer.Add( self.m_textCtrl1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.btnClose = wx.Button( self, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
		boxsizer.Add( self.btnClose, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( boxsizer )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.btnStart.Bind( wx.EVT_LEFT_DOWN, self.onStartClick )
		self.btnClose.Bind( wx.EVT_LEFT_DOWN, self.onCloseClick )
	
	def __del__( self ):
		pass
	
	def onStartClick( self, event ):
		proc = subprocess.Popen(['python','main.py'],stdout=subprocess.PIPE)
		while True:
			line = proc.stdout.readline()
			if line != '':
				self.m_textCtrl1.AppendText(line.rstrip())
			else:
				break
	
	# Virtual event handlers, overide them in your derived class
	def onCloseClick( self, event ):
		self.Close(True)
	


app = wx.App(False)
frame = MainFrame(None)
frame.Show(True)
app.MainLoop()
