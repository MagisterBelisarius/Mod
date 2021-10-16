# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 23:08:51 2021

@author: Jakke
"""

from FWButcher import MapConstants,PythonRandom,HeightMap,ClimateMap,RiverMap,SmallMaps,EuropeMap

mc = MapConstants()
PRand = PythonRandom()
hm = HeightMap()
cm = ClimateMap
rm = RiverMap
sm = SmallMaps()
em = EuropeMap()

mc.initialize()
PRand.seed()
hm.performTectonics()
hm.generateHeightMap()
hm.combineMaps()
hm.calculateSeaLevel()
hm.printHeightMap()

hm.fillInLakes()
hm.addWaterBands()
hm.printHeightMap()

cm.createClimateMaps()
cm.printRainFallMap(False)
sm.initialize()
rm.generateRiverMap()
hm.printHeightMap()

sm.printHeightMap()
sm.printPlotMap()
sm.printTerrainMap()
rm.printFlowMap()
rm.printRiverMap()
rm.printRiverAndTerrainAlign()
rm.printFlowAndLakesAlign(2)
rm.printFlowAndLakesAlign(1)
rm.printLakeMap()
rm.printLakeIDMap()

sm.printHeightMap()
cm.printTempMap(cm.summerTempsMap)
cm.printTempMap(cm.winterTempsMap)
cm.printTempMap(cm.averageTempMap)



#%% 

mc.initialize()
PRand.seed()
hm.performTectonics()
hm.generateHeightMap()
hm.combineMaps()
hm.calculateSeaLevel()

hm.fillInLakes()
hm.addWaterBands()

cm.createClimateMaps()
sm.initialize()
rm.generateRiverMap()

rm.printRiverMap()

rm.printLakeMap()