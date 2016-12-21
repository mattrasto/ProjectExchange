#-------------------------------------------------------------------------------
# Name:        DBUpdateBasicOrder
# Version:     3.0
# Purpose:     Updates Basic Order's specified attribute with specified value
#
# Author:      Matthew
#
# Created:     05/21/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/15/2014
#-------------------------------------------------------------------------------

#Only log record/control if update passes
#Add support for order logging when contract number is changed

import MySQLdb
import sys



def main(OrderNumber, Attribute, NewValue):
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    
    
    '''Verifying Order'''
    
    
    
    print ""
    #Exits if OrderNumber is not an integer
    if not isinstance(OrderNumber, int):
        print "CRITICAL ERROR: Order Number not an integer"
        sys.exit()
    OrderSearch = "SELECT * FROM BasicOrderBook WHERE OrderNumber = %d" % (OrderNumber)
    try:
        cursor.execute(OrderSearch)
        Order = cursor.fetchone()
        if Order != None:
            #print "Order Found"
            pass
        else:
            print "CRITICAL ERROR: Order not found"
            sys.exit()
    except SystemExit:
        sys.exit()
    except:
        print "ERROR: Database fetch exception"
    
    
    
    '''Defining/Executing SQL Statements'''
    
    
    
    #Updates specified order's OrderNumber
    if Attribute == "ORDER NUMBER":
        #Converts OrderNumber value to integer type
        try:
            NewValue = int(NewValue)
        except:
            print "CRITICAL ERROR: Order Number unable to be converted to integer"
            sys.exit()
        #Attempts to change IDNumber to new desired value
        try:
            cursor.execute("UPDATE IDBook SET IDNumber = %d WHERE IDNumber = %d" % (NewValue, OrderNumber))
        except:
            cursor.execute("""SELECT * FROM IDBook WHERE IDNumber = %d""" % (NewValue))
            ExistingIDs = cursor.fetchall()
            if ExistingIDs == None:
                print "CRITICAL ERROR: IDBook unable to change IDNumber to specified value"
            else:
                print "CRITICAL ERROR: Specified OrderNumber is unavailable in IDBook"
            sys.exit()
        #Attempts to change OrderNumber to new desired value
        try:
            cursor.execute("UPDATE BasicOrderBook SET OrderNumber = %d WHERE OrderNumber = %d" % (NewValue, OrderNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Order Modified: " + str(OrderNumber)
            print "Attribute Modified: Order Number"
            print "New Value: " + str(NewValue)
        except:
            #If unsuccessful, searches for existing orders and displays any if found
            db.rollback()
            print "ERROR: Update Unsuccessful"
            cursor.execute("SELECT * FROM BasicOrderBook WHERE OrderNumber = %d" % (NewValue))
            ExistingOrders = cursor.fetchall()
            if ExistingOrders != ():
                print "ERROR: Order Number is already in use:"
                print ""
                print ExistingOrders
            sys.exit()
    
    
    
    #Updates specified order's Username
    if Attribute == "USERNAME":
        #Converts Username value to string type and capitalizes
        try:
            NewValue = str(NewValue.capitalize())
        except:
            print "CRITICAL ERROR: Username unable to be converted to string"
            sys.exit()
        #Attempts to change Username to new desired value
        try:
            cursor.execute("""UPDATE BasicOrderBook SET Username = "%s" WHERE OrderNumber = %d""" % (NewValue, OrderNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Order Modified: " + str(OrderNumber)
            print "Attribute Modified: Username"
            print "New Value: " + str(NewValue.capitalize())
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
            print "Ensure that an existing user has been entered"
    
    
    
    #Updates specified order's Price
    if Attribute == "PRICE":
        #Converts Price value to float type
        try:
            NewValue = float(NewValue)
        except:
            print "CRITICAL ERROR: Price unable to be converted to float"
            sys.exit()
        #Attempts to change Price to new desired value
        try:
            cursor.execute("UPDATE BasicOrderBook SET Price = %f WHERE OrderNumber = %d" % (NewValue, OrderNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Order Modified: " + str(OrderNumber)
            print "Attribute Modified: Price"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified order's Volume
    if Attribute == "VOLUME":
        #Converts Volume value to float type
        try:
            NewValue = float(NewValue)
        except:
            print "CRITICAL ERROR: Volume unable to be converted to float"
            sys.exit()
        #Attempts to change Volume to new desired value
        try:
            cursor.execute("UPDATE BasicOrderBook SET Volume = %f WHERE OrderNumber = %d" % (NewValue, OrderNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Order Modified: " + str(OrderNumber)
            print "Attribute Modified: Volume"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "Update Unsuccessful"
    
    
    
    #Updates specified order's Type
    if Attribute == "TYPE":
        #Converts Type value to string type and capitalizes
        try:
            NewValue = str(NewValue.capitalize())
        except:
            print "CRITICAL ERROR: Type unable to be converted to string"
            sys.exit()
        #Attempts to change Type to new desired value
        try:
            cursor.execute("""UPDATE BasicOrderBook SET Type = "%s" WHERE OrderNumber = %d""" % (NewValue, OrderNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Order Modified: " + str(OrderNumber)
            print "Attribute Modified: Type"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "Update Unsuccessful"
    
    
    
    #Updates specified order's Action
    if Attribute == "ACTION":
        #Converts Action value to string type
        try:
            NewValue = str(NewValue.title())
        except:
            print "CRITICAL ERROR: Action unable to be converted to string"
            sys.exit()
        #Attempts to change Action to new desired value
        try:
            cursor.execute("""UPDATE BasicOrderBook SET Action = "%s" WHERE OrderNumber = %d""" % (NewValue, OrderNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Order Modified: " + str(OrderNumber)
            print "Attribute Modified: Action"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "Update Unsuccessful"
    
    
    
    #Updates specified order's Trigger Type
    if Attribute == "TRIGGER TYPE":
        #Converts Trigger Type value to string type
        try:
            NewValue = str(NewValue.title())
        except:
            print "CRITICAL ERROR: Trigger Type unable to be converted to integer"
            sys.exit()
        #Attempts to change TriggerType to new desired value
        try:
            cursor.execute("""UPDATE BasicOrderBook SET TriggerType = "%s" WHERE OrderNumber = %d""" % (NewValue, OrderNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Order Modified: " + str(OrderNumber)
            print "Attribute Modified: Trigger Type"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "Update Unsuccessful"
    
    
    
    #Updates specified order's Trigger Value
    if Attribute == "TRIGGER VALUE":
        #Converts Trigger Value value to float type
        try:
            NewValue = float(NewValue)
        except:
            print "CRITICAL ERROR: Trigger Value unable to be converted to float"
            sys.exit()
        #Attempts to change TriggerValue to new desired value
        try:
            cursor.execute("UPDATE BasicOrderBook SET TriggerValue = %f WHERE OrderNumber = %d" % (NewValue, OrderNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Order Modified: " + str(OrderNumber)
            print "Attribute Modified: Trigger Value"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "Update Unsuccessful"
    
    
    
    #Updates specified order's Date Entered
    if Attribute == "DATE ENTERED":
        
        #Gathers current DateEntered and separates into date/time components
        try:
            cursor.execute("""SELECT DateEntered FROM BasicOrderBook WHERE OrderNumber = "%s" """ % (OrderNumber))
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
                print "CRITICAL ERROR: Order has no current date entered"
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
        
        
        
        #If user left any interval blank, turns search parameter to "%" for wildcard searching in database
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
        
        
        
        #Forms new DateEntered value by converting date/time components to strings and concatenating
        NewValue = str(NewYear) + "-" + str(NewMonth) + "-" + str(NewDay) + " " + str(NewHour) + ":" + str(NewMinute) + ":" + str(NewSecond)
        
        
        
        #Attempts to change DateEntered to new desired value
        try:
            cursor.execute("""UPDATE BasicOrderBook SET DateEntered = "%s" WHERE OrderNumber = "%s" """ % (NewValue, OrderNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Order Modified: " + str(OrderNumber)
            print "Attribute Modified: Date Entered"
            print "New Value: " + str(NewValue)
        except:
            print "ERROR: Database fetch exception"



    '''Creating Logging Record'''
    
    
    
    #Inserts record of order with changes into BasicOrderLog
    cursor.execute("""SELECT MAX(VersionNumber) FROM BasicOrderLog WHERE OrderNumber = %d""" % (OrderNumber))
    OldMaxVersion = int(cursor.fetchone()[0])
    NewVersion = OldMaxVersion + 1
    cursor.execute("""INSERT INTO BasicOrderLog(OrderNumber, VersionNumber, LastModified, Username, Price, Volume, Type, Action, TriggerType, TriggerValue, DateEntered) SELECT OrderNumber, %d, "%s", Username, Price, Volume, Type, Action, TriggerType, TriggerValue, DateEntered FROM BasicOrderBook WHERE OrderNumber = %d""" % (NewVersion, Attribute.title(), OrderNumber))
    db.commit()



    '''Logging Control'''
    
    
    
    #Assigns static variables for logging control
    #Note: "Employee" value changes based on user submitting manual control
    Employee = "***333"
    OrderID = "Order " + str(OrderNumber)
    Comment = "Updated Basic Order"
    
    
    
    #Inserts record of action into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update Basic Order", OrderID, Attribute.title(), Comment))
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
    
    
    
    '''Setting OrderNumber'''
    
    
    
    #Requests OrderNumber and verifies that it is valid
    while 1 == 1:
        OrderNumber = raw_input("Update Order Number: ")
        #Checks for integer type
        while 1 == 1:
            try:
                OrderNumber = int(OrderNumber)
                break;
            except:
                print "Order Number must be an integer. Please enter again: "
                OrderNumber = raw_input("Order Number: ")
        try:
            #Checks if order exists
            cursor.execute("""SELECT * FROM BasicOrderBook WHERE OrderNumber = %d""" % (OrderNumber))
            Order = cursor.fetchone()
            if Order != None:
                break;
            else:
                print "Order not found. Please search again:"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    '''Setting Attribute'''
    
    
    
    #Requests attribute to update and verifies that it is valid
    
    Attribute = (raw_input("Changing Attribute: ")).upper()
    
    #Gathers column titles from BasicOrderBook
    cursor.execute("SHOW COLUMNS FROM BasicOrderBook")
    FieldList = cursor.fetchall()
    #Iterates column names and matches entered Attribute against existing names
    for Field in FieldList:
        TargetAttribute = Field[0]
        if TargetAttribute.upper() == Attribute or Attribute == "ORDER NUMBER" or Attribute == "DATE ENTERED" or Attribute == "TRIGGER TYPE" or Attribute == "TRIGGER VALUE":
            break;
    #Retrying until valid input is given
    while TargetAttribute.upper() != Attribute and Attribute != "ORDER NUMBER" and Attribute != "DATE ENTERED" and Attribute != "TRIGGER TYPE" and Attribute != "TRIGGER VALUE":
        print "Attribute is invalid. Please enter again:"
        print "Choices: " + str([Field[0] for Field in FieldList])
        Attribute = raw_input("Changing Attribute: ")
        Attribute = Attribute.upper()
        for Field in FieldList:
            TargetAttribute = Field[0]
            if TargetAttribute.upper() == Attribute or Attribute == "ORDER NUMBER" or Attribute == "DATE ENTERED" or Attribute == "TRIGGER TYPE" or Attribute == "TRIGGER VALUE":
                    break;
    
    
    
    '''Standardizing Parameter Names'''
    
    
    
    if Attribute == "ORDERNUMBER":
        Attribute = "ORDER NUMBER"
        print "Updating: Order Number"
    
    elif Attribute == "DATEENTERED":
        Attribute = "DATE ENTERED"
        print "Updating: Date Entered"
    
    elif Attribute == "TRIGGERTYPE":
        Attribute = "TRIGGER TYPE"
        print "Updating: Trigger Type"
    
    elif Attribute == "TRIGGERVALUE":
        Attribute = "TRIGGER VALUE"
        print "Updating: Trigger Value"
    
    else:
        print "Updating: " + Attribute.title()
    
    
    
    '''Setting NewValue'''
    
    
    
    #Requesting basic input value if not a date field
    if Attribute != "DATE ENTERED":
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
                        #print DateUpdateYear
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
                        #print DateUpdateMonth
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
                        #print DateUpdateDay
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
                        #print DateUpdateHour
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
                        #print DateUpdateMinute
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
                        #print DateUpdateSecond
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
    main(OrderNumber, Attribute, NewValue)


