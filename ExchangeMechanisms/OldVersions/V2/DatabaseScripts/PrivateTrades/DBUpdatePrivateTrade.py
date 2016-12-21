#-------------------------------------------------------------------------------
# Name:        DBUpdatePrivateTrade
# Version:     2.0
# Purpose:
#
# Author:      Matthew
#
# Created:     06/01/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/15/2014
#-------------------------------------------------------------------------------

#Add safe type checking in main()

import MySQLdb
import sys



def main(TradeNumber, Attribute, NewValue):
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    print ""
    
    
    
    '''Verifying Trade'''
    
    
    
    #Exits if TradeNumber is not an integer
    if not isinstance(TradeNumber, int):
        print ""
        print "CRITICAL ERROR: Trade Number not an integer"
        print ""
        sys.exit()
    try:
        cursor.execute("""SELECT * FROM PrivateTradeBook WHERE TradeNumber = %d""" % (TradeNumber))
        Trade = cursor.fetchone()
        if Trade != None:
            #print "Trade Found"
            pass
        else:
            print ""
            print "CRITICAL ERROR: Trade not found"
            print ""
            sys.exit()
    except SystemExit:
        sys.exit()
    except:
        print ""
        print "ERROR: Database fetch exception"
        print ""
    
    
    
    '''Defining/Executing SQL Statements'''
    
    
    
    #Updates specified trade's TradeNumber
    if Attribute == "TRADE NUMBER":
        #Converts TradeNumber value to integer type
        try:
            NewValue = int(NewValue)
        except:
            print "CRITICAL ERROR: Trade Number unable to be converted to integer"
            sys.exit()
        #Attempts to change IDNumber to new desired value
        try:
            cursor.execute("UPDATE IDBook SET IDNumber = %d WHERE IDNumber = %d" % (NewValue, TradeNumber))
        except:
            cursor.execute("""SELECT * FROM IDBook WHERE IDNumber = %d""" % (NewValue))
            ExistingIDs = cursor.fetchall()
            if ExistingIDs == None:
                print "CRITICAL ERROR: IDBook unable to change IDNumber to specified value"
            else:
                print "CRITICAL ERROR: Specified TradeNumber is unavailable in IDBook"
            sys.exit()
        #Attempts to change TradeNumber to new desired value
        try:
            cursor.execute("UPDATE PrivateTradeBook SET TradeNumber = %d WHERE TradeNumber = %d" % (NewValue, TradeNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Trade modified: " + str(TradeNumber)
            print "Attribute modified: Trade Number"
            print "New value: " + str(NewValue)
        except:
            #If unsuccessful, searches for existing trades and displays any if found
            db.rollback()
            cursor.execute("SELECT * FROM PrivateTradeBook WHERE TradeNumber = %d" % (NewValue))
            ExistingTrades = cursor.fetchall()
            if ExistingTrades != ():
                print "ERROR: Trade number is already in use"
                print ExistingTrades
            else:
                print "Update Unsuccessful"
    
    
    
    #Updates specified trade's Username
    if Attribute == "USERNAME":
        #Converts Username value to string type and capitalizes
        try:
            NewValue = str(NewValue.capitalize())
        except:
            print "CRITICAL ERROR: Username unable to be converted to string"
            sys.exit()
        #Attempts to change Username to new desired value
        try:
            cursor.execute("""UPDATE PrivateTradeBook SET Username = "%s" WHERE TradeNumber = %d""" % (NewValue, TradeNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Trade modified: " + str(TradeNumber)
            print "Attribute modified: Username"
            print "New value: " + str(NewValue.capitalize())
        except:
            db.rollback()
            print "Update Unsuccessful"
            print "Ensure that an existing user has been entered"
    
    
    
    #Updates specified trade's Price
    if Attribute == "PRICE":
        #Converts Price value to float type
        try:
            NewValue = float(NewValue)
        except:
            print "CRITICAL ERROR: Price unable to be converted to float"
            sys.exit()
        #Attempts to change Price to new desired value
        try:
            cursor.execute("UPDATE PrivateTradeBook SET Price = %f WHERE TradeNumber = %d" % (NewValue, TradeNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Trade modified: " + str(TradeNumber)
            print "Attribute modified: Price"
            print "New value: " + str(NewValue)
        except:
            db.rollback()
            print "Update Unsuccessful"
    
    
    
    #Updates specified trade's Volume
    if Attribute == "VOLUME":
        #Converts Volume value to float type
        try:
            NewValue = float(NewValue)
        except:
            print "CRITICAL ERROR: Volume unable to be converted to float"
            sys.exit()
        #Attempts to change Volume to new desired value
        try:
            cursor.execute("UPDATE PrivateTradeBook SET Volume = %f WHERE TradeNumber = %d" % (NewValue, TradeNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Trade modified: " + str(TradeNumber)
            print "Attribute modified: Volume"
            print "New value: " + str(NewValue)
        except:
            db.rollback()
            print "Update Unsuccessful"
    
    
    
    #Updates specified trade's Action
    if Attribute == "ACTION":
        #Converts Action value to string type
        try:
            NewValue = str(NewValue)
        except:
            print "CRITICAL ERROR: Action unable to be converted to string"
            sys.exit()
        #Attempts to change Action to new desired value
        try:
            cursor.execute("""UPDATE PrivateTradeBook SET Action = "%s" WHERE TradeNumber = %d""" % (NewValue, TradeNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Trade modified: " + str(TradeNumber)
            print "Attribute modified: Action"
            print "New value: " + str(NewValue)
        except:
            db.rollback()
            print "Update Unsuccessful"
    
    
    
    #Updates specified trade's amount of UserRequests
    if Attribute == "USER REQUESTS":
        #Converts UserRequests value to integer type
        try:
            NewValue = int(NewValue)
        except:
            print "CRITICAL ERROR: User Requests unable to be converted to integer"
            sys.exit()
        #Attempts to change UserRequests to new desired value
        try:
            cursor.execute("UPDATE PrivateTradeBook SET UserRequests = %d WHERE TradeNumber = %d" % (NewValue, TradeNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Trade modified: " + str(TradeNumber)
            print "Attribute modified: User Requests"
            print "New value: " + str(NewValue)
        except:
            db.rollback()
            print "Update Unsuccessful"
    
    
    
    #Updates specified trade's DateEntered
    if Attribute == "DATE ENTERED":
        
        #Gathers current DateEntered and separates into date/time components
        try:
            cursor.execute("""SELECT DateEntered FROM PrivateTradeBook WHERE TradeNumber = "%s" """ % (TradeNumber))
            CurrentDateEntered = cursor.fetchall()[0]
            if CurrentDateEntered != ():
                CurrentDateEntered = str(CurrentDateEntered[0])
                
                CurrentDateEnteredYear = CurrentDateEntered[:4]
                CurrentDateEnteredMonth = CurrentDateEntered[5:7]
                CurrentDateEnteredDay = CurrentDateEntered[8:10]
                CurrentDateEnteredHour = CurrentDateEntered[11:13]
                CurrentDateEnteredMinute = CurrentDateEntered[14:16]
                CurrentDateEnteredSecond = CurrentDateEntered[17:19]
            else:
                print "CRITICAL ERROR: User has no current join date"
                sys.exit()
        except:
            print "ERROR: Database fetch exception"
        
        
        
        #Separates NewValue variable into date/time components
        NewYear = NewValue[0]
        NewMonth = NewValue[1]
        NewDay = NewValue[2]
        NewHour = NewValue[3]
        NewMinute = NewValue[4]
        NewSecond = NewValue[5]
        
        
        
        #If any parameter was left blank by user, parameter is set to the current DateEntered interval value
        if NewYear == "":
            NewYear = CurrentDateEnteredYear
        if NewMonth == "":
            NewMonth = CurrentDateEnteredMonth
        if NewDay == "":
            NewDay = CurrentDateEnteredDay
        if NewHour == "":
            NewHour = CurrentDateEnteredHour
        if NewMinute == "":
            NewMinute = CurrentDateEnteredMinute
        if NewSecond == "":
            NewSecond = CurrentDateEnteredSecond
        
        
        
        #If any date/time value is under 10, converts value to string and adds a "0" before value for database compatibility
        if NewMonth < 10:
            NewMonth = "0" + str(NewMonth)
        if NewDay < 10:
            NewDay = "0" + str(NewDay)
        if NewHour < 10:
            NewHour = "0" + str(NewHour)
        if NewMinute < 10:
            NewMinute = "0" + str(NewMinute)
        if NewSecond < 10:
            NewSecond = "0" + str(NewSecond)
        
        
        
        #Forms new Duration value by converting date/time components to strings and concatenating
        NewValue = str(NewYear) + "-" + str(NewMonth) + "-" + str(NewDay) + " " + str(NewHour) + ":" + str(NewMinute) + ":" + str(NewSecond)
        
        
        
        #Attempts to change DateEntered to new desired value
        try:
            cursor.execute("""UPDATE PrivateTradeBook SET DateEntered = "%s" WHERE TradeNumber = %d""" % (NewValue, TradeNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Trade modified: " + str(TradeNumber)
            print "Attribute modified: Date Entered"
            print "New value: " + str(NewValue)
        except:
            db.rollback()
            print "Update Unsuccessful"
    
    
    
    '''Creating Logging Record'''
    
    
    
    #Inserts record of order with changes into MTCLog
    cursor.execute("""SELECT MAX(VersionNumber) FROM PrivateTradeLog WHERE TradeNumber = %d""" % (TradeNumber))
    OldMaxVersion = int(cursor.fetchone()[0])
    NewVersion = OldMaxVersion + 1
    cursor.execute("""INSERT INTO PrivateTradeLog(TradeNumber, VersionNumber, LastModified, Username, Price, Volume, Action, DateEntered) SELECT TradeNumber, %d, "%s", Username, Price, Volume, Action, DateEntered FROM PrivateTradeBook WHERE TradeNumber = %d""" % (NewVersion, Attribute.title(), TradeNumber))
    db.commit()
    
    
    
    '''Logging Control'''
    
    
    
    #Assigns static variables for logging control
    #Note: "Employee" value changes based on user submitting manual control
    Employee = "***333"
    TradeID = "Trade " + str(TradeNumber)
    Comment = "Updated Private Trade"
    
    
    
    #Inserts record of action into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update Private Trade", TradeID, Attribute.title(), Comment))
        db.commit()
        print "Control Successfully Logged"
    except:
        print "ERROR: Control Unsuccessfully Logged"



    db.close()



if __name__ == "__main__":
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    print ""
    
    
    
    '''Setting TradeNumber'''
    
    
    
    #Requests TradeNumber and verifies that it is valid
    while 1 == 1:
        TradeNumber = raw_input("Update Trade Number: ")
        #Checks for integer type
        while 1 == 1:
            try:
                TradeNumber = int(TradeNumber)
                break;
            except:
                print "Trade Number must be an integer. Please enter again: "
                TradeNumber = raw_input("Trade Number: ")
        try:
            #Checks if order exists
            cursor.execute("""SELECT * FROM PrivateTradeBook WHERE TradeNumber = %d""" % (TradeNumber))
            Trade = cursor.fetchone()
            if Trade != None:
                break;
            else:
                print "Trade not found. Please search again:"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    '''Setting Attribute'''
    
    
    
    #Requests attribute to update and verifies that it is valid
    
    Attribute = raw_input("Changing Attribute: ")
    Attribute = Attribute.upper()
    
    #Gathers column titles from PrivateTradeBook
    cursor.execute("SHOW COLUMNS FROM PrivateTradeBook")
    FieldList = cursor.fetchall()
    #Iterates column names and matches entered Attribute against existing names
    for Field in FieldList:
        TargetAttribute = Field[0]
        if TargetAttribute.upper() == Attribute or Attribute == "TRADE NUMBER" or Attribute == "DATE ENTERED" or Attribute == "USER REQUESTS":
            break;
    #Retrying until valid input is given
    while TargetAttribute.upper() != Attribute and Attribute != "TRADE NUMBER" and Attribute != "DATE ENTERED" and Attribute != "USER REQUESTS":
        print "Attribute is invalid. Please enter again:"
        print "Choices: " + str([Field[0] for Field in FieldList])
        Attribute = raw_input("Changing Attribute: ")
        Attribute = Attribute.upper()
        for Field in FieldList:
            TargetAttribute = Field[0]
            if TargetAttribute.upper() == Attribute or Attribute == "TRADE NUMBER" or Attribute == "DATE ENTERED" or Attribute == "USER REQUESTS":
                    break;
    
    
    
    '''Standardizing Parameter Names'''
    
    
    
    if Attribute == "TRADENUMBER":
        Attribute = "TRADE NUMBER"
        print "Updating: Trade Number"
    
    elif Attribute == "DATEENTERED":
        Attribute = "DATE ENTERED"
        print "Updating: Date Entered"
    
    elif Attribute == "USERREQUESTS":
        Attribute = "USER REQUESTS"
        print "Updating: User Requests"
    
    else:
        print "Updating: " + Attribute.title()
    
    
    
    '''Setting NewValue'''
    
    
    
    #Requesting basic input value if not a date field
    if Attribute != "DATEENTERED" and Attribute != "DATE ENTERED":
        NewValue = raw_input("New Value: ")
        while NewValue == "":
            print "Value is invalid. Please enter again:"
            NewValue = raw_input("New Value: ")
            NewValue = NewValue.upper()
    #Requesting date input values if not a basic input field
    else:
        
        YearValid = False
        MonthValid = False
        DayValid = False
        HourValid = False
        MinuteValid = False
        SecondValid = False
        
        
        
        while YearValid != True:
            DateUpdateYear = raw_input("Update Year: ")
            if DateUpdateYear != "":
                try:
                    DateUpdateYear = int(DateUpdateYear)
                    if DateUpdateYear >= 2014 and DateUpdateYear <= 2015:
                        print DateUpdateYear
                        YearValid = True
                    else:
                        print "Update parameter must be between 2014 and 2015. Please enter again:"
                except:
                    print "Update parameter must be an integer or blank. Please enter again:"
            else:
                YearValid = True
        
        
        
        while MonthValid != True:
            DateUpdateMonth = raw_input("Update Month: ")
            if DateUpdateMonth != "":
                try:
                    DateUpdateMonth = int(DateUpdateMonth)
                    if DateUpdateMonth >= 1 and DateUpdateMonth <= 12:
                        print DateUpdateMonth
                        MonthValid = True
                    else:
                        print "Update parameter must be between 1 and 12. Please enter again:"
                except:
                    print "Update parameter must be an integer or blank. Please enter again:"
            else:
                MonthValid = True
        
        
        
        while DayValid != True:
            DateUpdateDay = raw_input("Update Day: ")
            if DateUpdateDay != "":
                try:
                    DateUpdateDay = int(DateUpdateDay)
                    if DateUpdateDay >= 1 and DateUpdateDay <= 365:
                        print DateUpdateDay
                        DayValid = True
                    else:
                        print "Update parameter must be between 1 and 365. Please enter again:"
                except:
                    print "Update parameter must be an integer or blank. Please enter again:"
            else:
                DayValid = True
        
        
        
        while HourValid != True:
            DateUpdateHour = raw_input("Update Hour: ")
            if DateUpdateHour != "":
                try:
                    DateUpdateHour = int(DateUpdateHour)
                    if DateUpdateHour >= 0 and DateUpdateHour <= 23:
                        print DateUpdateHour
                        HourValid = True
                    else:
                        print "Update parameter must be between 0 and 23. Please enter again:"
                except:
                    print "Update parameter must be an integer or blank. Please enter again:"
            else:
                HourValid = True
        
        
        
        while MinuteValid != True:
            DateUpdateMinute = raw_input("Update Minute: ")
            if DateUpdateMinute != "":
                try:
                    DateUpdateMinute = int(DateUpdateMinute)
                    if DateUpdateMinute >= 0 and DateUpdateMinute <= 59:
                        print DateUpdateMinute
                        MinuteValid = True
                    else:
                        print "Update parameter must be between 0 and 59. Please enter again:"
                except:
                    print "Update parameter must be an integer or blank. Please enter again:"
            else:
                MinuteValid = True
        
        
        
        while SecondValid != True:
            DateUpdateSecond = raw_input("Update Second: ")
            if DateUpdateSecond != "":
                try:
                    DateUpdateSecond = int(DateUpdateSecond)
                    if DateUpdateSecond >= 0 and DateUpdateSecond <= 59:
                        print DateUpdateSecond
                        SecondValid = True
                    else:
                        print "Update parameter must be between 0 and 59. Please enter again:"
                except: 
                    print "Update parameter must be an integer or blank. Please enter again:"
            else:
                SecondValid = True
        
        
        
        #Combines all date/time component values into a list for passing to main()
        NewValue = [DateUpdateYear, DateUpdateMonth, DateUpdateDay, DateUpdateHour, DateUpdateMinute, DateUpdateSecond]
        
    
    
    #Execute
    main(TradeNumber, Attribute, NewValue)


