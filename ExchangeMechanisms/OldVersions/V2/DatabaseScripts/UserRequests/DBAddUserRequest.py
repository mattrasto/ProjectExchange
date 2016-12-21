#-------------------------------------------------------------------------------
# Name:        DBAddUserRequest
# Version:     2.0
# Purpose:     Adds user request to specified order under specified username
#
# Author:      Matthew
#
# Created:     06/02/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/15/2014
#-------------------------------------------------------------------------------

import MySQLdb
import sys



def main(Username, ContractNumber):
    
    
    
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    
    
    '''Checking Contract Ownership'''
    
    
    
    MTCUsername = ""
    LoanUsername = ""
    
    #Searches for contract in MTCBook
    cursor.execute("""SELECT Username FROM MTCBook WHERE MTCNumber = "%s" """ % (str(ContractNumber)))
    MTCUsernames = cursor.fetchone()
    if MTCUsernames != None:
        MTCUsername = MTCUsernames[0]
    
    #Searches for contract in LoanBook
    cursor.execute("""SELECT Username FROM LoanBook WHERE ContractNumber = "%s" """ % (str(ContractNumber)))
    LoanUsernames = cursor.fetchone()
    if LoanUsernames != None:
        LoanUsername = LoanUsernames[0]
    
    #Searches for contract in PrivateTradeBook
    cursor.execute("""SELECT Username FROM PrivateTradeBook WHERE TradeNumber = "%s" """ % (str(ContractNumber)))
    PrivateTradeUsernames = cursor.fetchone()
    if PrivateTradeUsernames != None:
        PrivateTradeUsername = PrivateTradeUsernames[0]
    
    print ""
    #Exits if specified contract does not belong to specified user
    if MTCUsername != Username and LoanUsername != Username and PrivateTradeUsername:
        print "CRITICAL ERROR: Specified contract does not belong to specified username"
        sys.exit()
    else:
        print "User Owns Contract"
    
    
    
    '''Assigning Request Number'''
    
    
    
    #Gathers current highest RequestID from log and adds one
    #NOTE: Since RequestID is in format "[ContractNumber]-[RequestNumber]", the ID must be converted to string,
    #cut off after the dash, then the RequestNumber must be calculated and appended to the ID again
    
    cursor.execute("""SELECT * FROM UserRequestBook WHERE ContractNumber = %d""" % (ContractNumber))
    UserRequests = cursor.fetchall()
    #If no current request exists, sets ID to "[ContractNumber]-1"
    if UserRequests == ():
        RequestID = str(ContractNumber) + "-1"
    else:
        
        #Iterates through each RequestID, changing OldRequestNumber to reflect RequestNumber that was just compared,
        #then compares those values with newly assigned RequestID again until loop is finished
        #NOTE: This allows for skips in the log due to error, whereas counting the number of constraints and appending would not
        
        OldRequestNumber = 0
        #Gathers ConstraintNumber from each constraint
        for Request in UserRequests:
            RequestCutOff = len(str(ContractNumber)) + 1
            RequestNumber = str(Request[0])[RequestCutOff:]
            #If new ConstraintNumber is greater than the iterated ConstraintNumber, creates new ConstraintID with +1 added to ConstraintNumber
            if int(RequestNumber) > int(OldRequestNumber):
                RequestID = (str(ContractNumber) + "-" + str(int(RequestNumber) + 1))
                OldRequestNumber = RequestNumber
    
    
    
    '''Inserting User Request'''
    
    
    
    #Inserts constraint into BorrowerConstraintBook and record into BorrowerConstraintLog
    try:
        print ""
        cursor.execute("""INSERT INTO UserRequestBook(RequestID, ContractNumber, Username) VALUES("%s", %d, "%s")""" % (RequestID, ContractNumber, Username))
        db.commit()
        print "User Request Successfully Added"
    except:
        print "ERROR: User Request Unsuccessfully Added"
    
    
    
    '''Logging User Request Record'''
    
    
    
    try:
        print ""
        cursor.execute("""INSERT INTO UserRequestLog(RequestID, ContractNumber, Username) VALUES("%s", %d, "%s")""" % (RequestID, ContractNumber, Username))
        db.commit()
        print "User Request Successfully Logged"
    except:
        print "ERROR: User Request Unsuccessfully Logged"
        
    
    
    #Gathers contract type
    cursor.execute("""SELECT * FROM IDBook WHERE IDNumber = %d""" % (ContractNumber))
    Contract = cursor.fetchall()
    ContractType = Contract[0][2]
    
    try:
        #If type is MTC, updates MTCBook record of contract to reflect change in request amount
        if ContractType.upper() == "MTC":
            cursor.execute("""UPDATE MTCBook SET UserRequests = (UserRequests + 1) WHERE MTCNumber = %s""" % (ContractNumber))
            db.commit()
        #If type is Loan, updates LoanBook record of contract to reflect change in request amount
        elif ContractType.upper() == "LOAN":
            cursor.execute("""UPDATE LoanBook SET UserRequests = (UserRequests + 1) WHERE ContractNumber = %s""" % (ContractNumber))
            db.commit()
        #If type is Private Trade, updates PrivateTradeBook record of contract to reflect change in request amount
        elif ContractType.upper() == "PRIVATE TRADE":
            cursor.execute("""UPDATE PrivateTradeBook SET UserRequests = (UserRequests + 1) WHERE TradeNumber = %s""" % (ContractNumber))
            db.commit()
        print "Request Value Successfully Updated"
    except:
        print "ERROR: Request Value Unsuccessfully Updated"
    
    
    
    '''Logging Control'''
        
    
    
    #Assigns static variables for logging control
    #Note: "Employee" value changes based on user submitting manual control
    Employee = "***333"
    RequestID = "Request " + str(RequestID)
    ContractNumber = "Contract " + str(ContractNumber)
    Comment = "Added User Request"
    
    
    
    #Inserts record of request addition into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Add User Request", RequestID, "All", Comment))
        db.commit()
        print "Control Successfully Logged"
    except:
        print "ERROR: Control Unsuccessfully Logged"
    
    
    
    #Inserts record of request amount update into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update User Request Amount", ContractNumber, "UserRequests", Comment))
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
    
    
    
    #Requests Username to put request under and verifies that it is valid
    Username = raw_input("Username: ")
    Username = Username.capitalize()
    UserFound = False
    while UserFound != True:
        cursor.execute("""SELECT * FROM UserBook WHERE Username = "%s" """ % (Username))
        UsernameList = cursor.fetchall()
        for User in UsernameList:
            if Username == User[0]:
                print "User found"
                UserFound = True
                break;
        else:
            print "User not found. Please enter again: "
            Username = raw_input("Username: ")
            Username = Username.capitalize()
    
    
    
    #Requests ContractNumber to assign constraint to and verifies that it is valid
    ContractFound = False
    while ContractFound != True:
        ContractNumber = raw_input("Contract Number: ")
        #Checks for integer type
        while 1 == 1:
            try:
                ContractNumber = int(ContractNumber)
                break;
            except:
                print "Contract Number must be an integer. Please enter again: "
                ContractNumber = raw_input("Contract Number: ")
        #Searches IDBook for a contract with specified ContractNumber
        cursor.execute("""SELECT * FROM IDBook WHERE IDNumber = "%s" """ % (ContractNumber))
        ContractList = cursor.fetchall()
        #If list is not empty, iterates list and checks owner of each loan, then compares values to ensure specified Username owns specified contract
        if ContractList != ():
            for Contract in ContractList:
                if ContractNumber == Contract[0]:
                    ContractType = Contract[1]
                    
                    #Searches MTCBook for Username of specified contract
                    cursor.execute("""SELECT Username FROM MTCBook WHERE MTCNumber = %d""" % (ContractNumber))
                    MTCUsername = cursor.fetchone()
                    
                    #Searches LoanBook for Username of specified contract
                    cursor.execute("""SELECT Username FROM LoanBook WHERE ContractNumber = %d""" % (ContractNumber))
                    LoanUsername = cursor.fetchone()
                    
                    #Searches PrivateTradeBook for Username of specified contract
                    cursor.execute("""SELECT Username FROM PrivateTradeBook WHERE ContractNumber = %d""" % (ContractNumber))
                    PrivateTradeUsername = cursor.fetchone()
                    
                    #If neither book has contract under specified username, retries input
                    if MTCUsername == None and LoanUsername == None and PrivateTradeUsername:
                        print "Specified contract does not belong to specified username. Please enter again:"
                    else:
                        print "Contract found"
                        ContractFound = True;
                        break;
        #If IDBook has no contract with specified ContractNumber, retries input
        else:
            print "Contract not found. Please enter again: "
    
    
    
    #Execute
    main(Username, ContractNumber)


