#-------------------------------------------------------------------------------
# Name:        DBDeleteLoan
# Version:     1.0
# Purpose:     
#
# Author:      Matthew
#
# Created:     05/29/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    05/30/2014
#-------------------------------------------------------------------------------



import time
import MySQLdb

db = MySQLdb.connect("localhost","root","***","exchangedatabase")

cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data



'''Setting Required Variables'''



OrderFound = False
while 1 == 1:
    ContractNumber = raw_input("Delete Contract Number: ")
    while 1 ==1:
        try:
            ContractNumber = int(ContractNumber)
            break;
        except:
            print "Contract Number must be an integer. Please enter again: "
            ContractNumber = raw_input("Delete Contract Number: ")
    ContractSearch = "SELECT * FROM LoanBook WHERE ContractNumber = %d" % (ContractNumber)
    try:
        cursor.execute(ContractSearch)
        FoundContract = cursor.fetchall()
        #print "Order found"
        #print "FoundOrder: " + str(FoundOrder)
        if FoundContract != ():
            ContractFound = True
            for Contract in FoundContract:
                print Contract
                Username = Contract[1]
                Price = Contract[2]
                Volume = Contract[3]
                Action = Contract[4]
                Type = "Loan"
                DateEntered = Contract[13]
                break;
        else:
            print "Contract not found. Please search again:"
        if ContractFound == True:
            break;
    except:
        print "ERROR: Database fetch exception"



print ""
Comment = raw_input("Administrative Comment: ")



'''Defining/Executing SQL Statement'''



sql = """DELETE FROM LoanBook WHERE ContractNumber = %d""" % (ContractNumber)

try:
    cursor.execute(sql)
    db.commit()
    print ""
    print "Delete Successful"
    print ""
    print "Contract deleted:"
    print ""
    print "Contract Number: " + str(ContractNumber)
    print "Username: " + Username
    print "Type: " + Type
    print "Action: " + Action
    print "Price: " + str(Price)
    print "Volume: " + str(Volume)
    print "Date Entered: " + str(DateEntered)
except:
    db.rollback()
    print ""
    print "Delete Unsuccessful"



'''Logging Order Termination'''



LocalTime = time.localtime(time.time())
LocalTimeMinutes = LocalTime[4]
LocalTimeSeconds = LocalTime[5]
if LocalTimeMinutes < 10:
    LocalTimeMinutes = "0" + str(LocalTimeMinutes)
if LocalTimeSeconds < 10:
    LocalTimeSeconds = "0" + str(LocalTimeSeconds)
FormattedDate = str(LocalTime[1]) + "/" +  str(LocalTime[2]) + "/" +  str(LocalTime[0])
FormattedDatabaseDate = str(LocalTime[0]) + "-" +  str(LocalTime[1]) + "-" +  str(LocalTime[2])
FormattedTime = str(LocalTime[3]) + ":" +  str(LocalTimeMinutes) + ":" +  str(LocalTimeSeconds)
FormattedDateTime = FormattedDatabaseDate + " " + FormattedTime

print ""
try:
    cursor.execute("UPDATE LoanLog SET TerminationReason = %s, TerminationDate = %s WHERE ContractNumber = %s", ("Administrative Delete", FormattedDateTime, ContractNumber))
    db.commit()
    print "Contract Deletion Successfully Logged"
except:
    print "ERROR: Database Insert Log Failure"



'''Logging Control'''
    


Employee = "***333"

ContractID = "Loan " + str(ContractNumber)

try:
    print ""
    cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Delete MTC", ContractID, "All", Comment))
    db.commit()
    print "Control Successfully Logged"
except:
    print "ERROR: Control Unsuccessfully Logged"




db.close()