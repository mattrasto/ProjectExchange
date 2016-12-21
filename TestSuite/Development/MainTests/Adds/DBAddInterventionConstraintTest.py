#-------------------------------------------------------------------------------
# Name:        DBAddBorrowerConstraintTest
# Version:     2.0
# Purpose:     Load and Remote Testing for DBAddInterventionConstraint
#
# Author:      Matthew
#
# Created:     08/05/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/15/2014
#-------------------------------------------------------------------------------

#Add loan support

import time
import random
import MySQLdb
import sys

#Starts timer
TimerStart = time.clock()

#Initializes database
db = MySQLdb.connect("localhost","root","***","exchange")
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
Data = cursor.fetchone()
print "Database Version: " + str(Data[0])

#Defines project path
sys.path.insert(0, "/home/mal/Programming/ExchangeMechanisms/Development")

#Imports main module
import DatabaseScripts.Constraints.DBAddInterventionConstraint as Mod

print ""
print "Mod Finished Importing"



#User that order is under
Username = "Username0"

#Contract to make constraints under
#Note: Put True for RandomContractNumber to select random MTC owned by user
ContractNumber = 5
RandomContractNumber = True

#Number of each order to make
Loops = 10



#Random contract number generator

def RandomContractNumber():
    cursor.execute("""SELECT MTCNumber FROM MTCBook WHERE Username = "%s" """ % (Username))
    MTCList = cursor.fetchall()
    if MTCList == ():
        print "CRITICAL ERROR: User has no orders able to handle constraints"
        sys.exit()
    Selector = random.randint(0, (len(MTCList)-1))
    ContractNumber = MTCList[Selector][0]
    return ContractNumber



#Random constraint value generator

def RandomValue(ConstraintType):
    if ConstraintType == "MARKET PRICE":
        UserInterventionConstraintValue = random.randrange(650, 750)
    elif ConstraintType == "PROFIT MARGIN":
        UserInterventionConstraintValue = random.randrange(1, 100)
    elif ConstraintType == "INTEREST RATE":
        UserInterventionConstraintValue = random.random()
    return UserInterventionConstraintValue



#Execute

for x in range(0, Loops):
    print ""
    print "----------Starting Round: " + str(x + 1) + "----------"
    print ""
    if RandomContractNumber:
        ContractNumber = RandomContractNumber()
    UserInterventionConstraintType = random.choice(["MARKET PRICE", "PROFIT MARGIN", "INTEREST RATE"])
    UserInterventionConstraintValue = RandomValue(UserInterventionConstraintType)
    Mod.main(Username, ContractNumber, UserInterventionConstraintType, UserInterventionConstraintValue)



#Ends timer
TimerEnd = time.clock()
TimePassed = TimerEnd - TimerStart

print ""
print "Run Time: " + str(TimePassed) + " Seconds"


