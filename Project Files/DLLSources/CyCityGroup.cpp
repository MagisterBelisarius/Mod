#include "CvGameCoreDLL.h"
#include "CyCityGroup.h"
#include "CvCityGroup.h"
#include "CvGlobals.h"

CyCityGroup::CyCityGroup() : m_pCityGroup(NULL){}
CyCityGroup::CyCityGroup(CvCityGroup* pCityGroup) : m_pCityGroup(pCityGroup)
{

}

int CyCityGroup::getID()
{
	return m_pCityGroup->getID();
}

std::wstring CyCityGroup::getName()
{
	return m_pCityGroup ? m_pCityGroup->getName(0) : std::wstring();
}


void CyCityGroup::setName(std::wstring szName)
{	
	if (m_pCityGroup)
		m_pCityGroup->setName(CvWString(szName).GetCString());
}
	
bool CyCityGroup::containsCity(int iCityID){
	return m_pCityGroup ? m_pCityGroup->containsCity(iCityID) : false;
}
