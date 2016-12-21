#-------------------------------------------------------------------------------
# Name:        DBAddUser
# Version:     2.0
# Purpose:     Adds user with specified attributes
#
# Author:      Matthew
#
# Created:     07/16/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/15/2014
#-------------------------------------------------------------------------------

import MySQLdb
import sys

def main(Username, Password, Email, FirstName, LastName):
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    
    
    '''Verifies Username'''
    
    
    
    #Checks that UserLog does not contain duplicate Username
    cursor.execute("""SELECT Username FROM UserLog WHERE Username = "%s" """ % (Username))
    ExistingUsername = cursor.fetchone()
    if ExistingUsername != None:
        print ""
        print "CRITICAL ERROR: Username is already in use"
        sys.exit()
    else:
        #print ""
        #print "Username available"
        pass
    
    
    
    '''Verifies Email'''
    
    
    
    #Checks that UserLog does not contain duplicate Email
    cursor.execute("""SELECT Email FROM UserLog WHERE Email = "%s" """ % (Email))
    ExistingEmail = cursor.fetchone()
    if ExistingEmail != None:
        print ""
        print "CRITICAL ERROR: Email is already in use"
        sys.exit()
    else:
        #print ""
        #print "Email available"
        pass
    
    
    
    '''Defining/Executing SQL Statements'''
    
    
    
    #Partial (Required Field) manual INSERT query
    UserAdd = """INSERT INTO UserBook(Username, Password, Email, FirstName, LastName) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Username, Password, Email, FirstName, LastName)
    
    #Full manual INSERT query
    #UserAdd =  """INSERT INTO Users(Username, Password, Email, USDCredit, BTCCredit, JoinDate, FirstName, LastName, BankName, Address, Verified, TradingFee, Volume) \
            #VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")""" % \
            #(Username, Password, Email, USD, BTC, JoinDate, FirstName, LastName, BankName, Address, Verified, TradingFee, Volume)
    
    #Full automatic INSERT query
    #UserAdd =  """INSERT INTO Users(Username, Password, Email, USDCredit, BTCCredit, JoinDate, FirstName, LastName, BankName, Address, Verified, TradingFee, Volume) \
            #VALUES("***333", "***", "matthewrastovac@yahoo.com", 0 , 0, "4/3/14", "Matthew", "Rastovac", "Chase", "220 LHR", "Yes", .005, 10000)"""
    
    print ""
    try:
        cursor.execute(UserAdd)
        db.commit()
        print "Insert Successful"
    except:
        db.rollback()
        print "Insert Unsuccessful"
    
    
    
    #Prints out last database addition
    try:
        cursor.execute("""SELECT * FROM UserBook WHERE Username = "%s" """ % (Username))
        User = cursor.fetchone()
        if User != None:
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
        else:
            print "CRITICAL ERROR: User added but not found"
            sys.exit()
    except:
        print "ERROR: Unable to fetch data"
    
    
    
    '''Logging User'''
    
    
    
    #Inserts record into UserLog
    try:
        print ""
        cursor.execute("""INSERT INTO UserLog(Username, Password, Email, FirstName, LastName) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Username, Password, Email, FirstName, LastName))
        db.commit()
        print "User Logged Successfully"
    except:
        print "ERROR: Database Insert Log Failure"
    
    
    
    '''Logging Control'''
        
    
    
    #Assigns static variables for logging control
    #Note: "Employee" value changes based on user submitting manual control
    Employee = "***333"
    Comment = "Added User"
    
    #Inserts record of action into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Add User", Username, "All", Comment))
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
    
    
    
    '''Setting Variables'''
    
    
    
    #Requests Username and verifies that it is valid
    while 1 == 1:
        Username = (raw_input("Username: ")).capitalize()
        if Username != "":
            try:
                cursor.execute("""SELECT * FROM UserLog WHERE Username = "%s" """ % (Username))
                DuplicateUsers = cursor.fetchall()
                #Asks for input again if duplicate name found
                if DuplicateUsers != ():
                    print "User already exists. Please enter again:"
                else:
                    print "Username Available"
                    break;
            except:
                print "ERROR: Database fetch exception"
        else:
            print "Username must not be left blank. Please enter again: "
    
    
    
    #Requests Password and verifies that it is valid
    while 1 == 1:
        Password = raw_input("Password: ")
        if Password == "":
            print "Password must not be left blank. Please enter again: "
        else:
            break;
    
    
    
    #Requests Email and verifies that it is valid
    while 1 == 1:
        Email = (raw_input("Email: ")).capitalize()
        if Email != "":
            try:
                cursor.execute("""SELECT * FROM UserLog WHERE Email = "%s" """ % (Email))
                DuplicateEmails = cursor.fetchall()
                #Asks for input again if duplicate email found
                if DuplicateEmails != ():
                    print "Email already in use. Please enter again:"
                else:
                    print "Email Available"
                    break;
            except:
                print "ERROR: Database fetch exception"
        else:
            print "Email must not be left blank. Please enter again: "
    
    
    
    #Requests First Name and verifies that it is valid
    while 1 == 1:
        FirstName = (raw_input("First Name: ")).title()
        if FirstName == "":
            print "First Name must not be left blank. Please enter again: "
        else:
            break;
    
    
    
    #Requests Last Name and verifies that it is valid
    while 1 == 1:
        LastName = (raw_input("Last Name: ")).title()
        if LastName == "":
            print "Last Name must not be left blank. Please enter again: "
        else:
            break;
    
    
    
    #Sets comment for manual run
    print ""
    Comment = raw_input("Administrative Comment: ")
    
    
    #Execute
    main(Username, Password, Email, FirstName, LastName)


