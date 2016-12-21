#-------------------------------------------------------------------------------
# Name:        DBUpdateBasicOrderTest
# Version:     2.0
# Purpose:     Load and Remote Testing for DBUpdateBasicOrder
#
# Author:      Matthew
#
# Created:     08/22/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/13/2014
#-------------------------------------------------------------------------------

#Check if DateEntered gets updated

import time
import random
import sys
import string
import MySQLdb

#Starts timer
TimerStart = time.clock()

#Defines project path
sys.path.insert(0, "C:\Programming\ExchangeMechanisms\Development")

#Imports main module
import DatabaseScripts.BasicOrders.DBUpdateBasicOrder as Mod

print ""
print "Mod Finished Importing"



#Option for orders to update
#Note: 0 for specified orders, 1 for random active orders
OrdersOption = 1

#UsersOption 0 settings
OrderNumber1 = 12
OrderNumber2 = 13
OrderNumberList = [OrderNumber1, OrderNumber2]



#Option for trade updating
#Note: 0 for static value update to orders, 1 for random value update to orders
Option = 1

#Option 0 settings
#Note: Do not set order number attribute, or loop will break
Username = "Username0"
Price = 600
Volume = 3
Type = "Limit"
Action = "Buy"
TriggerType = "Market Price"
TriggerValue = 300
#Note: Date format is "[Year]-[Month]-[Day] [Hour]:[Minute]:[Second]
#Note: Input date value as a tuple: [Year, Month, Day, Hour, Minute, Second]
DateEntered = [2014, 1, 1, 0, 0, 0]

AttributeNameList = ["USERNAME", "PRICE", "VOLUME", "TYPE", "ACTION", "TRIGGER TYPE", "TRIGGER VALUE", "DATE ENTERED"]
AttributeValueList = [Username, Price, Volume, Type, Action, TriggerType, TriggerValue, DateEntered]

#Option 1 Settings
Loops = 10



#Random String Generator

def RandomString(Characters):
    CharacterSet = string.ascii_letters + string.digits
    String = ""
    for x in range(0, Characters):
        Character = random.choice(CharacterSet)
        String += Character
    return String

#Random Integer Generator

def RandomInteger(Digits):
    Integer = ""
    for x in range(0, Digits):
        Digit = str(random.randint(0, 9))
        Integer += Digit
    Integer = int(Integer)
    return Integer

#Random Decimal Generator

def RandomDecimal(Precision):
    Decimal = float(str(random.random())[:(Precision + 2)])
    return Decimal

#Random Float generator

def RandomFloat(Digits, Precision):
    Integer = RandomInteger(Digits)
    Decimal = RandomDecimal(Precision)
    Float = float(Integer + Decimal)
    return Float

#Random Date Generator

def RandomDate():
    Year = random.randrange(2014, 2015)
    Month = random.randrange(1, 12)
    Day = random.randrange(1, 31)
    Hour = random.randrange(0, 23)
    Minute = random.randrange(0, 60)
    Second = random.randrange(0, 60)
    Date = [Year, Month, Day, Hour, Minute, Second]
    return Date

def RandomUsername():
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    
    cursor.execute("""SELECT Username FROM UserBook ORDER BY RAND() LIMIT 1""")
    Username = cursor.fetchone()[0]
    return Username



#Main update mechanism

def ValueUpdate(Username, AttributeNameList, AttributeValueList):
    if Option == 1:
        Username = RandomUsername()
        Price = RandomFloat(3, 2)
        Volume = RandomFloat(2, 8)
        Type = random.choice(["Instant", "Limit", "Liquid", "Conditional"])
        Action = random.choice(["Buy", "Sell"])
        TriggerType = random.choice(["Bid Price", "Ask Price", "Latest Price", "Average Price"])
        TriggerValue = RandomFloat(3, 2)
        #Note: Date format is "[Year]-[Month]-[Day] [Hour]:[Minute]:[Second]
        #Note: Input date value as a tuple: [Year, Month, Day, Hour, Minute, Second]
        DateEntered = RandomDate()
        AttributeValueList = [Username, Price, Volume, Type, Action, TriggerType, TriggerValue, DateEntered]
    for Index, Attribute in enumerate(AttributeNameList):
        print ""
        print "----------Starting Update Round: " + str(Index + 1) + "----------"
        print ""
        NewValue = AttributeValueList[Index]
        Mod.main(OrderNumber, Attribute, NewValue)
    


if OrdersOption == 0:
    for Index, OrderNumber in enumerate(OrderNumberList):
        print ""
        print ""
        print "----------Starting Order Round: " + str(Index + 1) + "----------"
        print ""
        print ""
        ValueUpdate(OrderNumber, AttributeNameList, AttributeValueList)

if OrdersOption == 1:
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    cursor.execute("""SELECT OrderNumber FROM BasicOrderBook ORDER BY RAND() LIMIT %d""" % (Loops))
    RandomOrderNumberList = cursor.fetchall()
    for Index, OrderNumber in enumerate(RandomOrderNumberList):
        OrderNumber = int(OrderNumber[0])
        print ""
        print ""
        print "----------Starting Order Round: " + str(Index + 1) + "----------"
        print ""
        print ""
        ValueUpdate(OrderNumber, AttributeNameList, AttributeValueList)



#Ends timer
TimerEnd = time.clock()
TimePassed = TimerEnd - TimerStart

print ""
print "Run Time: " + str(TimePassed) + " Seconds"


