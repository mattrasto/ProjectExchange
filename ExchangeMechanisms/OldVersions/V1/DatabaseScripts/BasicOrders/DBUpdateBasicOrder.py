#-------------------------------------------------------------------------------
# Name:        DBUpdateBasicOrder
# Version:     1.0
# Purpose:
#
# Author:      Matthew
#
# Created:     05/21/2014
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



OrderNumber = raw_input("Modified Order: ")
while 1 == 1:
    try:
        OrderNumber = int(OrderNumber)
        break;
    except:
        print "You must enter a number:"
        OrderNumber = raw_input("Modified Order: ")

OrderFound = False
try:
    while OrderFound != True:
        print OrderNumber
        cursor.execute("""SELECT * FROM BasicOrderBook WHERE OrderNumber = %s""" % (OrderNumber))
        FoundOrder = cursor.fetchall()
        if FoundOrder != ():
            print "Order found"
            print "FoundOrder: " + str(FoundOrder)
            OrderFound = True
            for Order in FoundOrder:
                print Order
                Username = Order[1]
                Price = Order[2]
                Volume = Order[3]
                Type = Order[4]
                Action = Order[5]
                if Type.upper() == "CONDITIONAL":
                    TriggerType = Order[6]
                    TriggerValue = Order[7]
                DateEntered = Order[8]
        else:
            print "Order not found. Please enter again: "
            OrderNumber = raw_input("Modified Order: ")
            while 1 == 1:
                try:
                    OrderNumber = int(OrderNumber)
                    break;
                except:
                    print "You must enter a number:"
                    OrderNumber = raw_input("Modified Order: ")
except:
    print "Order not found"

if OrderFound == True:
    Attribute = raw_input("Changing Attribute: ")
    Attribute = Attribute.upper()
    
    cursor.execute("SELECT * FROM BasicOrderBook WHERE OrderNumber = %s" % (OrderNumber))
    OrderBookOrders = cursor.fetchall()
    for Header in cursor.description:
        TargetAttribute = Header[0]
        if TargetAttribute.upper() == Attribute or Attribute == "ORDER NUMBER" or Attribute == "DATE ENTERED" or Attribute == "TRIGGER TYPE" or Attribute == "TRIGGER VALUE":
            break;
    while TargetAttribute.upper() != Attribute and Attribute != "ORDER NUMBER" and Attribute != "DATE ENTERED" and Attribute != "TRIGGER TYPE" and Attribute != "TRIGGER VALUE":
        print "Attribute is invalid. Please enter again:"
        print "Choices: " + str([Header[0] for Header in cursor.description])
        Attribute = raw_input("Changing Attribute: ")
        Attribute = Attribute.upper()
        for Header in cursor.description:
            TargetAttribute = Header[0]
            if TargetAttribute.upper() == Attribute or Attribute == "ORDER NUMBER" or Attribute == "DATE ENTERED" or Attribute == "TRIGGER TYPE" or Attribute == "TRIGGER VALUE":
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
    
    if Attribute == "ORDERNUMBER" or Attribute == "ORDER NUMBER":
        NewValue = int(NewValue)
        try:
            cursor.execute("UPDATE BasicOrderBook SET OrderNumber = %d WHERE OrderNumber = %d" % (NewValue, OrderNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Order modified: " + str(OrderNumber)
            print "Attribute modified: Order Number"
            print "New value: " + str(NewValue)
            UpdateComplete = True
        except:
            db.rollback()
            cursor.execute("SELECT * FROM BasicOrderBook WHERE OrderNumber = %d" % (NewValue))
            ExistingOrders = cursor.fetchall()
            if ExistingOrders != ():
                print "Order number is already in use:"
                print ""
                print ExistingOrders
            else:
                print "Update Unsuccessful"
        
    if Attribute == "USERNAME":
        NewValue = str(NewValue.capitalize())
        try:
            cursor.execute("SELECT * FROM BasicOrderBook WHERE OrderNumber = %d" % (OrderNumber))
            OrderBookOrders = cursor.fetchall()
            cursor.execute("""UPDATE BasicOrderBook SET Username = "%s" WHERE OrderNumber = %d""" % (NewValue, OrderNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Order modified: " + str(OrderNumber)
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
            cursor.execute("SELECT * FROM BasicOrderBook WHERE OrderNumber = %d" % (OrderNumber))
            OrderBookOrders = cursor.fetchall()
            cursor.execute("UPDATE BasicOrderBook SET Price = %f WHERE OrderNumber = %d" % (NewValue, OrderNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Order modified: " + str(OrderNumber)
            print "Attribute modified: Price"
            print "New value: " + str(NewValue)
            UpdateComplete = True
        except:
            db.rollback()
            print "Update Unsuccessful"
        
    if Attribute == "VOLUME":
        NewValue = float(NewValue)
        try:
            cursor.execute("SELECT * FROM BasicOrderBook WHERE OrderNumber = %d" % (OrderNumber))
            OrderBookOrders = cursor.fetchall()
            cursor.execute("UPDATE BasicOrderBook SET Volume = %f WHERE OrderNumber = %d" % (NewValue, OrderNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Order modified: " + str(OrderNumber)
            print "Attribute modified: Volume"
            print "New value: " + str(NewValue)
            UpdateComplete = True
        except:
            db.rollback()
            print "Update Unsuccessful"
    
    if Attribute == "TYPE":
        NewValue = str(NewValue)
        try:
            cursor.execute("SELECT * FROM BasicOrderBook WHERE OrderNumber = %d" % (OrderNumber))
            OrderBookOrders = cursor.fetchall()
            cursor.execute("""UPDATE BasicOrderBook SET Type = "%s" WHERE OrderNumber = %d""" % (NewValue, OrderNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "User modified: " + str(OrderNumber)
            print "Attribute modified: Type"
            print "New value: " + str(NewValue)
            UpdateComplete = True
        except:
            db.rollback()
            print "Update Unsuccessful"
    
    if Attribute == "ACTION":
        NewValue = str(NewValue)
        try:
            cursor.execute("SELECT * FROM BasicOrderBook WHERE OrderNumber = %d" % (OrderNumber))
            OrderBookOrders = cursor.fetchall()
            cursor.execute("""UPDATE BasicOrderBook SET Action = "%s" WHERE OrderNumber = %d""" % (NewValue, OrderNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Order modified: " + str(OrderNumber)
            print "Attribute modified: Action"
            print "New value: " + str(NewValue)
            UpdateComplete = True
        except:
            db.rollback()
            print "Update Unsuccessful"
    
    if Attribute == "TRIGGERTYPE" or Attribute == "TRIGGER TYPE":
        NewValue = str(NewValue)
        try:
            cursor.execute("SELECT * FROM BasicOrderBook WHERE OrderNumber = %d" % (OrderNumber))
            OrderBookOrders = cursor.fetchall()
            cursor.execute("""UPDATE BasicOrderBook SET TriggerType = "%s" WHERE OrderNumber = %d""" % (NewValue, OrderNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Order modified: " + str(OrderNumber)
            print "Attribute modified: Trigger Type"
            print "New value: " + str(NewValue)
            UpdateComplete = True
        except:
            db.rollback()
            print "Update Unsuccessful"
    
    if Attribute == "TRIGGERVALUE" or Attribute == "TRIGGER VALUE":
        NewValue = float(NewValue)
        try:
            cursor.execute("SELECT * FROM BasicOrderBook WHERE OrderNumber = %d" % (OrderNumber))
            OrderBookOrders = cursor.fetchall()
            cursor.execute("UPDATE BasicOrderBook SET TriggerValue = %f WHERE OrderNumber = %d" % (NewValue, OrderNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Order modified: " + str(OrderNumber)
            print "Attribute modified: Trigger Value"
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
            cursor.execute("SELECT * FROM BasicOrderBook WHERE OrderNumber = %d" % (OrderNumber))
            BasicOrderBookOrders = cursor.fetchall()
        except:
            print "ERROR: Database fetch exception"
    
        for Order in BasicOrderBookOrders:
            print Order
            
            if DateSearchYearOmit == True:
                YearValue = ""
                #print Order[8]
                for Character in str(Order[8])[:4]:
                    YearValue += str(Character)
                Year = YearValue
            
            if DateSearchMonthOmit == True:
                MonthValue = ""
                #print Order[8]
                for Character in str(Order[8])[5:7]:
                    MonthValue += str(Character)
                Month = MonthValue
                
            if DateSearchDayOmit == True:
                DayValue = ""
                #print Order[8]
                for Character in str(Order[8])[8:10]:
                    DayValue += str(Character)
                Day = DayValue
                
            if DateSearchHourOmit == True:
                HourValue = ""
                #print Order[8]
                for Character in str(Order[8])[11:13]:
                    HourValue += str(Character)
                Hour = HourValue
                
            if DateSearchMinuteOmit == True:
                MinuteValue = ""
                #print Order[8]
                for Character in str(Order[8])[14:16]:
                    MinuteValue += str(Character)
                Minute = MinuteValue
            
            if DateSearchSecondOmit == True:
                SecondValue = ""
                #print Order[8]
                for Character in str(Order[8])[17:19]:
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
            cursor.execute("SELECT * FROM BasicOrderBook WHERE OrderNumber = %d" % (OrderNumber))
            OrderBookOrders = cursor.fetchall()
            cursor.execute("""UPDATE BasicOrderBook SET DateEntered = "%s" WHERE OrderNumber = %d""" % (FormattedDateTime, OrderNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Order modified: " + str(OrderNumber)
            print "Attribute modified: Date Entered"
            print "New value: " + str(FormattedDateTime)
            UpdateComplete = True
        except:
            db.rollback()
            print "Update Unsuccessful"



    '''Logging Control'''
    
    
    
    if UpdateComplete == True:
        Employee = "***333"
        
        OrderID = "Order " + str(OrderNumber)
        
        try:
            print ""
            cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update Basic Order", OrderID, Attribute.title(), Comment))
            db.commit()
            print "Control Successfully Logged"
        except:
            print "ERROR: Control Unsuccessfully Logged"



db.close()