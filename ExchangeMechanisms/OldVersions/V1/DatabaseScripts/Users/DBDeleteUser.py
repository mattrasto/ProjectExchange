#-------------------------------------------------------------------------------
# Name:        DBDeleteUser
# Version:     1.0
# Purpose:
#
# Author:      Matthew
#
# Created:     04/21/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    05/10/2014
#-------------------------------------------------------------------------------

import time
import MySQLdb

db = MySQLdb.connect("localhost","root","***","exchangedatabase")

#Prepare a cursor object using cursor() method
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data



'''Setting Variables'''



Username = raw_input("Delete User: ")
Username = Username.upper()
UsernameCheck = """SELECT * FROM UserBook"""
try:
    cursor.execute(UsernameCheck)
    Usernames = cursor.fetchall()
    for User in Usernames:
        TargetUsername = User[0]
        if TargetUsername.upper() == Username:
            print "User found"
            Username = User[0]
            Password = User[1]
            Email = User[2]
            USDCredit = User[3]
            BTCCredit = User[4]
            JoinDate = User[5]
            FirstName = User[6]
            LastName = User[7]
            BankName = User[8]
            Address = User[9]
            Verified = User[10]
            TradingFee = User[11]
            Volume = User[12]
            break;
    while TargetUsername.upper() != Username.upper():
            print "User not found. Please enter again:"
            Username = raw_input("Modified User: ")
            Username = Username.upper()
            try:
                cursor.execute(UsernameCheck)
                Usernames = cursor.fetchall()
                if TargetUsername.upper() == Username:
                    print "User found"
                    Username = User[0]
                    Password = User[1]
                    Email = User[2]
                    USDCredit = User[3]
                    BTCCredit = User[4]
                    JoinDate = User[5]
                    FirstName = User[6]
                    LastName = User[7]
                    BankName = User[8]
                    Address = User[9]
                    Verified = User[10]
                    TradingFee = User[11]
                    Volume = User[12]
                    break;
            except:
                "ERROR: Database fetch exception"
except:
    print "ERROR: Database fetch exception"

Comment = raw_input("Administrative Comment: ")



'''Defining/Executing SQL Statement'''



LocalTime = time.localtime(time.time())
LocalTimeMinutes = LocalTime[4]
LocalTimeSeconds = LocalTime[5]
if LocalTimeMinutes < 10:
    LocalTimeMinutes = "0" + str(LocalTimeMinutes)
if LocalTimeSeconds < 10:
    LocalTimeSeconds = "0" + str(LocalTimeSeconds)
FormattedDateDashes = str(LocalTime[0]) + "-" +  str(LocalTime[1]) + "-" +  str(LocalTime[2])
FormattedDate = str(LocalTime[1]) + "/" +  str(LocalTime[2]) + "/" +  str(LocalTime[0])
FormattedTime = str(LocalTime[3]) + ":" +  str(LocalTimeMinutes) + ":" +  str(LocalTimeSeconds)
FormattedDateTime = str(FormattedDateDashes) + " " + str(FormattedTime)

try:
    cursor.execute("DELETE FROM UserBook WHERE Username = %s", (Username))
    db.commit()
    print "Delete Successful"
except:
    print "Delete Unsuccessful"

print ""
print "User deleted:"
print ""
print "Username: " + str(Username)
print "Password: " + str(Password)
print "Email: " + str(Email)
print "USD: " + str(USDCredit)
print "BTC: " + str(BTCCredit)
print "Join Date: " + str(JoinDate)
print "First Name: " + str(FirstName)
print "Last Name: " + str(LastName)
print "Bank: " + str(BankName)
print "Address: " + str(Address)
print "Verified: " + str(Verified)
print "Trading Fee: " + str(TradingFee)
print "Volume: " + str(Volume)
print ""
print "Deletion Comment: " + str(Comment)
print "----------"



'''Logging User Deletion'''



print ""
try:
    cursor.execute("UPDATE UserLog SET DeletionComment = %s, DeletionDate = %s WHERE Username = %s", (DeleteComment, FormattedDateTime, Username))
    db.commit()
    print "User Deletion Logged Successfully"
except:
    print "ERROR: Database Insert Log Failure"



'''Logging Control'''
    


Employee = "***333"

try:
    print ""
    cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Delete User", Username, "All", Comment))
    db.commit()
    print "Control Successfully Logged"
except:
    print "ERROR: Control Unsuccessfully Logged"


db.close()