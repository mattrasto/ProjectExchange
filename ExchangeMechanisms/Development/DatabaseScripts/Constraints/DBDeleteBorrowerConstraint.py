#-------------------------------------------------------------------------------
# Name:        DBDeleteBorrowerConstraint
# Version:     3.0
# Purpose:     Deletes specified User Intervention Constraint
#
# Author:      Matthew
#
# Created:     05/14/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/04/2014
#-------------------------------------------------------------------------------

import MySQLdb
import sys



def main(ContractNumber, ConstraintID):

    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    
    
    '''Gathering Constraint Details'''
    
    
    
    try:
        print ""
        cursor.execute("""SELECT * FROM BorrowerConstraintBook WHERE ConstraintID = "%s" """ % (ConstraintID))
        Constraint = cursor.fetchone()
        #If contract is found, assigns attribute values to static variables
        if Constraint != None:
            print "Constraint Found"
            Username = Constraint[2]
            ConstraintType = Constraint[3]
            ConstraintValue = Constraint[4]
        else:
            print "CRITICAL ERROR: Constraint not found"
            sys.exit()
    except SystemExit:
        sys.exit()
    except:
        print "ERROR: Database fetch exception"
    
    
    
    '''Defining/Executing SQL Statements'''
    
    
    
    #Deletes constraint from BorrowerConstraintBook
    try:
        cursor.execute("""DELETE FROM BorrowerConstraintBook WHERE ConstraintID = "%s" """ % (ConstraintID))
        db.commit()
        print ""
        print "Delete Successful"
        print ""
        print "Constraint deleted:"
        print ""
        print "Constraint ID: " + str(ConstraintID)
        print "Contract Number: " + str(ContractNumber)
        print "Username: " + str(Username)
        print "Constraint Type: " + str(ConstraintType)
        print "Constraint Value: " + str(ConstraintValue)
    except:
        db.rollback()
        print ""
        print "Delete Unsuccessful"
    
    
    
    '''Updating Constraint Amount'''
    
    
    
    #Gathers contract type
    cursor.execute("""SELECT Type FROM IDBook WHERE IDNumber = %d""" % (ContractNumber))
    ContractType = cursor.fetchone()
    if ContractType != None:
        ContractType =  ContractType[0]
    else:
        print "CRITICAL ERROR: Contract has no type"
        sys.exit()
    
    
    
    #Updates contract in MTCBook to reflect change in constraint amount
    if ConstraintType == "MTC":
        try:
            cursor.execute("""UPDATE MTCBook SET MinimumBorrowerConstraints = (MinimumBorrowerConstraints - 1) WHERE MTCNumber = %d""" % (ContractNumber))
            db.commit()
            print ""
            print "Minimum Borrower Constraints Successfully Updated"
        except:
            print "ERROR: Minimum Borrower Constraint Unsuccessfully Updated"
    
    
    
    #Updates contract in LoanBook to reflect change in constraint amount
    if ConstraintType == "Loan":
        try:
            cursor.execute("""UPDATE LoanBook SET MinimumBorrowerConstraints = (MinimumBorrowerConstraints - 1) WHERE ContractNumber = %d""" % (ContractNumber))
            db.commit()
            print ""
            print "Minimum Borrower Constraints Successfully Updated"
        except:
            print "ERROR: Minimum Borrower Constraint Unsuccessfully Updated"
    
    
    
    #Updates contract in PrivateTradeBook to reflect change in constraint amount
    if ConstraintType == "Private Trade":
        try:
            cursor.execute("""UPDATE PrivateTradeBook SET MinimumBorrowerConstraints = (MinimumBorrowerConstraints - 1) WHERE TradeNumber = %d""" % (ContractNumber))
            db.commit()
            print ""
            print "Minimum Borrower Constraints Successfully Updated"
        except:
            print "ERROR: Minimum Borrower Constraint Unsuccessfully Updated"
    
    
    
    '''Logging Control'''
        
    
    
    #Assigns static variables for logging control
    #Note: "Employee" value changes based on user submitting manual control
    Employee = "***333"
    ConstraintID = "Constraint " + str(ConstraintID)
    ContractNumber = "MTC " + str(ContractNumber)
    Comment = "Deleted Minimum Borrower Constraint"
    
    
    
    #Inserts record of constraint deletion into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Delete Minimum Borrower Constraint", ConstraintID, "All", Comment))
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
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    
    
    '''Setting Contract Number'''
    
    
    
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
    
    
    
    '''Setting Constraint Number'''
    
    
    
    #Requests ConstraintNumber
    ConstraintNumber = raw_input("Delete Constraint Number: ")
    #Creates ConstraintID by concatenating "-[ConstraintNumber]" to ConstractNumber
    ConstraintID = str(ContractNumber) + "-" + str(ConstraintNumber)
    while 1 == 1:
        #Checks for integer type
        while 1 == 1:
            try:
                ConstraintNumber = int(ConstraintNumber)
                break;
            except:
                print "Constraint Number must be an integer. Please enter again: "
                ConstraintNumber = raw_input("Constraint Number: ")
        #Verifies that constraint exists
        try:
            cursor.execute("""SELECT * FROM BorrowerConstraintBook WHERE ConstraintID = "%s" """ % (ConstraintID))
            ConstraintEntry = cursor.fetchall()[0]
            print "Constraint ID Found: " + str(ConstraintID)
            break;
        except:
            print "Constraint not found. Please enter again: "
            ConstraintNumber = raw_input("Delete Constraint Number: ")
            ConstraintID = str(ContractNumber) + "-" + str(ConstraintNumber)
    
    
    
    #Execute
    main(ContractNumber, ConstraintID)


