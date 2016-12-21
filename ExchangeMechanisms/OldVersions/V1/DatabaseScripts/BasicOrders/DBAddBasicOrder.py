#-------------------------------------------------------------------------------
# Name:        DBAddBasicOrder
# Version:     1.0
# Purpose:
#
# Author:      Matthew
#
# Created:     04/14/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    05/31/2014
#-------------------------------------------------------------------------------

import MySQLdb

db = MySQLdb.connect("localhost","root","***","exchangedatabase")

cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data



'''Setting Variables'''



OrderType = raw_input("Type (Liquid/Limit/Conditional): ")
OrderType = OrderType.upper()
while OrderType != "LIQUID" and OrderType != "LIMIT" and OrderType != "CONDITIONAL":
    print "Incorrect order type. Please enter again:"
    OrderType = raw_input("Type (Liquid/Limit/Conditional): ")
    OrderType = OrderType.upper()



OrderAction = raw_input("Action (Buy/Sell): ")
OrderAction = OrderAction.upper()
while OrderAction != "BUY" and OrderAction != "SELL":
    print "Incorrect order action. Please enter again:"
    OrderAction = raw_input("Action (Buy/Sell): ")
    OrderAction = OrderAction.upper()



Username = raw_input("Username: ")
#Username = "***333"
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
cursor.execute("""SELECT * FROM UserBook WHERE Username = "%s" """ % (Username))
UserDetails = cursor.fetchone()
AccountBalance = UserDetails[3]
AccountVolume = UserDetails[4]
print ""
print "User Balance: " + str(AccountBalance)
print "User Volume: " + str(AccountVolume)
print ""



Volume = raw_input("Volume: ")
while 1 == 1:
    try:
        Volume = float(Volume)
        break;
    except:
        print "Volume must be an integer. Please enter again: "
        Volume = raw_input("Volume: ")
if OrderAction == "SELL":
    if Volume > AccountVolume:
        print "Volume higher than balance. Defaulting to current balance."
        Volume = AccountVolume
        print "Volume: " + str(Volume)



Price = raw_input("Price: ")
while 1 == 1:
    try:
        Price = float(Price)
        break;
    except:
        print "Price must be an integer. Please enter again: "
        Price = raw_input("Price: ")
OrderTotal = Price * Volume
if OrderAction == "BUY":
    if OrderTotal > AccountBalance:
        print "Total higher than balance. Lowering volume to minimum allowance:"
        Volume = (AccountBalance / Price)
        print "Volume: " + str(Volume)
OrderTotal = Price * Volume



print ""
print "Order Total: " + str(OrderTotal)



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
    
    
    
    TriggerValue = raw_input("Trigger Value: ")
    while 1 ==1:
        try:
            TriggerValue = float(TriggerValue)
            break;
        except:
            print "Trigger Value must be an integer. Please enter again: "
            TriggerValue = raw_input("Trigger Value: ")

print ""
Comment = raw_input("Administrative Comment: ")


'''Assigning/Executing SQL Statements'''



if OrderType == "CONDITIONAL":
    sql = """INSERT INTO BasicOrderBook(Username, Price, Volume, Type, Action, TriggerType, TriggerValue) VALUES("%s", %d, %d, "%s", "%s", "%s", %d)""" % (Username, Price, Volume, OrderType.capitalize(), OrderAction.capitalize(), TriggerType.title(), TriggerValue)
elif OrderType == "LIQUID":
    sql = """INSERT INTO BasicOrderBook(Username, Price, Volume, Type, Action, Active) VALUES("%s", %d, %d, "%s", "%s", %d)""" % (Username, Price, Volume, OrderType.capitalize(), OrderAction.capitalize(), 1)
else:
    sql = """INSERT INTO BasicOrderBook(Username, Price, Volume, Type, Action) VALUES("%s", %d, %d, "%s", "%s")""" % (Username, Price, Volume, OrderType.capitalize(), OrderAction.capitalize())
    
try:
    cursor.execute("""INSERT INTO IDBook(Type, Action) VALUES("%s", "%s")""" % (OrderType.capitalize(), OrderAction.capitalize()))
    cursor.execute(sql)
    db.commit()
    print ""
    print "Order Added Successfully"
    try:
        cursor.execute("""SELECT * FROM BasicOrderBook ORDER BY OrderNumber DESC LIMIT 1""")
        LatestOrders = cursor.fetchall()
        for Order in LatestOrders:
            print Order
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
                ConditionalActive = Order[8]
            DateEntered = Order[9]
            print "Order Number: "+ str(OrderNumber)
            print "Order Type: " + str(OrderType)
            print "Order Action: " + str(OrderAction)
            print "Username: " + str(Username)
            print "Price: " + str(Price)
            print "Volume: " + str(Volume)
            if OrderType == "CONDITIONAL":
                print "Trigger Type: " + str(TriggerType)
                print "Trigger Value: " + str(TriggerValue)
                print "Active: " + str(ConditionalActive)
            print "Date Entered: " + str(DateEntered)
            break;
    except:
        print "ERROR: Unable to fetch data"
except:
    db.rollback()
    print "ERROR: Database Insert Failure"



'''Logging Order'''



if OrderType == "Conditional":
    log = ("""INSERT INTO BasicOrderLog(OrderNumber, Username, Price, Volume, Type, Action, TriggerType, TriggerValue) VALUES(%d, "%s", %d, %d, "%s", "%s", "%s", %d)""" % (OrderNumber, Username, Price, Volume, OrderType.capitalize(), OrderAction.capitalize(), TriggerType.title(), TriggerValue))
elif OrderType == "Liquid":
    log = """INSERT INTO BasicOrderLog(OrderNumber, Username, Price, Volume, Type, Action) VALUES(%d, "%s", %d, %d, "%s", "%s")""" % (OrderNumber, Username, Price, Volume, OrderType.capitalize(), OrderAction.capitalize())
else:
    log = """INSERT INTO BasicOrderLog(OrderNumber, Username, Price, Volume, Type, Action) VALUES(%d, "%s", %d, %d, "%s", "%s")""" % (OrderNumber, Username, Price, Volume, OrderType.capitalize(), OrderAction.capitalize())

try:
    cursor.execute(log)
    db.commit()
    print ""
    print "Order Successfully Logged"
except:
    print "ERROR: Database Log Insert Failure"



'''Logging Control'''
    


Employee = "***333"

OrderID = "Order " + str(OrderNumber)

try:
    print ""
    cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Add Basic Order", OrderID, "All", Comment))
    db.commit()
    print "Control Successfully Logged"
except:
    print "ERROR: Control Unsuccessfully Logged"



db.close()