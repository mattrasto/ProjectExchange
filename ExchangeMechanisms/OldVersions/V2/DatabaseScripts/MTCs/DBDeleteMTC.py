#-------------------------------------------------------------------------------
# Name:        DBDeleteMTC
# Version:     2.0
# Purpose:     
#
# Author:      Matthew
#
# Created:     05/07/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    08/26/2014
#-------------------------------------------------------------------------------

#Return funds once MTC is deleted

import time
import MySQLdb
import sys


def main(MTCNumber):

    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)


    print ""
    #Exits if MTCNumber is not an integer
    if not isinstance(MTCNumber, int):
        print "CRITICAL ERROR: MTC Number not an integer"
        sys.exit()
    MTCSearch = "SELECT * FROM MTCBook WHERE MTCNumber = %d" % (MTCNumber)
    try:
        cursor.execute(MTCSearch)
        MTC = cursor.fetchone()
        #If order is found, assigns attribute values to static variables
        if MTC != None:
            print "MTC Found"
            Username = MTC[1]
            Price = MTC[2]
            Volume = MTC[3]
            Action = MTC[4]
            Type = "MTC"
            DateEntered = MTC[13]
        else:
            print "CRITICAL ERROR: MTC not found"
            sys.exit()
    except SystemExit:
        sys.exit()
    except:
        print "ERROR: Database fetch exception"



    '''Defining/Executing SQL Statement'''
    
    
    
    #Deletes contract from MTCBook
    try:
        cursor.execute("""DELETE FROM MTCBook WHERE MTCNumber = %d""" % (MTCNumber))
        db.commit()
        print ""
        print "Delete Successful"
        print ""
        print "MTC deleted:"
        print ""
        print "MTC Number: " + str(MTCNumber)
        print "Username: " + Username
        print "Type: " + Type
        print "Action: " + Action
        print "Medium: " + str(Price)
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
    FormattedDate = str(LocalTime[1]) + "/" +  str(LocalTime[2]) + "/" +  str(LocalTime[0])
    FormattedDatabaseDate = str(LocalTime[0]) + "-" +  str(LocalTime[1]) + "-" +  str(LocalTime[2])
    FormattedTime = str(LocalTime[3]) + ":" +  str(LocalTimeMinutes) + ":" +  str(LocalTimeSeconds)
    FormattedDateTime = FormattedDatabaseDate + " " + FormattedTime
    
    #Updates LoanLog with TerminationReason and TerminationDate (Current date)
    try:
        print ""
        cursor.execute("UPDATE MTCLog SET TerminationReason = %s, TerminationDate = %s WHERE MTCNumber = %s", ("Administrative Delete", FormattedDateTime, MTCNumber))
        db.commit()
        print "MTC Deletion Successfully Logged"
    except:
        print "ERROR: Database Insert Log Failure"
    
    
    
    '''Logging Control'''
        
    
    
    #Assigns static variables for logging control
    #Note: "Employee" value changes based on user submitting manual control
    Employee = "***333"
    MTCID = "MTC " + str(MTCNumber)
    Comment = "Deleted MTC"
    
    #Inserts record of action into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Delete MTC", MTCID, "All", Comment))
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
    
    

    OrderFound = False
    #Requests ContractNumber and verifies that it is valid
    while 1 == 1:
        MTCNumber = raw_input("Delete MTC Number: ")
        #Checks for integer type
        while 1 ==1:
            try:
                MTCNumber = int(MTCNumber)
                break;
            except:
                print "MTC Number must be an integer. Please enter again: "
                MTCNumber = raw_input("Delete MTC Number: ")
        try:
            #Checks if contract exists
            cursor.execute("""SELECT * FROM MTCBook WHERE MTCNumber = %d""" % (MTCNumber))
            FoundMTC = cursor.fetchone()
            if FoundMTC != None:
                break;
            else:
                print "MTC not found. Please search again:"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Execute
    main(MTCNumber)
    
    
    