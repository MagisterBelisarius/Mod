#pragma once
#ifndef CyCityGroup_h
#define CyCityGroup_h
//
// Python wrapper class for CvCityGroup
//
class CyCityGroup;

class CyCityGroup
{
public:
	CyCityGroup();
	CyCityGroup(CvCityGroup* pCityGroup);

	int getID();
	std::wstring getName();
	void setName(std::wstring);
	bool containsCity(int iCityID);
	
private:
	CvCityGroup* m_pCityGroup;
};
#endif	// CyCityGroup_h