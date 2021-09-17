## Sid Meier's Civilization 4
## Copyright Firaxis Games 2008

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import array


#R&R mod, vetiarvind, trade groups - start
import CvPopupInterface
import CvEventInterface 
#R&R mod, vetiarvind, trade groups - end

#import time

##
## New Trade Routes Advisor
## Version 1.02
## by koma13
##

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvTradeCitySelector:
	"Trade Routes Advisor"
	
	def __init__(self):
		
		self.WIDGET_ID = "TradeCityWidget"
		self.nWidgetCount = 0
		
		self.SCREEN_NAME = "TradeCitiesScreen"
		self.BACKGROUND_ID = "TradeCitiesBackground"

		self.XResolution = 0
		self.YResolution = 0

		# Table enums
		self.NO_TABLE = -1
		self.CITY_TABLE = 1
		#R&R mod, vetiarvind, trade groups - start
		self.LOAD_GROUP_TABLE = 2 		
		self.DELETE_GROUP_TABLE = 3
		#R&R mod, vetiarvind, trade groups - end

		# Button ids
		self.SELECT_ID = 1
		self.DANGER_ID = 2
		self.RETURN_ID = 3
		
		#R&R mod, vetiarvind, trade groups - START
		self.LOAD_GROUP_ID = 4
		self.SAVE_GROUP_ID = 5		
		self.DELETE_GROUP_ID = 6
		#R&R mod, vetiarvind, trade groups - END

		
	def interfaceScreen (self):
		screen = self.getScreen()
		if screen.isActive():
			return
		
		self.player = gc.getPlayer(gc.getGame().getActivePlayer())
		
		# Transport Unit
		self.pTransport = CyInterface().getHeadSelectedUnit()
		if self.pTransport == None:
			return
		
		# City list
		self.CityList = []
		self.CityDistanceList = []
		self.ExistingCities, self.AssignedCities = [], {}
		self.AccessibleCities = []

		(city, iter) = self.player.firstCity(false)
		while (city):
			self.CityList.append(city)
			turns = self.pTransport.generatePath2(city.plot(), 0, false, true)
			if turns >= 0:
				self.AccessibleCities.append(true)
				self.CityDistanceList.append(turns)
			else:
				self.AccessibleCities.append(false)
				self.CityDistanceList.append(-1)
			self.AssignedCities[city.getID()] = self.pTransport.getGroup().isAssignedTradeRoute(city.getID())
			(city, iter) = self.player.nextCity(iter, false)
		
		if self.CityList == []:
			return
		
		
		self.bAssigned, self.bSelected = false, false
		self.bDanger = self.pTransport.isIgnoreDanger()
		
		# Table names		
		self.TableNames = []
		self.TableNames.append("CityTable")
		#R&R mod, vetiarvind, trade groups - START
		self.TableNames.append("LoadGroupTable")
		self.TableNames.append("DeleteGroupTable")
		#R&R mod, vetiarvind, trade groups - END
		
		self.TableLabel = []		
		szTitle = localText.getText("TXT_KEY_TRADE_ROUTES_MAIN_TABLE", ())
		self.TableLabel.append(szTitle)	
		#R&R mod, vetiarvind, trade groups - START				
		szTitle = localText.getText("TXT_KEY_TRADE_ROUTES_LOAD_GROUP_TABLE", ()) 
		self.TableLabel.append(szTitle) 
		szTitle = localText.getText("TXT_KEY_TRADE_ROUTES_DELETE_GROUP_TABLE", ()) 		
		self.TableLabel.append(szTitle) 
		#R&R mod, vetiarvind, trade groups - END		
		
		self.CURRENT_TABLE = self.NO_TABLE
		
		# Widget positions
		self.XResolution = self.getScreen().getXResolution()
		self.YResolution = self.getScreen().getYResolution()

		self.STANDARD_MARGIN = 16
		
		self.PANEL_WIDTH = 420
		self.PANEL_X = self.XResolution - self.PANEL_WIDTH - self.STANDARD_MARGIN
		self.PANEL_Y = 55
		
		self.PANEL_HEIGHT = self.YResolution - self.PANEL_Y - self.STANDARD_MARGIN - self.YResolution * 31 * 28 / 10000
		self.PANEL_BORDER_SIZE = 3
		
		self.PREVIEW_X = self.STANDARD_MARGIN
		self.PREVIEW_WIDTH = (self.PANEL_WIDTH - self.STANDARD_MARGIN * 3) / 3
		self.PREVIEW_HEIGHT = self.PREVIEW_WIDTH * 3 / 4
		self.PREVIEW_Y = self.PANEL_HEIGHT - self.PREVIEW_HEIGHT - self.STANDARD_MARGIN - 36
		
		self.TABLE_X = self.STANDARD_MARGIN
		self.TABLE_Y = self.STANDARD_MARGIN * 2
		self.TABLE_WIDTH = self.PANEL_WIDTH - self.STANDARD_MARGIN * 2
		self.TABLE_HEIGHT = self.PREVIEW_Y - self.TABLE_Y - self.STANDARD_MARGIN / 2 - 40 #R&R mod, vetiarvind, trade groups
		self.ROW_HIGHT = 32		
		
		self.EXIT_Y = self.PANEL_HEIGHT - 45
		
		#R&R mod, vetiarvind, trade groups - start
		self.GROUPBUTTON_Y = self.EXIT_Y - 140
		self.GROUPBUTTON_WIDTH = self.TABLE_WIDTH/3 - 10
		#R&R mod, vetiarvind, trade groups - end
		
		self.BUTTON_SIZE = 24
		self.BUTTON_X = self.PANEL_WIDTH - self.STANDARD_MARGIN - self.BUTTON_SIZE * 4 - 4
		self.BUTTON_Y = self.STANDARD_MARGIN / 4
		self.BUTTON_WIDTH = self.BUTTON_SIZE * 4 + 8
		self.BUTTON_HEIGHT = self.BUTTON_SIZE + 2
		
		# Set the background and exit button, and show the screen
		screen.setRenderInterfaceOnly(False)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.setDimensions(self.PANEL_X, self.PANEL_Y, self.PANEL_WIDTH, self.PANEL_HEIGHT)
		screen.showWindowBackground(False)
		
		screen.addDDSGFC(self.BACKGROUND_ID, "Art/Interface/Screens/TradeRoutes/Background.dds", 0, 0, self.PANEL_WIDTH, self.PANEL_HEIGHT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		self.szTitle = "PanelTitle"
		screen.setLabelAt( self.szTitle, self.BACKGROUND_ID, u"<font=3b>-</font>", CvUtil.FONT_LEFT_JUSTIFY, self.STANDARD_MARGIN, self.STANDARD_MARGIN + 2, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		#R&R mod, vetiarvind, trade groups - start		
		
		screen.setButtonGFC("BtnLoad", u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_SCREEN_LOAD_GROUP", ()).upper() + u"</font>", "", self.TABLE_X, self.GROUPBUTTON_Y, self.GROUPBUTTON_WIDTH, 30, WidgetTypes.WIDGET_GENERAL, self.LOAD_GROUP_ID, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("BtnSave", u"<font=3b>" + localText.getText("TXT_KEY_PITBOSS_SAVE", ()).upper() + u"</font>", "", self.TABLE_X + self.TABLE_WIDTH/3, self.GROUPBUTTON_Y, self.GROUPBUTTON_WIDTH, 30, WidgetTypes.WIDGET_GENERAL, self.SAVE_GROUP_ID, -1, ButtonStyles.BUTTON_STYLE_STANDARD)	
		screen.setButtonGFC("BtnDelete", u"<font=3b>" + localText.getText("TXT_KEY_GLOBELAYER_STRATEGY_DELETE", ()).upper() + u"</font>", "", self.TABLE_X + self.TABLE_WIDTH*2/3, self.GROUPBUTTON_Y, self.GROUPBUTTON_WIDTH, 30, WidgetTypes.WIDGET_GENERAL, self.DELETE_GROUP_ID, -1, ButtonStyles.BUTTON_STYLE_STANDARD)	
		
		#R&R mod, vetiarvind, trade groups - end
		
		screen.setButtonGFC("ScreenExit", u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + u"</font>", "", self.TABLE_X, self.EXIT_Y, self.TABLE_WIDTH, 30, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setActivation( "ScreenExit", ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )
		
		# Panel border
		szBorderArt = "Art/Interface/Screens/TradeRoutes/Pixel.dds"
		
		screen.addDDSGFC(self.getNextWidgetName(), szBorderArt, 0, 0, self.PANEL_WIDTH, self.PANEL_BORDER_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addDDSGFC(self.getNextWidgetName(), szBorderArt, self.PANEL_WIDTH - self.PANEL_BORDER_SIZE, self.PANEL_BORDER_SIZE, self.PANEL_BORDER_SIZE, self.PANEL_HEIGHT - self.PANEL_BORDER_SIZE * 2, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addDDSGFC(self.getNextWidgetName(), szBorderArt, 0, self.PANEL_HEIGHT - self.PANEL_BORDER_SIZE, self.PANEL_WIDTH, self.PANEL_BORDER_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addDDSGFC(self.getNextWidgetName(), szBorderArt, 0, self.PANEL_BORDER_SIZE, self.PANEL_BORDER_SIZE, self.PANEL_HEIGHT - self.PANEL_BORDER_SIZE * 2, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		# Upper buttons
		self.szButtonPanel = "ButtonPanel"
		
		screen.addMultiListControlGFC(self.szButtonPanel, u"", self.BUTTON_X, self.BUTTON_Y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT, 0, self.BUTTON_SIZE, self.BUTTON_SIZE, TableStyles.TABLE_STYLE_STANDARD )
			
		CyCamera().LookAtUnit(self.pTransport)
		
		self.cityTable()
		
		return 0

	
	def getCityAssignment(self, iCity):
		if self.AssignedCities[iCity]:
			szLabel = u"%c" % CyGame().getSymbolID(FontSymbols.CHECKBOX_SELECTED_CHAR)
		elif not self.AssignedCities[iCity]:
			szLabel = u"%c" % CyGame().getSymbolID(FontSymbols.CHECKBOX_CHAR)
		else:
			szLabel = u"x"
		return szLabel

	
	def toggleCityAssignment(self, iRow):
		iCity = self.getCityByTableRow(iRow)
			
		if self.AssignedCities[iCity]:
			self.AssignedCities[iCity] = false
			szLabel = u"%c" % CyGame().getSymbolID(FontSymbols.CHECKBOX_CHAR)
		elif not self.AssignedCities[iCity]:
			self.AssignedCities[iCity] = true
			szLabel = u"%c" % CyGame().getSymbolID(FontSymbols.CHECKBOX_SELECTED_CHAR)
		else:
			szLabel = u"x"
		
		self.getScreen().setTableText(self.TableNames[self.CURRENT_TABLE], 1, iRow, szLabel, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
	
	def getCityByTableRow(self, iRow):
		return int(self.getScreen().getTableText(self.TableNames[self.CURRENT_TABLE], 0, iRow))

	def cityTable(self):
		# Export, import table
		screen = self.getScreen()
		
		screen.hide(self.TableNames[self.CURRENT_TABLE])
		self.CURRENT_TABLE = self.CITY_TABLE
			
		szTable = self.TableNames[self.CURRENT_TABLE]
		szYieldHeader = u"city list"
			
		screen.modifyLabel(self.szTitle, u"<font=3b>" + self.TableLabel[self.CURRENT_TABLE] + u"</font>", CvUtil.FONT_LEFT_JUSTIFY)
		screen.addTableControlGFC(szTable, 5, self.TABLE_X, self.TABLE_Y, self.TABLE_WIDTH, self.TABLE_HEIGHT, true, false, 32, 32, TableStyles.TABLE_STYLE_STANDARD)
		screen.setStyle(szTable, "Table_StandardCiv_Style")
		screen.enableSort(szTable)
		screen.enableSelect(szTable, true)
		screen.setTableColumnHeader(szTable, 0, u"id", 90)
		screen.setTableColumnHeader(szTable, 1, u"", 32)
		screen.setTableColumnHeader(szTable, 2, u"<img=%s size=16></img>" % "Art/Interface/Screens/TradeRoutes/Anchor.dds", 32)
		screen.setTableColumnHeader(szTable, 3, localText.getText("TXT_KEY_TRADE_ROUTES_EXPORT_TABLE_2", ()), self.TABLE_WIDTH * 2 / 3 - 80)
		screen.setTableColumnHeader(szTable, 4, u"distance", 60)
		
		iI = 0
		for city in self.CityList:
			if self.AccessibleCities[iI]:
				szColor = u"<color=255,255,255>"
			else:
				szColor = u"<color=200,80,80>"
			screen.appendTableRow(szTable)
			screen.setTableRowHeight(szTable, iI, self.ROW_HIGHT)
			screen.setTableText(szTable, 0, iI, u"%08d" % city.getID(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableText(szTable, 1, iI, self.getCityAssignment(city.getID()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableText(szTable, 2, iI, self.getHarbor(city), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableText(szTable, 3, iI, szColor + u"%s" % city.getName() + u"</color>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText(szTable, 4, iI, u"%02d" % self.CityDistanceList[iI], "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			
			iI += 1
			
		self.updateButtons()
	
	#R&R mod, vetiarvind, trade groups - start
	
	
	def populateGroupTable(self, newTable, headerLabel):
		#self.getScreen().modifyLabel(self.szTitle, u"<font=3b>" + self.TableLabel[self.CURRENT_TABLE] + "blaa" + u"</font>", CvUtil.FONT_LEFT_JUSTIFY)		
		
		screen = self.getScreen()		
		screen.hide(self.TableNames[self.CURRENT_TABLE])
		self.CURRENT_TABLE = newTable
		screen.modifyLabel(self.szTitle, u"<font=3b>" + self.TableLabel[self.CURRENT_TABLE] + headerLabel + u"</font>", CvUtil.FONT_LEFT_JUSTIFY)	
		
		
		szTable = self.TableNames[self.CURRENT_TABLE]		
		screen.addTableControlGFC(szTable, 4, self.TABLE_X, self.TABLE_Y, self.TABLE_WIDTH, self.TABLE_HEIGHT, true, false, 32, 32, TableStyles.TABLE_STYLE_STANDARD)
		screen.setStyle(szTable, "Table_StandardCiv_Style")
		screen.enableSort(szTable)
		screen.enableSelect(szTable, false)
		screen.setTableColumnHeader(szTable, 0, u"id", 0)		
		screen.setTableColumnHeader(szTable, 1, u"Routes", 0)		
		screen.setTableColumnHeader(szTable, 2, localText.getText("TXT_KEY_NAME_COL_TRADE_GROUP", ()), self.TABLE_WIDTH / 4)				
		screen.setTableColumnHeader(szTable, 3, localText.getText("TXT_KEY_DESC_COL_TRADE_GROUP", ()), self.TABLE_WIDTH * 3 / 4)		
		iI = 0
		numTg = self.player.getNumTradeGroups()		
		
		for itg in range(numTg):
			tg = self.player.getTradeGroup(itg)
			
			iRoutes = []			
			iRouteDetails = {}
			iRC = tg.getRouteCount()
			
			for iRt in range(iRC):
				rt = tg.getRouteByIndex(iRt)				
				srcCityName = rt.getSourceCityName()
				destCityName = rt.getDestinationCityName()
				if len(srcCityName)==0 or len(destCityName) == 0:
					continue
				iRoutes.append(str(rt.getSourceCity().iID) + " " + str(rt.getDestinationCity().iID) + " " + str(rt.getYield()))	
				descKeyStr = srcCityName + "-" + destCityName				
				if descKeyStr in iRouteDetails:
					iRouteDetails[descKeyStr].append(u"<font=3>%c</font>" % gc.getYieldInfo(rt.getYield()).getChar())
				else:
					iRouteDetails[descKeyStr] = [u"<font=3>%c</font>" % gc.getYieldInfo(rt.getYield()).getChar()]
				
			routeIdsStr = ','.join(str(x) for x in iRoutes)			
			routeDetailsStr = ','.join("%s%s" % (''.join(val), key) for (key, val) in iRouteDetails.iteritems() )
			screen.appendTableRow(szTable)
			screen.setTableRowHeight(szTable, iI, self.ROW_HIGHT)
			screen.setTableText(szTable, 0, iI, u"%d" % tg.getID(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableText(szTable, 1, iI, u"%s" % routeIdsStr, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableText(szTable, 2, iI, u"%s" % tg.getName(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)			
			screen.setTableText(szTable, 3, iI, u"%s" % routeDetailsStr, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			
			iI += 1		
		self.updateButtons()
		return
	
	# displays the load group table
	def loadGroupTable(self):			
		self.populateGroupTable(self.LOAD_GROUP_TABLE, localText.getText("TXT_KEY_HELP_LOAD_TRADE_GROUP", ()))		
		return		
		
	#concat route id's in form (s1 d1 y1,s2 d2 y2...) and pass into popup for save
	def saveGroupPopup(self):								
		idlist=[]
		
		for pRoute in self.CurrentList:
			if self.AssignedRoutes[pRoute.getID()]:
				idlist.append(str(pRoute.getSourceCity().iID) + " " + str(pRoute.getDestinationCity().iID) + " " + str(pRoute.getYield()))

		idstr =','.join(str(x) for x in idlist)		
		popupInfo = CyPopupInfo()		
		popupInfo.setText(idstr) 
		
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_SAVE_TRADEGROUP)
		CyInterface().addPopup(popupInfo, gc.getGame().getActivePlayer(), true, false)			
		return	
		
	def deleteGroupTable(self):		
		self.populateGroupTable(self.DELETE_GROUP_TABLE, localText.getText("TXT_KEY_HELP_DELETE_TRADE_GROUP", ()))
		return	
		
	#Loads selected routes in trade group into the main trade screen
	def loadSelectedGroup(self, iRow):		
		for pRoute in self.CurrentList:			
			self.AssignedRoutes[pRoute.getID()] = false
			
		tableCellValue = str(self.getScreen().getTableText(self.TableNames[self.CURRENT_TABLE], 1, iRow))
		
		routeTokens = tableCellValue.split(",")
				
		for token in routeTokens:
			spl = token.split(" ")			
			for pRoute in self.CurrentList:				
				if str(pRoute.getSourceCity().iID) == spl[0] and str(pRoute.getDestinationCity().iID) == spl[1] and str(pRoute.getYield()) == spl[2]:								
					self.AssignedRoutes[pRoute.getID()] = true		
		
		self.routesTable(false)		
		self.updateRoutes()
		
		
		return
		
	#"deletes selected row"		
	def deleteSelectedGroup(self, iRow):
		tableCellValue = str(self.getScreen().getTableText(self.TableNames[self.CURRENT_TABLE], 0, iRow))
		
		self.player.removeTradeRouteGroup(int(tableCellValue))						
		
		self.routesTable(false)						
		
		return
		
	#R&R mod, vetiarvind, trade groups - end
	
	def getHarbor(self, city):
		szLabel = u"%c" % CyGame().getSymbolID(FontSymbols.NO_ANCHOR_CHAR)
		if city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
			szLabel = u"%c" % CyGame().getSymbolID(FontSymbols.ANCHOR_CHAR)
		
		return szLabel
	

	def getCityByTableRow(self, iRow):
		return int(self.getScreen().getTableText(self.TableNames[self.CURRENT_TABLE], 0, iRow))

	def updateButtons(self):
		# Updates button panel
		screen = self.getScreen()
		
		szSelectButton = "Art/Interface/Screens/TradeRoutes/Select.dds"
		if self.bSelected:
			szSelectButton = "Art/Interface/Screens/TradeRoutes/Deselect.dds"
		szDangerButton = "Art/Interface/Screens/TradeRoutes/IgnoreDangerOff.dds"
		if self.bDanger:
			szDangerButton = "Art/Interface/Screens/TradeRoutes/IgnoreDanger.dds"
		szRoutesButton = "Art/Interface/Screens/TradeRoutes/AddRoute.dds"
		szReturnButton = "Art/Interface/Screens/TradeRoutes/Return.dds"
		szHelpButton = "Art/Interface/Screens/TradeRoutes/Help.dds"
		
		screen.clearMultiList(self.szButtonPanel)
		
		if self.CURRENT_TABLE == self.CITY_TABLE:
			screen.appendMultiListButton(self.szButtonPanel, szSelectButton, 0, WidgetTypes.WIDGET_GENERAL, self.SELECT_ID, -1, False)
		else:
			screen.appendMultiListButton(self.szButtonPanel, szReturnButton, 0, WidgetTypes.WIDGET_GENERAL, self.RETURN_ID, -1, False)
		
		screen.appendMultiListButton(self.szButtonPanel, szDangerButton, 0, WidgetTypes.WIDGET_GENERAL, self.DANGER_ID, -1, False)
		screen.appendMultiListButton(self.szButtonPanel, szHelpButton, 0, WidgetTypes.WIDGET_PEDIA_DESCRIPTION, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, gc.getInfoTypeForString("CONCEPT_TRADE_ROUTE"), False)


	def toggleCitySelect(self):
		self.bSelected = not self.bSelected
		for city in self.CityList:
			self.AssignedCities[city.getID()] = self.bSelected
		self.cityTable()
		
	def toggleDanger(self):
		#CyMessageControl().sendDoCommand(self.pTransport.getID(), CommandTypes.COMMAND_ASSIGN_TRADE_ROUTE, self.CityList[0].getID(), 3, true)
		self.bDanger = not self.bDanger
		CyMessageControl().sendDoCommand(self.pTransport.getID(), CommandTypes.COMMAND_IGNORE_DANGER, self.bDanger, -1, false)
		self.updateButtons()

	def handleInput(self, inputClass):
		if inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED:
			if inputClass.getFunctionName() ==  self.TableNames[self.CITY_TABLE]:
				self.toggleCityAssignment(inputClass.getMouseY())
			elif inputClass.getFunctionName() == self.szButtonPanel:
				if inputClass.getData1() == self.SELECT_ID:
					self.toggleCitySelect()
				elif inputClass.getData1() == self.DANGER_ID:
					self.toggleDanger()
				elif inputClass.getData1() == self.RETURN_ID:
					self.cityTable()
			#R&R mod, vetiarvind, trade groups - START
			elif inputClass.getFunctionName() == self.TableNames[self.LOAD_GROUP_TABLE]:							
				self.loadSelectedGroup(inputClass.getMouseY())									
			elif inputClass.getFunctionName() == self.TableNames[self.DELETE_GROUP_TABLE]:							
				self.deleteSelectedGroup(inputClass.getMouseY())
			#R&R mod, vetiarvind, trade groups - END	
		elif inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
			if inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL:
				#R&R mod, vetiarvind, trade groups - START
				if inputClass.getData1() == self.LOAD_GROUP_ID:
					self.loadGroupTable()
				elif inputClass.getData1() == self.SAVE_GROUP_ID:					
					self.saveGroupPopup()				
				elif inputClass.getData1() == self.DELETE_GROUP_ID:					
					self.deleteGroupTable()				
				#R&R mod, vetiarvind, trade groups - END
					
		return 0
		

	def getWidgetHelp(self, argsList):
		iScreen, eWidgetType, iData1, iData2, bOption = argsList
		player = gc.getPlayer(gc.getGame().getActivePlayer())
	
		if eWidgetType == WidgetTypes.WIDGET_GENERAL:
			if iData1 == self.SELECT_ID:
				if self.bSelected:
					return localText.getText("TXT_KEY_TRADE_ROUTES_DESELECT_ROUTES_HELP", ())
				else:
					return localText.getText("TXT_KEY_TRADE_ROUTES_SELECT_ROUTES_HELP", ())
			elif iData1 == self.DANGER_ID:
				if self.bDanger:
					return localText.getText("TXT_KEY_TRADE_ROUTES_CANCEL_IGNORE_DANGER_HELP", ())
				else:
					return localText.getText("TXT_KEY_TRADE_ROUTES_IGNORE_DANGER_HELP", ())
			elif iData1 == self.RETURN_ID:
				return localText.getText("TXT_KEY_TRADE_ROUTES_RETURN_HELP", ())

		if eWidgetType == WidgetTypes.WIDGET_PEDIA_DESCRIPTION:
			if iData1 == CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT:
				return localText.getText("TXT_KEY_TRADE_ROUTES_HELP_HELP", ())
		
		return u""
	
	
	def update(self, fDelta):
		if (CyInterface().isDirty(InterfaceDirtyBits.TradeCitySelector_DIRTY_BIT)):
			CyInterface().setDirty(InterfaceDirtyBits.TradeCitySelector_DIRTY_BIT, False)
			self.cityTable()
				
		return 0
	
	
	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.TRADE_CITY_SELECTOR)
	
	
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName

		
	def onClose(self) :
		for iCity, bAssigned in self.AssignedCities.iteritems():
			#CyMessageControl().sendDoCommand(self.pTransport.getID(), CommandTypes.COMMAND_ASSIGN_TRADE_ROUTE, iCity, bAssigned+2, false)
			CyMessageControl().sendDoCommand(self.pTransport.getID(), CommandTypes.COMMAND_IGNORE_DANGER, iCity, bAssigned+2, false)
		
		return 0
	
