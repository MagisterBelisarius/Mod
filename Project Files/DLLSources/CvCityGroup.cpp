#include "CvCityGroup.h"
#include "CvGameCoreDLL.h"
#include "CvCity.h"
#include "CvDLLInterfaceIFaceBase.h"
#include "CvSavegame.h"
#include "CvCityGroup.h"

CvCityGroup::CvCityGroup() 
{
	m_aCityIDs.clear();
}

CvCityGroup::~CvCityGroup()
{
	m_aCityIDs.clear();
}

int CvCityGroup::getID() const
{
	return m_iId;
}

void CvCityGroup::setID(int iId)
{
	m_iId = iId;
}

void CvCityGroup::addCity(int iCityId)
{	

	m_aCityIDs.insert(iCityId);
	
}

void CvCityGroup::removeCity(int iCityId)
{
	m_aCityIDs.erase(iCityId);
}

void CvCityGroup::clearCities()
{
	m_aCityIDs.clear();
}

int CvCityGroup::getCityCount() const
{
	return m_aCityIDs.size();
}

bool CvCityGroup::containsCity(int iCityId){

	if (m_aCityIDs.find(iCityId) != m_aCityIDs.end()){
		return true;
	}else{
		return false;
	}
}

const CvWString CvCityGroup::getName(uint uiForm) const
{
	return gDLL->getObjectText(m_sName, uiForm, true);
}

void CvCityGroup::setName(const wchar* szNewValue)
{
	CvWString szName(szNewValue);
	gDLL->stripSpecialCharacters(szName);
	if (!isEmpty(szName))
		m_sName = szName;
}