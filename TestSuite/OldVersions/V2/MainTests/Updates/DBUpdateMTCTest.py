#-------------------------------------------------------------------------------
# Name:        DBUpdateMTCTest
# Version:     2.0
# Purpose:     Load and Remote Testing for DBUpdateMTC
#
# Author:      Matthew
#
# Created:     08/23/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    08/24/2014
#-------------------------------------------------------------------------------

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
import DatabaseScripts.MTCs.DBUpdateMTC as Mod

print ""
print "Mod Finished Importing"



#Option for users to update
#Note: 0 for specified MTCs, 1 for random active MTCs
MTCsOption = 1

#UsersOption 0 settings
MTCNumber1 = 2
MTCNumber2 = 3
MTCNumberList = [MTCNumber1, MTCNumber2]



#Option for MTC updating
#Note: 0 for static value update to MTCs, 1 for random value update to MTCs
Option = 1

#Option 0 settings
#Note: Do not set MTC number attribute, or loop will break
Username = "Username1"
Price = 600
Volume = 3
Action = "Borrow"
#Note: Rate format is "[Number] [Interval]"
#Note: Input rate value as a tuple: [Interval, Number]
InterestCompoundRate = ["HOUR", 2]
InterestRate = .005
StopLossPrice = 300
FulfillmentPrice = 500
#Note: Rate format is "[Number] [Interval]"
#Note: Input rate value as a tuple: [Interval, Number]
Duration = ["DAY", 5]
#Note: Date format is "[Year]-[Month]-[Day] [Hour]:[Minute]:[Second]
#Note: Input date value as a tuple: [Year, Month, Day, Hour, Minute, Second]
EndPoint = [2015, 1, 1, 0, 0, 0]
DividendType = "Flat"
MinimumBorrowerConstraints = 5
UserInterventionConstraints = 3
UserRequests = 2
#Note: Date format is "[Year]-[Month]-[Day] [Hour]:[Minute]:[Second]
#Note: Input date value as a tuple: [Year, Month, Day, Hour, Minute, Second]
DateEntered = [2014, 1, 1, 0, 0, 0]

AttributeNameList = ["USERNAME", "PRICE", "VOLUME", "ACTION", "INTEREST COMPOUND RATE", "INTEREST RATE", "STOP LOSS PRICE", "FULFILLMENT PRICE", "DURATION", "END POINT", "DIVIDEND TYPE", "MINIMUM BORROWER CONSTRAINTS", "USER INTERVENTION CONSTRAINTS", "USER REQUESTS", "DATE ENTERED"]
AttributeValueList = [Username, Price, Volume, Action, InterestCompoundRate, InterestRate, StopLossPrice, FulfillmentPrice, Duration, EndPoint, DividendType, MinimumBorrowerConstraints, UserInterventionConstraints, UserRequests, DateEntered]

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



def RandomEndPoint(DateEntered):
    
    Year = DateEntered[0]
    Month = DateEntered[1]
    Day = DateEntered[2]
    Hour = DateEntered[3]
    Minute = DateEntered[4]
    Second = DateEntered[5]
    
    EndPointYear = Year + random.randrange(1, 3)
    EndPointMonth = Month + random.randrange(1, 6)
    EndPointDay = Day + random.randrange(1, 15)
    EndPointHour = Hour + random.randrange(1, 12)
    EndPointMinute = Minute + random.randrange(1, 30)
    EndPointSecond = Second + random.randrange(1, 30)
    
    if EndPointMonth > 12:
        EndPointMonth = Month
    if EndPointDay > 28:
        EndPointDay = Day
    if EndPointHour > 23:
        EndPointHour = Hour
    if EndPointMinute > 59:
        EndPointMinute = Minute
    if EndPointSecond > 59:
        EndPointSecond = Second
    
    EndPoint = [EndPointYear, EndPointMonth, EndPointDay, EndPointHour, EndPointMinute, EndPointSecond]
    return EndPoint



#Main update mechanism

def ValueUpdate(Username, AttributeNameList, AttributeValueList):
    if Option == 1:
        Username = RandomUsername()
        Price = RandomFloat(3, 2)
        Volume = RandomFloat(2, 8)
        Action = random.choice(["Borrow", "Loan"])
        StopLossPrice = RandomFloat(3, 2)
        FulfillmentPrice = RandomFloat(3, 2)
        #Note: Rate format is "[Number] [Interval]"
        #Note: Input rate value as a tuple: [Interval, Number]
        InterestCompoundRate = [random.choice(["SECOND", "MINUTE", "HOUR", "DAY"]), RandomInteger(3)]
        InterestRate = RandomDecimal(3)
        #Note: Date format is "[Year]-[Month]-[Day] [Hour]:[Minute]:[Second]
        #Note: Input date value as a tuple: [Year, Month, Day, Hour, Minute, Second]
        #Note: DateEntered is defined first to allow EndPoint to be defined as a future date
        DateEntered = RandomDate()
        DividendType = random.choice(["Flat", "Percent"])
        MinimumBorrowerConstraints = RandomInteger(1)
        UserInterventionConstraints = RandomInteger(1)
        UserRequests = RandomInteger(1)
        if InterestRate < .5:
            #Note: Rate format is "[Number] [Interval]"
            #Note: Input rate value as a tuple: [Interval, Number]
            Duration = [random.choice(["SECOND", "MINUTE", "HOUR", "DAY"]), RandomInteger(3)]
            AttributeNameList = ["USERNAME", "PRICE", "VOLUME", "ACTION", "INTEREST COMPOUND RATE", "INTEREST RATE", "STOP LOSS PRICE", "FULFILLMENT PRICE", "DURATION", "DIVIDEND TYPE", "MINIMUM BORROWER CONSTRAINTS", "USER INTERVENTION CONSTRAINTS", "USER REQUESTS", "DATE ENTERED"]
            AttributeValueList = [Username, Price, Volume, Action, InterestCompoundRate, InterestRate, StopLossPrice, FulfillmentPrice, Duration, DividendType, MinimumBorrowerConstraints, UserInterventionConstraints, UserRequests, DateEntered]
        else:
            #Note: Date format is "[Year]-[Month]-[Day] [Hour]:[Minute]:[Second]
            #Note: Input date value as a tuple: [Year, Month, Day, Hour, Minute, Second]
            EndPoint = RandomEndPoint(DateEntered)
            AttributeNameList = ["USERNAME", "PRICE", "VOLUME", "ACTION", "INTEREST COMPOUND RATE", "INTEREST RATE", "STOP LOSS PRICE", "FULFILLMENT PRICE", "END POINT", "DIVIDEND TYPE", "MINIMUM BORROWER CONSTRAINTS", "USER INTERVENTION CONSTRAINTS", "USER REQUESTS", "DATE ENTERED"]
            AttributeValueList = [Username, Price, Volume, Action, InterestCompoundRate, InterestRate, StopLossPrice, FulfillmentPrice, EndPoint, DividendType, MinimumBorrowerConstraints, UserInterventionConstraints, UserRequests, DateEntered]
    for Index, Attribute in enumerate(AttributeNameList):
        print ""
        print "----------Starting Update Round: " + str(Index + 1) + "----------"
        print ""
        NewValue = AttributeValueList[Index]
        Mod.main(MTCNumber, Attribute, NewValue)
    


if MTCsOption == 0:
    for Index, MTCNumber in enumerate(MTCNumberList):
        print ""
        print ""
        print "----------Starting MTC Round: " + str(Index + 1) + "----------"
        print ""
        print ""
        ValueUpdate(MTCNumber, AttributeNameList, AttributeValueList)

if MTCsOption == 1:
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    cursor.execute("""SELECT MTCNumber FROM MTCBook ORDER BY RAND() LIMIT %d""" % (Loops))
    RandomMTCNumberList = cursor.fetchall()
    for Index, MTCNumber in enumerate(RandomMTCNumberList):
        MTCNumber = int(MTCNumber[0])
        print ""
        print ""
        print "----------Starting MTC Round: " + str(Index + 1) + "----------"
        print ""
        print ""
        ValueUpdate(MTCNumber, AttributeNameList, AttributeValueList)



#Ends timer
TimerEnd = time.clock()
TimePassed = TimerEnd - TimerStart

print ""
print "Run Time: " + str(TimePassed) + " Seconds"


