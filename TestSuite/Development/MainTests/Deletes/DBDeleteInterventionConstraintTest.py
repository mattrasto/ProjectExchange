#-------------------------------------------------------------------------------
# Name:        DBDeleteInterventionConstraintTest
# Version:     2.0
# Purpose:     Load and Remote Testing for DBDeleteInterventionConstraint
#
# Author:      Matthew
#
# Created:     08/20/2014
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
sys.path.insert(0, "/home/mal/Programming/ExchangeMechanisms/Development")

#Imports main module
import DatabaseScripts.Constraints.DBDeleteInterventionConstraint as Mod

print ""
print "Mod Finished Importing"
print ""


#Option for order deletion
#Note: 0 for specific constraint deletion, 1 for constraint iteration deletion ("[ContractNumber]-0" - "[ContractNumber]-[#]"), 2 for smart deletion

Option = 2

#Option 0 settings
#To add more, create variables and add to respective lists

ContractNumber1 = 10
ConstraintNumber1 = 10

ContractNumber2 = 4
ConstraintNumber2 = 1

ContractNumberList = [ContractNumber1, ContractNumber2]
ConstraintNumberList = [ConstraintNumber1, ConstraintNumber2]


#Option 1 settings
#To add more, change number
#Note: This operation starts constraint deletion from "[ContractNumber]-0" and goes until "ContractNumber-[Loops]"
#Note: ContractNumber states which contract to search for constraints under

ContractNumber = 5
OptionOneLoops = 11

#Option 2 settings
#To add more, change number
#Note: This operation automatically detects active constraints and deletes randomly

OptionTwoLoops = 5



#Execute

if Option == 0:
    for Index, ContractNumber in enumerate(ContractNumberList):
        print ""
        print "----------Starting Round: " + str(Index + 1) + "----------"
        print ""
        ConstraintNumber = ConstraintNumberList[Index]
        ConstraintID = str(ContractNumber) + "-" + str(ConstraintNumber)
        Mod.main(ContractNumber, ConstraintID)



if Option == 1:
    for x in range(0, OptionOneLoops):
        print ""
        print "----------Starting Round: " + str(x + 1) + "----------"
        print ""
        ConstraintID = str(ContractNumber) + "-" + str(x + 1)
        Mod.main(ContractNumber, ConstraintID)



#WARNING: Query uses "ORDER BY RAND()": This uses full table scan and is very slow for large table

if Option == 2:
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    cursor.execute("""SELECT ConstraintID FROM InterventionConstraintBook ORDER BY RAND() LIMIT %d """ % (OptionTwoLoops))
    ConstraintIDs = cursor.fetchall()
    print ConstraintIDs
    if ConstraintIDs != ():
        for Index, ConstraintID in enumerate(ConstraintIDs):
            ConstraintID = ConstraintID[0]
            print ""
            print "----------Starting Round: " + str(Index + 1) + "----------"
            print ""
            cursor.execute("""SELECT ContractNumber FROM InterventionConstraintBook WHERE ConstraintID = "%s" """ % (ConstraintID))
            ContractNumber = cursor.fetchone()[0]
            Mod.main(ContractNumber, ConstraintID)
    else:
        print ""
        print "No constraints found"
        



#Ends timer
TimerEnd = time.clock()
TimePassed = TimerEnd - TimerStart

print ""
print "Run Time: " + str(TimePassed) + " Seconds"


