#-------------------------------------------------------------------------------
# Name:        InstantOrderCollaborative
# Version:     1.3
# Purpose:     Improved version of InstantOrderCollaborative-v1.1
#
# Author:      Matthew
#
# Created:     05/04/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    05/12/2014
#-------------------------------------------------------------------------------

#Add Credit Updating
#Add Balance/Volume Stops

from __future__ import division
import time
import MySQLdb

db = MySQLdb.connect("localhost","root","***","exchangedatabase")

cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data

global TransactionCount

try:
    cursor.execute("""SELECT MAX(TransactionNumber) FROM TransactionLog""")
    MaxOrderNumber = cursor.fetchone()[0]
    TransactionCount = MaxOrderNumber + 1
    print ""
    print "Transaction Number: " +str(TransactionCount)
except:
    TransactionCount = 1
    print
    print "Transaction Number: " +str(TransactionCount)



'''Setting Variables'''



#Testing variables:
OrderNumber = 50
OrderAccount = "***333"
OrderType = "Instant"
TradingFeeProfit = 0



cursor.execute("""SELECT * FROM UserBook WHERE Username = "%s" """ % (OrderAccount))
UserDetails = cursor.fetchone()
InstantOrderAccountBalance = UserDetails[3]
InstantOrderAccountVolume = UserDetails[4]
print ""
print "User Balance: " + str(InstantOrderAccountBalance)
print "User Volume: " + str(InstantOrderAccountVolume)
print ""

OrderAction = raw_input("Action (Buy/Sell): ")
OrderAction = OrderAction.upper()
while OrderAction != "BUY" and OrderAction != "SELL":
    print "Incorrect action. Please enter again:"
    OrderAction = raw_input("Action (Buy/Sell): ")
    OrderAction = OrderAction.upper()

OrderConstraint = raw_input("Place By (Price/Volume): ")
OrderConstraint = OrderConstraint.upper()
while OrderConstraint != "PRICE" and OrderConstraint != "VOLUME":
    print "Incorrect order constraint. Please enter again:"
    OrderConstraint = raw_input("Place By (Price/Volume): ")
    OrderConstraint = OrderConstraint.upper()

if OrderConstraint == "PRICE":
    Price = raw_input("Absolute Total: ")
    while 1 == 1:
        try:
            Price = float(Price)
            break;
        except:
            print "Total must be an integer. Please enter again: "
            Price = raw_input("Absolute Total: ")
    if OrderAction == "BUY":
        if Price > UserDetails[3]:
            print "Total higher than balance. Defaulting to current balance."
            Price = UserDetails[3]
        print "Price: " + str(Price)

elif OrderConstraint == "VOLUME":
    Volume = raw_input("Volume: ")
    while 1 == 1:
        try:
            Volume = float(Volume)
            break;
        except:
            print "Volume must be an integer. Please enter again: "
            Volume = raw_input("Volume: ")
    if OrderAction == "SELL":
        if Volume > UserDetails[4]:
            print "Volume higher than balance. Defaulting to current balance."
            Volume = UserDetails[4]
        print "Volume: " + str(Volume)



'''Checking Bid/Ask Prices'''



def BidPriceChecker():
    global BidPrice
    cursor.execute("""SELECT MAX(Price) FROM BasicOrderBook WHERE Action = "Buy" AND NOT (Type = "Conditional" AND Active = 0)""")
    MinOrderList = cursor.fetchall()
    #print MinOrderList
    MinOrder = MinOrderList[0]
    #print MinOrder
    BidPrice = MinOrder[0]
    if BidPrice == None:
        print "No Bid Price"
        BidPrice = 0
    else:
        print "Bid Price: " + str(BidPrice)


def AskPriceChecker():
    global AskPrice
    cursor.execute("""SELECT MIN(Price) FROM BasicOrderBook WHERE Action = "Sell" AND NOT (Type = "Conditional" AND Active = 0)""")
    MinOrderList = cursor.fetchall()
    #print MinOrderList
    MinOrder = MinOrderList[0]
    #print MinOrder
    AskPrice = MinOrder[0]
    if AskPrice == None:
        print "No Ask Price"
        AskPrice = 0
    else:
        print "Ask Price: " + str(AskPrice)



print ""
BidPriceChecker()
#print BidPrice
AskPriceChecker()
#print AskPrice
print ""
print ""



'''Setting Transaction Variables'''



TopBuyOrderFound = False
TopSellOrderFound = False
TransactionPossible = False
OrderPlace = "NO"



'''Creating Buy/Sell Order Queues'''



try:
    cursor.execute("""SELECT * FROM BasicOrderBook WHERE Action = "Buy" AND Active = 1 ORDER BY Price""")
    BuyOrderQueue = cursor.fetchall()
    if BuyOrderQueue == ():
        print "No Buy Orders"
        PriceSortedBuyOrderQueue = []
    else:
        #print "Buy Order Queue:"
        #print BuyOrderQueue
        VolumeSortedBuyOrderQueue = sorted(BuyOrderQueue, key = lambda tup: tup[3], reverse = True)
        #print ""
        #print "Volume Sorted Buy Order Queue:"
        #print VolumeSortedBuyOrderQueue
        TypeSortedBuyOrderQueue = []
        for BuyOrder in VolumeSortedBuyOrderQueue:
            if BuyOrder[4] == "Liquid":
                TypeSortedBuyOrderQueue.append(BuyOrder)
        for BuyOrder in VolumeSortedBuyOrderQueue:
            if BuyOrder[4] == "Limit":
                TypeSortedBuyOrderQueue.append(BuyOrder)
        for BuyOrder in VolumeSortedBuyOrderQueue:
            if BuyOrder[4] == "Conditional":
                TypeSortedBuyOrderQueue.append(BuyOrder)
        #print ""
        #print "Type Sorted Buy Order Queue:"
        #print TypeSortedBuyOrderQueue
        PriceSortedBuyOrderQueue = sorted(TypeSortedBuyOrderQueue, key = lambda tup: tup[2], reverse = True)
        print ""
        print "Price Sorted Buy Order Queue:"
        print PriceSortedBuyOrderQueue
        TopBuyOrderFound = True
except:
    print ""
    print "ERROR: Database Fetch Exception"
    print "Possible Cause: No Ask Price"



try:
    cursor.execute("""SELECT * FROM BasicOrderBook WHERE Action = "Sell" AND Active = 1 ORDER BY Price""")
    SellOrderQueue = cursor.fetchall()
    if SellOrderQueue == ():
        print ""
        print "No Sell Orders"
        PriceSortedSellOrderQueue = []
    else:
        #print ""
        #print "Sell Order Queue:"
        #print SellOrderQueue
        VolumeSortedSellOrderQueue = sorted(SellOrderQueue, key = lambda tup: tup[3], reverse = True)
        #print ""
        #print "Volume Sorted Sell Order Queue:"
        #print VolumeSortedSellOrderQueue
        TypeSortedSellOrderQueue = []
        for SellOrder in VolumeSortedSellOrderQueue:
            if SellOrder[4] == "Liquid":
                TypeSortedSellOrderQueue.append(SellOrder)
        for SellOrder in VolumeSortedSellOrderQueue:
            if SellOrder[4] == "Limit":
                TypeSortedSellOrderQueue.append(SellOrder)
        for SellOrder in VolumeSortedSellOrderQueue:
            if SellOrder[4] == "Conditional":
                TypeSortedSellOrderQueue.append(SellOrder)
        #print ""
        #print "Type Sorted Sell Order Queue:"
        #print TypeSortedSellOrderQueue
        PriceSortedSellOrderQueue = sorted(TypeSortedSellOrderQueue, key = lambda tup: tup[2])
        print ""
        print "Price Sorted Sell Order Queue:"
        print PriceSortedSellOrderQueue
        TopSellOrderFound = True
except:
    print ""
    print "ERROR: Database Fetch Exception"
    print "Possible Cause: No Bid Price"



'''Transaction Price Ticker'''


if OrderConstraint == "VOLUME":
    while OrderPlace != "YES":
        OrderList = []
        ExistingOrderCompletionList = []
        InstantOrderCompletionList = []
        TransactionList = []
        TransactionPriceTicker = 0
        TransactionVolumeTicker = 0
        RemainingInstantOrderVolume = Volume
        NewInstantOrderAccountBalance = InstantOrderAccountBalance
        NewInstantOrderAccountVolume = InstantOrderAccountVolume
        CompletelyFulfilled = False
        print ""
        print ""
        print ""
        if OrderAction == "BUY":
            print "Orders:"
            while RemainingInstantOrderVolume > 0:
                QueueLoop = 0
                for Order in PriceSortedSellOrderQueue:
                    SellOrderPrice = Order[2]
                    SellOrderVolume = Order[3]
                    SellOrderTotal = SellOrderPrice * SellOrderVolume
                    print ""
                    print Order
                    if SellOrderVolume > RemainingInstantOrderVolume:
                        TransactionPrice  = SellOrderPrice
                        TransactionVolume = RemainingInstantOrderVolume
                        TransactionTotal = TransactionPrice * TransactionVolume
                        print "INSTANT BUY ORDER FULLY FULFILLED"
                        print "EXISTING SELL ORDER PARTIALLY FULFILLED"
                        ExistingOrderCompletion = "Partial"
                        InstantOrderCompletion = "Full"
                        TransactionPriceTicker += RemainingInstantOrderVolume * SellOrderPrice
                        TransactionVolumeTicker += RemainingInstantOrderVolume
                        NewInstantOrderAccountBalance -= RemainingInstantOrderVolume * SellOrderPrice
                        NewInstantOrderAccountVolume += RemainingInstantOrderVolume
                        NewExistingOrderVolume = SellOrderVolume - TransactionVolume
                        RemainingInstantOrderVolume = 0
                    elif SellOrderVolume < RemainingInstantOrderVolume:
                        TransactionPrice  = SellOrderPrice
                        TransactionVolume = SellOrderVolume
                        TransactionTotal = TransactionPrice * TransactionVolume
                        print "INSTANT BUY ORDER PARTIALLY FULFILLED"
                        print "EXISTING SELL ORDER FULLY FULFILLED"
                        ExistingOrderCompletion = "Full"
                        InstantOrderCompletion = "Partial"
                        TransactionPriceTicker += SellOrderTotal
                        TransactionVolumeTicker += SellOrderVolume
                        NewInstantOrderAccountBalance -= SellOrderTotal
                        NewInstantOrderAccountVolume += SellOrderVolume
                        RemainingInstantOrderVolume -= SellOrderVolume
                    else:
                        TransactionPrice  = SellOrderPrice
                        TransactionVolume = SellOrderVolume
                        TransactionTotal = TransactionPrice * TransactionVolume
                        print "INSTANT BUY ORDER FULLY FULFILLED"
                        print "EXISTING SELL ORDER FULLY FULFILLED"
                        ExistingOrderCompletion = "Full"
                        InstantOrderCompletion = "Full"
                        TransactionPriceTicker += SellOrderTotal
                        TransactionVolumeTicker += SellOrderVolume
                        NewInstantOrderAccountBalance -= SellOrderTotal
                        NewInstantOrderAccountVolume += SellOrderVolume
                        RemainingInstantOrderVolume -= SellOrderVolume
                    OrderList.append(Order)
                    ExistingOrderCompletionList.append(ExistingOrderCompletion)
                    InstantOrderCompletionList.append(InstantOrderCompletion)
                    TransactionDetails = [TransactionPrice, TransactionVolume, TransactionTotal]
                    TransactionList.append(TransactionDetails)
                    if InstantOrderCompletion == "Full":
                        break;
                if RemainingInstantOrderVolume == 0:
                    CompletelyFulfilled = True
                else:
                    print ""
                    print "Not enough orders to fulfill"
                break;
        elif OrderAction == "SELL":
            print "Orders:"
            while RemainingInstantOrderVolume > 0:
                for Order in PriceSortedBuyOrderQueue:
                    BuyOrderPrice = Order[2]
                    BuyOrderVolume = Order[3]
                    BuyOrderTotal = BuyOrderPrice * BuyOrderVolume
                    print ""
                    print Order
                    if BuyOrderVolume > RemainingInstantOrderVolume:
                        TransactionPrice  = BuyOrderPrice
                        TransactionVolume = RemainingInstantOrderVolume
                        TransactionTotal = TransactionPrice * TransactionVolume
                        print "EXISTING BUY ORDER PARTIALLY FULFILLED"
                        print "INSTANT SELL ORDER FULLY FULFILLED"
                        ExistingOrderCompletion = "Partial"
                        InstantOrderCompletion = "Full"
                        TransactionPriceTicker += RemainingInstantOrderVolume * BuyOrderPrice
                        TransactionVolumeTicker += RemainingInstantOrderVolume
                        NewInstantOrderAccountBalance += RemainingInstantOrderVolume * BuyOrderPrice
                        NewInstantOrderAccountVolume -= RemainingInstantOrderVolume
                        NewExistingOrderVolume = BuyOrderVolume - TransactionVolume
                        RemainingInstantOrderVolume = 0
                    elif BuyOrderVolume < RemainingInstantOrderVolume:
                        TransactionPrice  = BuyOrderPrice
                        TransactionVolume = BuyOrderVolume
                        TransactionTotal = TransactionPrice * TransactionVolume
                        print "EXISTING BUY ORDER FULLY FULFILLED"
                        print "INSTANT SELL ORDER PARTIALLY FULFILLED"
                        ExistingOrderCompletion = "Full"
                        InstantOrderCompletion = "Partial"
                        TransactionPriceTicker += BuyOrderTotal
                        TransactionVolumeTicker += BuyOrderVolume
                        NewInstantOrderAccountBalance += BuyOrderTotal
                        NewInstantOrderAccountVolume -= BuyOrderVolume
                        RemainingInstantOrderVolume -= BuyOrderVolume
                    else:
                        TransactionPrice  = BuyOrderPrice
                        TransactionVolume = BuyOrderVolume
                        TransactionTotal = TransactionPrice * TransactionVolume
                        print "EXISTING BUY ORDER FULLY FULFILLED"
                        print "INSTANT SELL ORDER FULLY FULFILLED"
                        ExistingOrderCompletion = "Full"
                        InstantOrderCompletion = "Full"
                        TransactionPriceTicker += BuyOrderTotal
                        TransactionVolumeTicker += BuyOrderVolume
                        NewInstantOrderAccountBalance += BuyOrderTotal
                        NewInstantOrderAccountVolume -= BuyOrderVolume
                        RemainingInstantOrderVolume -= BuyOrderVolume
                    OrderList.append(Order)
                    ExistingOrderCompletionList.append(ExistingOrderCompletion)
                    InstantOrderCompletionList.append(InstantOrderCompletion)
                    TransactionDetails = [TransactionPrice, TransactionVolume, TransactionTotal]
                    TransactionList.append(TransactionDetails)
                    if InstantOrderCompletion == "Full":
                        break;
                if RemainingInstantOrderVolume == 0:
                    CompletelyFulfilled = True
                else:
                    print ""
                    print "Not enough orders to fulfill"
                break;


        print ""
        print ""
        print ""
        ExchangeVolume = TransactionVolumeTicker
        ExchangePrice = TransactionPriceTicker
        if ExchangeVolume == 0:
            print "No orders to fulfill"
            break;
        else:
            print "Amount to Exchange: " + str(ExchangeVolume)
            print "Current Price: " + str(ExchangePrice)
            if ExchangeVolume != 0:
                AveragePrice = ExchangePrice / ExchangeVolume
                print "Average Price Per BTC: " + str(AveragePrice)
            OrderPlace = "Yes"
            OrderPlace = raw_input("Accept (Yes/No): ")
            OrderPlace = OrderPlace.upper()
            while OrderPlace != "YES" and OrderPlace != "NO":
                print "Incorrect option. Please enter again:"
                OrderPlace = raw_input("Accept (Yes/No): ")
                OrderPlace = OrderPlace.upper()
            if OrderPlace == "YES":
                print "Performing Transaction With Orders:"
                break;





elif OrderConstraint == "PRICE":
    while OrderPlace != "YES":
        OrderList = []
        ExistingOrderCompletionList = []
        InstantOrderCompletionList = []
        TransactionList = []
        TransactionPriceTicker = 0
        TransactionVolumeTicker = 0
        RemainingInstantOrderBalance = Price
        NewInstantOrderAccountBalance = InstantOrderAccountBalance
        NewInstantOrderAccountVolume = InstantOrderAccountVolume
        CompletelyFulfilled = False
        print ""
        print ""
        print ""
        RemainingInstantOrderBalance = Price
        if OrderAction == "BUY":
            print "Orders:"
            while RemainingInstantOrderBalance > 0:
                for Order in PriceSortedSellOrderQueue:
                    SellOrderPrice = Order[2]
                    SellOrderVolume = Order[3]
                    SellOrderTotal = SellOrderPrice * SellOrderVolume
                    print ""
                    print Order
                    if SellOrderTotal > RemainingInstantOrderBalance:
                        TransactionPrice  = SellOrderPrice
                        TransactionVolume = RemainingInstantOrderBalance / SellOrderPrice
                        TransactionTotal = TransactionPrice * TransactionVolume
                        print "INSTANT BUY ORDER FULLY FULFILLED"
                        print "EXISTING SELL ORDER PARTIALLY FULFILLED"
                        ExistingOrderCompletion = "Partial"
                        InstantOrderCompletion = "Full"
                        TransactionPriceTicker += RemainingInstantOrderBalance
                        TransactionVolumeTicker += RemainingInstantOrderBalance / SellOrderPrice
                        NewInstantOrderAccountBalance -= RemainingInstantOrderBalance
                        NewInstantOrderAccountVolume += RemainingInstantOrderBalance / SellOrderPrice
                        NewExistingOrderVolume = SellOrderVolume - TransactionVolume
                        RemainingInstantOrderBalance = 0
                    elif SellOrderTotal < RemainingInstantOrderBalance:
                        TransactionPrice  = SellOrderPrice
                        TransactionVolume = SellOrderVolume
                        TransactionTotal = TransactionPrice * TransactionVolume
                        print "INSTANT BUY ORDER PARTIALLY FULFILLED"
                        print "EXISTING SELL ORDER FULLY FULFILLED"
                        ExistingOrderCompletion = "Full"
                        InstantOrderCompletion = "Partial"
                        TransactionPriceTicker += SellOrderTotal
                        TransactionVolumeTicker += SellOrderVolume
                        NewInstantOrderAccountBalance -= SellOrderTotal
                        NewInstantOrderAccountVolume += SellOrderVolume
                        RemainingInstantOrderBalance -= SellOrderTotal
                    else:
                        TransactionPrice  = SellOrderPrice
                        TransactionVolume = SellOrderVolume
                        TransactionTotal = TransactionPrice * TransactionVolume
                        print "INSTANT BUY ORDER FULLY FULFILLED"
                        print "EXISTING SELL ORDER FULLY FULFILLED"
                        ExistingOrderCompletion = "Full"
                        InstantOrderCompletion = "Full"
                        TransactionPriceTicker += SellOrderTotal
                        TransactionVolumeTicker += SellOrderVolume
                        NewInstantOrderAccountBalance -= SellOrderTotal
                        NewInstantOrderAccountVolume += SellOrderVolume
                        RemainingInstantOrderBalance -= SellOrderTotal
                    OrderList.append(Order)
                    ExistingOrderCompletionList.append(ExistingOrderCompletion)
                    InstantOrderCompletionList.append(InstantOrderCompletion)
                    TransactionDetails = [TransactionPrice, TransactionVolume, TransactionTotal]
                    TransactionList.append(TransactionDetails)
                    if InstantOrderCompletion == "Full":
                        break;
                if RemainingInstantOrderBalance == 0:
                    CompletelyFulfilled = True
                else:
                    print ""
                    print "Not enough orders to fulfill"
                break;
        elif OrderAction == "SELL":
            print "Orders:"
            while RemainingInstantOrderBalance > 0:
                for Order in PriceSortedBuyOrderQueue:
                    BuyOrderPrice = Order[2]
                    BuyOrderVolume = Order[3]
                    BuyOrderTotal = BuyOrderPrice * BuyOrderVolume
                    print ""
                    print Order
                    if BuyOrderTotal > RemainingInstantOrderBalance:
                        TransactionPrice  = BuyOrderPrice
                        TransactionVolume = RemainingInstantOrderBalance / BuyOrderPrice
                        TransactionTotal = TransactionPrice * TransactionVolume
                        print "EXISTING BUY ORDER PARTIALLY FULFILLED"
                        print "INSTANT SELL ORDER FULLY FULFILLED"
                        ExistingOrderCompletion = "Partial"
                        InstantOrderCompletion = "Full"
                        TransactionPriceTicker += RemainingInstantOrderBalance
                        TransactionVolumeTicker += RemainingInstantOrderBalance / BuyOrderPrice
                        NewInstantOrderAccountBalance += RemainingInstantOrderBalance
                        NewInstantOrderAccountVolume -= RemainingInstantOrderBalance / BuyOrderPrice
                        NewExistingOrderVolume = BuyOrderVolume - TransactionVolume
                        RemainingInstantOrderBalance = 0
                    elif BuyOrderTotal < RemainingInstantOrderBalance:
                        TransactionPrice  = BuyOrderPrice
                        TransactionVolume = BuyOrderVolume
                        TransactionTotal = TransactionPrice * TransactionVolume
                        print "EXISTING BUY ORDER FULLY FULFILLED"
                        print "INSTANT SELL ORDER PARTIALLY FULFILLED"
                        ExistingOrderCompletion = "Full"
                        InstantOrderCompletion = "Partial"
                        TransactionPriceTicker += BuyOrderTotal
                        TransactionVolumeTicker += BuyOrderVolume
                        NewInstantOrderAccountBalance -= BuyOrderTotal
                        NewInstantOrderAccountVolume += BuyOrderVolume
                        RemainingInstantOrderBalance -= BuyOrderTotal
                    else:
                        TransactionPrice  = BuyOrderPrice
                        TransactionVolume = BuyOrderVolume
                        TransactionTotal = TransactionPrice * TransactionVolume
                        print "EXISTING BUY ORDER FULLY FULFILLED"
                        print "INSTANT SELL ORDER FULLY FULFILLED"
                        ExistingOrderCompletion = "Full"
                        InstantOrderCompletion = "Full"
                        TransactionPriceTicker += BuyOrderTotal
                        TransactionVolumeTicker += BuyOrderVolume
                        NewInstantOrderAccountBalance -= BuyOrderTotal
                        NewInstantOrderAccountVolume += BuyOrderVolume
                        RemainingInstantOrderBalance -= BuyOrderTotal
                    OrderList.append(Order)
                    ExistingOrderCompletionList.append(ExistingOrderCompletion)
                    InstantOrderCompletionList.append(InstantOrderCompletion)
                    TransactionDetails = [TransactionPrice, TransactionVolume, TransactionTotal]
                    TransactionList.append(TransactionDetails)
                if RemainingInstantOrderBalance == 0:
                    CompletelyFulfilled = True
                else:
                    print ""
                    print "Not enough orders to fulfill"
                break;
        print ""



        '''Prompts User Confirmation'''


        print ""
        print ""
        print ""
        ExchangeVolume = TransactionVolumeTicker
        ExchangePrice = TransactionPriceTicker
        if ExchangeVolume == 0:
            print "No orders to fulfill"
            break;
        else:
            print "Amount to Exchange: " + str(ExchangeVolume)
            print "Current Price: " + str(ExchangePrice)
            if ExchangeVolume != 0:
                AveragePrice = ExchangePrice / ExchangeVolume
                print "Average Price Per BTC: " + str(AveragePrice)
            OrderPlace = "Yes"
            OrderPlace = raw_input("Accept (Yes/No): ")
            OrderPlace = OrderPlace.upper()
            while OrderPlace != "YES" and OrderPlace != "NO":
                print "Incorrect option. Please enter again:"
                OrderPlace = raw_input("Accept (Yes/No): ")
                OrderPlace = OrderPlace.upper()
            if OrderPlace == "YES":
                print "Performing Transaction With Orders:"
                break;



'''Deletes/Updates Fulfilled Orders'''



print ""
print ""
print ""
print "Order List"
print OrderList
for Index, Order in enumerate(OrderList):
    if ExistingOrderCompletionList[Index] == "Full":
        print "Order Deleted: " + str(Order[0])
        #cursor.execute("""DELETE FROM BasicOrderBook WHERE OrderNumber = %s""" % (Order[0]))
        #db.commit()
    elif ExistingOrderCompletionList[Index] == "Partial":
        print "Order Updated: " + str(Order[0])
        print "Volume Updated: " + str(NewExistingOrderVolume)
        cursor.execute("""UPDATE BasicOrderBook SET Volume = %s WHERE OrderNumber = %s""" % (NewExistingOrderVolume, Order[0]))
        db.commit()
    pass
print ""
print "Existing Order Completion List"
print ExistingOrderCompletionList
print ""
print "Instant Order Completion List"
print InstantOrderCompletionList
print ""
print "Transaction List"
print TransactionList



'''Logs Transactions'''



if CompletelyFulfilled != True:
    print ""
    print "Not enough orders to fulfill"
LocalTime = time.localtime(time.time())
LocalTimeMinutes = LocalTime[4]
LocalTimeSeconds = LocalTime[5]
if LocalTimeMinutes < 10:
    LocalTimeMinutes = "0" + str(LocalTimeMinutes)
if LocalTimeSeconds < 10:
    LocalTimeSeconds = "0" + str(LocalTimeSeconds)
FormattedDate = str(LocalTime[1]) + "/" +  str(LocalTime[2]) + "/" +  str(LocalTime[0])
FormattedDatabaseDate = str(LocalTime[0]) + "-" +  str(LocalTime[1]) + "-" +  str(LocalTime[2])
FormattedTime = str(LocalTime[3]) + ":" +  str(LocalTimeMinutes) + ":" +  str(LocalTimeSeconds)
FormattedDateTime = FormattedDatabaseDate + " " + FormattedTime



for Index, Order in enumerate(OrderList):

    cursor.execute("""SELECT TradingFee FROM UserBook WHERE Username = "%s" """ % (OrderAccount))
    InstantOrderTradingFeeRate = cursor.fetchall()[0][0]
    cursor.execute("""SELECT TradingFee FROM UserBook WHERE Username = "%s" """ % (Order[1]))
    ExistingOrderTradingFeeRate = cursor.fetchall()[0][0]
    print "Instant Order Trading Fee Rate: " + str(InstantOrderTradingFeeRate)
    print "Existing Order Trading Fee Rate: " + str(ExistingOrderTradingFeeRate)

    print ""
    #print "Index: " + str(Index)
    #print "TransactionCount: " + str(TransactionCount)
    TransactionPrice = TransactionList[Index][0]
    TransactionVolume = TransactionList[Index][1]
    TransactionTotal = TransactionList[Index][2]

    if OrderAction == "BUY":
        print str(ExistingOrderCompletionList[Index]) + " Sell"
        BuyOrderAccount = OrderAccount
        BuyOrderNumber = OrderNumber
        BuyOrderPrice = SellOrder[2]
        BuyOrderTradingFeeRate = InstantOrderTradingFeeRate
        AdjustedBuyOrderVolume = TransactionVolume - (TransactionVolume * InstantOrderTradingFeeRate)
        BuyOrderVolume = ExchangeVolume
        BuyOrderType = "Instant"
        BuyOrderCompletion = InstantOrderCompletionList[Index]
        SellOrderAccount = Order[1]
        SellOrderNumber = Order[0]
        SellOrderPrice = Order[2]
        SellOrderTradingFeeRate = ExistingOrderTradingFeeRate
        AdjustedSellOrderPrice = SellOrderPrice - (SellOrderPrice * ExistingOrderTradingFeeRate)
        SellOrderVolume = Order[3]
        SellOrderType = Order[4]
        SellOrderCompletion = ExistingOrderCompletionList[Index]
        print "BuyCompletion: " + str(BuyOrderCompletion)
        print "SellCompletion: " + str(SellOrderCompletion)
    if OrderAction == "SELL":
        print str(ExistingOrderCompletionList[Index]) + " Buy"
        BuyOrderAccount = Order[1]
        BuyOrderNumber = Order[0]
        BuyOrderPrice = Order[2]
        BuyOrderVolume = Order[3]
        BuyOrderTradingFeeRate = ExistingOrderTradingFeeRate
        AdjustedBuyOrderVolume = TransactionVolume - (TransactionVolume * ExistingOrderTradingFeeRate)
        BuyOrderType = Order[4]
        BuyOrderCompletion = ExistingOrderCompletionList[Index]
        SellOrderAccount = OrderAccount
        SellOrderNumber = OrderNumber
        SellOrderPrice = Order[2]
        SellOrderTradingFeeRate = ExistingOrderTradingFeeRate
        AdjustedSellOrderPrice = SellOrderPrice - (SellOrderPrice * InstantOrderTradingFeeRate)
        SellOrderVolume = ExchangeVolume
        SellOrderType = "Instant"
        SellOrderCompletion = InstantOrderCompletionList[Index]
        print "BuyCompletion: " + str(BuyOrderCompletion)
        print "SellCompletion: " + str(SellOrderCompletion)

    print ""
    print "Trading Fee Adjusted Buy Order Volume: " + str(AdjustedBuyOrderVolume)
    print "Trading Fee Adjusted Sell Order Price: " + str(AdjustedSellOrderPrice)

    AdjustedSellOrderTotal = AdjustedSellOrderPrice * TransactionVolume
    TradingFeeProfit = ((TransactionVolume - AdjustedBuyOrderVolume) * TransactionPrice) + (TransactionTotal - (TransactionVolume * AdjustedSellOrderPrice))
    SpreadProfitPerBTC = BuyOrderPrice - SellOrderPrice #Calculates profit gained by Bid/Ask spread
    SpreadProfit = SpreadProfitPerBTC * TransactionVolume
    TotalProfit = TradingFeeProfit + SpreadProfit
    print ""

    print ""
    print "--------------------"
    print  "Transaction Details:"
    print "Transaction Number: " + str(TransactionCount)
    print "Transaction Date: " + FormattedDate
    print "Transaction Time: " + FormattedTime
    print "Transaction Price: " + str(TransactionPrice)
    print "Transaction Volume: " + str(TransactionVolume)
    print "Transaction Total: " + str(TransactionTotal)
    print "Spread Profit: " + str(SpreadProfit)
    print "Trading Fee Profit: " + str(TradingFeeProfit)
    print "Total Profit: " +  str(TotalProfit)
    print ""
    print "Buy Order Number: " + str(BuyOrderNumber)
    print "Buy Order Account: " + BuyOrderAccount
    print "Buy Order Price: " + str(BuyOrderPrice)
    print "Buy Order Volume: " + str(BuyOrderVolume)
    print "Buy Order Trading Fee Rate: " + str(BuyOrderTradingFeeRate)
    print "Buy Order Adjusted Volume: " + str(AdjustedBuyOrderVolume)
    print "Buy Order Type: " + BuyOrderType
    print "Buy Order Completion: " + BuyOrderCompletion
    print ""
    print "Sell Order Number: " + str(SellOrderNumber)
    print "Sell Order Account: " + SellOrderAccount
    print "Sell Order Price: " + str(SellOrderPrice)
    print "Sell Order Trading Fee Rate: " + str(SellOrderTradingFeeRate)
    print "Sell Order Adjusted Price: " + str(AdjustedSellOrderPrice)
    print "Sell Order Volume: " + str(SellOrderVolume)
    print "Sell Order Type: " + SellOrderType
    print "Sell Order Completion: " + SellOrderCompletion
    print ""
    print BuyOrderAccount + ": -$" + str(TransactionTotal) + " and +" + str(AdjustedBuyOrderVolume) + " BTC"
    print SellOrderAccount + ": +$" + str(AdjustedSellOrderTotal) + " and -" + str(TransactionVolume) + " BTC"
    print ""

    try:
        cursor.execute("""INSERT INTO TransactionLog(TransactionNumber, TransactionDate, TransactionPrice, TransactionVolume, TransactionTotal, TradingFeeProfit, SpreadProfit, TotalProfit, BuyOrderNumber, BuyOrderAccount, BuyOrderPrice, BuyOrderVolume, BuyOrderType, BuyOrderCompletion, SellOrderNumber, SellOrderAccount, SellOrderPrice, SellOrderVolume, SellOrderType, SellOrderCompletion) VALUES (%d, "%s", %d, %d, %d, %d, %d, %d, %d, "%s", %d, %d, "%s", "%s", %d, "%s", %d, %d, "%s", "%s")""" % (TransactionCount, FormattedDateTime, TransactionPrice, TransactionVolume, TransactionTotal, TradingFeeProfit, SpreadProfit, TotalProfit, BuyOrderNumber, BuyOrderAccount, BuyOrderPrice, BuyOrderVolume, BuyOrderType, BuyOrderCompletion, SellOrderNumber, SellOrderAccount, SellOrderPrice, SellOrderVolume, SellOrderType, SellOrderCompletion))
        db.commit()
        print "Transaction Successfully Logged"
    except:
        print "ERROR: Transaction Unsuccessfully Logged"



    '''Updating Account Volumes'''



    cursor.execute("""SELECT Volume FROM UserBook WHERE Username = "%s" """ % (BuyOrderAccount))
    BuyOrderAccountVolume = cursor.fetchall()[0][0]

    cursor.execute("""SELECT Volume FROM UserBook WHERE Username = "%s" """ % (SellOrderAccount))
    SellOrderAccountVolume = cursor.fetchall()[0][0]

    NewBuyOrderAccountVolume = BuyOrderAccountVolume + TransactionVolume
    NewSellOrderAccountVolume = SellOrderAccountVolume + TransactionVolume

    try:
        print ""
        print "Updating Account Volumes:"
        print NewBuyOrderAccountVolume
        print NewSellOrderAccountVolume
        print BuyOrderAccount + ": +" + str(TransactionVolume) + " BTC"
        print SellOrderAccount + ": +" + str(TransactionVolume) + " BTC"
        cursor.execute("""UPDATE UserBook SET Volume = %d WHERE Username = "%s" """ % (NewBuyOrderAccountVolume, BuyOrderAccount))
        cursor.execute("""UPDATE UserBook SET Volume = %d WHERE Username = "%s" """ % (NewSellOrderAccountVolume, SellOrderAccount))
        db.commit()
        print "Account Volumes Successfully Updated"
    except:
        print "ERROR: Account Volumes Unsuccessfully Updated"



    '''Updating Account Credits'''



    cursor.execute("""SELECT USDCredit, BTCCredit FROM UserBook WHERE Username = "%s" """ % (BuyOrderAccount))
    BuyOrderAccountCredits = cursor.fetchall()[0]
    BuyOrderAccountUSDCredit = BuyOrderAccountCredits[0]
    BuyOrderAccountBTCCredit = BuyOrderAccountCredits[1]

    cursor.execute("""SELECT USDCredit, BTCCredit FROM UserBook WHERE Username = "%s" """ % (SellOrderAccount))
    SellOrderAccountCredits = cursor.fetchall()[0]
    SellOrderAccountUSDCredit = SellOrderAccountCredits[0]
    SellOrderAccountBTCCredit = SellOrderAccountCredits[1]

    NewBuyOrderAccountUSDCredit = BuyOrderAccountUSDCredit - TransactionTotal
    NewBuyOrderAccountBTCCredit = BuyOrderAccountBTCCredit + AdjustedBuyOrderVolume
    NewSellOrderAccountUSDCredit = SellOrderAccountUSDCredit + AdjustedSellOrderTotal
    NewSellOrderAccountBTCCredit = SellOrderAccountBTCCredit - TransactionVolume

    print ""
    print NewBuyOrderAccountUSDCredit
    print NewBuyOrderAccountBTCCredit
    print NewSellOrderAccountUSDCredit
    print NewSellOrderAccountBTCCredit

    try:
        print ""
        print "Updating Account Credits:"
        cursor.execute("""UPDATE UserBook SET USDCredit = %d, BTCCredit = %d WHERE Username = "%s" """ % (NewBuyOrderAccountUSDCredit, NewBuyOrderAccountBTCCredit, BuyOrderAccount))
        cursor.execute("""UPDATE UserBook SET USDCredit = %d, BTCCredit = %d WHERE Username = "%s" """ % (NewSellOrderAccountUSDCredit, NewSellOrderAccountBTCCredit, SellOrderAccount))
        db.commit()
        print BuyOrderAccount + ": -$" + str(TransactionTotal) + " and +" + str(AdjustedBuyOrderVolume) + " BTC"
        print SellOrderAccount + ": +$" + str(AdjustedSellOrderTotal) + " and -" + str(TransactionVolume) + " BTC"
        print "Account Credits Successfully Updated"
    except:
        print "ERROR: Account Credits Unsuccessfully Updated"



    '''Logging Transaction Statistics'''



    log = open("Transaction" + str(TransactionCount) + ".txt", "a") #Defines log file open variable
    log.write("----------" + "\n" + "Transaction Details:" + "\n" + "\n")
    log.write("Transaction Number: " + str(TransactionCount) + "\n")
    log.write("Transaction Date: " + FormattedDate + "\n")
    log.write("Transaction Time: " + FormattedTime + "\n")
    log.write("Transaction Price: " + str(TransactionPrice) + "\n")
    log.write("Transaction Volume: " + str(TransactionVolume) + "\n")
    log.write("Transaction Total: " + str(TransactionTotal) + "\n")
    log.write("Spread Profit: " + str(SpreadProfit) + "\n")
    log.write("Trading Fee Profit: " + str(TradingFeeProfit) + "\n")
    log.write("Total Profit: " +  str(TotalProfit) + "\n" + "\n")

    log.write("Buy Order Number: " + str(BuyOrderNumber) + "\n")
    log.write("Buy Order Account: " + BuyOrderAccount + "\n")
    log.write("Buy Order Price: " + str(BuyOrderPrice) + "\n")
    log.write("Buy Order Volume: " + str(BuyOrderVolume) + "\n")
    log.write("Buy Order Trading Fee Rate: " + str(BuyOrderTradingFeeRate))
    log.write("Buy Order Adjusted Volume: " + str(AdjustedBuyOrderVolume))
    log.write("Buy Order Type: " + BuyOrderType + "\n")
    log.write("Buy Order Completion: " + BuyOrderCompletion + "\n" + "\n")

    log.write("Sell Order Number: " + str(SellOrderNumber) + "\n")
    log.write("Sell Order Account: " + SellOrderAccount + "\n")
    log.write("Sell Order Price: " + str(SellOrderPrice) + "\n")
    log.write("Sell Order Trading Fee Rate: " + str(SellOrderTradingFeeRate))
    log.write("Sell Order Adjusted Price: " + str(AdjustedSellOrderPrice))
    log.write("Sell Order Volume: " + str(SellOrderVolume) + "\n")
    log.write("Sell Order Type: " + SellOrderType + "\n")
    log.write("Sell Order Completion: " + SellOrderCompletion + "\n" + "\n")

    log.write(BuyOrderAccount + ": +$" + str(TransactionTotal) + " and -" + str(AdjustedBuyOrderVolume) + " BTC" + "\n")
    log.write(SellOrderAccount + ": -$" + str(AdjustedSellOrderTotal) + " and +" + str(TransactionVolume) + " BTC" + "\n")

    log.close()

    TransactionCount += 1



'''
Variables Index:

Instant Order:
-Account Name: OrderAccount
-Order Number: OrderNumber
-Type: OrderType
-Action: OrderAction
-Intended Price: Price
-Intended Volume: Volume

Fulfilled Order: (For loop through "FullOrderList" or "PartialOrderList")
-Account Name: Order[1]
-Order Number: Order[0]
-Type: Order[4]
-Action: Order[5]
-Price: Order[2]
-Volume: Order[3]

Transaction: (For loop through "FullOrderList" or "PartialOrderList")
-Date: FormattedDate
-Time: FormattedTime
-Number: TransactionCount
-Total: TransactionTotal
-Volume: BoughtVolume
-Average: AveragePrice

Miscellaneous:
-Remaining Volume: RemainingVolume
-Partial Fulfillment New Volume: NewOrderVolume

'''



db.close()
