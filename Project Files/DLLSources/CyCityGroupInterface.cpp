//City restricted auto transport - Belisarius
#include "CvGameCoreDLL.h"
#include "CyCityGroup.h"
//
// published python interface for CyCityGroup
//

void CyCityGroupPythonInterface()
{
	OutputDebugString("Python Extension Module - CyCityGroupPythonInterface\n");

	python::class_<CyCityGroup>("CyCityGroup")
		.def("getID", &CyCityGroup::getID, "int ()")
		.def("getName", &CyCityGroup::getName, "wstring ()")
		.def("setName", &CyCityGroup::setName, "void (wstring)")
		.def("containsCity", &CyCityGroup::containsCity,  "bool (int iCityID)")
	;
}
