#----------------------------------------------------------------------------
# Name:         ldmWidFrmAui.py
# Purpose:      ldmWidFrmAui.py
#               frame widget utilizing advanced user interface
# Author:       Walter Obweger
#
# Created:      20200405
# CVS-ID:       $Id$
# Copyright:    (c) 2020 by Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import wx
import wx.aui

from lindworm.ldmArg import ldmArg
from lindworm.ldmWidCore import ldmWidCore
import lindworm.ldmWidImgMed as ldmWidImgMed
from lindworm.ldmWidSizeRspWid import ldmWidSizeRspWid
from lindworm.ldmWidList import ldmWidList
from lindworm.ldmWidTree import ldmWidTree

#class ldmAuiMpw(aui.AuiMDIParentFrame):
class ldmWidFrmAui(ldmWidCore):
    ID_TBR_File=100
    ID_FILE_OPEN=101
    ID_FILE_SAVE=102
    ID_File_EXIT=190
    ID_EDIT_CUT=201
    ID_EDIT_COPY=202
    ID_EDIT_PASTE=203
    ID_CMD=300
    ID_DST=700
    def __initCls__(self,**kwargs):
        self.clsWid=wx.Frame
    def __initCfg__(self,**kwargs):
        try:
            # +++++ beg:initialize
            sOrg='ldmWidFrmAui::__initCfg__'
            self.logDbg('beg:%s'%(sOrg))
            ldmWidCore.__initCfg__(self,**kwargs)
            # ----- end:initialize
            # +++++ beg:
            self.tTbrBmpSz=wx.Size(32, 32)
            # ----- end:
            # +++++ beg:
            self.setCfgWid('toolbar','bmp.iSz','32')
            # ----- end:
            # +++++ beg:toolbar file
            self.setCfgWid('tbrFile','open.tip','Open Json File')
            self.setCfgWid('tbrFile','save.tip','Save Json File')
            # ----- end:toolbar file
            # +++++ beg:toolbar edit
            self.setCfgWid('tbrEdit','cut.tip','cut')
            self.setCfgWid('tbrEdit','copy.tip','copy')
            self.setCfgWid('tbrEdit','paste.tip','paste')
            # ----- end:toolbar edit
            # +++++ beg:toolbar command
            self.setCfgWid('tbrCmd','00.enable','1')
            self.setCfgWid('tbrCmd','01.enable','1')
            self.setCfgWid('tbrCmd','02.enable','1')
            self.setCfgWid('tbrCmd','03.enable','1')
            self.setCfgWid('tbrCmd','04.enable','0')
            self.setCfgWid('tbrCmd','05.enable','0')
            self.setCfgWid('tbrCmd','06.enable','0')
            self.setCfgWid('tbrCmd','07.enable','0')
            self.setCfgWid('tbrCmd','08.enable','0')
            self.setCfgWid('tbrCmd','09.enable','0')
            self.setCfgWid('tbrCmd','00.tip','command 00')
            self.setCfgWid('tbrCmd','01.tip','command 01')
            self.setCfgWid('tbrCmd','02.tip','command 02')
            self.setCfgWid('tbrCmd','03.tip','command 03')
            self.setCfgWid('tbrCmd','04.tip','command 04')
            self.setCfgWid('tbrCmd','05.tip','command 05')
            self.setCfgWid('tbrCmd','06.tip','command 06')
            self.setCfgWid('tbrCmd','07.tip','command 07')
            self.setCfgWid('tbrCmd','08.tip','command 08')
            self.setCfgWid('tbrCmd','09.tip','command 09')
            # ----- end:toolbar command
            # +++++ beg:
            self.setCfgWid('frmMain','sToolBarCommand','0')
            self.setCfgWid('frmMain','sToolBarDestination','0')
            #dCfgFrm={}
            #self.dCfgWidDft['frmMain']=dCfgFrm
            #dCfgFrm['sToolBarCommand']='0'
            #dCfgFrm['sToolBarDestination']='0'
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def __initObj__(self,**kwargs):
        """initialize object properties, widgets aren't present yet.
        data is supposed to be related to widgets or support their
        function.
        ### parameter
            kwargs  ... keyword arguments passed to all init methods
        """
        try:
            # +++++ beg:initialize
            sOrg='ldmWidCore::__initObj__'
            self.logDbg('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:
            ldmWidCore.__initObj__(self,**kwargs)
            # ----- end:
            # +++++ beg:
            iSz=self.getCfgWid('toolbar','bmp.iSz',sType='int',oDft='32')
            self.tTbrBmpSz=wx.Size(iSz, iSz)
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def __initWid__(self,**kwargs):
        try:
            # +++++ beg:
            # ----- end:
            # +++++ beg:initialize
            sOrg='ldmWidFrmAui::__initWid__'
            self.logDbg('beg:%s'%(sOrg))
            tSz=(
                    self.getCfgWid('frmMain','width',sType='int',oDft=640),
                    self.getCfgWid('frmMain','height',sType='int',oDft=480)
                    )
            style=wx.DEFAULT_FRAME_STYLE
            # ----- end:initialize
            self.logDbg('kw:%r',kwargs)
            lArg=['parent','id','title','pos','size','style']
            _args,_kwargs=self.GetWidArgs(kwargs,
                        ['id','name','parent','size','style','title'],
                        {'size':tSz,'style':style},
                        lArg=lArg)
            #self.logDbg('arg:%r',_args)
            #self.logDbg('kw:%r',_kwargs)
            self.wid=self.clsWid(*_args,**_kwargs)
            self.oApi=wx.aui.AuiPaneInfo()
            self.mgrMain=wx.aui.AuiManager()
            self.mgrMain.SetManagedWindow(self.wid)
            # set frame icon
            #self.SetIcon(images.Mondrian.GetIcon())

            #mb = self.MakeMenuBar()
            #self.SetMenuBar(mb)
            self.__initMenuBar__(**kwargs)
            self.__initStatusBar__(**kwargs)
            self.__initToolBar__(**kwargs)
            # +++++ beg:create center panel
            self.oApi.Name("nbCenter")
            self.oApi.CenterPane()
            self.oApi.PaneBorder(False)
            self.oApi.Center()
            wNb=self.__initPanCt__(**kwargs)
            # +++++ beg:create CLI argument panel
            oArg=kwargs.get('oArg',None)
            if oArg is not None:
                wCliArg=oArg.__initPan__(self,wNb)
                self.logDbg('    args init')
            else:
                self.logDbg('    args none found')
            # ----- end:create CLI argument panel
            # ----- end:create center panel
            self.oApi.Left()
            self.__initPanLf__(**kwargs)
            self.oApi.Bottom()
            self.__initPanBt__(**kwargs)
            self.mgrMain.Update()
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def __initToolBar__(self,**kwargs):
        try:
            # +++++ beg:initialize
            sOrg='ldmWidFrmAui::__initToolBar__'
            self.logDbg('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:
            self.__initTbrFile__(**kwargs)
            self.__initTbrEdit__(**kwargs)
            iVal=self.getCfgWid('toolbar','command',sType='int',oDft=0)
            if iVal>0:
                self.__initTbrCmd__(**kwargs)
            iVal=self.getCfgWid('toolbar','destination',sType='int',oDft=0)
            if iVal>0:
                self.__initTbrDst__(**kwargs)
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def __initTbrFile__(self,**kwargs):
        try:
            # +++++ beg:initialize
            sOrg='ldmWidFrmAui::__initTbrFile__'
            self.logDbg('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:
            oSz=self.tTbrBmpSz
            iStyle =wx.aui.AUI_TB_DEFAULT_STYLE
            #iStyle|=wx.aui.AUI_TB_OVERFLOW
            tbr = wx.aui.AuiToolBar(self.GetWid(),
                        -1,
                        wx.DefaultPosition,
                        size=oSz or wx.DefaultSize,
                        style=iStyle)
            
            bmp=wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN,size=oSz)
            sTip=self.getCfgWid('tbrFile','open.tip',oDft='open json file')
            w=tbr.AddTool(self.ID_FILE_OPEN,
                        label="Open",
                        bitmap=bmp,
                        kind=wx.ITEM_NORMAL,
                        short_help_string=sTip)
            self.BindEvent('mn',self.OnFileOpen,w)
            bmp=wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE,size=oSz)
            sTip=self.getCfgWid('tbrFile','save.tip',oDft='save json file')
            w=tbr.AddTool(self.ID_FILE_SAVE,
                        label="Save",
                        bitmap=bmp,
                        kind=wx.ITEM_NORMAL,
                        short_help_string=sTip)
            self.BindEvent('mn',self.OnFileSave,w)

            oApi=wx.aui.AuiPaneInfo().Name('tbrFile')
            oApi.Caption('file toolbar')
            oApi.ToolbarPane().Top()
            self.mgrMain.AddPane(tbr,oApi)
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def __initTbrEdit__(self,**kwargs):
        try:
            # +++++ beg:initialize
            sOrg='ldmWidFrmAui::__initTbrEdit__'
            self.logDbg('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:
            oSz=self.tTbrBmpSz
            iStyle =wx.aui.AUI_TB_DEFAULT_STYLE
            #iStyle|=wx.aui.AUI_TB_OVERFLOW
            tbr = wx.aui.AuiToolBar(self.GetWid(),
                        -1,
                        wx.DefaultPosition,
                        size=oSz or wx.DefaultSize,
                        style=iStyle)
            
            bmp=wx.ArtProvider.GetBitmap(wx.ART_CUT,size=oSz)
            sTip=self.getCfgWid('tbrEdit','cut.tip',oDft='cut')
            w=tbr.AddTool(self.ID_EDIT_CUT,
                        label="Cut",
                        bitmap=bmp,
                        kind=wx.ITEM_NORMAL,
                        short_help_string=sTip)
            self.BindEvent('mn',self.OnEditCut,w)
            bmp=wx.ArtProvider.GetBitmap(wx.ART_COPY,size=oSz)
            sTip=self.getCfgWid('tbrEdit','copy.tip',oDft='copy')
            w=tbr.AddTool(self.ID_EDIT_COPY,
                        label="Copy",
                        bitmap=bmp,
                        kind=wx.ITEM_NORMAL,
                        short_help_string=sTip)
            self.BindEvent('mn',self.OnEditCopy,w)
            bmp=wx.ArtProvider.GetBitmap(wx.ART_PASTE,size=oSz)
            sTip=self.getCfgWid('tbrEdit','paste.tip',oDft='paste')
            w=tbr.AddTool(self.ID_EDIT_PASTE,
                        label="Paste",
                        bitmap=bmp,
                        kind=wx.ITEM_NORMAL,
                        short_help_string=sTip)
            self.BindEvent('mn',self.OnEditPaste,w)
            
            oApi=wx.aui.AuiPaneInfo().Name('tbrEdit')
            oApi.Caption('edit toolbar')
            oApi.ToolbarPane().Top()
            self.mgrMain.AddPane(tbr,oApi)
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def __initTbrCmd__(self,**kwargs):
        try:
            # +++++ beg:initialize
            sOrg='ldmStorageFolderFrm::__initTbrDst__'
            self.logDbg('beg:%s',sOrg)
            # ----- end:initialize
            # +++++ beg:
            oSz=self.tTbrBmpSz
            iStyle =wx.aui.AUI_TB_DEFAULT_STYLE
            tbr = wx.aui.AuiToolBar(self.GetWid(),
                        -1,
                        wx.DefaultPosition,
                        size=oSz or wx.DefaultSize,
                        style=iStyle)
            #tbr.SetToolBitmapSize(oSz)
            
            iEn=self.getCfgWid('tbrCmd','00.enable',sType='int',oDft=1)
            if iEn>0:
                bmp=ldmWidImgMed.Gn00.GetBitmap()
                sTip=self.getCfgWid('tbrCmd','00.tip',oDft='command 00')
                w=tbr.AddTool(self.ID_CMD+0,
                            label="00",
                            bitmap=bmp,
                            kind=wx.ITEM_NORMAL,
                            short_help_string=sTip)
                self.BindEvent('mn',self.OnCmd00,w)
            
            iEn=self.getCfgWid('tbrCmd','01.enable',sType='int',oDft=1)
            if iEn>0:
                bmp=ldmWidImgMed.Gn01.GetBitmap()
                sTip=self.getCfgWid('tbrCmd','01.tip',oDft='command 01')
                w=tbr.AddTool(self.ID_CMD+1,
                            label="01",
                            bitmap=bmp,
                            kind=wx.ITEM_NORMAL,
                            short_help_string=sTip)
                self.BindEvent('mn',self.OnCmd01,w)
            
            iEn=self.getCfgWid('tbrCmd','02.enable',sType='int',oDft=1)
            if iEn>0:
                bmp=ldmWidImgMed.Gn02.GetBitmap()
                sTip=self.getCfgWid('tbrCmd','02.tip',oDft='command 02')
                w=tbr.AddTool(self.ID_CMD+1,
                            label="02",
                            bitmap=bmp,
                            kind=wx.ITEM_NORMAL,
                            short_help_string=sTip)
                self.BindEvent('mn',self.OnCmd02,w)
            
            iEn=self.getCfgWid('tbrCmd','03.enable',sType='int',oDft=1)
            if iEn>0:
                bmp=ldmWidImgMed.Gn03.GetBitmap()
                sTip=self.getCfgWid('tbrCmd','03.tip',oDft='command 03')
                w=tbr.AddTool(self.ID_CMD+1,
                            label="01",
                            bitmap=bmp,
                            kind=wx.ITEM_NORMAL,
                            short_help_string=sTip)
                self.BindEvent('mn',self.OnCmd03,w)
            
            iEn=self.getCfgWid('tbrCmd','04.enable',sType='int',oDft=1)
            if iEn>0:
                bmp=ldmWidImgMed.Gn04.GetBitmap()
                sTip=self.getCfgWid('tbrCmd','04.tip',oDft='command 04')
                w=tbr.AddTool(self.ID_CMD+1,
                            label="04",
                            bitmap=bmp,
                            kind=wx.ITEM_NORMAL,
                            short_help_string=sTip)
                self.BindEvent('mn',self.OnCmd04,w)
            
            iEn=self.getCfgWid('tbrCmd','05.enable',sType='int',oDft=1)
            if iEn>0:
                bmp=ldmWidImgMed.Gn05.GetBitmap()
                sTip=self.getCfgWid('tbrCmd','05.tip',oDft='command 05')
                w=tbr.AddTool(self.ID_CMD+1,
                            label="05",
                            bitmap=bmp,
                            kind=wx.ITEM_NORMAL,
                            short_help_string=sTip)
                self.BindEvent('mn',self.OnCmd05,w)
            
            iEn=self.getCfgWid('tbrCmd','06.enable',sType='int',oDft=1)
            if iEn>0:
                bmp=ldmWidImgMed.Gn06.GetBitmap()
                sTip=self.getCfgWid('tbrCmd','06.tip',oDft='command 06')
                w=tbr.AddTool(self.ID_CMD+1,
                            label="06",
                            bitmap=bmp,
                            kind=wx.ITEM_NORMAL,
                            short_help_string=sTip)
                self.BindEvent('mn',self.OnCmd06,w)
            
            iEn=self.getCfgWid('tbrCmd','07.enable',sType='int',oDft=1)
            if iEn>0:
                bmp=ldmWidImgMed.Gn07.GetBitmap()
                sTip=self.getCfgWid('tbrCmd','07.tip',oDft='command 07')
                w=tbr.AddTool(self.ID_CMD+1,
                            label="07",
                            bitmap=bmp,
                            kind=wx.ITEM_NORMAL,
                            short_help_string=sTip)
                self.BindEvent('mn',self.OnCmd07,w)
            
            iEn=self.getCfgWid('tbrCmd','08.enable',sType='int',oDft=1)
            if iEn>0:
                bmp=ldmWidImgMed.Gn07.GetBitmap()
                sTip=self.getCfgWid('tbrCmd','08.tip',oDft='command 08')
                w=tbr.AddTool(self.ID_CMD+1,
                            label="08",
                            bitmap=bmp,
                            kind=wx.ITEM_NORMAL,
                            short_help_string=sTip)
                self.BindEvent('mn',self.OnCmd08,w)
            
            iEn=self.getCfgWid('tbrCmd','09.enable',sType='int',oDft=1)
            if iEn>0:
                bmp=ldmWidImgMed.Gn09.GetBitmap()
                sTip=self.getCfgWid('tbrCmd','09.tip',oDft='command 09')
                w=tbr.AddTool(self.ID_CMD+1,
                            label="09",
                            bitmap=bmp,
                            kind=wx.ITEM_NORMAL,
                            short_help_string=sTip)
                self.BindEvent('mn',self.OnCmd09,w)
            
            oApi=wx.aui.AuiPaneInfo().Name('tbrCmd')
            oApi.Caption('command toolbar')
            oApi.ToolbarPane().Top()
            self.mgrMain.AddPane(tbr,oApi)
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def __initTbrDst__(self,**kwargs):
        try:
            # +++++ beg:initialize
            sOrg='ldmWidFrmAui::__initTbrDst__'
            self.logDbg('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:
            oSz=self.tTbrBmpSz
            iStyle =wx.aui.AUI_TB_DEFAULT_STYLE
            iStyle|=wx.aui.AUI_TB_VERTICAL
            tbr = wx.aui.AuiToolBar(self.GetWid(),
                        -1,
                        wx.DefaultPosition,
                        size=oSz or wx.DefaultSize,
                        style=iStyle)
            #tbr.SetToolBitmapSize(oSz)
            
            bmp=ldmWidImgMed.Gn00.GetBitmap()
            w=tbr.AddTool(self.ID_DST+0,
                        label="00",
                        bitmap=bmp,
                        kind=wx.ITEM_RADIO,
                        short_help_string='destination 00')
            self.BindEvent('mn',self.OnDst00,w)
            #AUI_BUTTON_STATE_NORMAL
            #AUI_BUTTON_STATE_HOVER
            #AUI_BUTTON_STATE_PRESSED
            #AUI_BUTTON_STATE_DISABLED
            #AUI_BUTTON_STATE_HIDDEN
            w.SetState(wx.aui.AUI_BUTTON_STATE_CHECKED)
            
            bmp=ldmWidImgMed.Gn01.GetBitmap()
            w=tbr.AddTool(self.ID_DST+1,
                        label="01",
                        bitmap=bmp,
                        kind=wx.ITEM_RADIO,
                        short_help_string='destination 01')
            self.BindEvent('mn',self.OnDst01,w)
            
            oApi=wx.aui.AuiPaneInfo().Name('tbrDst')
            oApi.Caption('destination toolbar')
            oApi.ToolbarPane().Right()
            oApi.GripperTop().TopDockable(False).BottomDockable(False)
            self.mgrMain.AddPane(tbr,oApi)
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def __initPanCt__(self,**kwargs):
        try:
            # +++++ beg:initialize
            sOrg='ldmWidFrmAui::__initPanCt__'
            self.logDbg('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:
            iStyle =wx.aui.AUI_NB_TOP | wx.aui.AUI_NB_TAB_SPLIT 
            iStyle|=wx.aui.AUI_NB_SCROLL_BUTTONS
            #iStyle|=wx.aui.AUI_NB_TAB_MOVE
            #iStyle|=wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB
            #iStyle|=wx.aui.AUI_NB_MIDDLE_CLICK_CLOSE
            wNb=wx.aui.AuiNotebook(self.GetWid(), -1, 
                        (0,0),
                        wx.Size(430, 200),
                        style=iStyle)
            self.mgrMain.AddPane(wNb,self.oApi)
            self.oApi.Name("nbCenter")
            self.oApi.CenterPane()
            self.oApi.PaneBorder(False)
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
            return wNb
            oWid=ldmWidSizeRspWid(wNb, -1,mgr=self.mgrMain)
            wNb.AddPage(oWid,'first',True)
        except:
            self.logTB()
        return None
    def __initPanLf__(self,**kwargs):
        try:
            # +++++ beg:initialize
            sOrg='ldmWidFrmAui::__initPanLf__'
            self.logDbg('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:
            oWid=ldmWidTree(parent=self.GetWid(),iLv=0,size=(200,120),sLogger='tr')
            self.oApi.Name('trDat')
            self.oApi.Caption("tree 0")
            self.oApi.Dockable(True)
            self.mgrMain.AddPane(oWid.GetWid(),self.oApi)
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def __initPanBt__(self,**kwargs):
        try:
            # +++++ beg:initialize
            sOrg='ldmWidFrmAui::__initPanBt__'
            self.logDbg('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:
            oWid=ldmWidList(parent=self.GetWid(),iLv=0,
                        size=(200,120),sLogger='lstLog',
                        lCol=[
                            ['No',      'lf',80],
                            ['Info',    'lf',250],
                            ['Status',  'rg',60],
                        ])
            self.oApi.Name('lstLog')
            self.oApi.Caption("logging")
            self.mgrMain.AddPane(oWid.GetWid(),self.oApi)
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def __initMenuBar__(self,**kwargs):
        try:
            # +++++ beg:initialize
            sOrg='ldmWidFrmAui::__initMenuBar__'
            self.logDbg('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:
            mnBar = wx.MenuBar()

            mnFile=wx.Menu()
            mnFile.Append(self.ID_FILE_OPEN, "&Open\tCtrl+O")
            mnFile.Append(self.ID_FILE_SAVE, "&Save\tCtrl+S")
            w=mnFile.Append(wx.ID_EXIT, "Exit\tAlt+X")
            self.BindEvent('mn',self.OnExit,w)
            
            mnEdit=wx.Menu()
            mnEdit.Append(self.ID_EDIT_CUT, "Cut\tCtrl+X")
            mnEdit.Append(self.ID_EDIT_COPY, "Copy\tCtrl+C")
            mnEdit.Append(self.ID_EDIT_PASTE, "Paste\tCtrl+V")

            mnHelp=wx.Menu()
            mnHelp.Append(wx.ID_ABOUT, "About...")

            mnBar.Append(mnFile, "&File")
            mnBar.Append(mnEdit, "&Edit")
            mnBar.Append(mnHelp, "&Help")

            self.wid.SetMenuBar(mnBar)
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def __initStatusBar__(self,**kwargs):
        try:
            # +++++ beg:initialize
            sOrg='ldmWidFrmAui::__initStatusBar__'
            self.logDbg('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:
            self.wid.CreateStatusBar()
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def __initEvt__(self,**kwargs):
        try:
            # +++++ beg:initialize
            sOrg='ldmWidFrmAui::__initEvt__'
            self.logDbg('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:
            #self.Bind(aui.EVT_AUITOOLBAR_TOOL_DROPDOWN, self.OnDropDownToolbarItem, id=ID_DropDownToolbarItem)
            #self.Bind(aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
            #self.Bind(aui.EVT_AUINOTEBOOK_ALLOW_DND, self.OnAllowNotebookDnD)
            #self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnNotebookPageClose)

            #self.Bind(aui.EVT_AUI_PANE_FLOATING, self.OnFloatDock)
            #self.Bind(aui.EVT_AUI_PANE_FLOATED, self.OnFloatDock)
            #self.Bind(aui.EVT_AUI_PANE_DOCKING, self.OnFloatDock)
            #self.Bind(aui.EVT_AUI_PANE_DOCKED, self.OnFloatDock)
            
            self.wid.Bind(wx.EVT_ERASE_BACKGROUND, self.OnFrmEraseBackground)
            self.wid.Bind(wx.EVT_SIZE, self.OnFrmSize)
            self.wid.Bind(wx.EVT_CLOSE, self.OnFrmClose)
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def GetDockArt(self):
        return self.mgrMain.GetArtProvider()
    def OnFileOpen(self,evt):
        try:
            self.logDbg('OnFileOpen')
        except:
            self.logTB()
    def OnFileSave(self,evt):
        try:
            self.logDbg('OnFileSave')
        except:
            self.logTB()
    def OnEditCut(self,evt):
        try:
            self.logDbg('OnEditCut')
        except:
            self.logTB()
    def OnEditCopy(self,evt):
        try:
            self.logDbg('OnEditCopy')
        except:
            self.logTB()
    def OnEditPaste(self,evt):
        try:
            self.logDbg('OnEditPaste')
        except:
            self.logTB()
    def prcCmd(self,sCmd):
        try:
            # +++++ beg:initialize
            sOrg='ldmStorageFolderFrm::prcCmd'
            self.logDbg('beg:%s sCmd',sOrg,sCmd)
            # ----- end:initialize
            # +++++ beg:
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def OnCmd00(self,evt):
        try:
            # +++++ beg:initialize
            sOrg='ldmStorageFolderFrm::OnCmd00'
            self.logDbg('beg:%s',sOrg)
            # ----- end:initialize
            # +++++ beg:
            iRet=self.prcCmd('cmd00')
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def OnCmd01(self,evt):
        try:
            # +++++ beg:initialize
            sOrg='ldmStorageFolderFrm::OnCmd01'
            self.logDbg('beg:%s',sOrg)
            # ----- end:initialize
            # +++++ beg:
            iRet=self.prcCmd('cmd01')
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def OnCmd02(self,evt):
        try:
            # +++++ beg:initialize
            sOrg='ldmStorageFolderFrm::OnCmd02'
            self.logDbg('beg:%s',sOrg)
            # ----- end:initialize
            # +++++ beg:
            iRet=self.prcCmd('cmd02')
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def OnCmd03(self,evt):
        try:
            # +++++ beg:initialize
            sOrg='ldmStorageFolderFrm::OnCmd03'
            self.logDbg('beg:%s',sOrg)
            # ----- end:initialize
            # +++++ beg:
            iRet=self.prcCmd('cmd03')
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def OnCmd04(self,evt):
        try:
            # +++++ beg:initialize
            sOrg='ldmStorageFolderFrm::OnCmd04'
            self.logDbg('beg:%s',sOrg)
            # ----- end:initialize
            # +++++ beg:
            iRet=self.prcCmd('cmd04')
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def OnCmd05(self,evt):
        try:
            # +++++ beg:initialize
            sOrg='ldmStorageFolderFrm::OnCmd05'
            self.logDbg('beg:%s',sOrg)
            # ----- end:initialize
            # +++++ beg:
            iRet=self.prcCmd('cmd05')
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def OnCmd06(self,evt):
        try:
            # +++++ beg:initialize
            sOrg='ldmStorageFolderFrm::OnCmd06'
            self.logDbg('beg:%s',sOrg)
            # ----- end:initialize
            # +++++ beg:
            iRet=self.prcCmd('cmd06')
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def OnCmd07(self,evt):
        try:
            # +++++ beg:initialize
            sOrg='ldmStorageFolderFrm::OnCmd07'
            self.logDbg('beg:%s',sOrg)
            # ----- end:initialize
            # +++++ beg:
            iRet=self.prcCmd('cmd07')
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def OnCmd08(self,evt):
        try:
            # +++++ beg:initialize
            sOrg='ldmStorageFolderFrm::OnCmd08'
            self.logDbg('beg:%s',sOrg)
            # ----- end:initialize
            # +++++ beg:
            iRet=self.prcCmd('cmd08')
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def OnCmd09(self,evt):
        try:
            # +++++ beg:initialize
            sOrg='ldmStorageFolderFrm::OnCmd09'
            self.logDbg('beg:%s',sOrg)
            # ----- end:initialize
            # +++++ beg:
            iRet=self.prcCmd('cmd09')
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def OnDst00(self,evt):
        try:
            self.logDbg('OnDst00')
        except:
            self.logTB()
    def OnDst01(self,evt):
        try:
            self.logDbg('OnDst01')
        except:
            self.logTB()
    def OnFrmEraseBackground(self, event):
        event.Skip()
    def OnFrmSize(self, event):
        event.Skip()
    def OnFrmClose(self, event):
        #self.timer.Stop()
        self.mgrMain.UnInit()
        event.Skip()
    def OnExit(self, event):
        try:
            self.logDbg('OnExit')
            self.wid.Close(True)
        except:
            self.logTB()
    def DoUpdate(self):
        self.mgrMain.Update()
        self.Refresh()
