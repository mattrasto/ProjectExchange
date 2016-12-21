#-------------------------------------------------------------------------------
# Name:        DBSearchPrivateTradeBookTest
# Version:     2.0
# Purpose:     Load and Remote Testing for DBSearchPrivateTradeBook
#
# Author:      Matthew
#
# Created:     08/12/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    08/12/2014
#-------------------------------------------------------------------------------

import time
import sys

#Starts timer
TimerStart = time.clock()

#Defines project path
sys.path.insert(0, "C:\Programming\ExchangeMechanisms\Development")

#Imports main module
import DatabaseScripts.PrivateTrades.DBSearchPrivateTradeBook as Mod

print ""
print "Mod Finished Importing"
print ""



#Parameter to search with
#To add more, create variable and add to list

SearchParameter1 = "Trade Number"
SearchParameter2 = "Username"
SearchParameterList = [SearchParameter1, SearchParameter2]

#Value to search for
#To add more, create variable and add to list
#Make sure value numbers match parameter numbers or search will be inaccurate

SearchValue1 = "211"
SearchValue2 = "Username0"
SearchValueList = [SearchValue1, SearchValue2]



#Execute

for Parameter in SearchParameterList:
    Index = SearchParameterList.index(Parameter)
    print ""
    print "----------Starting Round: " + str(Index + 1) + "----------"
    print ""
    SearchValue = SearchValueList[Index]
    Mod.main(Parameter.upper(), SearchValue.capitalize())



#Ends timer
TimerEnd = time.clock()
TimePassed = TimerEnd - TimerStart

print ""
print "Run Time: " + str(TimePassed) + " Seconds"


