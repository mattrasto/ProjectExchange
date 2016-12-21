#-------------------------------------------------------------------------------
# Name:        DBUpdatePrivateTradeTest
# Version:     2.0
# Purpose:     Load and Remote Testing for DBUpdatePrivateTrade
#
# Author:      Matthew
#
# Created:     08/24/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/01/2014
#-------------------------------------------------------------------------------

import time
import random
import sys
import string
import MySQLdb

#Starts timer
TimerStart = time.clock()

#Defines project path
sys.path.insert(0, "/home/mal/Programming/ExchangeMechanisms/Development")

#Imports main module
import DatabaseScripts.PrivateTrades.DBUpdatePrivateTrade as Mod

print ""
print "Mod Finished Importing"



#Option for trades to update
#Note: 0 for specified trades, 1 for random active trades
TradesOption = 1

#UsersOption 0 settings
TradeNumber1 = 12
TradeNumber2 = 13
TradeNumberList = [TradeNumber1, TradeNumber2]



#Option for trades updating
#Note: 0 for static value update to trades, 1 for random value update to trades
Option = 1

#Option 0 settings
#Note: Do not set trade number attribute, or loop will break
Username = "Username1"
Price = 600
Volume = 3
Action = "Buy"
UserRequests = 3
#Note: Date format is "[Year]-[Month]-[Day] [Hour]:[Minute]:[Second]
#Note: Input date value as a tuple: [Year, Month, Day, Hour, Minute, Second]
DateEntered = [2014, 1, 1, 0, 0, 0]

AttributeNameList = ["USERNAME", "PRICE", "VOLUME", "ACTION", "USER REQUESTS", "DATE ENTERED"]
AttributeValueList = [Username, Price, Volume, Action, UserRequests, DateEntered]

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
        #Option 0 settings
        #Note: Do not set trade number attribute, or loop will break
        Username = RandomUsername()
        print Username
        Price = RandomFloat(3, 2)
        Volume = RandomFloat(2, 8)
        Action = random.choice(["Buy", "Sell"])
        UserRequests = RandomInteger(1)
        #Note: Date format is "[Year]-[Month]-[Day] [Hour]:[Minute]:[Second]
        #Note: Input date value as a tuple: [Year, Month, Day, Hour, Minute, Second]
        DateEntered = RandomDate()
        AttributeValueList = [Username, Price, Volume, Action, UserRequests, DateEntered]
    for Index, Attribute in enumerate(AttributeNameList):
        print ""
        print "----------Starting Update Round: " + str(Index + 1) + "----------"
        print ""
        NewValue = AttributeValueList[Index]
        Mod.main(TradeNumber, Attribute, NewValue)
    


if TradesOption == 0:
    for Index, TradeNumber in enumerate(TradeNumberList):
        print ""
        print ""
        print "----------Starting Trade Round: " + str(Index + 1) + "----------"
        print ""
        print ""
        ValueUpdate(TradeNumber, AttributeNameList, AttributeValueList)

if TradesOption == 1:
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    cursor.execute("""SELECT TradeNumber FROM PrivateTradeBook ORDER BY RAND() LIMIT %d""" % (Loops))
    RandomTradeNumberList = cursor.fetchall()
    for Index, TradeNumber in enumerate(RandomTradeNumberList):
        TradeNumber = int(TradeNumber[0])
        print ""
        print ""
        print "----------Starting Trade Round: " + str(Index + 1) + "----------"
        print ""
        print ""
        ValueUpdate(TradeNumber, AttributeNameList, AttributeValueList)



#Ends timer
TimerEnd = time.clock()
TimePassed = TimerEnd - TimerStart

print ""
print "Run Time: " + str(TimePassed) + " Seconds"


