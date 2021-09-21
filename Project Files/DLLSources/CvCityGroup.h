// Belisarius
#pragma once

#ifndef CIV4_CITY_GROUP_H
#define CIV4_CITY_GROUP_H
#include "CvCity.h" 
class CvCityGroup
{
public:
	CvCityGroup();
	~CvCityGroup();	

	int getID() const;
	void setID(int iId);
	void CvCityGroup::addCity(int iCityId);
	void removeCity(int iCityId);
	void clearCities();
	int getCityCount() const;
	bool containsCity(int iCityId);
	//CvCity* getCityByIndex(int iIdx);

	const CvWString getName(uint uiForm) const;
	void setName(const wchar* name);
	
	void read(CvSavegameReader reader);
	void write(CvSavegameWriter writer);

	void resetSavedData();
	
protected:	
	int m_iId;	
	CvWString m_sName;	
	std::set<int> m_aCityIDs;
	
};


#endif  // CIV4_CITY_GROUP_H
