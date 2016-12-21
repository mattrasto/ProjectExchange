#-------------------------------------------------------------------------------
# Name:        DBAddBorrowerConstraintTest
# Version:     2.0
# Purpose:     Load and Remote Testing for DBAddBorrowerConstraint
#
# Author:      Matthew
#
# Created:     08/05/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    08/30/2014
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
sys.path.insert(0, "C:\Programming\ExchangeMechanisms\Development")

#Imports main module
import DatabaseScripts.Constraints.DBAddBorrowerConstraint as Mod

print ""
print "Mod Finished Importing"



#User that order is under
Username = "Username0"

#Contract to make constraints under
#Note: Put True for RandomContractNumber to select random MTC owned by user
ContractNumber = 3
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
    if ConstraintType == "ACCOUNT BALANCE":
        MinimumBorrowerConstraintValue = random.randrange(100, 100000)
    elif ConstraintType == "VOLUME":
        MinimumBorrowerConstraintValue = random.randrange(100, 10000)
    elif ConstraintType == "CONTRACTS":
        MinimumBorrowerConstraintValue = random.randrange(1, 100)
    elif ConstraintType == "TRANSACTIONS":
        MinimumBorrowerConstraintValue = random.randrange(1, 100)
    elif ConstraintType == "LIQUIDITY VALUE":
        MinimumBorrowerConstraintValue = random.randrange(1, 1000)
    return MinimumBorrowerConstraintValue



#Execute

for x in range(0, Loops):
    print ""
    print "----------Starting Round: " + str(x + 1) + "----------"
    print ""
    if RandomContractNumber:
        ContractNumber = RandomContractNumber()
    MinimumBorrowerConstraintType = random.choice(["ACCOUNT BALANCE", "VOLUME", "CONTRACTS", "TRANSACTIONS", "LIQUIDITY VALUE"])
    MinimumBorrowerConstraintValue = RandomValue(MinimumBorrowerConstraintType)
    Mod.main(Username, ContractNumber, MinimumBorrowerConstraintType, MinimumBorrowerConstraintValue)



#Ends timer
TimerEnd = time.clock()
TimePassed = TimerEnd - TimerStart

print ""
print "Run Time: " + str(TimePassed) + " Seconds"


