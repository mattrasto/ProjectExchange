#-------------------------------------------------------------------------------
# Name:        DBDeletePrivateTrade
# Version:     3.0
# Purpose:     Deletes specified Private Trade
#
# Author:      Matthew
#
# Created:     06/01/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/15/2014
#-------------------------------------------------------------------------------

#Return funds once trade is deleted

import MySQLdb
import time
import sys



def main(TradeNumber):

    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)



    '''Gathering Trade Details'''
    
    
    
    print ""
    #Exits if OrderNumber is not an integer
    if not isinstance(TradeNumber, int):
        print "CRITICAL ERROR: Trade Number not an integer"
        sys.exit()
    TradeSearch = "SELECT * FROM PrivateTradeBook WHERE TradeNumber = %d" % (TradeNumber)
    try:
        cursor.execute(TradeSearch)
        Trade = cursor.fetchone()
        #If order is found, assigns attribute values to static variables
        if Trade != None:
            print "Private Trade Found"
            Username = Trade[1]
            Price = Trade[2]
            Volume = Trade[3]
            Action = Trade[4]
            Type = "Private Trade"
            DateEntered = Trade[6]
        else:
            print "CRITICAL ERROR: Trade not found"
            sys.exit()
    except SystemExit:
        sys.exit()
    except:
        print "ERROR: Database fetch exception"
    
    
    
    '''Defining/Executing SQL Statement'''
    
    
    
    #Deletes order from PrivateTradeBook
    try:
        cursor.execute("""DELETE FROM PrivateTradeBook WHERE TradeNumber = %d""" % (TradeNumber))
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
    FormattedDateTime = FormattedDate + " " + FormattedTime
    
    print ""
    try:
        #Updates BasicOrderLog with TerminationReason and TerminationDate (Current date)
        cursor.execute("UPDATE PrivateTradeLog SET TerminationReason = %s, TerminationDate = %s WHERE TradeNumber = %s", ("Administrative Delete", FormattedDateTime, TradeNumber))
        db.commit()
        print "Trade Deletion Successfully Logged"
    except:
        print "ERROR: Database Insert Log Failure"
    
    
    
    '''Logging Control'''
        
    
    
    #Assigns static variables for logging control
    #Note: "Employee" value changes based on user submitting manual control
    Employee = "***333"
    TradeID = "Trade " + str(TradeNumber)
    Comment = "Deleted Private Trade"
    
    #Inserts record of action into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Delete Private Trade", TradeID, "All", Comment))
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
    
    
    
    #Requests TradeNumber and verifies that it is valid
    while 1 == 1:
        TradeNumber = raw_input("Delete Trade Number: ")
        #Checks for integer type
        while 1 ==1:
            try:
                TradeNumber = int(TradeNumber)
                break;
            except:
                print "Trade Number must be an integer. Please enter again: "
                TradeNumber = raw_input("Trade Number: ")
        try:
            #Checks if trade exists
            cursor.execute("""SELECT * FROM PrivateTradeBook WHERE TradeNumber = %d""" % (TradeNumber))
            FoundTrade = cursor.fetchone()
            if FoundTrade != None:
                #print Trade
                Username = Trade[1]
                Price = Trade[2]
                Volume = Trade[3]
                Action = Trade[4]
                DateEntered = Trade[6]
                break;
            else:
                print "Trade not found. Please search again:"
        except:
            print "ERROR: Database fetch exception"
            break;
    
    
    
    #Execute
    main(TradeNumber)


