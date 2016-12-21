#-------------------------------------------------------------------------------
# Name:        DBDeletePrivateTrade
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
import time

db = MySQLdb.connect("localhost","root","***","exchangedatabase")

cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data



'''Setting Variables'''



TradeFound = False
while 1 == 1:
    TradeNumber = raw_input("Delete Trade Number: ")
    while 1 ==1:
        try:
            TradeNumber = int(TradeNumber)
            break;
        except:
            print "Trade Number must be an integer. Please enter again: "
            TradeNumber = raw_input("Trade Number: ")
    TradeSearch = "SELECT * FROM PrivateTradeBook WHERE TradeNumber = %d" % (TradeNumber)
    try:
        cursor.execute(TradeSearch)
        FoundTrade = cursor.fetchall()
        #print "Trade found"
        #print "FoundTrade: " + str(FoundTrade)
        if FoundTrade != ():
            TradeFound = True
            for Trade in FoundTrade:
                #print Trade
                Username = Trade[1]
                Price = Trade[2]
                Volume = Trade[3]
                Action = Trade[4]
                DateEntered = Trade[6]
                break;
        else:
            print "Trade not found. Please search again:"
        if TradeFound == True:
            break;
    except:
        print "ERROR: Database fetch exception"
        break;



print ""
Comment = raw_input("Administrative Comment: ")



'''Defining/Executing SQL Statement'''



sql = """DELETE FROM PrivateTradeBook WHERE TradeNumber = %d""" % (TradeNumber)

try:
    cursor.execute(sql)
    db.commit()
    print ""
    print "Delete Successful"
    print ""
    print "Trade deleted:"
    print ""
    print "Trade Number: " + str(TradeNumber)
    print "Action: " + Action
    print "Username: " + Username
    print "Price: " + str(Price)
    print "Volume: " + str(Volume)
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
    cursor.execute("UPDATE PrivateTradeLog SET TerminationReason = %s, TerminationDate = %s WHERE TradeNumber = %s", ("Administrative Delete", FormattedDateTime, TradeNumber))
    db.commit()
    print "Trade Deletion Successfully Logged"
except:
    print "ERROR: Database Insert Log Failure"



'''Logging Control'''
    


Employee = "***333"

TradeID = "Trade " + str(TradeNumber)

try:
    print ""
    cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Delete Private Trade", TradeID, "All", Comment))
    db.commit()
    print "Control Successfully Logged"
except:
    print "ERROR: Control Unsuccessfully Logged"



db.close()