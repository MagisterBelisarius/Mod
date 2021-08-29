#ifndef NETWORK_DATA_PACKING_H
#define NETWORK_DATA_PACKING_H

// Firaxis has provided us with network packages where the number of arguments are fixed.
// This becomes a problem if we need to transfer more variables than there are available arguments.
//
// The solution is either to send multiple packages or to pack multiple variables into a single int.
// The less data being transmitted the better meaning packing variables is preferred if possible.
// However merging variables into a single int requires bitmasks, bitshifts and as such magic numbers, which are prone to bugs.
// It becomes even worse if the programmer isn't used to working with binary data like that.
//
// The goal of this file is to make a human readable interface between being a single int and multiple variables.
// The idea is to make structs (everything public) consisting of a union of an int and a struct, both nameless.
// The inner struct and the int are then in the same memory (hence the union) and the struct is used with sensible variable names for reading and writing.
// The network interface then read/write to the int.
// Each such struct should be static asserted against using more than 4 bytes (size of int)
//
// If size is an issue and the compiler won't handle it automatically, then bitfields can be used.
// bool bSomeBool :1;
// That will specify that bool to use only a single bit, allowing up to 32 bools in a single int.
// The tradeoff with bitfields is that they can be slower, particularly when writing to the variable.
// However performance is not a concern for this use case.
//


struct NetworkDataTradeRouteInts
{
	NetworkDataTradeRouteInts(int a = 0) : iNetwork(a) {}

	union
	{
		int iNetwork;
		struct
		{
			unsigned short iImportLimitLevel;
			unsigned short iMaintainLevel;
		};
	};
};

struct NetworkDataTradeRouteInts2
{
	NetworkDataTradeRouteInts2(int a = 0) : iNetwork2(a) {}

	union
	{
		int iNetwork2;
		YieldTypes eYield : 16;
		struct
		{
			short iYieldPlaceHolder; // access this variable via eYield instead
			unsigned short iFeederThreshold;
		};
	};
};

struct NetworkDataTradeRouteInts3
{
	NetworkDataTradeRouteInts3(int a = 0) : iNetwork3(a) {}

	union
	{
		int iNetwork3;
		YieldTypes eYield : 16;
		struct
		{
			short iYieldPlaceHolder; // access this variable via eYield instead
			unsigned short iAutoExportThreshold;
		};
	};
};

struct NetworkDataTradeRouteInts4
{
	NetworkDataTradeRouteInts4(int a = 0) : iNetwork4(a) {}

	union
	{
		int iNetwork4;
		struct
		{
			bool bAutoDomesticAll : 1;
			bool bBit2 : 1; // space for more
			bool bBit3 : 1;
			bool bBit4 : 1;
			bool bBit5 : 1;
			bool bBit6 : 1;
			bool bBit7 : 1;
			bool bBit8 : 1;
			bool bBit9 : 1;
			bool bBit10 : 1;
			bool bBit11 : 1;
			bool bBit12 : 1;
			bool bBit13 : 1;
			bool bBit14 : 1;
			bool bBit15 : 1;
			bool bBit16 : 1;
			
			unsigned short dummy; // space for more
		};
	};
};

BOOST_STATIC_ASSERT(sizeof(NetworkDataTradeRouteInts) == sizeof(int));
BOOST_STATIC_ASSERT(sizeof(NetworkDataTradeRouteInts2) == sizeof(int));
BOOST_STATIC_ASSERT(sizeof(NetworkDataTradeRouteInts3) == sizeof(int));
BOOST_STATIC_ASSERT(sizeof(NetworkDataTradeRouteInts4) == sizeof(int));

#endif // !NETWORK_DATA_PACKING_H
