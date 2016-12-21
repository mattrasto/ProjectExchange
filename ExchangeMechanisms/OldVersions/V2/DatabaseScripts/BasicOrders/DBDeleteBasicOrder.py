#-------------------------------------------------------------------------------
# Name:        DBDeleteBasicOrder
# Version:     2.0
# Purpose:
#
# Author:      Matthew
#
# Created:     05/17/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    08/26/2014
#-------------------------------------------------------------------------------

#Return funds once order is deleted

import MySQLdb
import time
import sys



def main(OrderNumber):
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    
    
    '''Gathering Order Details'''
    
    
    
    print ""
    #Exits if OrderNumber is not an integer
    if not isinstance(OrderNumber, int):
        print "CRITICAL ERROR: Order Number not an integer"
        sys.exit()
    OrderSearch = "SELECT * FROM BasicOrderBook WHERE OrderNumber = %d" % (OrderNumber)
    try:
        cursor.execute(OrderSearch)
        Order = cursor.fetchone()
        #If order is found, assigns attribute values to static variables
        if Order != None:
            print "Order Found"
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
            print "CRITICAL ERROR: Order not found"
            sys.exit()
    except SystemExit:
        sys.exit()
    except:
        print "ERROR: Database fetch exception"
    
    
    
    '''Defining/Executing SQL Statement'''
    
    
    
    #Deletes order from BasicOrderBook
    try:
        cursor.execute("""DELETE FROM BasicOrderBook WHERE OrderNumber = %d""" % (OrderNumber))
        db.commit()
        print ""
        print "Delete Successful"
        print ""
        print "Order deleted:"
        print ""
        print "Order Number: " + str(OrderNumber)
        print "Type: " + Type
        print "Action: " + Action
        print "Username: " + Username
        print "Price: " + str(Price)
        print "Volume: " + str(Volume)
        if Type.upper() == "CONDITIONAL":
            print "Trigger Type: " + str(TriggerType)
            print "Trigger Value: " + str(TriggerValue)
        print "Date Entered: " + str(DateEntered)
    except:
        db.rollback()
        print ""
        print "Delete Unsuccessful"
    
    
    
    '''Logging Order Termination'''
    
    
    
    #Gets current time and formats for database insertion
    LocalTime = time.localtime(time.time())
    LocalTimeMinutes = LocalTime[4]
    LocalTimeSeconds = LocalTime[5]
    if LocalTimeMinutes < 10:
        LocalTimeMinutes = "0" + str(LocalTimeMinutes)
    if LocalTimeSeconds < 10:
        LocalTimeSeconds = "0" + str(LocalTimeSeconds)
    FormattedDate = str(LocalTime[0]) + "-" +  str(LocalTime[1]) + "-" +  str(LocalTime[2])
    FormattedTime = str(LocalTime[3]) + ":" +  str(LocalTimeMinutes) + ":" +  str(LocalTimeSeconds)
    TerminationDate = FormattedDate + " " + FormattedTime
    
    try:
        print ""
        #Updates BasicOrderLog with TerminationReason and TerminationDate (Current date)
        cursor.execute("UPDATE BasicOrderLog SET TerminationReason = %s, TerminationDate = %s WHERE OrderNumber = %s", ("Administrative Delete", TerminationDate, OrderNumber))
        db.commit()
        print "Order Deletion Successfully Logged"
    except:
        print "ERROR: Database Insert Log Failure"
    
    
    
    '''Logging Control'''
    
    
    
    #Assigns static variables for logging control
    #Note: "Employee" value changes based on user submitting manual control
    Employee = "***333"
    OrderID = "Order " + str(OrderNumber)
    Comment = "Deleted User"
    
    #Inserts record of action into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Delete Basic Order", OrderID, "All", Comment))
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
    
    
    
    #Requests OrderNumber and verifies that it is valid
    OrderFound = False
    while 1 == 1:
        OrderNumber = raw_input("Delete Order Number: ")
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
    
    
    
    #Execute
    main(OrderNumber)


