#-------------------------------------------------------------------------------
# Name:        DBAddInterventionConstraint
# Version:     2.0
# Purpose:     Adds user intervention constraint to specified order with specified constraints
#
# Author:      Matthew
#
# Created:     05/14/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/14/2014
#-------------------------------------------------------------------------------

import MySQLdb

def main(Username, ContractNumber, UserInterventionConstraintType, UserInterventionConstraintValue):
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()
    print "Database Version: " + str(Data[0])
    
    
    
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
    if MTCUsername != Username and LoanUsername != Username and PrivateTradeUsername != Username:
        print "CRITICAL ERROR: Specified contract does not belong to specified username"
        sys.exit()
    else:
        print "User Owns Contract"



    '''Defining ConstraintID'''
    
    
    
    #Gathers current highest ConstraintID from log and adds one
    #NOTE: Since ConstraintID is in format "[ContractNumber]-[ConstraintNumber]", the ID must be converted to string,
    #cut off after the dash, then the ConstraintNumber must be calculated and appended to the ID again
    
    cursor.execute("""SELECT * FROM InterventionConstraintLog WHERE ContractNumber = %s""" % (ContractNumber))
    InterventionConstraintBookConstraints = cursor.fetchall()
    #If no current constraints exists, sets ID to "[ContractNumber]-1"
    if InterventionConstraintBookConstraints == ():
        ConstraintID = str(ContractNumber) + "-1"
    else:
        
        #Iterates through each ConstraintID, changing OldConstraintNumber to reflect ConstraintNumber that was just compared,
        #then compares those values with newly assigned ConstraintID again until loop is finished
        #NOTE: This allows for skips in the log due to error, whereas counting the number of constraints and appending would not
        
        OldConstraintNumber = 0
        #Gathers ConstraintNumber from each constraint
        for Constraint in InterventionConstraintBookConstraints:
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
        cursor.execute("""INSERT INTO InterventionConstraintBook(ConstraintID, ContractNumber, Username, Type, Value) VALUES("%s", %d, "%s", "%s", %f)""" % (ConstraintID, ContractNumber, Username, UserInterventionConstraintType.title(), UserInterventionConstraintValue))
        db.commit()
        print "User Intervention Constraint Successfully Added"
    except:
        print "ERROR: User Intervention Constraint Unsuccessfully Added"
    
    
    
    #Inserts record of constraint into InterventionConstraintLog
    try:
        print ""
        cursor.execute("""INSERT INTO InterventionConstraintLog(ConstraintID, ContractNumber, Username, Type, Value) VALUES("%s", %d, "%s", "%s", %f)""" % (ConstraintID, ContractNumber, Username, UserInterventionConstraintType.title(), UserInterventionConstraintValue))
        db.commit()
        print "User Intervention Constraint Successfully Logged"
    except:
        print "ERROR: User Intervention Constraint Unsuccessfully Logged"
    
    
    
    '''Updating Constraint Amount'''
    
    
    
    #Gathers contract type
    cursor.execute("""SELECT Type FROM IDBook WHERE IDNumber = %d""" % (ContractNumber))
    ContractType = cursor.fetchall()[0][0]
    
    print ""
    try:
        #If type is MTC, updates MTCBook record of contract to reflect change in constraint amount
        if ContractType.upper() == "MTC":
            cursor.execute("""UPDATE MTCBook SET UserInterventionConstraints = (UserInterventionConstraints + 1) WHERE MTCNumber = %s""" % (ContractNumber))
            db.commit()
        #If type is Loan, updates LoanBook record of contract to reflect change in constraint amount
        elif ContractType.upper() == "LOAN":
            cursor.execute("""UPDATE LoanBook SET UserInterventionConstraints = (UserInterventionConstraints + 1) WHERE ContractNumber = %s""" % (ContractNumber))
            db.commit()
        #If type is Private Trade, updates PrivateTradeBook record of contract to reflect change in constraint amount
        elif ContractType.upper() == "PRIVATE TRADE":
            cursor.execute("""UPDATE PrivateTradeBook SET UserInterventionConstraints = (UserInterventionConstraints + 1) WHERE TradeNumber = %s""" % (ContractNumber))
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
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Add User Intervention Constraint", ConstraintID, "All", Comment))
        db.commit()
        print "Control Successfully Logged"
    except:
        print "ERROR: Control Unsuccessfully Logged"
    
    
    
    #Inserts record of constraint amount update into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update Constraint Amount", ContractNumber, "UserInterventionConstraints", Comment))
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
    UserInterventionConstraintType = raw_input("User Intervention Constraint Type (Market Price, Profit Margin, Interest Rate): ")
    UserInterventionConstraintType = UserInterventionConstraintType.upper()
    #Checks for valid input (MARKET PRICE, PROFIT MARGIN, INTEREST RATE)
    while 1 == 1:
        if UserInterventionConstraintType == "":
            print "User Intervention Constraint Failed"
            UserInterventionConstraintPresent = False
            break;
        if UserInterventionConstraintType != "MARKETPRICE" and UserInterventionConstraintType != "MARKET PRICE" and UserInterventionConstraintType != "PROFITMARGIN" and UserInterventionConstraintType != "PROFIT MARGIN" and UserInterventionConstraintType != "INTERESTRATE" and UserInterventionConstraintType != "INTEREST RATE":
            print "Incorrect User Intervention Constraint Type. Please enter again:"
            UserInterventionConstraintType = raw_input("User Intervention Constraint Type (Market Price, Profit Margin, Interest Rate): ")
            UserInterventionConstraintType = UserInterventionConstraintType.upper()
        else:
            UserInterventionConstraintPresent = True
            break;
    
    
    
    '''Standardizing Constraint Type Names'''
    
    
    
    if UserInterventionConstraintType == "MARKETPRICE":
        UserInterventionConstraintType = "MARKET PRICE"
    elif UserInterventionConstraintType == "PROFITMARGIN":
        UserInterventionConstraintType = "PROFIT MARGIN"
    elif UserInterventionConstraintType == "INTERESTRATE":
        UserInterventionConstraintType = "INTEREST RATE"
    
    
    
    '''Setting Constraint Value'''
    
    
    
    #Requests Constraint Value and verifies that it is valid
    while 1 == 1:
        UserInterventionConstraintValue = raw_input("User Intervention Constraint Value: ")
        if UserInterventionConstraintValue == "":
            print "Invalid Constraint Value. Please enter again:"
        else:
            try:
                #Converts Constraint Value to float type
                UserInterventionConstraintValue = float(UserInterventionConstraintValue)
                break;
            except:
                print "Constraint Value must be an integer. Please enter again:"
    
    
    
    #Execute
    main(Username, ContractNumber, UserInterventionConstraintType, UserInterventionConstraintValue)


