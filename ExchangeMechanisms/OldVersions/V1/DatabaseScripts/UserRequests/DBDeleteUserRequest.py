#-------------------------------------------------------------------------------
# Name:        DBDeleteUserRequest
# Version:     1.0
# Purpose:     
#
# Author:      Matthew
#
# Created:     06/02/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    06/02/2014
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
    cursor.execute("""SELECT * FROM IDBook WHERE IDNumber = %d""" % (ContractNumber))
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



RequestNumber = raw_input("Delete Request Number: ")
RequestID = str(ContractNumber) + "-" + str(RequestNumber)
while 1 == 1:
    try:
        cursor.execute("""SELECT * FROM UserRequestBook WHERE RequestID = "%s" """ % (RequestID))
        RequestEntry = cursor.fetchall()[0]
        print RequestEntry
        RequestID = RequestEntry[0]
        ContractNumber = RequestEntry[1]
        Username = RequestEntry[2]
        print "Request ID Found: " + str(RequestID)
        break;
    except:
        print "Request not found. Please enter again: "
        RequestNumber = raw_input("Delete Request Number: ")
        RequestID = str(ContractNumber) + "-" + str(RequestNumber)



Comment = raw_input("Administrative Comment: ")



'''Defining/Executing SQL Statements'''



sql = """DELETE FROM UserRequestBook WHERE RequestID = "%s" """ % (RequestID)

try:
    cursor.execute(sql)
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


'''
try:
    cursor.execute("""UPDATE ContractBook SET MinimumBorrowerRequests = (MinimumBorrowerRequests - 1) WHERE ContractNumber = %d""" % (ContractNumber))
    db.commit()
    print ""
    print "Minimum Borrower Requests Successfully Updated"
except:
    print "ERROR: Minimum Borrower Request Unsuccessfully Updated"
'''


if ContractType.upper() == "MTC":
    cursor.execute("""UPDATE MTCBook SET UserRequests = (UserRequests - 1) WHERE MTCNumber = %s""" % (ContractNumber))
    db.commit()
elif ContractType.upper() == "LOAN":
    cursor.execute("""UPDATE LoanBook SET UserRequests = (UserRequests - 1) WHERE ContractNumber = %s""" % (ContractNumber))
    db.commit()
elif ContractType.upper() == "PRIVATE TRADE":
    cursor.execute("""UPDATE PrivateTradeBook SET UserRequests = (UserRequests - 1) WHERE TradeNumber = %s""" % (ContractNumber))
    db.commit()


'''Logging Control'''
    


Employee = "***333"

RequestID = "Request " + str(RequestID)
ContractNumber = "Contract " + str(ContractNumber)

try:
    print ""
    cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Delete User Request", RequestID, "All", Comment))
    db.commit()
    print "Control Successfully Logged"
except:
    print "ERROR: Control Unsuccessfully Logged"

try:
    print ""
    cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update Request Amount", ContractNumber, "UserRequests", Comment))
    db.commit()
    print "Control Successfully Logged"
except:
    print "ERROR: Control Unsuccessfully Logged"



db.close()