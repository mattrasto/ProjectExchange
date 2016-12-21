#-------------------------------------------------------------------------------
# Name:        DBDeleteLoan
# Version:     3.0
# Purpose:     Deletes specified Loan
#
# Author:      Matthew
#
# Created:     05/29/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    10/04/2014
#-------------------------------------------------------------------------------

#Return funds once loan is deleted

import time
import MySQLdb
import sys



def main(ContractNumber):
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    
    
    '''Gathering Contract Details'''
    
    
    
    print ""
    #Exits if ContractNumber is not an integer
    if not isinstance(ContractNumber, int):
        print "CRITICAL ERROR: Contract Number not an integer"
        sys.exit()
    ContractSearch = "SELECT * FROM LoanBook WHERE ContractNumber = %d" % (ContractNumber)
    try:
        cursor.execute(ContractSearch)
        Contract = cursor.fetchone()
        #If order is found, assigns attribute values to static variables
        if Contract != None:
            print "Contract Found"
            Username = Contract[1]
            Price = Contract[2]
            Volume = Contract[3]
            Action = Contract[4]
            Type = "Loan"
            DateEntered = Contract[12]
        else:
            print "CRITICAL ERROR: Contract not found"
            sys.exit()
    except SystemExit:
        sys.exit()
    except:
        print "ERROR: Database fetch exception"
    
    
    
    '''Defining/Executing SQL Statement'''
    
    
    
    #Deletes contract from LoanBook
    try:
        cursor.execute("""DELETE FROM LoanBook WHERE ContractNumber = %d""" % (ContractNumber))
        db.commit()
        print ""
        print "Delete Successful"
        print ""
        print "Contract deleted:"
        print ""
        print "Contract Number: " + str(ContractNumber)
        print "Username: " + str(Username)
        print "Type: " + str(Type)
        print "Action: " + str(Action)
        print "Price: " + str(Price)
        print "Volume: " + str(Volume)
        print "Date Entered: " + str(DateEntered)
    except:
        db.rollback()
        print ""
        print "Delete Unsuccessful"
    
    
    
    '''Logging Contract Termination'''
    
    
    
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
        cursor.execute("UPDATE LoanLog SET TerminationReason = %s, TerminationDate = %s WHERE ContractNumber = %s", ("Administrative Delete", FormattedDateTime, ContractNumber))
        db.commit()
        print "Contract Deletion Successfully Logged"
    except:
        print "ERROR: Database Insert Log Failure"
    
    
    
    '''Logging Control'''
        
    
    
    #Assigns static variables for logging control
    #Note: "Employee" value changes based on user submitting manual control
    Employee = "***333"
    ContractID = "Loan " + str(ContractNumber)
    Comment = "Deleted Loan"
    
    #Inserts record of action into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Delete MTC", ContractID, "All", Comment))
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
    
    
    
    #Requests ContractNumber and verifies that it is valid
    while 1 == 1:
        ContractNumber = raw_input("Delete Contract Number: ")
        #Checks for integer type
        while 1 == 1:
            try:
                ContractNumber = int(ContractNumber)
                break;
            except:
                print "Contract Number must be an integer. Please enter again: "
                ContractNumber = raw_input("Delete Contract Number: ")
        try:
            #Checks if contract exists
            cursor.execute("""SELECT * FROM LoanBook WHERE ContractNumber = %d""" % (ContractNumber))
            FoundContract = cursor.fetchone()
            if FoundContract != None:
                break;
            else:
                print "Contract not found. Please search again:"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Execute
    main(ContractNumber)


