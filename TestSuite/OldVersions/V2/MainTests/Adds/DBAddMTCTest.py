#-------------------------------------------------------------------------------
# Name:        DBAddMTCTest
# Version:     2.0
# Purpose:     Load and Remote Testing for DBAddMTC
#
# Author:      Matthew
#
# Created:     07/29/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/15/2014
#-------------------------------------------------------------------------------

import time
import random
import sys

#Starts timer
TimerStart = time.clock()

#Defines project path
sys.path.insert(0, "C:\Programming\ExchangeMechanisms\Development")

#Imports main module
import DatabaseScripts.MTCs.DBAddMTC as Mod

print ""
print "Mod Finished Importing"



#User to make MTC's under
Username = "Username0"

#Number of MTC's to make
Loops = 10



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

#Random Interval Generators

def RandomInterestCompoundRate():
    Interval = random.choice(["SECOND", "MINUTE", "HOUR", "DAY"])
    Value = random.randrange(1, 1000)
    InterestCompoundRate = str(Value) + " " +  Interval
    return InterestCompoundRate

def RandomDuration():
    global Duration
    global DurationTuple
    Interval = random.choice(["SECOND", "MINUTE", "HOUR", "DAY"])
    Value = random.randrange(1, 1000)
    Duration = str(Value) + " " + Interval
    DurationTuple = (Value, Interval)

#Constraint Generators

def RandomMinimumBorrowerConstraint():
    global MinimumBorrowerConstraintType
    global MinimumBorrowerConstraintValue
    MinimumBorrowerConstraintType = random.choice(["ACCOUNT BALANCE", "LIQUIDITY VALUE"])
    MinimumBorrowerConstraintValue = random.randrange(1, 10000)

def RandomUserInterventionConstraint():
    global UserInterventionConstraintType
    global UserInterventionConstraintValue
    UserInterventionConstraintType = random.choice(["MARKET PRICE", "PROFIT MARGIN", "INTEREST RATE"])
    if UserInterventionConstraintType == "MARKET PRICE":
        UserInterventionConstraintValue = random.randrange(500, 800)
    elif UserInterventionConstraintType == "PROFIT MARGIN":
        UserInterventionConstraintValue = random.randrange(1, 100)
    elif UserInterventionConstraintType == "INTEREST RATE":
        UserInterventionConstraintValue = random.random()



#Execute

for x in range(0, Loops):
    print ""
    print "----------Starting Round: " + str(x + 1) + "----------"
    print ""
    Price = RandomPrice()
    Volume = RandomVolume()
    OrderAction = random.choice(["LOAN", "BORROW"])
    InterestCompoundRate = RandomInterestCompoundRate()
    InterestRate = random.random()
    RandomDuration()
    StopLossPrice = Price - 20
    FulfillmentPrice = Price + 20
    DividendType = random.choice(["FLAT", "PERCENT"])
    RandomMinimumBorrowerConstraint()
    RandomUserInterventionConstraint()
    Mod.main(Username, Price, Volume, OrderAction, InterestCompoundRate, InterestRate, StopLossPrice, FulfillmentPrice, Duration, DurationTuple, DividendType, MinimumBorrowerConstraintType, MinimumBorrowerConstraintValue, UserInterventionConstraintType, UserInterventionConstraintValue)



#Ends timer
TimerEnd = time.clock()
TimePassed = TimerEnd - TimerStart

print ""
print "Run Time: " + str(TimePassed) + " Seconds"


