#-------------------------------------------------------------------------------
# Name:        DBDeleteLoanTest
# Version:     2.0
# Purpose:     Load and Remote Testing for DBDeleteLoan
#
# Author:      Matthew
#
# Created:     08/17/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    08/20/2014
#-------------------------------------------------------------------------------

import time
import sys
import MySQLdb



#Starts timer
TimerStart = time.clock()

#Defines project path
sys.path.insert(0, "C:\Programming\ExchangeMechanisms\Development")

#Imports main module
import DatabaseScripts.Loans.DBDeleteLoan as Mod

print ""
print "Mod Finished Importing"
print ""


#Option for order deletion
#Note: 0 for specific contract deletion, 1 for contract number iteration deletion (0 - [#]), 2 for smart deletion

Option = 2

#Option 0 settings
#To add more, create variable and add to list

ContractNumber1 = 215
ContractNumber2 = 216
ContractNumberList = [ContractNumber1, ContractNumber2]

#Option 1 settings
#To add more, change number
#Note: This operation starts contract deletion from "0" and goes until "[Loops - 1]"

OptionOneLoops = 10

#Option 2 settings
#To add more, change number
#Note: This operation automatically detects active contracts and deletes randomly

OptionTwoLoops = 5



#Execute

if Option == 0:
    for Index, ContractNumber in enumerate(ContractNumberList):
        print ""
        print "----------Starting Round: " + str(Index + 1) + "----------"
        print ""
        Mod.main(ContractNumber)



if Option == 1:
    for x in range(0, OptionOneLoops):
        print ""
        print "----------Starting Round: " + str(x + 1) + "----------"
        print ""
        Mod.main(x)



#WARNING: Query uses "ORDER BY RAND()": This uses full table scan and is very slow for large table

if Option == 2:
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    cursor.execute("""SELECT ContractNumber FROM LoanBook ORDER BY RAND() LIMIT %d """ % (OptionTwoLoops))
    ContractNumbers = cursor.fetchall()
    if ContractNumbers != ():
        for Index, ContractNumber in enumerate(ContractNumbers):
            print ""
            print "----------Starting Round: " + str(Index + 1) + "----------"
            print ""
            ContractNumber = int(ContractNumber[0])
            Mod.main(ContractNumber)
    else:
        print ""
        print "No contracts found"
        



#Ends timer
TimerEnd = time.clock()
TimePassed = TimerEnd - TimerStart

print ""
print "Run Time: " + str(TimePassed) + " Seconds"


