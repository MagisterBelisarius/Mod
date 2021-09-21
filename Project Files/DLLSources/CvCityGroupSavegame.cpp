#include "CvGameCoreDLL.h"
#include "CvInitCore.h"

#include "CvSavegame.h"

// set the default values

const int defaultId = 0;

// 
enum SavegameVariableTypes
{
	CityGroupSave_END,
	CityGroupSave_Id,
	CityGroupSave_Name,
	CityGroupSave_Cities,
	NUM_SAVE_ENUM_VALUES,
};

const char* getSavedEnumNameCityGroup(SavegameVariableTypes eType)
{
	switch (eType)
	{
	case CityGroupSave_END: return "CityGroupSave_END";
	case CityGroupSave_Id: return "CityGroupSave_Id";
	case CityGroupSave_Name: return "CityGroupSave_Name";
	case CityGroupSave_Cities: return "CityGroupSave_Cities";
	}
	return "";
}

int getNumSavedEnumValuesCityGroup()
{
	return NUM_SAVE_ENUM_VALUES;
}

// assign everything to default values
void CvCityGroup::resetSavedData()
{
	m_iId = defaultId;
	m_sName.clear();
	m_aCityIDs.clear();
}

void CvCityGroup::read(CvSavegameReader reader)
{
	reader.AssignClassType(SAVEGAME_CLASS_CITYGROUP);

	// Init data before load
	// This will ensure that all variables not included in the savegame will have default values
	resetSavedData();

	// loop read all the variables
	// As long as each variable has a UnitSavegameVariables "header", order doesn't matter.
	// Variables can be read in any order and any number of variables can be skipped.
	bool bContinue = true;
	while (bContinue)
	{
		SavegameVariableTypes eType;
		reader.Read(eType);

		switch (eType)
		{
		case CityGroupSave_END: bContinue = false; break;
		case CityGroupSave_Id: reader.Read(m_iId); break;
		case CityGroupSave_Name: reader.Read(m_sName); break;
		case CityGroupSave_Cities: 
			int iSize;
			reader.Read(iSize);
			for(int iI=0;iI<iSize;iI++)
			{
				int iCityID;
				reader.Read(iCityID);
				m_aCityIDs.insert(iCityID);
			}
			break;
		}
	}
	
}

void CvCityGroup::write(CvSavegameWriter writer)
{
	writer.AssignClassType(SAVEGAME_CLASS_CITYGROUP);

	// Write the data.
	// Use WriteSwitch since it will automatically include WriteSwitch in the savegame.
	// Also it will not save anything if the variable and the default values are identical.
	// If nothing is saved, the loading code will use the default values.
	// Less data saved/loaded means smaller savegames.
	writer.Write(CityGroupSave_Id, m_iId, defaultId);
	writer.Write(CityGroupSave_Name, m_sName);
	int iSize = m_aCityIDs.size();
	if(iSize>0)
	{
		writer.Write(CityGroupSave_Cities);
		writer.Write(iSize);
		for(std::set<int>::iterator it = m_aCityIDs.begin(); it != m_aCityIDs.end(); ++it)
		{
			writer.Write(*it);
		}
	}
	
	writer.Write(CityGroupSave_END);
}
