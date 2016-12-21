#-------------------------------------------------------------------------------
# Name:        DBAddBasicOrder
# Version:     3.0
# Purpose:     Adds Basic Order with specified attributes to specified user
#
# Author:      Matthew
#
# Created:     04/14/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/25/2014
#-------------------------------------------------------------------------------

#Remove funds once order is added

import sys
import MySQLdb



def main(Username, Price, Volume, OrderType, OrderAction, TriggerType, TriggerValue):
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database version: "+ str(Data)
    
    
    
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
    
    
    
    
    '''Verifies Trading Fee Applicability'''
    
    
    
    TradingFee = UserDetails[11]
    if OrderAction == "BUY":
        if (Price + (Price * TradingFee)) > AccountBalance:
            print "CRITICAL ERROR: User's balance is too low to apply order at current price and trading fee"
            print Price
            print TradingFee
            print AccountBalance
            sys.exit()
    elif OrderAction == "SELL":
        if (Volume + (Volume * TradingFee)) > AccountVolume:
            print "CRITICAL ERROR: User's balance is too low to apply order at current price and trading fee"
            print Price
            print TradingFee
            print AccountBalance
            sys.exit()
    else:
        print "CRITICAL ERROR: Order has no action"
        sys.exit()
        
    
    
    
    '''Assigning/Executing SQL Statements'''
    
    
    
    #Assigning query statements depending on order type
    if OrderType == "CONDITIONAL":
        InsertQuery = """INSERT INTO BasicOrderBook(Username, Price, Volume, Type, Action, TriggerType, TriggerValue) VALUES("%s", %f, %f, "%s", "%s", "%s", %f)""" % (Username, Price, Volume, OrderType.capitalize(), OrderAction.capitalize(), TriggerType.title(), TriggerValue)
    elif OrderType == "LIQUID":
        InsertQuery = """INSERT INTO BasicOrderBook(Username, Price, Volume, Type, Action, Active) VALUES("%s", %f, %f, "%s", "%s", %d)""" % (Username, Price, Volume, OrderType.capitalize(), OrderAction.capitalize(), 1)
    elif OrderType == "LIMIT":
        InsertQuery = """INSERT INTO BasicOrderBook(Username, Price, Volume, Type, Action) VALUES("%s", %f, %f, "%s", "%s")""" % (Username, Price, Volume, OrderType.capitalize(), OrderAction.capitalize())
    else:
        print "CRITICAL ERROR: Invalid Order Type"
        sys.exit()
    
    
    
    try:
        #Inserts record into IDBook
        cursor.execute("""INSERT INTO IDBook(Type, Action) VALUES("%s", "%s")""" % (OrderType.capitalize(), OrderAction.capitalize()))
        #Inserts order into BasicOrderBook
        cursor.execute(InsertQuery)
        db.commit()
        print ""
        print "Order Added Successfully"
        try:
            #Gathers and reads order details
            cursor.execute("""SELECT * FROM BasicOrderBook ORDER BY OrderNumber DESC LIMIT 1""")
            LatestOrders = cursor.fetchall()
            for Order in LatestOrders:
                print ""
                print "Order added:"
                print ""
                OrderNumber = Order[0]
                Username = Order[1]
                Price = Order[2]
                Volume = Order[3]
                OrderType = Order[4]
                OrderAction = Order[5]
                if OrderType == "CONDITIONAL":
                    TriggerType = Order[6]
                    TriggerValue = Order[7]
                Active = Order[8]
                DateEntered = Order[9]
                print "Order Number: "+ str(OrderNumber)
                print "Order Type: " + str(OrderType)
                print "Order Action: " + str(OrderAction)
                print "Username: " + str(Username)
                print "Price: " + str(Price)
                print "Volume: " + str(Volume)
                if OrderType.upper() == "CONDITIONAL":
                    print "Trigger Type: " + (str(TriggerType)).title()
                    print "Trigger Value: " + str(TriggerValue)
                print "Active: " + str(Active)
                print "Date Entered: " + str(DateEntered)
                break;
        except:
            print "ERROR: Unable to fetch data"
    except:
        db.rollback()
        print "ERROR: Database Insert Failure"
    
    
    
    '''Logging Order'''
    
    
    
    #Assigning query statements depending on order type
    if OrderType == "Conditional":
        Log = ("""INSERT INTO BasicOrderLog(OrderNumber, Username, Price, Volume, Type, Action, TriggerType, TriggerValue) VALUES(%d, "%s", %f, %f, "%s", "%s", "%s", %f)""" % (OrderNumber, Username, Price, Volume, OrderType.capitalize(), OrderAction.capitalize(), TriggerType.title(), TriggerValue))
    elif OrderType == "Liquid":
        Log = """INSERT INTO BasicOrderLog(OrderNumber, Username, Price, Volume, Type, Action) VALUES(%d, "%s", %f, %f, "%s", "%s")""" % (OrderNumber, Username, Price, Volume, OrderType.capitalize(), OrderAction.capitalize())
    elif OrderType == "Limit":
        Log = """INSERT INTO BasicOrderLog(OrderNumber, Username, Price, Volume, Type, Action) VALUES(%d, "%s", %f, %f, "%s", "%s")""" % (OrderNumber, Username, Price, Volume, OrderType.capitalize(), OrderAction.capitalize())
    else:
        print "CRITICAL ERROR: Invalid Order Type"
        sys.exit()
    
    
    
    #Inserts record into BasicOrderLog
    try:
        cursor.execute(Log)
        db.commit()
        print ""
        print "Order Successfully Logged"
    except:
        print "ERROR: Database Log Insert Failure"
    
    
    
    '''Logging Control'''
        
    
    
    #Assigns static variables for logging control
    #Note: "Employee" value changes based on user submitting manual control
    Employee = "***333"
    OrderID = "Order " + str(OrderNumber)
    Comment = "Added Basic Order"
    
    #Inserts record of action into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Add Basic Order", OrderID, "All", Comment))
        db.commit()
        print "Control Successfully Logged"
    except:
        print "ERROR: Control Unsuccessfully Logged"
    
    
    
    db.close()
    
    return OrderNumber



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
        User = cursor.fetchone()
        if Username != None:
            AccountBalance = User[3]
            AccountVolume = User[4]
            print "User found"
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
    
    
    
    #Determines basic order type of order
    OrderType = raw_input("Type (Liquid/Limit/Conditional): ")
    OrderType = OrderType.upper()
    while OrderType != "LIQUID" and OrderType != "LIMIT" and OrderType != "CONDITIONAL":
        print "Incorrect order type. Please enter again:"
        OrderType = raw_input("Type (Liquid/Limit/Conditional): ")
        OrderType = OrderType.upper()
    
    
    
    #Determines action of order
    OrderAction = raw_input("Action (Buy/Sell): ")
    OrderAction = OrderAction.upper()
    while OrderAction != "BUY" and OrderAction != "SELL":
        print "Incorrect order action. Please enter again:"
        OrderAction = raw_input("Action (Buy/Sell): ")
        OrderAction = OrderAction.upper()
    
    
    
    #Determines volume of order
    Volume = raw_input("Volume: ")
    while 1 == 1:
        try:
            Volume = float(Volume)
            if Volume > 0:
                break;
            else:
                print "Volume must be higher than 0. Please enter again: "
                Volume = raw_input("Volume: ")
        except:
            print "Volume must be an integer. Please enter again: "
            Volume = raw_input("Volume: ")
    #Checks if user tried to specify volume higher than available in account funds
    #Lowers order volume to account volume value if so
    if OrderAction == "SELL":
        if Volume > AccountVolume:
            print "Volume higher than balance. Defaulting to current balance."
            Volume = AccountVolume
            print "Volume: " + str(Volume)
    
    
    
    #Determines price per unit of order
    Price = raw_input("Price: ")
    while 1 == 1:
        try:
            Price = float(Price)
            break;
        except:
            print "Price must be an integer. Please enter again: "
            Price = raw_input("Price: ")
    OrderTotal = Price * Volume
    #Checks if user tried to specify price higher than available in account funds
    #Lowers order volume to user's balance divided by specified price if so (Uses all of user's funds)
    if OrderAction == "BUY":
        if OrderTotal > AccountBalance:
            print "Total higher than balance. Lowering volume to minimum allowance:"
            Volume = (AccountBalance / Price)
            print "Volume: " + str(Volume)
    
    #Calculates order total
    OrderTotal = Price * Volume
    print ""
    print "Order Total: " + str(OrderTotal)
    
    
    
    #Sets trigger types if order type is conditional
    if OrderType == "CONDITIONAL":
        TriggerType = raw_input("Trigger Type (Bid Price, Ask Price, Latest Price, Average Price): ")
        TriggerType = TriggerType.upper()
        while TriggerType != "BIDPRICE" and TriggerType != "ASKPRICE" and TriggerType != "LATESTPRICE" and TriggerType != "AVERAGEPRICE" and TriggerType != "BID PRICE" and TriggerType != "ASK PRICE" and TriggerType != "LATEST PRICE" and TriggerType != "AVERAGE PRICE":
            print "Incorrect order trigger type. Please enter again:"
            TriggerType = raw_input("Trigger Type: ")
            TriggerType = TriggerType.upper()
        if TriggerType == "BIDPRICE":
            TriggerType = "BID PRICE"
        elif TriggerType == "ASKPRICE":
            TriggerType = "ASK PRICE"
        elif TriggerType == "LATESTPRICE":
            TriggerType = "LATEST PRICE"
        elif TriggerType == "AVERAGEPRICE":
            TriggerType = "AVERAGE PRICE"
        
        
        
        #Sets trigger value of order type is conditional
        TriggerValue = raw_input("Trigger Value: ")
        while 1 ==1:
            try:
                TriggerValue = float(TriggerValue)
                break;
            except:
                print "Trigger Value must be an integer. Please enter again: "
                TriggerValue = raw_input("Trigger Value: ")
    else:
        TriggerType = ""
        TriggerValue = ""
    
    
    
    #Sets comment for manual run
    print ""
    Comment = raw_input("Administrative Comment: ")
    
    
    
    #Execute
    if Price != None and Volume != None:
        main(Username, Price, Volume, OrderType, OrderAction, TriggerType, TriggerValue);
    else:
        print ""
        print "ERROR: Price or Volume are undefined"
    
    
    