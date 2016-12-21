#-------------------------------------------------------------------------------
# Name:        DBAddUserRequest
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



Comment = raw_input("Administrative Comment: ")



'''Defining/Executing SQL Statements'''



cursor.execute("""SELECT * FROM IDBook WHERE IDNumber = %d""" % (ContractNumber))
Contract = cursor.fetchall()
ContractType = Contract[0][2]



cursor.execute("""SELECT * FROM UserRequestBook WHERE ContractNumber = %d""" % (ContractNumber))
UserRequests = cursor.fetchall()
#print UserRequests
if UserRequests == ():
    RequestID = str(ContractNumber) + "-1"
else:
    OldRequestNumber = 0
    for Request in UserRequests:
        #print ""
        #print "Previous Request: " + str(Request[0])
        RequestCutOff = len(str(ContractNumber)) + 1
        #print "Request Cut-Off: " + str(RequestCutOff)
        RequestNumber = str(Request[0])[RequestCutOff:]
        #print "Request Number: " + str(RequestNumber)
        #print "Old Request Number: " + str(OldRequestNumber)
        if int(RequestNumber) > int(OldRequestNumber):
            #print "Request Number: " + str(RequestNumber)
            #print "Old Request Number: " + str(OldRequestNumber)
            RequestID = (str(ContractNumber) + "-" + str(int(RequestNumber) + 1))
            #print "Request ID: " + str(RequestID)
            OldRequestNumber = RequestNumber
            #print "Old Request Number: " + str(OldRequestNumber)
print ""
try:
    cursor.execute("""INSERT INTO UserRequestBook(RequestID, ContractNumber, Username) VALUES("%s", %d, "%s")""" % (RequestID, ContractNumber, Username))
    cursor.execute("""INSERT INTO UserRequestLog(RequestID, ContractNumber, Username) VALUES("%s", %d, "%s")""" % (RequestID, ContractNumber, Username))
    db.commit()
    print "User Request Successfully Added"
except:
    print "ERROR: User Request Unsuccessfully Added"



if ContractType.upper() == "MTC":
    cursor.execute("""UPDATE MTCBook SET UserRequests = (UserRequests + 1) WHERE MTCNumber = %s""" % (ContractNumber))
    db.commit()
elif ContractType.upper() == "LOAN":
    cursor.execute("""UPDATE LoanBook SET UserRequests = (UserRequests + 1) WHERE ContractNumber = %s""" % (ContractNumber))
    db.commit()
elif ContractType.upper() == "PRIVATE TRADE":
    cursor.execute("""UPDATE PrivateTradeBook SET UserRequests = (UserRequests + 1) WHERE TradeNumber = %s""" % (ContractNumber))
    db.commit()



'''Logging Control'''
    


Employee = "***333"

RequestID = "Request " + str(RequestID)
ContractNumber = "Contract " + str(ContractNumber)

try:
    print ""
    cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Add User Request", RequestID, "All", Comment))
    db.commit()
    print "Control Successfully Logged"
except:
    print "ERROR: Control Unsuccessfully Logged"

try:
    print ""
    cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update User Request Amount", ContractNumber, "UserRequests", Comment))
    db.commit()
    print "Control Successfully Logged"
except:
    print "ERROR: Control Unsuccessfully Logged"



db.close()