#-------------------------------------------------------------------------------
# Name:        DBDeleteBasicOrderTest
# Version:     2.0
# Purpose:     Load and Remote Testing for DBDeleteBasicOrder
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
sys.path.insert(0, "/home/mal/Programming/ExchangeMechanisms/Development")

#Imports main module
import DatabaseScripts.BasicOrders.DBDeleteBasicOrder as Mod

print ""
print "Mod Finished Importing"
print ""


#Option for order deletion
#Note: 0 for specific order deletion, 1 for order number iteration deletion (0 - [#]), 2 for smart deletion

Option = 2

#Option 0 settings
#To add more, create variable and add to list

OrderNumber1 = 121
OrderNumber2 = 122
OrderNumberList = [OrderNumber1, OrderNumber2]

#Option 1 settings
#To add more, change number
#Note: This operation starts order deletion from "0" and goes until "[Loops - 1]"

OptionOneLoops = 10

#Option 2 settings
#To add more, change number
#Note: This operation automatically detects active orders and deletes randomly

OptionTwoLoops = 5



#Execute

if Option == 0:
    for Index, OrderNumber in enumerate(OrderNumberList):
        print ""
        print "----------Starting Round: " + str(Index + 1) + "----------"
        print ""
        Mod.main(OrderNumber)



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
    
    cursor.execute("""SELECT OrderNumber FROM BasicOrderBook ORDER BY RAND() LIMIT %d """ % (OptionTwoLoops))
    OrderNumbers = cursor.fetchall()
    if OrderNumbers != ():
        for Index, OrderNumber in enumerate(OrderNumbers):
            print ""
            print "----------Starting Round: " + str(Index + 1) + "----------"
            print ""
            OrderNumber = int(OrderNumber[0])
            Mod.main(OrderNumber)
    else:
        print ""
        print "No orders found"
        



#Ends timer
TimerEnd = time.clock()
TimePassed = TimerEnd - TimerStart

print ""
print "Run Time: " + str(TimePassed) + " Seconds"


