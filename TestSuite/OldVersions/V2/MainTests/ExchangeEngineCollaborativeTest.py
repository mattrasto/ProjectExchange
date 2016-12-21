#-------------------------------------------------------------------------------
# Name:        DBExchangeCollaborativeTest
# Version:     2.0
# Purpose:     Load and Remote Testing for ExchangeEngineCollaborative
#
# Author:      Matthew
#
# Created:     07/16/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    08/12/2014
#-------------------------------------------------------------------------------

#Note: Loops are built into ExchangeEngineCollaborative's main() function for ease of use in production application as it is not adding an order

import time
import sys

#Starts timer
TimerStart = time.clock()

#Defines project path
sys.path.insert(0, "C:\Programming\ExchangeMechanisms\Development")

#Imports main module
import ExchangeEngineCollaborative as Mod

print ""
print "Mod Finished Importing"
print ""


#Times to check for transactions
Loops = 10



#Execute

Mod.main(Loops)



print ""
print "Test Completed"
print "Loops Performed: " + str(Mod.LoopCount)
print "Transactions Processed: " + str(Mod.TransactionsProcessed)
print "Successful Logs: " + str(Mod.SuccessfulLogs)

#Ends timer
TimerEnd = time.clock()
TimePassed = TimerEnd - TimerStart

print ""
print "Run Time: " + str(TimePassed) + " Seconds"


