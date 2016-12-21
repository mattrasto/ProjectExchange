#-------------------------------------------------------------------------------
# Name:        DBAddInterventionConstraint
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



UserInterventionConstraintType = raw_input("User Intervention Constraint Type (Market Price, Profit Margin, Interest Rate): ")
UserInterventionConstraintType = UserInterventionConstraintType.upper()
while 1 == 1:
    if UserInterventionConstraintType == "":
        print "User Intervention Constraint Failed"
        UserInterventionConstraintPresent = False
        break;
    if UserInterventionConstraintType != "MARKETPRICE" and UserInterventionConstraintType != "MARKET PRICE" and UserInterventionConstraintType != "PROFITMARGIN" and UserInterventionConstraintType != "PROFIT MARGIN" and UserInterventionConstraintType != "INTERESTRATE" and UserInterventionConstraintType != "INTEREST RATE":
        print "Incorrect User Intervention Constraint Type. Please enter again:"
        UserInterventionConstraintType = raw_input("User Intervention Constraint Type (Account Balance, Volume, Contracts, Transactions, Liquidity Value): ")
        UserInterventionConstraintType = UserInterventionConstraintType.upper()
    else:
        UserInterventionConstraintPresent = True
        break;

if UserInterventionConstraintPresent == True:    
    UserInterventionConstraintValue = raw_input("User Intervention Constraint Value: ")
    while 1 == 1:
        if UserInterventionConstraintValue == "":
            print "User Intervention Constraint Failed"
            UserInterventionConstraintPresent = False
            break;
        try:
            UserInterventionConstraintValue = float(UserInterventionConstraintValue)
            UserInterventionConstraintPresent = True
            break;
        except:
            print "User Intervention Constraint Type must be a rational number. Please enter again:"
            UserInterventionConstraintValue = raw_input("User Intervention Constraint Value: ")



Comment = raw_input("Administrative Comment: ")



'''Defining/Executing SQL Statements'''



if UserInterventionConstraintPresent == True:
    if UserInterventionConstraintType == "MARKETPRICE":
        UserInterventionConstraintType = "MARKET PRICE"
    elif UserInterventionConstraintType == "PROFITMARGIN":
        UserInterventionConstraintType = "PROFIT MARGIN"
    elif UserInterventionConstraintType == "INTERESTRATE":
        UserInterventionConstraintType = "INTEREST RATE"
    #print ""
    cursor.execute("""SELECT * FROM InterventionConstraintLog WHERE ContractNumber = %s""" % (ContractNumber))
    InterventionConstraintBookConstraints = cursor.fetchall()
    #print InterventionConstraintBookConstraints
    if InterventionConstraintBookConstraints == ():
        ConstraintID = str(ContractNumber) + "-1"
    else:
        OldConstraintNumber = 0
        for Constraint in InterventionConstraintBookConstraints:
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
        cursor.execute("""INSERT INTO InterventionConstraintBook(ConstraintID, ContractNumber, Username, Type, Value) VALUES("%s", %d, "%s", "%s", %f)""" % (ConstraintID, ContractNumber, Username, UserInterventionConstraintType.title(), UserInterventionConstraintValue))
        cursor.execute("""INSERT INTO InterventionConstraintLog(ConstraintID, ContractNumber, Username, Type, Value) VALUES("%s", %d, "%s", "%s", %f)""" % (ConstraintID, ContractNumber, Username, UserInterventionConstraintType.title(), UserInterventionConstraintValue))
        db.commit()
        print "User Intervention Constraint Successfully Added"
    except:
        print "ERROR: User Intervention Constraint Unsuccessfully Added"
    
    
    
    if ContractType.upper() == "MTC":
        cursor.execute("""UPDATE MTCBook SET UserInterventionConstraints = (UserInterventionConstraints + 1) WHERE MTCNumber = %s""" % (ContractNumber))
        db.commit()
    elif ContractType.upper() == "LOAN":
        cursor.execute("""UPDATE LoanBook SET UserInterventionConstraints = (UserInterventionConstraints + 1) WHERE ContractNumber = %s""" % (ContractNumber))
        db.commit()



'''Logging Control'''
    


Employee = "***333"

ConstraintID = "Constraint " + str(ConstraintID)
ContractNumber = "Contract " + str(ContractNumber)

try:
    print ""
    cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Add User Intervention Constraint", ConstraintID, "All", Comment))
    db.commit()
    print "Control Successfully Logged"
except:
    print "ERROR: Control Unsuccessfully Logged"

try:
    print ""
    cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update Constraint Amount", ContractNumber, "UserInterventionConstraints", Comment))
    db.commit()
    print "Control Successfully Logged"
except:
    print "ERROR: Control Unsuccessfully Logged"



db.close()