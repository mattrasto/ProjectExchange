#-------------------------------------------------------------------------------
# Name:        DBDeleteInterventionConstraintBook
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



MTCNumber = raw_input("MTC Number: ")
while 1 == 1:
    try:
        MTCNumber = int(MTCNumber)
        break;
    except:
        print "MTC Number must be an integer. Please enter again: "
        MTCNumber = raw_input("MTC Number: ")
MTCFound = False
while MTCFound != True:
    cursor.execute("""SELECT * FROM MTCBook WHERE MTCNumber = "%s" """ % (MTCNumber))
    MTCList = cursor.fetchall()
    for MTC in MTCList:
        if MTCNumber == MTC[0]:
            print "MTC found"
            MTCFound = True
            break;
    else:
        print "MTC not found. Please enter again: "
        MTCNumber = raw_input("MTC Number: ")
        while 1 == 1:
            try:
                MTCNumber = int(MTCNumber)
                break;
            except:
                print "MTC Number must be an integer. Please enter again: "
                MTCNumber = raw_input("MTC Number: ")



ConstraintNumber = raw_input("Delete Constraint Number: ")
ConstraintID = str(MTCNumber) + "-" + str(ConstraintNumber)
while 1 == 1:
    try:
        cursor.execute("""SELECT * FROM BorrowerConstraintBook WHERE ConstraintID = "%s" """ % (ConstraintID))
        ConstraintEntry = cursor.fetchall()[0]
        print ConstraintEntry
        ConstraintID = ConstraintEntry[0]
        ContractNumber = ConstraintEntry[1]
        Username = ConstraintEntry[2]
        ConstraintType = ConstraintEntry[3]
        ConstraintValue = ConstraintEntry[4]
        print "Constraint ID Found: " + str(ConstraintID)
        break;
    except:
        print "Constraint not found. Please enter again: "
        ConstraintNumber = raw_input("Delete Constraint Number: ")
        ConstraintID = str(MTCNumber) + "-" + str(ConstraintNumber)



Comment = raw_input("Administrative Comment: ")



'''Defining/Executing SQL Statements'''



sql = """DELETE FROM BorrowerConstraintBook WHERE ConstraintID = "%s" """ % (ConstraintID)

try:
    cursor.execute(sql)
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



try:
    cursor.execute("""UPDATE MTCBook SET MinimumBorrowerConstraints = (MinimumBorrowerConstraints - 1) WHERE MTCNumber = %d""" % (ContractNumber))
    db.commit()
    print ""
    print "Minimum Borrower Constraints Successfully Updated"
except:
    print "ERROR: Minimum Borrower Constraint Unsuccessfully Updated"



'''Logging Control'''
    


Employee = "***333"

ConstraintID = "Constraint " + str(ConstraintID)
ContractNumber = "MTC " + str(ContractNumber)

try:
    print ""
    cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Delete Minimum Borrower Constraint", ConstraintID, "All", Comment))
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