#-------------------------------------------------------------------------------
# Name:        DBAddUserRequestTest
# Version:     2.0
# Purpose:     Load and Remote Testing for DBAddUserRequest
#
# Author:      Matthew
#
# Created:     08/06/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    08/30/2014
#-------------------------------------------------------------------------------

#Add Loan and Private Trade Support

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
import DatabaseScripts.UserRequests.DBAddUserRequest as Mod

print ""
print "Mod Finished Importing"



#User that user request is under
Username = "Username0"

#Contract to make constraints under
#Note: Put True for RandomContractNumber to select random MTC owned by user
ContractNumber = 5
RandomContractNumber = True

#Number of each order to make
Loops = 10



#Random contract number generator

def RandomContractNumber():
    cursor.execute("""SELECT MTCNumber FROM MTCBook WHERE Username = "%s" ORDER BY RAND()""" % (Username))
    ContractNumber = cursor.fetchone()
    if ContractNumber != None:
        ContractNumber = ContractNumber[0]
        return ContractNumber
    else:
        print "Specified user has no active MTC's"
        sys.exit()



#Execute

for x in range(0, Loops):
    print ""
    print "----------Starting Round: " + str(x + 1) + "----------"
    print ""
    if RandomContractNumber:
        ContractNumber = RandomContractNumber()
    Mod.main(Username, ContractNumber)



#Ends timer
TimerEnd = time.clock()
TimePassed = TimerEnd - TimerStart

print ""
print "Run Time: " + str(TimePassed) + " Seconds"


