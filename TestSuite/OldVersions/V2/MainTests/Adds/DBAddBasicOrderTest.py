#-------------------------------------------------------------------------------
# Name:        DBAddBasicOrderTest
# Version:     2.0
# Purpose:     Load and Remote Testing for DBAddBasicOrder
#
# Author:      Matthew
#
# Created:     07/16/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    08/30/2014
#-------------------------------------------------------------------------------

import time
import random
import sys

#Starts timer
TimerStart = time.clock()

#Defines project path
sys.path.insert(0, "C:\Programming\ExchangeMechanisms\Development")

#Imports main module
import DatabaseScripts.BasicOrders.DBAddBasicOrder as Mod

print ""
print "Mod Finished Importing"



#User to make orders under
Username = "Username0"

#Number of each order to make
LimitLoops = 20
LiquidLoops = 20
ConditionalLoops = 20



#Random Number (.00 Specificity) Generators

def RandomPrice():
    PriceInt = random.randrange(690, 710)
    PriceDec = random.random()
    PriceDec = str(PriceDec)[:4]
    Price = PriceInt + float(PriceDec)
    return Price

def RandomVolume():
    VolumeInt = random.randrange(1, 3)
    VolumeDec = random.random()
    VolumeDec = str(VolumeDec)[:4]
    Volume = VolumeInt + float(VolumeDec)
    return Volume



#Execute

for x in range(0, LimitLoops):
    print ""
    print "----------Starting Round: " + str(x + 1) + "----------"
    print ""
    Price = RandomPrice()
    Volume = RandomVolume()
    OrderType = "LIMIT"
    OrderAction = random.choice(["BUY", "SELL"])
    TriggerType = ""
    TriggerValue = ""
    Mod.main(Username, Price, Volume, OrderType, OrderAction, TriggerType, TriggerValue)

for x in range(0, LiquidLoops):
    print ""
    print "----------Starting Round: " + str(x + 1) + "----------"
    print ""
    Price = RandomPrice()
    Volume = RandomVolume()
    OrderType = "LIQUID"
    OrderAction = random.choice(["BUY", "SELL"])
    TriggerType = ""
    TriggerValue = ""
    Mod.main(Username, Price, Volume, OrderType, OrderAction, TriggerType, TriggerValue)

for x in range(0, ConditionalLoops):
    print ""
    print "----------Starting Round: " + str(x + 1) + "----------"
    print ""
    Price = RandomPrice()
    Volume = RandomVolume()
    OrderType = "CONDITIONAL"
    OrderAction = random.choice(["BUY", "SELL"])
    TriggerType = random.choice(["BID PRICE", "ASK PRICE", "LATEST PRICE", "AVERAGE PRICE"])
    TriggerValue = RandomPrice()
    Mod.main(Username, Price, Volume, OrderType, OrderAction, TriggerType, TriggerValue)



#Ends timer
TimerEnd = time.clock()
TimePassed = TimerEnd - TimerStart

print ""
print "Run Time: " + str(TimePassed) + " Seconds"


