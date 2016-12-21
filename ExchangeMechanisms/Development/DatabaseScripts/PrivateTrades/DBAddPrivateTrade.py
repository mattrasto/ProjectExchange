#-------------------------------------------------------------------------------
# Name:        DBAddPrivateTrade
# Version:     3.0
# Purpose:     Adds Private Trade with specified attributes to specified user
#
# Author:      Matthew
#
# Created:     05/31/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/15/2014
#-------------------------------------------------------------------------------

#Remove funds once trade is added
#Check if trade amount is below account balance

import MySQLdb
import sys

def main(Username, Price, Volume, TradeAction):
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    print ""
    
    
    
    '''Verifies Balances'''
    
    
    
    #Checks if order exists
    cursor.execute("""SELECT * FROM UserBook WHERE Username = "%s" """ % (Username))
    UserDetails = cursor.fetchone()
    #Exits if order is not found
    if UserDetails == None:
        print ""
        print "CRITICAL ERROR: User not found"
        sys.exit()
    AccountBalance = UserDetails[3]
    AccountVolume = UserDetails[4]
    
    #Checks for negative balances and exits if found
    if (AccountBalance < 0) or (AccountVolume < 0):
        print ""
        print "CRITICAL ERROR: User has negative balance"
        print "Exiting..."
        sys.exit()
    
    
    
    '''Assigning/Executing SQL Statements'''
    
    
    
    #Sets Order Type
    OrderType = "Private Trade"
    
    try:
        #Inserts record into IDBook
        cursor.execute("""INSERT INTO IDBook(Type, Action) VALUES("%s", "%s")""" % (OrderType, TradeAction.capitalize()))
        #Inserts record into PrivateTradeBook
        cursor.execute("""INSERT INTO PrivateTradeBook(Username, Price, Volume, Action) VALUES("%s", %f, %f, "%s")""" % (Username, Price, Volume, TradeAction.capitalize()))
        db.commit()
        print ""
        print "Trade Added Successfully"
        try:
            #Gathers and reads trade details
            cursor.execute("""SELECT * FROM PrivateTradeBook ORDER BY TradeNumber DESC LIMIT 1""")
            LatestOrders = cursor.fetchall()
            for Order in LatestOrders:
                print ""
                print "Trade added:"
                print ""
                TradeNumber = Order[0]
                Username = Order[1]
                Price = Order[2]
                Volume = Order[3]
                TradeAction = Order[4]
                DateEntered = Order[6]
                print "Trade Number: "+ str(TradeNumber)
                print "Trade Action: " + str(TradeAction)
                print "Username: " + str(Username)
                print "Price: " + str(Price)
                print "Volume: " + str(Volume)
                print "Date Entered: " + str(DateEntered)
                break;
        except:
            print "ERROR: Unable to fetch data"
    except:
        db.rollback()
        print "ERROR: Database Insert Failure"
    
    
    
    '''Logging Order'''
    
    
    
    #Inserts record into PrivateTradeLog
    try:
        cursor.execute("""INSERT INTO PrivateTradeLog(TradeNumber, Username, Price, Volume, Action) VALUES(%d, "%s", %d, %d, "%s")""" % (TradeNumber, Username, Price, Volume, TradeAction.capitalize()))
        db.commit()
        print ""
        print "Order Successfully Logged"
    except:
        print "ERROR: Database Log Insert Failure"
    
    
    
    '''Logging Control'''
        
    
    
    #Assigns static variables for logging control
    #Note: "Employee" value changes based on user submitting manual control
    Employee = "***333"
    TradeID = "Trade " + str(TradeNumber)
    Comment = "Added Private Trade"
    
    #Inserts record of action into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Add Private Trade", TradeID, "All", Comment))
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
    
    
    
    #Requests Username to put order under and verifies that it is valid
    while 1 == 1:
        Username = (raw_input("Username: ")).capitalize()
        cursor.execute("""SELECT * FROM UserBook WHERE Username = "%s" """ % (Username))
        UsernameList = cursor.fetchall()
        for User in UsernameList:
            if Username == User[0]:
                print "User found"
                AccountBalance = User[3]
                AccountVolume = User[4]
                break;
        else:
            print "User not found. Please enter again: "
    print ""
    print "User Balance: " + str(AccountBalance)
    print "User Volume: " + str(AccountVolume)
    print ""
    
    #Checks for negative balances and exits if found
    if (AccountBalance < 0) or (AccountVolume < 0):
        print "CRITICAL ERROR: User has negative balance"
        print "Exiting..."
        sys.exit()
    
    
    
    #Determines action of trade
    TradeAction = raw_input("Action (Buy/Sell): ")
    TradeAction = TradeAction.upper()
    while TradeAction != "BUY" and TradeAction != "SELL":
        print "Incorrect trade action. Please enter again:"
        TradeAction = raw_input("Action (Buy/Sell): ")
        TradeAction = TradeAction.upper()
    
    
    
    #Determines volume of trade
    Volume = raw_input("Volume: ")
    while 1 == 1:
        try:
            Volume = float(Volume)
            break;
        except:
            print "Volume must be an integer. Please enter again: "
            Volume = raw_input("Volume: ")
    #Checks if user tried to specify volume higher than available in account funds
    #Lowers order volume to account volume value if so
    if TradeAction == "SELL":
        if Volume > AccountVolume:
            print "Volume higher than balance. Defaulting to current balance."
            Volume = AccountVolume
            print "Volume: " + str(Volume)
    
    
    
    #Determines price per unit of trade
    Price = raw_input("Price: ")
    while 1 == 1:
        try:
            Price = float(Price)
            break;
        except:
            print "Price must be an integer. Please enter again: "
            Price = raw_input("Price: ")
    TradeTotal = Price * Volume
    #Checks if user tried to specify price higher than available in account funds
    #Lowers order volume to user's balance divided by specified price if so (Uses all of user's funds)
    if TradeAction == "BUY":
        if TradeTotal > AccountBalance:
            print "Total higher than balance. Lowering volume to minimum allowance:"
            Volume = (AccountBalance / Price)
            print "Volume: " + str(Volume)
    TradeTotal = Price * Volume
    
    
    
    print ""
    print "Trade Total: " + str(TradeTotal)
    
    
    
    #Execute
    main(Username, Price, Volume, TradeAction)


