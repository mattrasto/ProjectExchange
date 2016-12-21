#-------------------------------------------------------------------------------
# Name:        DBUpdateUserTest
# Version:     2.0
# Purpose:     Load and Remote Testing for DBUpdateUser
#
# Author:      Matthew
#
# Created:     08/21/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    08/22/2014
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
import DatabaseScripts.Users.DBUpdateUser as Mod

print ""
print "Mod Finished Importing"



#Option for users to update
#Note: 0 for specified users, 1 for random active users
UsersOption = 1

#UsersOption 0 settings
Username1 = "Username1"
Username2 = "Username2"
UsernameList = [Username1, Username2]



#Option for user updating
#Note: 0 for static value update to users, 1 for random value update to users
Option = 1

#Option 0 settings
#Note: Do not set username attribute, or loop will break
Password = "password1"
#Note: A random number will be generated and appended to email in order to maintain unique email id's in database
Email = "email"
USDCredit = 100
BTCCredit = 1
#Note: Date format is "[Year]-[Month]-[Day] [Hour]:[Minute]:[Second]
#Note: Input date value as a tuple: [Year, Month, Day, Hour, Minute, Second]
JoinDate = [2014, 1, 1, 0, 0, 0]
FirstName = "firstname1"
LastName = "lastname1"
BankName = "bankname1"
Address = "address1"
#Note: Must be a value of 0 or 1
Verified = True
TradingFee = ".001"
Volume = 300

AttributeNameList = ["PASSWORD", "EMAIL", "USD CREDIT", "BTC CREDIT", "JOIN DATE", "FIRST NAME", "LAST NAME", "BANK NAME", "ADDRESS", "VERIFIED", "TRADING FEE", "VOLUME"]
AttributeValueList = [Password, Email, USDCredit, BTCCredit, JoinDate, FirstName, LastName, BankName, Address, Verified, TradingFee, Volume]

#Option 1 Settings
Loops = 1



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



#Main update mechanism

def ValueUpdate(Username, AttributeNameList, AttributeValueList):
    if Option == 1:
        Password = RandomString(7)
        Email = RandomString(20)
        USDCredit = RandomFloat(4, 2)
        BTCCredit = RandomFloat(2, 5)
        #Note: Date format is "[Year]-[Month]-[Day] [Hour]:[Minute]:[Second]
        #Note: Input date value as a tuple: [Year, Month, Day, Hour, Minute, Second]
        JoinDate = RandomDate()
        FirstName = RandomString(7)
        LastName = RandomString(7)
        BankName = RandomString(30)
        Address = RandomString(40)
        #Note: Must be a value of 0 or 1
        Verified = random.choice([0, 1])
        TradingFee = RandomDecimal(4)
        Volume = RandomFloat(4, 2)
        AttributeValueList = [Password, Email, USDCredit, BTCCredit, JoinDate, FirstName, LastName, BankName, Address, Verified, TradingFee, Volume]
    for Index, Attribute in enumerate(AttributeNameList):
        print ""
        print "----------Starting Update Round: " + str(Index + 1) + "----------"
        print ""
        NewValue = AttributeValueList[Index]
        if Attribute == "EMAIL":
            NewValue += str(random.randrange(1,100000))
        Mod.main(Username, Attribute, NewValue)
    


if UsersOption == 0:
    for Index, Username in enumerate(UsernameList):
        print ""
        print ""
        print "----------Starting User Round: " + str(Index + 1) + "----------"
        print ""
        print ""
        ValueUpdate(Username, AttributeNameList, AttributeValueList)

if UsersOption == 1:
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    cursor.execute("""SELECT Username FROM UserBook ORDER BY RAND() LIMIT %d""" % (Loops))
    RandomUsernameList = cursor.fetchall()
    for Index, Username in enumerate(RandomUsernameList):
        Username = Username[0]
        print ""
        print ""
        print "----------Starting User Round: " + str(Index + 1) + "----------"
        print ""
        print ""
        ValueUpdate(Username, AttributeNameList, AttributeValueList)



#Ends timer
TimerEnd = time.clock()
TimePassed = TimerEnd - TimerStart

print ""
print "Run Time: " + str(TimePassed) + " Seconds"


