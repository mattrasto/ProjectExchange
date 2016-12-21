#-------------------------------------------------------------------------------
# Name:        DBAddBorrowerConstraint
# Version:     3.0
# Purpose:     Adds Minimum Borrower Constraint to specified order with specified constraints
#
# Author:      Matthew
#
# Created:     05/14/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    08/26/2014
#-------------------------------------------------------------------------------

import MySQLdb
import sys

def main(Username, ContractNumber, MinimumBorrowerConstraintType, MinimumBorrowerConstraintValue):
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()
    print "Database Version: " + str(Data[0])
    
    
    
    '''Checking Contract Ownership'''
    
    
    
    MTCUsername = ""
    LoanUsername = ""
    PrivateTradeUsername = ""
    
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
    if MTCUsername != Username and LoanUsername != Username and PrivateTradeUsername != Username:
        print "CRITICAL ERROR: Specified contract does not belong to specified username"
        sys.exit()
    else:
        print "User Owns Contract"
    
    
    
    '''Defining ConstraintID'''
    
    
    
    #Gathers current highest ConstraintID from log and adds one
    #NOTE: Since ConstraintID is in format "[ContractNumber]-[ConstraintNumber]", the ID must be converted to string,
    #cut off after the dash, then the ConstraintNumber must be calculated and appended to the ID again
    
    cursor.execute("""SELECT * FROM BorrowerConstraintLog WHERE ContractNumber = %s""" % (ContractNumber))
    BorrowerConstraintBookConstraints = cursor.fetchall()
    #If no current constraints exists, sets ID to "[ContractNumber]-1"
    if BorrowerConstraintBookConstraints == ():
        ConstraintID = str(ContractNumber) + "-1"
    else:
        
        #Iterates through each ConstraintID, changing OldConstraintNumber to reflect ConstraintNumber that was just compared,
        #then compares those values with newly assigned ConstraintID again until loop is finished
        #NOTE: This allows for skips in the log due to error, whereas counting the number of constraints and appending would not
        
        OldConstraintNumber = 0
        #Gathers ConstraintNumber from each constraint
        for Constraint in BorrowerConstraintBookConstraints:
            ConstraintCutOff = len(str(ContractNumber)) + 1
            ConstraintNumber = str(Constraint[0])[ConstraintCutOff:]
            #If new ConstraintNumber is greater than the iterated ConstraintNumber, creates new ConstraintID with +1 added to ConstraintNumber
            if int(ConstraintNumber) > int(OldConstraintNumber):
                ConstraintID = (str(ContractNumber) + "-" + str(int(ConstraintNumber) + 1))
                OldConstraintNumber = ConstraintNumber
    
    
    
    '''Defining/Executing SQL Statements'''
    
    
    
    #Inserts constraint into BorrowerConstraintBook
    try:
        print ""
        cursor.execute("""INSERT INTO BorrowerConstraintBook(ConstraintID, ContractNumber, Username, Type, Value) VALUES("%s", %d, "%s", "%s", %f)""" % (ConstraintID, ContractNumber, Username, MinimumBorrowerConstraintType.title(), MinimumBorrowerConstraintValue))
        db.commit()
        print "Minimum Borrower Constraint Successfully Added"
    except:
        print "ERROR: Minimum Borrower Constraint Unsuccessfully Added"
    
    
    
    #Inserts record of constraint into BorrowerConstraintLog
    try:
        print ""
        cursor.execute("""INSERT INTO BorrowerConstraintLog(ConstraintID, ContractNumber, Username, Type, Value) VALUES("%s", %d, "%s", "%s", %f)""" % (ConstraintID, ContractNumber, Username, MinimumBorrowerConstraintType.title(), MinimumBorrowerConstraintValue))
        db.commit()
        print "Minimum Borrower Constraint Successfully Logged"
    except:
        print "ERROR: Minimum Borrower Constraint Unsuccessfully Logged"    
    
    '''Updating Constraint Amount'''
    
    
    
    #Gathers contract type
    cursor.execute("""SELECT Type FROM IDBook WHERE IDNumber = %d""" % (ContractNumber))
    ContractType = cursor.fetchall()[0][0]
    
    try:
        print ""
        #If type is MTC, updates MTCBook record of contract to reflect change in constraint amount
        if ContractType.upper() == "MTC":
            cursor.execute("""UPDATE MTCBook SET MinimumBorrowerConstraints = (MinimumBorrowerConstraints + 1) WHERE MTCNumber = %s""" % (ContractNumber))
            db.commit()
        #If type is Loan, updates LoanBook record of contract to reflect change in constraint amount
        elif ContractType.upper() == "LOAN":
            cursor.execute("""UPDATE LoanBook SET MinimumBorrowerConstraints = (MinimumBorrowerConstraints + 1) WHERE ContractNumber = %s""" % (ContractNumber))
            db.commit()
        #If type is Private Trade, updates PrivateTradeBook record of contract to reflect change in constraint amount
        elif ContractType.upper() == "PRIVATE TRADE":
            cursor.execute("""UPDATE PrivateTradeBook SET MinimumBorrowerConstraints = (MinimumBorrowerConstraints + 1) WHERE TradeNumber = %s""" % (ContractNumber))
            db.commit()
        print "Constraint Value Successfully Updated"
    except:
        print "ERROR: Constraint Value Unsuccessfully Updated"
    
    
    
    '''Logging Control'''
    
    
    
    #Assigns static variables for logging control
    #Note: "Employee" value changes based on user submitting manual control
    Employee = "***333"
    ConstraintID = "Constraint " + str(ConstraintID)
    ContractNumber = "Contract " + str(ContractNumber)
    Comment = "Added Constraint"
    
    
    
    #Inserts record of constraint addition into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Add Minimum Borrower Constraint", ConstraintID, "All", Comment))
        db.commit()
        print "Control Successfully Logged"
    except:
        print "ERROR: Control Unsuccessfully Logged"
    
    
    
    #Inserts record of constraint amount update into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update Constraint Amount", ContractNumber, "MinimumBorrowerConstraints", Comment))
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
    Data = cursor.fetchone()
    print "Database Version: " + str(Data[0])
    
    
    
    '''Setting Username'''
    
    
    
    #Requests Username to put constraint under and verifies that it is valid
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
    
    
    
    '''Setting Contract Number'''
    
    
    
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
                    cursor.execute("""SELECT Username FROM PrivateTradeBook WHERE TradeNumber = %d""" % (ContractNumber))
                    PrivateTradeUsername = cursor.fetchone()
                    
                    #If neither book has contract under specified username, retries input
                    if MTCUsername == None and LoanUsername == None and PrivateTradeUsername == None:
                        print "Specified contract does not belong to specified username. Please enter again:"
                    else:
                        print "Contract found"
                        ContractFound = True;
                        break;
        #If IDBook has no contract with specified ContractNumber, retries input
        else:
            print "Contract not found. Please enter again: "
    
    
    
    '''Setting Constraint Type'''
    
    
    
    #Requests Constraint Type and verifies that it is valid
    MinimumBorrowerConstraintType = raw_input("Minimum Borrower Constraint Type (Account Balance, Volume, Contracts, Transactions, Liquidity Value): ")
    MinimumBorrowerConstraintType = MinimumBorrowerConstraintType.upper()
    #Checks for valid input (ACCOUNT BALANCE, VOLUME, CONTRACTS, TRANSACTIONS, LIQUIDITY VALUE)
    while 1 == 1:
        if MinimumBorrowerConstraintType == "":
            print "You must specify a value for the Minimum Borrower Constraint Type. Please enter again:"
            MinimumBorrowerConstraintType = raw_input("Minimum Borrower Constraint Type (Account Balance, Volume, Contracts, Transactions, Liquidity Value): ")
        if MinimumBorrowerConstraintType != "ACCOUNTBALANCE" and MinimumBorrowerConstraintType != "ACCOUNT BALANCE" and MinimumBorrowerConstraintType != "VOLUME" and MinimumBorrowerConstraintType != "CONTRACTS" and MinimumBorrowerConstraintType != "TRANSACTIONS" and MinimumBorrowerConstraintType != "LIQUIDITYVALUE" and MinimumBorrowerConstraintType != "LIQUIDITY VALUE":
            print "Incorrect Minimum Borrower Constraint Type. Please enter again:"
            MinimumBorrowerConstraintType = raw_input("Minimum Borrower Constraint Type (Account Balance, Volume, Contracts, Transactions, Liquidity Value): ")
            MinimumBorrowerConstraintType = MinimumBorrowerConstraintType.upper()
        else:
            break;
    
    
    
    '''Standardizing Constraint Type Names'''
    
    
    
    if MinimumBorrowerConstraintType == "ACCOUNTBALANCE":
        MinimumBorrowerConstraintType = "ACCOUNT BALANCE"
    elif MinimumBorrowerConstraintType == "LIQUIDITYVALUE":
        MinimumBorrowerConstraintType = "LIQUIDITY VALUE"
    
    
    
    '''Setting Constraint Value'''
    
    
    
    #Requests Constraint Value and verifies that it is valid
    while 1 == 1:
        MinimumBorrowerConstraintValue = raw_input("Minimum Borrower Constraint Value: ")
        if MinimumBorrowerConstraintValue == "":
            print "Invalid Constraint Value. Please enter again:"
        else:
            try:
                #Converts Constraint Value to float type
                MinimumBorrowerConstraintValue = float(MinimumBorrowerConstraintValue)
                break;
            except:
                print "Value must be an integer. Please enter again:"
    
    
    
    #Execute
    main(Username, ContractNumber, MinimumBorrowerConstraintType, MinimumBorrowerConstraintValue)


