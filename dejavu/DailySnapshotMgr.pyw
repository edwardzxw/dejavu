import wx, datetime, os, subprocess, sys, ConfigParser

ID_ICON_TIMER = wx.NewId()
OPEN_SNAPSHOT_DIR=wx.NewId()
OPEN_DEFECT_DIR=wx.NewId()
OPEN_PREFS=wx.NewId()

class MainTaskBarIcon(wx.TaskBarIcon):
    def __init__(self, parent):
        wx.TaskBarIcon.__init__(self)
        self.parentApp = parent
        self.icon = wx.Icon("icon.png",wx.BITMAP_TYPE_PNG)
        self.CreateMenu()
        self.SetIcon(self.icon, "Daily Snapshot Manager")

    def CreateMenu(self):
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.ShowMenu)
        self.Bind(wx.EVT_MENU, self.parentApp.openSnapshotDir, id=OPEN_SNAPSHOT_DIR)
        self.Bind(wx.EVT_MENU, self.parentApp.OpenPrefs, id=OPEN_PREFS)
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.parentApp.openSnapshotDir)
        self.menu=wx.Menu()
        self.menu.Append(OPEN_SNAPSHOT_DIR, "Open Snapshot Dir")
        self.menu.Append(OPEN_PREFS, "Preferences")
        self.menu.AppendSeparator()
        self.menu.Append(wx.ID_EXIT, "Exit")

    def ShowMenu(self,event):
        self.PopupMenu(self.menu)

class PrefsDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title)
        
        # Add a panel so it looks correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)
        
        topSizer   = wx.BoxSizer(wx.VERTICAL)
        inputSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer   = wx.BoxSizer(wx.HORIZONTAL)
        
        #wx.StaticBox(self.panel, wx.ID_ANY, 'Snapshot', (5,5), size=(394, 50))
        labelSnapshotRoot = wx.StaticText(self.panel, wx.ID_ANY, 'Snapshots Root Directory:')
        config = ConfigParser.RawConfigParser()
        config.read('config.ini')
        self.tbRoot = wx.TextCtrl(self.panel, wx.ID_ANY, config.get('snapshot', 'root'))
        inputSizer.Add(labelSnapshotRoot, 0, wx.ALL, 5)
        inputSizer.Add(self.tbRoot, 1, wx.ALL|wx.EXPAND, 5)

        okBtn = wx.Button(self.panel, wx.ID_ANY, 'OK')
        cancelBtn = wx.Button(self.panel, wx.ID_ANY, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.onOK, okBtn)
        self.Bind(wx.EVT_BUTTON, self.onCancel, cancelBtn)
        btnSizer.Add(okBtn,  0, wx.ALL, 5)
        btnSizer.Add(cancelBtn,  0, wx.ALL, 5)
        
        topSizer.Add(inputSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(btnSizer, 0, wx.ALIGN_RIGHT|wx.RIGHT, 5)
        
        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)

    def onOK(self, event):
        config = ConfigParser.RawConfigParser()
        config.read('config.ini')
        config.set('snapshot', 'root', self.tbRoot.GetValue())
        config.write( open('config.ini', 'wb') )
        self.EndModal(wx.ID_OK)
    
    def onCancel(self, event):
        self.EndModal(wx.ID_CANCEL)

class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title, size = (1, 1), 
            style=wx.FRAME_NO_TASKBAR|wx.NO_FULL_REPAINT_ON_RESIZE)

        self.tbicon = MainTaskBarIcon(self)
        self.tbicon.Bind(wx.EVT_MENU, self.exitApp, id=wx.ID_EXIT)
        self.Show(True)

    def exitApp(self, event):
        self.tbicon.RemoveIcon()
        self.tbicon.Destroy()
        sys.exit()
    
    def openSnapshotDir(self, event):
        config = ConfigParser.RawConfigParser()
        config.read('config.ini')
        snapshotsRoot = config.get( 'snapshot', 'root' )
        now = datetime.datetime.now()
        snapshotDir = os.path.abspath(snapshotsRoot + '/' + now.strftime('%Y%m%d'))
        if not os.path.exists(snapshotDir):
            os.makedirs(snapshotDir)
        subprocess.Popen('explorer "%s"'%snapshotDir)
        
    def OpenPrefs(self,event):
        prefsDlg = PrefsDialog(None, -1, 'Preferences')
        prefsDlg.ShowModal()
        prefsDlg.Destroy()

def main(argv=None):
    app = wx.App(False)
    frame = MainFrame(None, -1, ' ')
    frame.Show(False)
    app.MainLoop()

if __name__ == '__main__':
    main()

'''
Change history
2015/6/27 initial check-in to GitHub.
This tool were wrote while I was in Qilinsoft, at that time I need a tool to create a directory using date as name
to store temp files which can be referenced in future.
The initial version has a desktop bottom right icon, by double click it will create the directory aforementioned.
Right click it would pop-up preference menu which allows you to set the root directory contains created directories.
It's pretty simple right now, but do save my time creating those directories manually.

'''
