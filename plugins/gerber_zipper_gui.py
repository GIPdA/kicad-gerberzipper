# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class GerberZipperGui
###########################################################################

class GerberZipperGui ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 693,829 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer37 = wx.BoxSizer( wx.VERTICAL )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Make Gerber files and ZIP for specific PCB manufacturers.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		mainSizer.Add( self.m_staticText1, 0, wx.ALL|wx.EXPAND, 5 )

		self.mainSizerLine = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		mainSizer.Add( self.mainSizerLine, 0, wx.EXPAND |wx.ALL, 5 )

		fgSizer4 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer4.AddGrowableCol( 1 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Manufacturer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		fgSizer4.Add( self.m_staticText3, 0, wx.ALL, 5 )

		cb_manufacturersChoices = []
		self.cb_manufacturers = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cb_manufacturersChoices, 0 )
		self.cb_manufacturers.SetSelection( 0 )
		fgSizer4.Add( self.cb_manufacturers, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"URL", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		fgSizer4.Add( self.m_staticText5, 0, wx.ALL, 5 )

		self.tf_url = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.tf_url.Enable( False )

		fgSizer4.Add( self.tf_url, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Gerber Directory", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		fgSizer4.Add( self.m_staticText6, 0, wx.ALL, 5 )

		self.tf_gerberDir = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.tf_gerberDir, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Zip Filename", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		fgSizer4.Add( self.m_staticText7, 0, wx.ALL, 5 )

		self.tf_zipFilename = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.tf_zipFilename, 0, wx.ALL|wx.EXPAND, 5 )
		self.tf_zipFilename.SetFocus()

		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Description", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		fgSizer4.Add( self.m_staticText8, 0, wx.ALL, 5 )

		self.label_description = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_description.Wrap( -1 )

		fgSizer4.Add( self.label_description, 0, wx.ALL|wx.EXPAND, 5 )


		mainSizer.Add( fgSizer4, 1, wx.EXPAND, 5 )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_showSettings = wx.ToggleButton( self, wx.ID_ANY, u"Show Settings Data", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.btn_showSettings, 0, wx.ALL, 5 )

		self.btn_create = wx.Button( self, wx.ID_ANY, u"Create Gerber and ZIP file", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.btn_create, 0, wx.ALL, 5 )


		bSizer3.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_close = wx.Button( self, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.btn_close, 0, wx.ALL, 5 )


		mainSizer.Add( bSizer3, 0, wx.EXPAND, 5 )


		bSizer37.Add( mainSizer, 1, wx.EXPAND, 5 )

		self.settingsPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		settingsSizer = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText13 = wx.StaticText( self.settingsPanel, wx.ID_ANY, u"The changes made here are temporary. If you want to change it permanently, edit the corresponding json file.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )

		settingsSizer.Add( self.m_staticText13, 0, wx.ALL|wx.EXPAND, 5 )

		self.settingsSizerLine = wx.StaticLine( self.settingsPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		settingsSizer.Add( self.settingsSizerLine, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		sbSizer6 = wx.StaticBoxSizer( wx.StaticBox( self.settingsPanel, wx.ID_ANY, u"Gerber" ), wx.HORIZONTAL )

		self.layersGrid = wx.grid.Grid( sbSizer6.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.layersGrid.CreateGrid( 0, 0 )
		self.layersGrid.EnableEditing( True )
		self.layersGrid.EnableGridLines( True )
		self.layersGrid.EnableDragGridSize( False )
		self.layersGrid.SetMargins( 0, 0 )

		# Columns
		self.layersGrid.EnableDragColMove( False )
		self.layersGrid.EnableDragColSize( True )
		self.layersGrid.SetColLabelSize( wx.grid.GRID_AUTOSIZE )
		self.layersGrid.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.layersGrid.AutoSizeRows()
		self.layersGrid.EnableDragRowSize( False )
		self.layersGrid.SetRowLabelSize( 0 )
		self.layersGrid.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.layersGrid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		self.layersGrid.SetMinSize( wx.Size( 100,-1 ) )

		sbSizer6.Add( self.layersGrid, 0, wx.EXPAND, 5 )

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.opt_PlotBorderAndTitle = wx.CheckBox( sbSizer6.GetStaticBox(), wx.ID_ANY, u"PlotBorderAndTitle", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.opt_PlotBorderAndTitle, 0, wx.ALL, 5 )

		self.opt_PlotFootprintValues = wx.CheckBox( sbSizer6.GetStaticBox(), wx.ID_ANY, u"PlotFootprintValues", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.opt_PlotFootprintValues, 0, wx.ALL, 5 )

		self.opt_PlotFootprintReferences = wx.CheckBox( sbSizer6.GetStaticBox(), wx.ID_ANY, u"PlotFootprintReferences", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.opt_PlotFootprintReferences, 0, wx.ALL, 5 )

		self.opt_ForcePlotInvisible = wx.CheckBox( sbSizer6.GetStaticBox(), wx.ID_ANY, u"ForcePlotInvisible", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.opt_ForcePlotInvisible, 0, wx.ALL, 5 )

		self.opt_ExcludeEdgeLayer = wx.CheckBox( sbSizer6.GetStaticBox(), wx.ID_ANY, u"ExcludeEdgeLayer", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.opt_ExcludeEdgeLayer, 0, wx.ALL, 5 )

		self.opt_ExcludePadsFromSilk = wx.CheckBox( sbSizer6.GetStaticBox(), wx.ID_ANY, u"ExcludePadsFromSilk", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.opt_ExcludePadsFromSilk, 0, wx.ALL, 5 )

		self.opt_DoNotTentVias = wx.CheckBox( sbSizer6.GetStaticBox(), wx.ID_ANY, u"DoNotTentVias", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.opt_DoNotTentVias, 0, wx.ALL, 5 )

		self.opt_UseAuxOrigin = wx.CheckBox( sbSizer6.GetStaticBox(), wx.ID_ANY, u"UseAuxOrigin", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.opt_UseAuxOrigin, 0, wx.ALL, 5 )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText12 = wx.StaticText( sbSizer6.GetStaticBox(), wx.ID_ANY, u"LineWidth(mm):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		bSizer9.Add( self.m_staticText12, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.opt_LineWidth = wx.TextCtrl( sbSizer6.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.opt_LineWidth, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		bSizer8.Add( bSizer9, 0, wx.EXPAND, 5 )

		self.opt_SubtractMaskFromSilk = wx.CheckBox( sbSizer6.GetStaticBox(), wx.ID_ANY, u"SubtractMaskFromSilk", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.opt_SubtractMaskFromSilk, 0, wx.ALL, 5 )

		self.opt_UseExtendedX2format = wx.CheckBox( sbSizer6.GetStaticBox(), wx.ID_ANY, u"UseExtendedX2format", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.opt_UseExtendedX2format, 0, wx.ALL, 5 )

		self.opt_CoodinateFormat46 = wx.CheckBox( sbSizer6.GetStaticBox(), wx.ID_ANY, u"CoodinateFormat46", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.opt_CoodinateFormat46, 0, wx.ALL, 5 )

		self.opt_IncludeNetlistInfo = wx.CheckBox( sbSizer6.GetStaticBox(), wx.ID_ANY, u"IncludeNetlistInfo", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.opt_IncludeNetlistInfo, 0, wx.ALL, 5 )


		sbSizer6.Add( bSizer8, 1, wx.EXPAND, 5 )


		bSizer7.Add( sbSizer6, 2, wx.EXPAND, 5 )


		bSizer12.Add( bSizer7, 1, wx.EXPAND, 5 )

		sbSizer8 = wx.StaticBoxSizer( wx.StaticBox( self.settingsPanel, wx.ID_ANY, u"Drill" ), wx.VERTICAL )

		self.drillsGrid = wx.grid.Grid( sbSizer8.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.drillsGrid.CreateGrid( 0, 0 )
		self.drillsGrid.EnableEditing( True )
		self.drillsGrid.EnableGridLines( True )
		self.drillsGrid.EnableDragGridSize( False )
		self.drillsGrid.SetMargins( 0, 0 )

		# Columns
		self.drillsGrid.EnableDragColMove( False )
		self.drillsGrid.EnableDragColSize( True )
		self.drillsGrid.SetColLabelSize( wx.grid.GRID_AUTOSIZE )
		self.drillsGrid.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.drillsGrid.AutoSizeRows()
		self.drillsGrid.EnableDragRowSize( False )
		self.drillsGrid.SetRowLabelSize( 0 )
		self.drillsGrid.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.drillsGrid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		sbSizer8.Add( self.drillsGrid, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer81 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText10 = wx.StaticText( sbSizer8.GetStaticBox(), wx.ID_ANY, u"Drill Unit:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		bSizer81.Add( self.m_staticText10, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		opt_DrillUnitChoices = [ u"mm", u"inch" ]
		self.opt_DrillUnit = wx.Choice( sbSizer8.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, opt_DrillUnitChoices, 0 )
		self.opt_DrillUnit.SetSelection( 0 )
		bSizer81.Add( self.opt_DrillUnit, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		sbSizer8.Add( bSizer81, 0, wx.EXPAND, 5 )

		self.opt_MirrorYAxis = wx.CheckBox( sbSizer8.GetStaticBox(), wx.ID_ANY, u"MirrorYAxis", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer8.Add( self.opt_MirrorYAxis, 0, wx.ALL, 5 )

		self.opt_MinimalHeader = wx.CheckBox( sbSizer8.GetStaticBox(), wx.ID_ANY, u"MinimalHeader", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer8.Add( self.opt_MinimalHeader, 0, wx.ALL, 5 )

		self.opt_MergePTHandNPTH = wx.CheckBox( sbSizer8.GetStaticBox(), wx.ID_ANY, u"MergePTHandNPTH", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer8.Add( self.opt_MergePTHandNPTH, 0, wx.ALL, 5 )

		self.opt_RouteModeForOvalHoles = wx.CheckBox( sbSizer8.GetStaticBox(), wx.ID_ANY, u"RouteModeForOvalHoles", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer8.Add( self.opt_RouteModeForOvalHoles, 0, wx.ALL, 5 )

		bSizer91 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText111 = wx.StaticText( sbSizer8.GetStaticBox(), wx.ID_ANY, u"Zeros:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText111.Wrap( -1 )

		bSizer91.Add( self.m_staticText111, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		opt_ZerosFormatChoices = [ u"DecimalFormat", u"SuppressLeading", u"SuppresTrailing", u"KeepZeros" ]
		self.opt_ZerosFormat = wx.Choice( sbSizer8.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, opt_ZerosFormatChoices, 0 )
		self.opt_ZerosFormat.SetSelection( 0 )
		bSizer91.Add( self.opt_ZerosFormat, 0, wx.ALL, 5 )


		sbSizer8.Add( bSizer91, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText121 = wx.StaticText( sbSizer8.GetStaticBox(), wx.ID_ANY, u"MapFileFormat:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText121.Wrap( -1 )

		bSizer10.Add( self.m_staticText121, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		opt_MapFileFormatChoices = [ u"HPGL", u"PostScript", u"Gerber", u"DXF", u"SVG", u"PDF" ]
		self.opt_MapFileFormat = wx.Choice( sbSizer8.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, opt_MapFileFormatChoices, 0 )
		self.opt_MapFileFormat.SetSelection( 0 )
		bSizer10.Add( self.opt_MapFileFormat, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		sbSizer8.Add( bSizer10, 0, wx.EXPAND, 5 )


		bSizer12.Add( sbSizer8, 1, wx.EXPAND, 5 )


		settingsSizer.Add( bSizer12, 1, wx.EXPAND, 5 )

		sbSizer9 = wx.StaticBoxSizer( wx.StaticBox( self.settingsPanel, wx.ID_ANY, u"Other" ), wx.VERTICAL )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText11 = wx.StaticText( sbSizer9.GetStaticBox(), wx.ID_ANY, u"OptionalFile:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		bSizer11.Add( self.m_staticText11, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.opt_OptionalFile = wx.TextCtrl( sbSizer9.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.opt_OptionalFile, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		sbSizer9.Add( bSizer11, 0, wx.EXPAND, 5 )

		self.opt_OptionalContent = wx.TextCtrl( sbSizer9.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer9.Add( self.opt_OptionalContent, 1, wx.ALL|wx.EXPAND, 5 )


		settingsSizer.Add( sbSizer9, 1, wx.EXPAND, 5 )


		self.settingsPanel.SetSizer( settingsSizer )
		self.settingsPanel.Layout()
		settingsSizer.Fit( self.settingsPanel )
		bSizer37.Add( self.settingsPanel, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer37 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.cb_manufacturers.Bind( wx.EVT_CHOICE, self.on_manufacturerChanged )
		self.btn_showSettings.Bind( wx.EVT_TOGGLEBUTTON, self.on_showSettings )
		self.btn_create.Bind( wx.EVT_BUTTON, self.on_create )
		self.btn_close.Bind( wx.EVT_BUTTON, self.on_close )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def on_manufacturerChanged( self, event ):
		event.Skip()

	def on_showSettings( self, event ):
		event.Skip()

	def on_create( self, event ):
		event.Skip()

	def on_close( self, event ):
		event.Skip()
