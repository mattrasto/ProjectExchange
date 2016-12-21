#-------------------------------------------------------------------------------
# Name:        DBUpdatePrivateTrade
# Version:     1.0
# Purpose:
#
# Author:      Matthew
#
# Created:     06/01/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    06/01/2014
#-------------------------------------------------------------------------------

import MySQLdb

db = MySQLdb.connect("localhost","root","***","exchangedatabase")

cursor = db.cursor()

cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data



'''Defining Variables'''



TradeNumber = raw_input("Modified Trade: ")
while 1 == 1:
    try:
        TradeNumber = int(TradeNumber)
        break;
    except:
        print "You must enter a number:"
        TradeNumber = raw_input("Modified Trade: ")

TradeFound = False
try:
    while TradeFound != True:
        print TradeNumber
        cursor.execute("""SELECT * FROM PrivateTradeBook WHERE TradeNumber = %d""" % (TradeNumber))
        FoundTrade = cursor.fetchall()
        if FoundTrade != ():
            print "Trade found"
            print "FoundTrade: " + str(FoundTrade)
            TradeFound = True
            for Trade in FoundTrade:
                print Trade
                Username = Trade[1]
                Price = Trade[2]
                Volume = Trade[3]
                Action = Trade[5]
                DateEntered = Trade[6]
        else:
            print "Trade not found. Please enter again: "
            TradeNumber = raw_input("Modified Trade: ")
            while 1 == 1:
                try:
                    TradeNumber = int(TradeNumber)
                    break;
                except:
                    print "You must enter a number:"
                    TradeNumber = raw_input("Modified Trade: ")
except:
    print "Trade not found"

if TradeFound == True:
    Attribute = raw_input("Changing Attribute: ")
    Attribute = Attribute.upper()
    
    cursor.execute("SELECT * FROM PrivateTradeBook WHERE TradeNumber = %d" % (TradeNumber))
    TradeBookTrades = cursor.fetchall()
    for Header in cursor.description:
        TargetAttribute = Header[0]
        if TargetAttribute.upper() == Attribute or Attribute == "TRADE NUMBER" or Attribute == "DATE ENTERED" or Attribute == "USER REQUESTS":
            break;
    while TargetAttribute.upper() != Attribute and Attribute != "TRADE NUMBER" and Attribute != "DATE ENTERED" and Attribute != "USER REQUESTS":
        print "Attribute is invalid. Please enter again:"
        print "Choices: " + str([Header[0] for Header in cursor.description])
        Attribute = raw_input("Changing Attribute: ")
        Attribute = Attribute.upper()
        for Header in cursor.description:
            TargetAttribute = Header[0]
            if TargetAttribute.upper() == Attribute or Attribute == "TRADE NUMBER" or Attribute == "DATE ENTERED" or Attribute == "USER REQUESTS":
                    break;
    
    if Attribute != "DATEENTERED" and Attribute != "DATE ENTERED":
        NewValue = raw_input("New Value: ")
        while NewValue == "":
            print "Value is invalid. Please enter again:"
            NewValue = raw_input("New Value: ")
            NewValue = NewValue.upper()
    
    Comment = raw_input("Administrative Comment: ")
    
    
    
    
    '''Defining/Executing SQL Statements'''
    
    
    
    UpdateComplete = False
    
    if Attribute == "TRADENUMBER" or Attribute == "TRADE NUMBER":
        NewValue = int(NewValue)
        try:
            cursor.execute("UPDATE PrivateTradeBook SET TradeNumber = %d WHERE TradeNumber = %d" % (NewValue, TradeNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Trade modified: " + str(TradeNumber)
            print "Attribute modified: Trade Number"
            print "New value: " + str(NewValue)
            UpdateComplete = True
        except:
            db.rollback()
            cursor.execute("SELECT * FROM PrivateTradeBook WHERE TradeNumber = %d" % (NewValue))
            ExistingTrades = cursor.fetchall()
            if ExistingTrades != ():
                print "Trade number is already in use"
                print ExistingTrades
            else:
                print "Update Unsuccessful"
        
    if Attribute == "USERNAME":
        NewValue = str(NewValue.capitalize())
        try:
            cursor.execute("SELECT * FROM PrivateTradeBook WHERE TradeNumber = %d" % (TradeNumber))
            TradeBookTrades = cursor.fetchall()
            cursor.execute("""UPDATE PrivateTradeBook SET Username = "%s" WHERE TradeNumber = %d""" % (NewValue, TradeNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Trade modified: " + str(TradeNumber)
            print "Attribute modified: Username"
            print "New value: " + str(NewValue.capitalize())
            UpdateComplete = True
        except:
            db.rollback()
            print "Update Unsuccessful"
            print "Ensure that an existing user has been entered"
        
    if Attribute == "PRICE":
        NewValue = float(NewValue)
        try:
            cursor.execute("SELECT * FROM PrivateTradeBook WHERE TradeNumber = %d" % (TradeNumber))
            TradeBookTrades = cursor.fetchall()
            cursor.execute("UPDATE PrivateTradeBook SET Price = %f WHERE TradeNumber = %d" % (NewValue, TradeNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "User modified: " + str(TradeNumber)
            print "Attribute modified: Price"
            print "New value: " + str(NewValue)
            UpdateComplete = True
        except:
            db.rollback()
            print "Update Unsuccessful"
        
    if Attribute == "VOLUME":
        NewValue = float(NewValue)
        try:
            cursor.execute("SELECT * FROM PrivateTradeBook WHERE TradeNumber = %d" % (TradeNumber))
            TradeBookTrades = cursor.fetchall()
            cursor.execute("UPDATE PrivateTradeBook SET Volume = %f WHERE TradeNumber = %d" % (NewValue, TradeNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Trade modified: " + str(TradeNumber)
            print "Attribute modified: Volume"
            print "New value: " + str(NewValue)
            UpdateComplete = True
        except:
            db.rollback()
            print "Update Unsuccessful"
    
    
    
    if Attribute == "ACTION":
        NewValue = str(NewValue)
        try:
            cursor.execute("SELECT * FROM PrivateTradeBook WHERE TradeNumber = %d" % (TradeNumber))
            TradeBookTrades = cursor.fetchall()
            cursor.execute("""UPDATE PrivateTradeBook SET Action = "%s" WHERE TradeNumber = %d""" % (NewValue, TradeNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Trade modified: " + str(TradeNumber)
            print "Attribute modified: Action"
            print "New value: " + str(NewValue)
            UpdateComplete = True
        except:
            db.rollback()
            print "Update Unsuccessful"
    
    
    
    if Attribute == "USERREQUESTS" or Attribute == "USER REQUESTS":
        NewValue = int(NewValue)
        try:
            cursor.execute("SELECT * FROM PrivateTradeBook WHERE TradeNumber = %d" % (TradeNumber))
            TradeBookTrades = cursor.fetchall()
            cursor.execute("UPDATE PrivateTradeBook SET UserRequests = %d WHERE TradeNumber = %d" % (NewValue, TradeNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "User modified: " + str(TradeNumber)
            print "Attribute modified: User Requests"
            print "New value: " + str(NewValue)
            UpdateComplete = True
        except:
            db.rollback()
            print "Update Unsuccessful"
    
    
    
    if Attribute == "DATEENTERED" or Attribute == "DATE ENTERED":
    
        while 1 == 1:
            Year = raw_input("Year: ")
            if Year == "":
                DateSearchYearOmit = True
                break;
            try:
                Year = int(Year)
                if Year > 2014 or Year <= 2013:
                    print "Year not valid. Please enter again:"
                else:
                    DateSearchYearOmit = False
                    break;
            except:
                print "Value must be an integer. Please enter again:"
        
        while 1 == 1:
            Month = raw_input("Month: ")
            if Month == "":
                DateSearchMonthOmit = True
                break;
            try:
                Month = int(Month)
                if Month > 12 or Month <= 0:
                    print "Month not valid. Please enter again:"
                else:
                    DateSearchMonthOmit = False
                    break;
            except:
                print "Value must be an integer. Please enter again:"
        
        while 1 == 1:
            Day = raw_input("Day: ")
            if Day == "":
                DateSearchDayOmit = True
                break;
            try:
                Day = int(Day)
                if Day > 31 or Day <= 0:
                    print "Day not valid. Please enter again:"
                else:
                    DateSearchDayOmit = False
                    break;
            except:
                print "Value must be an integer. Please enter again:"
        
        while 1 == 1:
            Hour = raw_input("Hour: ")
            if Hour == "":
                DateSearchHourOmit = True
                break;
            try:
                Hour = int(Hour)
                if Hour > 24 or Hour < 0:
                    print "Hour not valid. Please enter again:"
                else:
                    DateSearchHourOmit = False
                    break;
            except:
                print "Value must be an integer. Please enter again:"
        
        while 1 == 1:
            Minute = raw_input("Minute: ")
            if Minute == "":
                DateSearchMinuteOmit = True
                break;
            try:
                Minute = int(Minute)
                if Minute > 60 or Minute < 0:
                    print "Minute not valid. Please enter again:"
                else:
                    DateSearchMinuteOmit = False
                    break;
            except:
                print "Value must be an integer. Please enter again:"
        
        while 1 == 1:
            Second = raw_input("Second: ")
            if Second == "":
                DateSearchSecondOmit = True
                break;
            try:
                Second = int(Second)
                if Second > 60 or Second < 0:
                    print "Second not valid. Please enter again:"
                else:
                    DateSearchSecondOmit = False
                    break;
            except:
                print type(Second)
                print "Value must be an integer. Please enter again:"
        
        try:
            cursor.execute("SELECT * FROM PrivateTradeBook WHERE TradeNumber = %d" % (TradeNumber))
            PrivateTradeBookTrades = cursor.fetchall()
        except:
            print "ERROR: Database fetch exception"
    
        for Trade in PrivateTradeBookTrades:
            print Trade
            
            if DateSearchYearOmit == True:
                YearValue = ""
                #print Trade[8]
                for Character in str(Trade[6])[:4]:
                    YearValue += str(Character)
                Year = YearValue
            
            if DateSearchMonthOmit == True:
                MonthValue = ""
                #print Trade[8]
                for Character in str(Trade[6])[5:7]:
                    MonthValue += str(Character)
                Month = MonthValue
                
            if DateSearchDayOmit == True:
                DayValue = ""
                #print Trade[8]
                for Character in str(Trade[6])[8:10]:
                    DayValue += str(Character)
                Day = DayValue
                
            if DateSearchHourOmit == True:
                HourValue = ""
                #print Trade[8]
                for Character in str(Trade[6])[11:13]:
                    HourValue += str(Character)
                Hour = HourValue
                
            if DateSearchMinuteOmit == True:
                MinuteValue = ""
                #print Trade[8]
                for Character in str(Trade[6])[14:16]:
                    MinuteValue += str(Character)
                Minute = MinuteValue
            
            if DateSearchSecondOmit == True:
                SecondValue = ""
                #print Trade[8]
                for Character in str(Trade[6])[17:19]:
                    SecondValue += str(Character)
                Second = SecondValue
    
        if Month < 10:
            Month = "0" + str(Month)
        if Day < 10:
            Day = "0" + str(Day)
        if Hour < 10:
            Hour = "0" + str(Hour)
        if Minute < 10:
            Minute = "0" + str(Minute)
        if Second < 10:
            Second = "0" + str(Second)
        
        FormattedDateTime = str(Year) + "-" + str(Month) + "-" + str(Day) + " " + str(Hour) + ":" + str(Minute) + ":" + str(Second)
        try:
            cursor.execute("SELECT * FROM PrivateTradeBook WHERE TradeNumber = %d" % (TradeNumber))
            TradeBookTrades = cursor.fetchall()
            cursor.execute("""UPDATE PrivateTradeBook SET DateEntered = "%s" WHERE TradeNumber = %d""" % (FormattedDateTime, TradeNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Trade modified: " + str(TradeNumber)
            print "Attribute modified: Date Entered"
            print "New value: " + str(FormattedDateTime)
            UpdateComplete = True
        except:
            db.rollback()
            print "Update Unsuccessful"



    '''Logging Control'''
    
    
    
    if UpdateComplete == True:
        Employee = "***333"
        
        TradeID = "Trade " + str(TradeNumber)
        
        try:
            print ""
            cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update Private Trade", TradeID, Attribute.title(), Comment))
            db.commit()
            print "Control Successfully Logged"
        except:
            print "ERROR: Control Unsuccessfully Logged"



db.close()