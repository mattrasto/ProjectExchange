#-------------------------------------------------------------------------------
# Name:        DBDeleteBasicOrder
# Version:     1.0
# Purpose:
#
# Author:      Matthew
#
# Created:     05/17/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    05/29/2014
#-------------------------------------------------------------------------------

import MySQLdb
import time

db = MySQLdb.connect("localhost","root","***","exchangedatabase")

cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data



'''Setting Variables'''



OrderFound = False
while 1 == 1:
    OrderNumber = raw_input("Delete Order Number: ")
    while 1 ==1:
        try:
            OrderNumber = int(OrderNumber)
            break;
        except:
            print "Order Number must be an integer. Please enter again: "
            OrderNumber = raw_input("Order Number: ")
    OrderSearch = "SELECT * FROM BasicOrderBook WHERE OrderNumber = %d" % (OrderNumber)
    try:
        cursor.execute(OrderSearch)
        FoundOrder = cursor.fetchall()
        #print "Order found"
        #print "FoundOrder: " + str(FoundOrder)
        if FoundOrder != ():
            OrderFound = True
            for Order in FoundOrder:
                #print Order
                Username = Order[1]
                Price = Order[2]
                Volume = Order[3]
                Type = Order[4]
                Action = Order[5]
                if Type.upper() == "CONDITIONAL":
                    TriggerType = Order[6]
                    TriggerValue = Order[7]
                DateEntered = Order[8]
                break;
        else:
            print "Order not found. Please search again:"
        if OrderFound == True:
            break;
    except:
        print "ERROR: Database fetch exception"
        break;



print ""
Comment = raw_input("Administrative Comment: ")



'''Defining/Executing SQL Statement'''



sql = """DELETE FROM BasicOrderBook WHERE OrderNumber = %d""" % (OrderNumber)

try:
    cursor.execute(sql)
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



LocalTime = time.localtime(time.time())
LocalTimeMinutes = LocalTime[4]
LocalTimeSeconds = LocalTime[5]
if LocalTimeMinutes < 10:
    LocalTimeMinutes = "0" + str(LocalTimeMinutes)
if LocalTimeSeconds < 10:
    LocalTimeSeconds = "0" + str(LocalTimeSeconds)
FormattedDate = str(LocalTime[1]) + "/" +  str(LocalTime[2]) + "/" +  str(LocalTime[0])
FormattedDatabaseDate = str(LocalTime[0]) + "-" +  str(LocalTime[1]) + "-" +  str(LocalTime[2])
FormattedTime = str(LocalTime[3]) + ":" +  str(LocalTimeMinutes) + ":" +  str(LocalTimeSeconds)
FormattedDateTime = FormattedDatabaseDate + " " + FormattedTime
print FormattedDateTime

print ""
try:
    cursor.execute("UPDATE BasicOrderLog SET TerminationReason = %s, TerminationDate = %s WHERE OrderNumber = %s", ("Administrative Delete", FormattedDateTime, OrderNumber))
    db.commit()
    print "Order Deletion Successfully Logged"
except:
    print "ERROR: Database Insert Log Failure"



'''Logging Control'''
    


Employee = "***333"

OrderID = "Order " + str(OrderNumber)

try:
    print ""
    cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Delete Basic Order", OrderID, "All", Comment))
    db.commit()
    print "Control Successfully Logged"
except:
    print "ERROR: Control Unsuccessfully Logged"



db.close()