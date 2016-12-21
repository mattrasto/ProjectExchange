#-------------------------------------------------------------------------------
# Name:        DBAddUser
# Version:     1.0
# Purpose:
#
# Author:      Matthew
#
# Created:     04/01/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    05/27/2014
#-------------------------------------------------------------------------------

#Add Logging

import MySQLdb

db = MySQLdb.connect("localhost","root","***","exchange")

cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data



'''Setting Variables'''



Username = raw_input("Username: ")
Username = Username.capitalize()
Password = raw_input("Password: ")
Email = raw_input("Email: ")
#USD = raw_input("USD Credit: ")
#BTC = raw_input("BTC Credit: ")
#JoinDate = raw_input("Join Date: ")
FirstName = raw_input("First Name: ")
FirstName = FirstName.capitalize()
LastName = raw_input("Last Name: ")
LastName = LastName.capitalize()
#BankName = raw_input("Bank Name: ")
#Address = raw_input("Address: ")
#Verified = raw_input("Verified: ")
#TradingFee = raw_input("Trading Fee: ")
#Volume = raw_input("Volume: ")

print ""
Comment = raw_input("Administrative Comment: ")



'''Defining/Executing SQL Statements'''



#Partial (Required Field) manual INSERT query
sql =   """INSERT INTO UserBook(Username, Password, Email, FirstName, LastName) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Username, Password, Email, FirstName, LastName)

#Full manual INSERT query
#sql =  """INSERT INTO Users(Username, Password, Email, USDCredit, BTCCredit, JoinDate, FirstName, LastName, BankName, Address, Verified, TradingFee, Volume) \
        #VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")""" % \
        #(Username, Password, Email, USD, BTC, JoinDate, FirstName, LastName, BankName, Address, Verified, TradingFee, Volume)

#Full automatic INSERT query
#sql =  """INSERT INTO Users(Username, Password, Email, USDCredit, BTCCredit, JoinDate, FirstName, LastName, BankName, Address, Verified, TradingFee, Volume) \
        #VALUES("***333", "***", "matthewrastovac@yahoo.com", 0 , 0, "4/3/14", "Matthew", "Rastovac", "Chase", "220 LHR", "Yes", .005, 10000)"""

print ""
try:
    cursor.execute(sql)
    db.commit()
    print "Insert Successful"
except:
    db.rollback()
    print "Insert Unsuccessful"

readback = "SELECT * FROM UserBook"

try:
    cursor.execute(readback)
    Usernames = cursor.fetchall()
    for User in Usernames:
        TargetUsername = User[0]
        if TargetUsername == Username:
            print ""
            print "User added:"
            print ""
            Username = User[0]
            Password = User[1]
            Email = User[2]
            USD_Credit = User[3]
            BTC_Credit = User[4]
            Join_Date = User[5]
            First_Name = User[6]
            Last_Name = User[7]
            Bank_Name = User[8]
            Address = User[9]
            Verified = User[10]
            Trading_Fee = User[11]
            Volume = User[12]
            #Now print fetched result
            print "Username: %s" %(Username)
            print "Password: %s" %(Password)
            print "Email: %s" %Email
            print "USD: %s" %USD_Credit
            print "BTC: %s" %BTC_Credit
            print "Join Date: %s" %Join_Date
            print "First Name: %s" %First_Name
            print "Last Name: %s" %Last_Name
            print "Bank: %s" %Bank_Name
            print "Address: %s" %Address
            print "Verified: %s" %Verified
            print "Trading Fee: %s" %Trading_Fee
            print "Volume: %s" %Volume
            break;
except:
    print "ERROR: Unable to fetch data"



'''Logging User'''



print ""
try:
    cursor.execute("""INSERT INTO UserLog(Username, Password, Email, FirstName, LastName) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Username, Password, Email, FirstName, LastName))
    db.commit()
    print "User Logged Successfully"
except:
    print "ERROR: Database Insert Log Failure"



'''Logging Control'''
    


Employee = "***333"

try:
    print ""
    cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Add User", Username, "All", Comment))
    db.commit()
    print "Control Successfully Logged"
except:
    print "ERROR: Control Unsuccessfully Logged"



db.close()
