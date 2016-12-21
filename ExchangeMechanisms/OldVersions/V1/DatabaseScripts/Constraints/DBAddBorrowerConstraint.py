#-------------------------------------------------------------------------------
# Name:        DBAddBorrowerConstraint
# Version:     1.0
# Purpose:     
#
# Author:      Matthew
#
# Created:     05/14/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    05/26/2014
#-------------------------------------------------------------------------------



import MySQLdb

db = MySQLdb.connect("localhost","root","***","exchangedatabase")

cursor = db.cursor()

cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data



'''Setting Variables'''



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



ContractNumber = raw_input("Contract Number: ")
while 1 == 1:
    try:
        ContractNumber = int(ContractNumber)
        break;
    except:
        print "Contract Number must be an integer. Please enter again: "
        ContractNumber = raw_input("Contract Number: ")
ContractFound = False
while ContractFound != True:
    cursor.execute("""SELECT * FROM IDBook WHERE IDNumber = "%s" """ % (ContractNumber))
    ContractList = cursor.fetchall()
    for Contract in ContractList:
        if ContractNumber == Contract[0]:
            print "Contract found"
            ContractFound = True
            ContractAction = Contract[1]
            ContractType = Contract[2]
            break;
    else:
        print "Contract not found. Please enter again: "
        ContractNumber = raw_input("Contract Number: ")
        while 1 == 1:
            try:
                ContractNumber = int(ContractNumber)
                break;
            except:
                print "Contract Number must be an integer. Please enter again: "
                ContractNumber = raw_input("Contract Number: ")



MinimumBorrowerConstraintType = raw_input("Minimum Borrower Constraint Type (Account Balance, Volume, Contracts, Transactions, Liquidity Value): ")
MinimumBorrowerConstraintType = MinimumBorrowerConstraintType.upper()
while 1 == 1:
    if MinimumBorrowerConstraintType == "":
        print "Minimum Borrower Constraint Failed"
        MinimumBorrowerConstraintPresent = False
        break;
    if MinimumBorrowerConstraintType != "ACCOUNTBALANCE" and MinimumBorrowerConstraintType != "ACCOUNT BALANCE" and MinimumBorrowerConstraintType != "VOLUME" and MinimumBorrowerConstraintType != "CONTRACTS" and MinimumBorrowerConstraintType != "TRANSACTIONS" and MinimumBorrowerConstraintType != "LIQUIDITYVALUE" and MinimumBorrowerConstraintType != "LIQUIDITY VALUE":
        print "Incorrect Minimum Borrower Constraint Type. Please enter again:"
        MinimumBorrowerConstraintType = raw_input("Minimum Borrower Constraint Type (Account Balance, Volume, Contracts, Transactions, Liquidity Value): ")
        MinimumBorrowerConstraintType = MinimumBorrowerConstraintType.upper()
    else:
        MinimumBorrowerConstraintPresent = True
        break;

if MinimumBorrowerConstraintPresent == True:    
    MinimumBorrowerConstraintValue = raw_input("Minimum Borrower Constraint Value: ")
    while 1 == 1:
        if MinimumBorrowerConstraintValue == "":
            print "Minimum Borrower Constraint Failed"
            MinimumBorrowerConstraintPresent = False
            break;
        try:
            MinimumBorrowerConstraintValue = float(MinimumBorrowerConstraintValue)
            MinimumBorrowerConstraintPresent = True
            break;
        except:
            print "Minimum Borrower Constraint Type must be a rational number. Please enter again:"
            MinimumBorrowerConstraintValue = raw_input("Minimum Borrower Constraint Value: ")



Comment = raw_input("Administrative Comment: ")



'''Defining/Executing SQL Statements'''



if MinimumBorrowerConstraintPresent == True:
    if MinimumBorrowerConstraintType == "ACCOUNTBALANCE":
        MinimumBorrowerConstraintType = "ACCOUNT BALANCE"
    elif MinimumBorrowerConstraintType == "LIQUIDITYVALUE":
        MinimumBorrowerConstraintType = "LIQUIDITY VALUE"
    #print ""
    cursor.execute("""SELECT * FROM BorrowerConstraintLog WHERE ContractNumber = %s""" % (ContractNumber))
    BorrowerConstraintBookConstraints = cursor.fetchall()
    #print BorrowerConstraintBookConstraints
    if BorrowerConstraintBookConstraints == ():
        ConstraintID = str(ContractNumber) + "-1"
    else:
        OldConstraintNumber = 0
        for Constraint in BorrowerConstraintBookConstraints:
            #print ""
            #print "Previous Constraint: " + str(Constraint[0])
            ConstraintCutOff = len(str(ContractNumber)) + 1
            #print "Constraint Cut-Off: " + str(ConstraintCutOff)
            ConstraintNumber = str(Constraint[0])[ConstraintCutOff:]
            #print "Constraint Number: " + str(ConstraintNumber)
            #print "Old Constraint Number: " + str(OldConstraintNumber)
            if int(ConstraintNumber) > int(OldConstraintNumber):
                #print "Constraint Number: " + str(ConstraintNumber)
                #print "Old Constraint Number: " + str(OldConstraintNumber)
                ConstraintID = (str(ContractNumber) + "-" + str(int(ConstraintNumber) + 1))
                #print "Constraint ID: " + str(ConstraintID)
                OldConstraintNumber = ConstraintNumber
                #print "Old Constraint Number: " + str(OldConstraintNumber)
    print ""
    try:
        cursor.execute("""INSERT INTO BorrowerConstraintBook(ConstraintID, ContractNumber, Username, Type, Value) VALUES("%s", %d, "%s", "%s", %f)""" % (ConstraintID, ContractNumber, Username, MinimumBorrowerConstraintType.title(), MinimumBorrowerConstraintValue))
        cursor.execute("""INSERT INTO BorrowerConstraintLog(ConstraintID, ContractNumber, Username, Type, Value) VALUES("%s", %d, "%s", "%s", %f)""" % (ConstraintID, ContractNumber, Username, MinimumBorrowerConstraintType.title(), MinimumBorrowerConstraintValue))
        db.commit()
        print "Minimum Borrower Constraint Successfully Added"
    except:
        print "ERROR: Minimum Borrower Constraint Unsuccessfully Added"
    
    
    
    if ContractType.upper() == "MTC":
        cursor.execute("""UPDATE MTCBook SET MinimumBorrowerConstraints = (MinimumBorrowerConstraints + 1) WHERE MTCNumber = %s""" % (ContractNumber))
        db.commit()
    elif ContractType.upper() == "LOAN":
        cursor.execute("""UPDATE LoanBook SET MinimumBorrowerConstraints = (MinimumBorrowerConstraints + 1) WHERE ContractNumber = %s""" % (ContractNumber))
        db.commit()



'''Logging Control'''
    


Employee = "***333"

ConstraintID = "Constraint " + str(ConstraintID)
ContractNumber = "Contract " + str(ContractNumber)

try:
    print ""
    cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Add Minimum Borrower Constraint", ConstraintID, "All", Comment))
    db.commit()
    print "Control Successfully Logged"
except:
    print "ERROR: Control Unsuccessfully Logged"

try:
    print ""
    cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update Constraint Amount", ContractNumber, "MinimumBorrowerConstraints", Comment))
    db.commit()
    print "Control Successfully Logged"
except:
    print "ERROR: Control Unsuccessfully Logged"



db.close()