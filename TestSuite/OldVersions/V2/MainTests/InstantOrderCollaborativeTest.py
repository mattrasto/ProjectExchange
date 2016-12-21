#-------------------------------------------------------------------------------
# Name:        InstantOrderCollaborativeTest
# Version:     2.0
# Purpose:     Load and Remote Testing for InstantOrderCollaborative
#
# Author:      Matthew
#
# Created:     07/22/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    07/31/2014
#-------------------------------------------------------------------------------

import time
import MySQLdb
import random
import sys

#Starts timer
TimerStart = time.clock()

#Defines project path
sys.path.insert(0, "C:\Programming\ExchangeMechanisms\Development")

#Imports main module
import InstantOrderCollaborative as Mod

print ""
print "Mod Finished Importing"
print ""



#Initializes database

def Initialize():
    
    global db
    global cursor
    
    #Initializing database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)



Initialize()
cursor.execute("""SELECT COUNT(*) FROM TransactionLog""")
InitialTransactionCount = cursor.fetchone()[0]
#print ""
#print "Initial Transaction Count: " + str(InitialTransactionCount)
db.close()



#Number of instant orders to make
Loops = 10

#User to make orders under
OrderAccount = "Username0"

#Percentage chance that the OrderConstraint will be "PRICE"
ConstraintPercentage = .5

#Random Number (.00 Specificity) Generators

def RandomPrice():
    global Price
    PriceInt = random.randrange(690, 710)
    PriceDec = random.random()
    PriceDec = str(PriceDec)[:4]
    Price = PriceInt + float(PriceDec)

def RandomVolume():
    global Volume
    VolumeInt = random.randrange(1, 3)
    VolumeDec = random.random()
    VolumeDec = str(VolumeDec)[:4]
    Volume = VolumeInt + float(VolumeDec)



#Manual confirmation for orders
#Options: Yes/No in any capitalization
Confirmation = "NO"

#Execute

FinishedTransactions = 0

for x in range(0, Loops):
    print ""
    print "----------Starting Round: " + str(x + 1) + "----------"
    print ""
    if x % 2 == 0:
        OrderAction = "BUY"
    else:
        OrderAction = "SELL"
    if random.random() <= ConstraintPercentage:
        OrderConstraint = "PRICE"
        RandomPrice()
        Volume = None
    else:
        OrderConstraint = "VOLUME"
        Price = None
        RandomVolume()
    FinishedTransactions += 1
    
    
    
    print "------------------------------"
    print "Testing Parameters:"
    print "Order Account: " + str(OrderAccount)
    print "Order Action: " + str(OrderAction)
    print "Order Constraint: " + str(OrderConstraint)
    print "Price: " + str(Price)
    print "Volume: " + str(Volume)
    print "Confirmation: " + str(Confirmation)
    print "------------------------------"
    print ""
        
    Mod.main(OrderAccount, OrderAction, OrderConstraint, Price, Volume, Confirmation)



print ""
Initialize()
cursor.execute("""SELECT COUNT(*) FROM TransactionLog""")
FinalTransactionCount = cursor.fetchone()[0]
#print ""
#print "Final Transaction Count: " + str(FinalTransactionCount)
db.close()

TransactionsProcessed = FinalTransactionCount - InitialTransactionCount



print ""
print "Test Completed"
print "Orders Created: " + str(FinishedTransactions)
print "Transactions Processed: " + str(TransactionsProcessed)

#Ends timer
TimerEnd = time.clock()
TimePassed = TimerEnd - TimerStart

print ""
print "Run Time: " + str(TimePassed) + " Seconds"


