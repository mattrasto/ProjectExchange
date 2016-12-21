#-------------------------------------------------------------------------------
# Name:        DBAddPrivateTrade
# Version:     1.0
# Purpose:
#
# Author:      Matthew
#
# Created:     05/31/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    06/01/2014
#-------------------------------------------------------------------------------

import MySQLdb

db = MySQLdb.connect("localhost","root","***","exchangedatabase")

cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data



'''Setting Variables'''



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



TradeAction = raw_input("Action (Buy/Sell): ")
TradeAction = TradeAction.upper()
while TradeAction != "BUY" and TradeAction != "SELL":
    print "Incorrect trade action. Please enter again:"
    TradeAction = raw_input("Action (Buy/Sell): ")
    TradeAction = TradeAction.upper()



Volume = raw_input("Volume: ")
while 1 == 1:
    try:
        Volume = float(Volume)
        break;
    except:
        print "Volume must be an integer. Please enter again: "
        Volume = raw_input("Volume: ")
if TradeAction == "SELL":
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
TradeTotal = Price * Volume
if TradeAction == "BUY":
    if TradeTotal > AccountBalance:
        print "Total higher than balance. Lowering volume to minimum allowance:"
        Volume = (AccountBalance / Price)
        print "Volume: " + str(Volume)
TradeTotal = Price * Volume



print ""
print "Trade Total: " + str(TradeTotal)



print ""
Comment = raw_input("Administrative Comment: ")



'''Assigning/Executing SQL Statements'''



sql = """INSERT INTO PrivateTradeBook(Username, Price, Volume, Action) VALUES("%s", %d, %d, "%s")""" % (Username, Price, Volume, TradeAction.capitalize())
    
try:
    cursor.execute("""INSERT INTO IDBook(Type, Action) VALUES("%s", "%s")""" % ("Private Trade", TradeAction.capitalize()))
    cursor.execute(sql)
    db.commit()
    print ""
    print "Trade Added Successfully"
    try:
        cursor.execute("""SELECT * FROM PrivateTradeBook ORDER BY TradeNumber DESC LIMIT 1""")
        LatestOrders = cursor.fetchall()
        for Order in LatestOrders:
            print Order
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



log = ("""INSERT INTO PrivateTradeLog(TradeNumber, Username, Price, Volume, Action) VALUES(%d, "%s", %d, %d, "%s")""" % (TradeNumber, Username, Price, Volume, TradeAction.capitalize()))

try:
    cursor.execute(log)
    db.commit()
    print ""
    print "Order Successfully Logged"
except:
    print "ERROR: Database Log Insert Failure"



'''Logging Control'''
    


Employee = "***333"

TradeID = "Trade " + str(TradeNumber)

try:
    print ""
    cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Add Private Trade", TradeID, "All", Comment))
    db.commit()
    print "Control Successfully Logged"
except:
    print "ERROR: Control Unsuccessfully Logged"



db.close()