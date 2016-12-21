#-------------------------------------------------------------------------------
# Name:        DBDeleteUser
# Version:     3.0
# Purpose:     Deletes specified user
#
# Author:      Matthew
#
# Created:     04/21/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/15/2014
#-------------------------------------------------------------------------------

import time
import MySQLdb
import sys



def main(Username):
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    
    
    '''Gathering User Details'''
    
    
    
    try:
        print ""
        cursor.execute("""SELECT * FROM UserBook WHERE Username = "%s" """ % (Username))
        User = cursor.fetchone()
        if User != None:
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
        else:
            print "CRITICAL ERROR: User not found"
            sys.exit()
    except SystemExit:
        sys.exit()
    except:
        print "ERROR: Database fetch exception"
        sys.exit()
    
    
    
    '''Gathering Related Orders'''
    
    
    
    #Searches for basic orders owned by user
    BasicOrderCheck = """SELECT * FROM BasicOrderBook WHERE Username = "%s" """ % (Username)
    cursor.execute(BasicOrderCheck)
    BasicOrderList = cursor.fetchall()
    
    #Searches for MTCs owned by user
    MTCCheck = """SELECT * FROM MTCBook WHERE Username = "%s" """ % (Username)
    cursor.execute(MTCCheck)
    MTCList = cursor.fetchall()
    
    #Searches for loans owned by user
    LoanCheck = """SELECT * FROM LoanBook WHERE Username = "%s" """ % (Username)
    cursor.execute(LoanCheck)
    LoanList = cursor.fetchall()
    
    #Searches for private trades owned by user
    PrivateTradeCheck = """SELECT * FROM PrivateTradeBook WHERE Username = "%s" """ % (Username)
    cursor.execute(PrivateTradeCheck)
    PrivateTradeList = cursor.fetchall()
    
    
    
    '''Defining/Executing SQL Statement'''
    
    
    
    #Gets current time and formats for database insertion
    LocalTime = time.localtime(time.time())
    LocalTimeMinutes = LocalTime[4]
    LocalTimeSeconds = LocalTime[5]
    if LocalTimeMinutes < 10:
        LocalTimeMinutes = "0" + str(LocalTimeMinutes)
    if LocalTimeSeconds < 10:
        LocalTimeSeconds = "0" + str(LocalTimeSeconds)
    FormattedDate = str(LocalTime[0]) + "-" +  str(LocalTime[1]) + "-" +  str(LocalTime[2])
    FormattedTime = str(LocalTime[3]) + ":" +  str(LocalTimeMinutes) + ":" +  str(LocalTimeSeconds)
    FormattedDateTime = str(FormattedDate) + " " + str(FormattedTime)
    
    
    
    #Deletes user from UserBook
    try:
        cursor.execute("DELETE FROM UserBook WHERE Username = %s", (Username))
        db.commit()
        print "Delete Successful"
    except:
        print "Delete Unsuccessful"
    
    
    
    #Reads user details
    print ""
    print "------------------------------"
    print "User deleted:"
    print "------------------------------"
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
    
    
    
    '''Printing Related Orders'''
    
    
    
    #Reads basic orders owned by user
    print ""
    print "------------------------------"
    print "Deleted Basic Orders:"
    print "------------------------------"
    print ""
    for BasicOrder in BasicOrderList:
        print "Order Number: " + str(BasicOrder[0])
    
    #Reads MTCs owned by user
    print ""
    print "------------------------------"
    print "Deleted MTC's:"
    print "------------------------------"
    print ""
    for MTC in MTCList:
        print "Order Number: " + str(MTC[0])
    
    #Reads loans owned by user
    print ""
    print "------------------------------"
    print "Deleted Loans:"
    print "------------------------------"
    print ""
    for Loan in LoanList:
        print "Order Number: " + str(Loan[0])
    
    #Reads private trades owned by user
    print ""
    print "------------------------------"
    print "Deleted Private Trades:"
    print "------------------------------"
    print ""
    for PrivateTrade in PrivateTradeList:
        print "Order Number: " + str(PrivateTrade[0])
    
    
    
    
    '''Logging User Deletion'''
    
    
    
    Comment = "Deleted User"
    
    #Updates UserLog with DeletionComment and DeletionDate (Current date)
    try:
        print ""
        cursor.execute("UPDATE UserLog SET DeletionComment = %s, DeletionDate = %s WHERE Username = %s", (Comment, FormattedDateTime, Username))
        db.commit()
        print "User Deletion Logged Successfully"
    except:
        print "ERROR: Database Insert Log Failure"
    
    
    
    '''Logging Control'''
        
    
    
    #Assigns static variables for logging control
    #Note: "Employee" value changes based on user submitting manual control
    Employee = "***333"
    
    #Inserts record of action into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Delete User", Username, "All", Comment))
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
    
    
    
    #Requests Username and verifies that it is valid
    while 1 == 1:
        Username = (raw_input("Username: ")).capitalize()
        cursor.execute("""SELECT * FROM UserBook WHERE Username = "%s" """ % (Username))
        Username = cursor.fetchone()
        if Username != None:
            print "User found"
            break;
        else:
            print "User not found. Please enter again: "
    
    
    
    main(Username)


