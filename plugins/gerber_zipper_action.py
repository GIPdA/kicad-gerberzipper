# coding: utf-8
# file : gerber_zipper_action.py
#
# Copyright (C) 2020 g200kg
#   Released under MIT License
#
# Modified by: Benjamin Balga (2022)
#

import pcbnew
from pcbnew import *
import wx
import wx.grid
import os
import locale
import zipfile
import glob
import json
import sys
import codecs
import inspect
import traceback
import tempfile

from .gerber_zipper_gui import GerberZipperGui

version = "1.2.0"
strtab = {}

layer_list = [
    {'name':'F.Cu', 'id':pcbnew.F_Cu, 'fnamekey':'${filename(F.Cu)}'},
    {'name':'B.Cu', 'id':pcbnew.B_Cu, 'fnamekey':'${filename(B.Cu)}'},
    {'name':'F.Adhes', 'id':pcbnew.F_Adhes, 'fnamekey':'${filename(F.Adhes)}'},
    {'name':'B.Adhes', 'id':pcbnew.B_Adhes, 'fnamekey':'${filename(B.Adhes)}'},
    {'name':'F.Paste', 'id':pcbnew.F_Paste, 'fnamekey':'${filename(F.Paste)}'},
    {'name':'B.Paste', 'id':pcbnew.B_Paste, 'fnamekey':'${filename(B.Paste)}'},
    {'name':'F.SilkS', 'id':pcbnew.F_SilkS, 'fnamekey':'${filename(F.SilkS)}'},
    {'name':'B.SilkS', 'id':pcbnew.B_SilkS, 'fnamekey':'${filename(B.SilkS)}'},
    {'name':'F.Mask', 'id':pcbnew.F_Mask, 'fnamekey':'${filename(F.Mask)}'},
    {'name':'B.Mask', 'id':pcbnew.B_Mask, 'fnamekey':'${filename(B.Mask)}'},
    {'name':'Dwgs.User', 'id':pcbnew.Dwgs_User, 'fnamekey':'${filename(Dwgs.User)}'},
    {'name':'Cmts.User', 'id':pcbnew.Cmts_User, 'fnamekey':'${filename(Cmts.User)}'},
    {'name':'Eco1.User', 'id':pcbnew.Eco1_User, 'fnamekey':'${filename(Eco1.User)}'},
    {'name':'Eco2.User', 'id':pcbnew.Eco2_User, 'fnamekey':'${filename(Eco2.User)}'},
    {'name':'Edge.Cuts', 'id':pcbnew.Edge_Cuts, 'fnamekey':'${filename(Edge.Cuts)}'},
    {'name':'F.CrtYd', 'id':pcbnew.F_CrtYd, 'fnamekey':'${filename(F.CrtYd)}'},
    {'name':'B.CrtYd', 'id':pcbnew.B_CrtYd, 'fnamekey':'${filename(B.CrtYd)}'},
    {'name':'F.Fab', 'id':pcbnew.F_Fab, 'fnamekey':'${filename(F.Fab)}'},
    {'name':'B.Fab', 'id':pcbnew.B_Fab, 'fnamekey':'${filename(B.Fab)}'},
    {'name':'In1.Cu', 'id':pcbnew.In1_Cu, 'fnamekey':'${filename(In1.Cu)}'},
    {'name':'In2.Cu', 'id':pcbnew.In2_Cu, 'fnamekey':'${filename(In2.Cu)}'},
    {'name':'In3.Cu', 'id':pcbnew.In3_Cu, 'fnamekey':'${filename(In3.Cu)}'},
    {'name':'In4.Cu', 'id':pcbnew.In4_Cu, 'fnamekey':'${filename(In4.Cu)}'},
    {'name':'In5.Cu', 'id':pcbnew.In5_Cu, 'fnamekey':'${filename(In5.Cu)}'},
    {'name':'In6.Cu', 'id':pcbnew.In6_Cu, 'fnamekey':'${filename(In6.Cu)}'}
]

default_settings = {
  "Name":"ManufacturersName",
  "Description":"description",
  "URL":"https://example.com/",
  "GerberDir":"Gerber",
  "ZipFilename":"*.ZIP",
  "Layers": {
    "F.Cu":"",
    "B.Cu":"",
    "F.Paste":"",
    "B.Paste":"",
    "F.SilkS":"",
    "B.SilkS":"",
    "F.Mask":"",
    "B.Mask":"",
    "Edge.Cuts":"",
    "In1.Cu":"",
    "In2.Cu":"",
    "In3.Cu":"",
    "In4.Cu":"",
    "In5.Cu":"",
    "In6.Cu":""
  },
  "PlotBorderAndTitle":False,
  "PlotFootprintValues":True,
  "PlotFootprintReferences":True,
  "ForcePlotInvisible":False,
  "ExcludeEdgeLayer":True,
  "ExcludePadsFromSilk":True,
  "DoNotTentVias":False,
  "UseAuxOrigin":False,
  "LineWidth":0.1,

  "CoodinateFormat46":True,
  "SubtractMaskFromSilk":True,
  "UseExtendedX2format": False,
  "IncludeNetlistInfo":False,

  "Drill": {
    "Drill":"",
    "DrillMap":"",
    "NPTH":"",
    "NPTHMap":"",
    "Report":""
  },
  "DrillUnitMM":True,
  "MirrorYAxis":False,
  "MinimalHeader":False,
  "MergePTHandNPTH":False,
  "RouteModeForOvalHoles":True,
  "ZerosFormat":{
    "DecimalFormat":True,
    "SuppressLeading":False,
    "SuppressTrailing":False,
    "KeepZeros":False
  },
  "MapFileFormat":{
    "HPGL":False,
    "PostScript":False,
    "Gerber":True,
    "DXF":False,
    "SVG":False,
    "PDF":False
  },
  "OptionalFiles":[]
}

chsize = (10,20)

def message(s):
    print('GerberZipper: '+s)

def alert(s, icon=0):
    wx.MessageBox(s, 'Gerber Zipper', wx.OK|icon)

def InitEm():
    global chsize
    dc=wx.ScreenDC()
    font=wx.Font(pointSize=10,family=wx.DEFAULT,style=wx.NORMAL,weight=wx.NORMAL)
    dc.SetFont(font)
    tx=dc.GetTextExtent("M")
    chsize=(tx[0],tx[1]*1.5)

def Em(x,y,dx=0,dy=0):
    return (chsize[0]*x+dx, chsize[1]*y+dy)

def getindex(s):
    for i in range(len(layer_list)):
        if layer_list[i]['name']==s:
            return i
    return -1

def getid(s):
    for i in range(len(layer_list)):
        if layer_list[i]['name']==s:
            return layer_list[i]['id']
    return 0

def getstr(s):
    lang = wx.Locale.GetCanonicalName(wx.GetLocale())
    lang = lang if lang else 'default'
    tab = strtab['default']
    if (lang in strtab):
        tab = strtab[lang]
    else:
        for x in strtab:
            if lang[0:3] in x:
                tab = strtab[x]
    return tab[s]

def forcedel(fname):
    if os.path.exists(fname):
        os.remove(fname)

def forceren(src, dst):
    if(src==dst):
        return
    forcedel(dst)
    if os.path.exists(src):
        os.rename(src, dst)

def refill(board):
    try:
        filler = pcbnew.ZONE_FILLER(board)
        zones = board.Zones()
        filler.Fill(zones)
    except:
        message('Refill Failed')



class GerberZipperDialog(GerberZipperGui):
    def SetSizeHints(self, sz1, sz2):
        # DO NOTHING
        pass

    def __init__(self, parent):
        super(GerberZipperDialog, self).__init__(parent)#, title='Gerber-Zipper '+version, size=Em(65,12))
        
        InitEm()

        # Find the status bar for messages output
        self.statusBar = next((item for item in parent.GetChildren() if isinstance(item, wx.StatusBar)), None)
        
        # Load JSON settings from file, or use default and write it to disk
        prefix_path = os.path.join(os.path.dirname(__file__))
        settings_fname = os.path.join(prefix_path, 'settings.json')
        self.plugin_settings_data = {}
        if os.path.exists(settings_fname):
            self.plugin_settings_data = json.load(open(settings_fname, encoding='utf-8'))
        else:
            self.plugin_settings_data["default"] = 0
            json.dump(self.plugin_settings_data, open(settings_fname, "w"))

        
        #self.settings=dict(default_settings,**settings)
        self.settings=dict(default_settings)

        # Load manufacturer JSON files
        self.manufacturers_dir = os.path.join(os.path.dirname(__file__), 'Manufacturers')
        manufacturers_list = glob.glob('%s/*.json' % self.manufacturers_dir)
        self.json_data = []
        for fname in manufacturers_list:
            try:
                self.json_data.append(json.load(open(fname, encoding='utf-8')))
            except Exception as err:
                alert('JSON error \n\n File : %s\n%s' % (os.path.basename(fname), err.message), wx.ICON_WARNING)
        
        self.json_data = sorted(self.json_data, key=lambda x: x['Name'])
        
        # Setup manufacturer list
        for item in self.json_data:
            self.cb_manufacturers.Append(item['Name'])


        # Build details pane
        # Gerber
        self.layersGrid.DeleteCols(0,self.layersGrid.GetNumberCols())
        self.layersGrid.DeleteRows(0,self.layersGrid.GetNumberRows())
        #self.layersGrid.CreateGrid(len(layer_list), 2)
        self.layersGrid.AppendCols(2)
        self.layersGrid.SetColLabelValue(0, 'Layer')
        self.layersGrid.SetColLabelValue(1, 'Filename')
        
        #self.layersGrid.SetColLabelSize(Em(1,1)[1])
        self.layersGrid.ShowScrollbars(wx.SHOW_SB_NEVER,wx.SHOW_SB_DEFAULT)
        
        self.layersGrid.SetColSize(0, Em(7,1)[0])
        self.layersGrid.SetColSize(1, Em(9,1)[0])
        self.layersGrid.SetMinSize(Em(18,1))
        
        self.layersGrid.AppendRows(len(layer_list))
        for i in range(len(layer_list)):
            self.layersGrid.SetCellValue(i, 0, layer_list[i]['name'])
            self.layersGrid.SetReadOnly(i, 0, isReadOnly=True)


        # Drills
        self.drillsGrid.DeleteCols(0, self.drillsGrid.GetNumberCols())
        self.drillsGrid.DeleteRows(0, self.drillsGrid.GetNumberRows())
        self.drillsGrid.AppendCols(2)
        
        self.drillsGrid.ShowScrollbars(wx.SHOW_SB_NEVER,wx.SHOW_SB_NEVER)
        
        self.drillsGrid.SetColLabelValue(0, 'Drill')
        self.drillsGrid.SetColLabelValue(1, 'Filename')

        self.drillsGrid.SetColSize(0, Em(9,1)[0])
        self.drillsGrid.SetColSize(1, Em(9,1)[0])
        self.drillsGrid.SetMinSize(Em(18,1))
        #self.drillsGrid.SetColLabelSize(Em(1,1)[1])
        
        drillfile = ['Drill', 'DrillMap', 'NPTH', 'NPTHMap', 'Report']
        self.drillsGrid.AppendRows(len(drillfile))
        for i in range(len(drillfile)):
            self.drillsGrid.SetCellValue(i, 0, drillfile[i])
            self.drillsGrid.SetReadOnly(i, 0, True)
            self.drillsGrid.SetRowSize(i, Em(1,1)[1])


        mfr_i = self.plugin_settings_data.get("default",0)
        self.cb_manufacturers.SetSelection(mfr_i)
        
        self.SelectManufacturerAt(mfr_i)
        
        self.initialWindowSize = self.GetSize()
        self.hideSettingsPane()
    

    def SaveDefaults(self):
        prefix_path = os.path.join(os.path.dirname(__file__))
        settings_fname = os.path.join(prefix_path, 'settings.json')
        json.dump(self.plugin_settings_data, open(settings_fname,"w"))
        

    def SelectManufacturerAt(self, n):
        self.settings = self.json_data[n]
        
        # Save this selection as default
        self.plugin_settings_data["default"] = n
        self.SaveDefaults() 
        
        # Set fields values
        self.label_description.SetLabel(self.settings.get('Description', ''))
        self.tf_url.SetValue(self.settings.get('URL','---'))
        self.tf_gerberDir.SetValue(self.settings.get('GerberDir','Gerber'))
        self.tf_zipFilename.SetValue(self.settings.get('ZipFilename','*.ZIP'))

        self.FillUiFromSettings(self.settings)

    
    def FillUiFromSettings(self, settings):
        self.settings = dict(default_settings, **settings)
        
        layers = self.settings.get('Layers',{})
        for i in range(self.layersGrid.GetNumberRows()):
            k = self.layersGrid.GetCellValue(i, 0)
            if layers.get(k,None) != None:
                self.layersGrid.SetCellValue(i, 1, layers.get(k))
            else:
                self.layersGrid.SetCellValue(i, 1, '')
        
        drills = self.settings.get('Drill',{})
        for i in range(self.drillsGrid.GetNumberRows()):
            k = self.drillsGrid.GetCellValue(i,0)
            if drills.get(k,None) != None:
                self.drillsGrid.SetCellValue(i, 1, drills.get(k))
            else:
                self.drillsGrid.SetCellValue(i, 1, '')
        
        self.opt_PlotBorderAndTitle.SetValue(self.settings.get('PlotBorderAndTitle',False))
        self.opt_PlotFootprintValues.SetValue(self.settings.get('PlotFootprintValues',True))
        self.opt_PlotFootprintReferences.SetValue(self.settings.get('PlotFootprintReferences',True))
        self.opt_ForcePlotInvisible.SetValue(self.settings.get('ForcePlotInvisible',False))
        self.opt_ExcludeEdgeLayer.SetValue(self.settings.get('ExcludeEdgeLayer',True))
        self.opt_ExcludePadsFromSilk.SetValue(self.settings.get('ExcludePadsFromSilk',True))
        self.opt_DoNotTentVias.SetValue(self.settings.get('DoNotTentVias',False))
        self.opt_UseAuxOrigin.SetValue(self.settings.get('UseAuxOrigin', False))
        self.opt_LineWidth.SetValue(str(self.settings.get('LineWidth', 0.1)))
        self.opt_SubtractMaskFromSilk.SetValue(self.settings.get('SubtractMaskFromSilk', False))
        self.opt_UseExtendedX2format.SetValue(self.settings.get('UseExtendedX2format', False))
        self.opt_CoodinateFormat46.SetValue(self.settings.get('CoodinateFormat46',True))
        self.opt_IncludeNetlistInfo.SetValue(self.settings.get('IncludeNetlistInfo',False))
        self.opt_DrillUnit.SetSelection(1 if self.settings.get('DrillUnitMM',True) else 0)
        self.opt_MirrorYAxis.SetValue(self.settings.get('MirrorYAxis', False))
        self.opt_MinimalHeader.SetValue(self.settings.get('MinimalHeader', False))
        self.opt_MergePTHandNPTH.SetValue(self.settings.get('MergePTHandNPTH', False))
        self.opt_RouteModeForOvalHoles.SetValue(self.settings.get('RouteModeForOvalHoles', True))
        
        zeros = self.settings.get('ZerosFormat',{})
        i = 0
        for k in self.settings.get('ZerosFormat',{}):
            if(zeros[k]):
                i = {'DecimalFormat':0,'SuppressLeading':1,'SuppressTrailing':2,'KeepZeros':3}.get(k,0)
        self.opt_ZerosFormat.SetSelection(i)


        mapFormat = self.settings.get('MapFileFormat',{})
        i = 2
        for k in mapFormat:
            if(mapFormat[k]):
                i = {'HPGL':0,'PostScript':1,'Gerber':2,'DXF':3,'SVG':4,'PDF':5}.get(k,2)
        self.opt_MapFileFormat.SetSelection(i)
        
        
        files = self.settings.get('OptionalFiles',[])
        if len(files)==0:
            files=[{'name':'','content':''}]
        self.opt_OptionalFile.SetValue(files[0]['name'])
        self.opt_OptionalContent.SetValue(files[0]['content'])

    
    def FillSettingsFromUi(self, settings):
        layers = settings.get('Layers',{})
        for i in range(self.layersGrid.GetNumberRows()):
            k = self.layersGrid.GetCellValue(i, 0)
            v = self.layersGrid.GetCellValue(i, 1)
            layers[k] = v
        self.settings['Layers'] = layers
        
        drills = self.settings.get('Drill',{})
        for i in range(self.drillsGrid.GetNumberRows()):
            k = self.drillsGrid.GetCellValue(i, 0)
            v = self.drillsGrid.GetCellValue(i, 1)
            drills[k] = v
        self.settings['Drill'] = drills
        
        self.settings['PlotBorderAndTitle'] = self.opt_PlotBorderAndTitle.GetValue()
        self.settings['PlotFootprintValues'] = self.opt_PlotFootprintValues.GetValue()
        self.settings['PlotFootprintReferences'] = self.opt_PlotFootprintReferences.GetValue()
        self.settings['ForcePlotInvisible'] = self.opt_ForcePlotInvisible.GetValue()
        self.settings['ExcludeEdgeLayer'] = self.opt_ExcludeEdgeLayer.GetValue()
        self.settings['ExcludePadsFromSilk'] = self.opt_ExcludePadsFromSilk.GetValue()
        self.settings['DoNotTentVias'] = self.opt_DoNotTentVias.GetValue()
        self.settings['UseAuxOrigin'] = self.opt_UseAuxOrigin.GetValue()
        self.settings['LineWidth'] = self.opt_LineWidth.GetValue()
        self.settings['SubtractMaskFromSilk'] = self.opt_SubtractMaskFromSilk.GetValue()
        self.settings['UseExtendedX2format'] = self.opt_UseExtendedX2format.GetValue()
        self.settings['CoodinateFormat46'] = self.opt_CoodinateFormat46.GetValue()
        self.settings['IncludeNetlistInfo'] = self.opt_IncludeNetlistInfo.GetValue()
        self.settings['DrillUnitMM'] = True if self.opt_DrillUnit.GetSelection() else False
        self.settings['MirrorYAxis'] = self.opt_MirrorYAxis.GetValue()
        self.settings['MinimalHeader'] = self.opt_MinimalHeader.GetValue()
        self.settings['MergePTHandNPTH'] = self.opt_MergePTHandNPTH.GetValue()
        self.settings['RouteModeForOvalHoles'] = self.opt_RouteModeForOvalHoles.GetValue()
        
        zeros = self.settings['ZerosFormat']
        i = self.opt_ZerosFormat.GetSelection()
        zeros['DecimalFormat'] = i == 0
        zeros['SuppressLeading'] = i == 1
        zeros['SuppressTrailing'] = i == 2
        zeros['KeepZeros'] = i == 3
        
        mapFormat = self.settings['MapFileFormat']
        i = self.opt_MapFileFormat.GetSelection()
        mapFormat['HPGL'] = i == 0
        mapFormat['PostScript'] = i == 1
        mapFormat['Gerber'] = i == 2
        mapFormat['DXF'] = i == 3
        mapFormat['SVG'] = i == 4
        mapFormat['PDF'] = i == 5
        
        files = {'name':self.opt_OptionalFile.GetValue(), 'content':self.opt_OptionalContent.GetValue()}
        self.settings['OptionalFiles'] = [files]
    
    # Display message in parent's window status bar if any, otherwise it uses alert()
    def showMessage( self, message ):
        if self.statusBar:
            self.statusBar.PushStatusText("GerberZipper: %s" % message)
        else:
            alert("GerberZipper: %s" % message, wx.ICON_INFORMATION)


    def on_manufacturerChanged(self, event):
        obj = event.GetEventObject()
        self.SelectManufacturerAt(obj.GetSelection())
        event.Skip()
    
    def hideSettingsPane(self, hide=True):
        # Save window size with settings, to restore it when showing settings again.
        if self.settingsPanel.IsShown():
            self.initialWindowSize = self.GetSize()
        else:
            self.initialWindowSize.SetWidth(self.GetSize().GetWidth())

        if hide:
            self.settingsPanel.Hide()
            self.Fit()
            # Restore width
            self.SetSize(self.initialWindowSize.GetWidth(), self.GetSize().GetHeight())
        else: # show
            self.settingsPanel.Show()
            # Restore previous size
            self.SetSize(self.initialWindowSize)
            self.Layout()

            # Move in-screen if clipping the bottom of the display
            windowRectInScreen = self.GetScreenRect()
            screenRect = wx.Display(self).GetClientArea()
            diff = windowRectInScreen.GetBottom() - screenRect.GetBottom()
            if diff > 0:
                #self.Center(wx.VERTICAL)
                self.Move(self.GetPosition().x, self.GetPosition().y-diff)


    def on_showSettings(self, event):
        self.hideSettingsPane(hide = self.btn_showSettings.GetValue() == 0)
        event.Skip()
    
    def on_create(self, event):
        self.createFile()
        event.Skip()

    def on_close(self, event):
        event.Skip()
        #self.Close()
        self.Destroy()


    def generate_plots(self, board, board_basename, outputDirName, zipfiles):
        message('PlotStart')
        pc = pcbnew.PLOT_CONTROLLER(board)
        po = pc.GetPlotOptions()

        po.SetOutputDirectory(outputDirName)
        po.SetPlotFrameRef( self.settings.get('PlotBorderAndTitle',False))
        po.SetPlotValue( self.settings.get('PlotFootprintValues',True))
        po.SetPlotReference( self.settings.get('PlotFootprintReferences',True))
        po.SetPlotInvisibleText( self.settings.get('ForcePlotInvisible',False))
        po.SetExcludeEdgeLayer( self.settings.get('ExcludeEdgeLayer',True))
        if hasattr(po,'SetPlotPadsOnSilkLayer'):
            po.SetPlotPadsOnSilkLayer( not self.settings.get('ExcludePadsFromSilk',False))
        po.SetPlotViaOnMaskLayer( self.settings.get('DoNotTentVias',False))
        if hasattr(po,'SetUseAuxOrigin'):
            po.SetUseAuxOrigin(self.settings.get('UseAuxOrigin',False))
        if hasattr(po,'SetLineWidth'):
            po.SetLineWidth(FromMM(float(self.settings.get('LineWidth'))))
        po.SetSubtractMaskFromSilk(self.settings.get('SubtractMaskFromSilk',True))
        po.SetUseGerberX2format(self.settings.get('UseExtendedX2format',False))
        po.SetIncludeGerberNetlistInfo(self.settings.get('IncludeNetlistInfo',False))
        po.SetGerberPrecision(6 if self.settings.get('CoodinateFormat46',True) else 5)
        
        # SetDrillMarksType() : Draw Drill point to Cu layers if 1 (default)
        #  but seems set to 0 in Plot Dialog
        po.SetDrillMarksType(0)
        layer = self.settings.get('Layers',{})
        
        for i in range(len(layer_list)):
            layer_list[i]['fname'] = ''

        for i in layer:
            fnam = layer[i]
            id = getid(i)

            if (len(fnam) > 0 and board.IsLayerEnabled(id)):
                pc.SetLayer(id)
                pc.OpenPlotfile(i,PLOT_FORMAT_GERBER,i)
                pc.PlotLayer()
                pc.ClosePlot()
                targetname = '%s/%s' % (outputDirName, fnam.replace('*', board_basename))
                forcedel(targetname)
                forceren(pc.GetPlotFileName(), targetname)
                layer_list[getindex(i)]['fname'] = targetname
                zipfiles.append(targetname)

    def generate_drills(self, board, board_basename, outputDirName, zipfiles):
        message('Drill')
        drill_fname = ''
        drill_map_fname = ''
        npth_fname = ''
        npth_map_fname =''
        drill_report_fname = ''
        drill = self.settings.get('Drill',{})

        fname = drill.get('Drill','')
        if len(fname)>0:
            drill_fname = '%s/%s' % (outputDirName, fname.replace('*', board_basename))

        fname = drill.get('DrillMap','')
        if len(fname)>0:
            drill_map_fname = '%s/%s' % (outputDirName, fname.replace('*', board_basename))

        fname = drill.get('NPTH','')
        if len(fname)>0:
            npth_fname = '%s/%s' % (outputDirName, fname.replace('*', board_basename))

        fname = drill.get('NPTHMap','')
        if len(fname)>0:
            npth_map_fname = '%s/%s' % (outputDirName, fname.replace('*', board_basename))

        fname = drill.get('Report','')
        if len(fname)>0:
            drill_report_fname = '%s/%s' % (outputDirName, fname.replace('*', board_basename))


        ew = EXCELLON_WRITER(board)
        excellon_format = EXCELLON_WRITER.DECIMAL_FORMAT
        zeros = self.settings.get('ZerosFormat')
        if zeros.get('SuppressLeading'):
            excellon_format = EXCELLON_WRITER.SUPPRESS_LEADING
        if zeros.get('SuppressTrailing'):
            excellon_format = EXCELLON_WRITER.SUPPRESS_TRAILING
        if zeros.get('KeepZeros'):
            excellon_format = EXCELLON_WRITER.KEEP_ZEROS

        ew.SetFormat(self.settings.get('DrillUnitMM',True), excellon_format, 3, 3)
        offset = wxPoint(0,0)
        if self.settings.get('UseAuxOrigin',False):
            if hasattr(board, 'GetAuxOrigin'):
                offset = board.GetAuxOrigin()
            else:
                bds = board.GetDesignSettings()
                offset = bds.m_AuxOrigin
        
        ew.SetOptions(self.settings.get('MirrorYAxis',False), self.settings.get('MinimalHeader',False), offset, self.settings.get('MergePTHandNPTH',False))
        ew.SetRouteModeForOvalHoles(self.settings.get('RouteModeForOvalHoles'))
        map_format = pcbnew.PLOT_FORMAT_GERBER
        map_ext = 'gbr'
        
        map = self.settings.get('MapFileFormat')
        if map.get('HPGL'):
            map_format = pcbnew.PLOT_FORMAT_HPGL
            map_ext = 'plt'
        if map.get('PostScript'):
            map_format = pcbnew.PLOT_FORMAT_POST
            map_ext = 'ps'
        if map.get('Gerber'):
            map_format = pcbnew.PLOT_FORMAT_GERBER
            map_ext = 'gbr'
        if map.get('DXF'):
            map_format = pcbnew.PLOT_FORMAT_DXF
            map_ext = 'dxf'
        if map.get('SVG'):
            map_format = pcbnew.PLOT_FORMAT_SVG
            map_ext = 'svg'
        if map.get('PDF'):
            map_format = pcbnew.PLOT_FORMAT_PDF
            map_ext = 'pdf'
        
        ew.SetMapFileFormat(map_format)
        enable_map = len(drill_map_fname)>0 or len(npth_map_fname)>0

        message('MapFile')
        ew.CreateDrillandMapFilesSet(outputDirName,True,enable_map)
        
        if self.settings.get('MergePTHandNPTH',False):
            if drill_fname:
                forceren('%s/%s.drl' % (outputDirName, board_basename), drill_fname)
                zipfiles.append(drill_fname)

            if drill_map_fname:
                forceren('%s/%s-drl_map.%s' % (outputDirName, board_basename, map_ext), drill_map_fname)
                zipfiles.append(drill_map_fname)

        else:
            if drill_fname:
                forceren('%s/%s-PTH.drl' % (outputDirName, board_basename), drill_fname)
                zipfiles.append(drill_fname)

            if drill_map_fname:
                forceren('%s/%s-PTH-drl_map.%s' % (outputDirName, board_basename, map_ext), drill_map_fname)
                zipfiles.append(drill_map_fname)

            if npth_fname:
                forceren('%s/%s-NPTH.drl' % (outputDirName, board_basename), npth_fname)
                zipfiles.append(npth_fname)

            if npth_map_fname:
                forceren('%s/%s-NPTH-drl_map.gbr' % (outputDirName, board_basename), npth_map_fname)
                zipfiles.append(npth_map_fname)
        
        if drill_report_fname:
            ew.GenDrillReportFile(drill_report_fname)
            zipfiles.append(drill_report_fname)

    def generate_optionals(self, board, board_basename, outputDirName, zipfiles):
        message('Optional')
        files = self.settings.get('OptionalFiles',[])
        for n in range(len(files)):
            if(len(files[n]['name'])):
                optional_fname = '%s/%s' % (tmpdirname, files[n]['name'])
                optional_content = files[n]['content']
                optional_content = optional_content.replace('${basename}',board_basename)

                for i in range(len(layer_list)):
                    kpath = '${filepath('+layer_list[i]['name']+')}'
                    kname = '${filename('+layer_list[i]['name']+')}'
                    path = layer_list[i]['fname']
                    name = os.path.basename(path)
                    optional_content = optional_content.replace(kname,name)

                if optional_fname:
                    with codecs.open(optional_fname, 'w', 'utf-8') as f:
                        f.write(optional_content)

                zipfiles.append(optional_fname)


    def createFile(self):
        try:
            self.FillSettingsFromUi(self.settings)
            
            board = pcbnew.GetBoard()
            board_fname = board.GetFileName()
            board_dir = os.path.dirname(board_fname)
            board_basename = (os.path.splitext(os.path.basename(board_fname)))[0]
            
            gerber_dir = '%s/%s' % (board_dir, self.tf_gerberDir.GetValue())
            zip_fname = '%s/%s' % (gerber_dir, self.tf_zipFilename.GetValue().replace('*',board_basename))
            
            # Remove previous ZIP file
            forcedel(zip_fname)

            if not os.path.exists(gerber_dir):
                os.makedirs(gerber_dir)
            
            # Refill all zones
            refill(board)
        
            # Save generated files in temp folder, deleted automatically
            with tempfile.TemporaryDirectory() as tmpdirname:
                zipfiles = [] # File list to zip

                # Generate gerber files
                self.generate_plots(board, board_basename, tmpdirname, zipfiles)
                self.generate_drills(board, board_basename, tmpdirname, zipfiles)
                self.generate_optionals(board, board_basename, tmpdirname, zipfiles)

                # Create ZIP
                message('Zip')
                with zipfile.ZipFile(zip_fname,'w',compression=zipfile.ZIP_DEFLATED) as f:
                    for i in range(len(zipfiles)):
                        fnam = zipfiles[i]
                        if os.path.exists(fnam):
                            f.write(fnam, os.path.basename(fnam))
            

            self.Hide()
            
            # Show success on status bar
            #alert("GerberZipper Complete. \n\n Output file : %s" % zip_fname, wx.ICON_INFORMATION)
            self.showMessage("ZIP generated: '%s'" % zip_fname)

            self.Destroy()
            
        except Exception:
            s = traceback.format_exc(chain=False)
            print(s)
            alert(s, wx.ICON_ERROR)


class GerberZipperAction( pcbnew.ActionPlugin ):
    def defaults( self ):
        self.name = "Gerber Zipper"
        self.category = "Plot"
        self.description = "Make Gerber-Zip-file for selected PCB manufacturers"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png')

    def Run(self):
        # grab PCB editor frame
        self.frame = wx.FindWindowByName("PcbFrame")

        # show dialog
        dlg = GerberZipperDialog(self.frame)
        dlg.CenterOnParent()

        dlg.Show()
