#-------------------------------------------------------------------------------
# Name:        DBDeleteMTC
# Version:     1.0
# Purpose:     
#
# Author:      Matthew
#
# Created:     05/07/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    05/29/2014
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
    MTCNumber = raw_input("Delete MTC Number: ")
    while 1 ==1:
        try:
            MTCNumber = int(MTCNumber)
            break;
        except:
            print "MTC Number must be an integer. Please enter again: "
            MTCNumber = raw_input("Delete MTC Number: ")
    MTCSearch = "SELECT * FROM MTCBook WHERE MTCNumber = %d" % (MTCNumber)
    try:
        cursor.execute(MTCSearch)
        MTC = cursor.fetchall()
        #print "Order found"
        #print "FoundOrder: " + str(FoundOrder)
        if FoundMTC != ():
            MTCFound = True
            for MTC in FoundMTC:
                print MTC
                Username = MTC[1]
                Medium = MTC[2]
                Volume = MTC[3]
                Action = MTC[4]
                Type = "MTC"
                DateEntered = MTC[15]
                break;
        else:
            print "MTC not found. Please search again:"
        if MTCFound == True:
            break;
    except:
        print "ERROR: Database fetch exception"



print ""
Comment = raw_input("Administrative Comment: ")



'''Defining/Executing SQL Statement'''



sql = """DELETE FROM MTCBook WHERE MTCNumber = %d""" % (MTCNumber)

try:
    cursor.execute(sql)
    db.commit()
    print ""
    print "Delete Successful"
    print ""
    print "MTC deleted:"
    print ""
    print "MTC Number: " + str(MTCNumber)
    print "Username: " + Username
    print "Type: " + Type
    print "Action: " + Action
    print "Medium: " + str(Price)
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
    cursor.execute("UPDATE MTCLog SET TerminationReason = %s, TerminationDate = %s WHERE MTCNumber = %s", ("Administrative Delete", FormattedDateTime, MTCNumber))
    db.commit()
    print "MTC Deletion Successfully Logged"
except:
    print "ERROR: Database Insert Log Failure"



'''Logging Control'''
    


Employee = "***333"

MTCID = "MTC " + str(MTCNumber)

try:
    print ""
    cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Delete MTC", MTCID, "All", Comment))
    db.commit()
    print "Control Successfully Logged"
except:
    print "ERROR: Control Unsuccessfully Logged"




db.close()