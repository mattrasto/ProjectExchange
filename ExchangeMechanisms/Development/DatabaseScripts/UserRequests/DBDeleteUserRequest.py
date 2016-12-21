#-------------------------------------------------------------------------------
# Name:        DBDeleteUserRequest
# Version:     3.0
# Purpose:     Deletes specified User Request
#
# Author:      Matthew
#
# Created:     06/02/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    06/26/2014
#-------------------------------------------------------------------------------

import MySQLdb
import sys



def main(ContractNumber, RequestID):

    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    
    
    '''Gathering User Request Details'''
    
    
    
    try:
        print ""
        cursor.execute("""SELECT * FROM UserRequestBook WHERE RequestID = "%s" """ % (RequestID))
        Request = cursor.fetchone()
        #If contract is found, assigns attribute values to static variables
        if Request != None:
            print "Request Found"
            Username = Request[2]
            RequestDate = Request[3]
            RequestStatus = Request[4]
        else:
            print "CRITICAL ERROR: Request not found"
            sys.exit()
    except SystemExit:
        sys.exit()
    except:
        print "ERROR: Database fetch exception"
    
    
    
    '''Defining/Executing SQL Statements'''
    
    
    
    #Deletes request from BorrowerConstraintBook
    try:
        cursor.execute("""DELETE FROM UserRequestBook WHERE RequestID = "%s" """ % (RequestID))
        db.commit()
        print ""
        print "Delete Successful"
        print ""
        print "Request deleted:"
        print ""
        print "Request ID: " + str(RequestID)
        print "Contract Number: " + str(ContractNumber)
        print "Username: " + str(Username)
    except:
        db.rollback()
        print ""
        print "Delete Unsuccessful"
    
    
    
    '''Updating User Request Amount'''
    
    
    
    #Gathers contract type
    cursor.execute("""SELECT Type FROM IDBook WHERE IDNumber = %d""" % (ContractNumber))
    ContractType = cursor.fetchone()
    if ContractType != None:
        ContractType =  ContractType[0]
    else:
        print "CRITICAL ERROR: Contract has no type"
        sys.exit()
    
    
    
    #Updates contract in MTCBook to reflect change in request amount
    if ContractType.upper() == "MTC":
        try:
            cursor.execute("""UPDATE MTCBook SET UserRequests = (UserRequests - 1) WHERE MTCNumber = %s""" % (ContractNumber))
            db.commit()
            print ""
            print "User Requests Successfully Updated"
        except:
            print "User Requests Unsuccessfully Updated"
    
    
    
    #Updates contract in LoanBook to reflect change in request amount
    elif ContractType.upper() == "LOAN":
        try:
            cursor.execute("""UPDATE LoanBook SET UserRequests = (UserRequests - 1) WHERE ContractNumber = %s""" % (ContractNumber))
            db.commit()
            print ""
            print "User Requests Successfully Updated"
        except:
            print "User Requests Unsuccessfully Updated"
    
    
    
    #Updates contract in PrivateTradeBook to reflect change in request amount
    elif ContractType.upper() == "PRIVATE TRADE":
        try:
            cursor.execute("""UPDATE PrivateTradeBook SET UserRequests = (UserRequests - 1) WHERE TradeNumber = %s""" % (ContractNumber))
            db.commit()
            print ""
            print "User Requests Successfully Updated"
        except:
            print "User Requests Unsuccessfully Updated"
    
    
    
    '''Logging Control'''
        
    
    
    #Assigns static variables for logging control
    #Note: "Employee" value changes based on user submitting manual control
    Employee = "***333"
    RequestID = "Request " + str(RequestID)
    ContractNumber = "Contract " + str(ContractNumber)
    Comment = "Deleted User Request"
    
    
    
    #Inserts record of user request deletion into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Delete User Request", RequestID, "All", Comment))
        db.commit()
        print "Control Successfully Logged"
    except:
        print "ERROR: Control Unsuccessfully Logged"
    
    
    
    #Inserts record of request amount update into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update Request Amount", ContractNumber, "UserRequests", Comment))
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



    '''Setting Variables'''
    
    
    
    #Requests ContractNumber and verifies that it is valid
    OrderFound = False
    while 1 == 1:
        ContractNumber = raw_input("Contract Number: ")
        #Checks for integer type
        while 1 == 1:
            try:
                ContractNumber = int(ContractNumber)
                break;
            except:
                print "Contract Number must be an integer. Please enter again: "
                ContractNumber = raw_input("Contract Number: ")
        try:
            #Checks if order exists
            cursor.execute("""SELECT * FROM IDBook WHERE IDNumber = "%s" """ % (ContractNumber))
            ContractList = cursor.fetchall()
            for Contract in ContractList:
                if ContractNumber == Contract[0]:
                    print "Contract found"
                    OrderFound = True
                    break;
            else:
                print "Contract not found. Please enter again: "
            if OrderFound == True:
                break;
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Requests RequestNumber
    RequestNumber = raw_input("Delete Request Number: ")
    #Creates RequestID by concatenating "-[RequestNumber]" to RequestNumber
    RequestID = str(ContractNumber) + "-" + str(RequestNumber)
    while 1 == 1:
        #Verifies that request exists
        try:
            cursor.execute("""SELECT * FROM UserRequestBook WHERE RequestID = "%s" """ % (RequestID))
            RequestEntry = cursor.fetchall()[0]
            RequestID = RequestEntry[0]
            ContractNumber = RequestEntry[1]
            Username = RequestEntry[2]
            print "Request ID Found: " + str(RequestID)
            break;
        except:
            print "Request not found. Please enter again: "
            RequestNumber = raw_input("Delete Request Number: ")
            RequestID = str(ContractNumber) + "-" + str(RequestNumber)
    print ""
    
    
    
    #Execute
    main(ContractNumber, RequestID)


