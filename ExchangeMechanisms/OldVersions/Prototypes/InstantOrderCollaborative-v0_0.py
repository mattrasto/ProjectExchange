#-------------------------------------------------------------------------------
# Name:        InstantOrderCollaborative-v0.1
# Purpose:
#
# Author:      Matthew
#
# Created:     05/04/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    07/05/2014
#-------------------------------------------------------------------------------

#Check Transaction Price Ticker

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
    print TransactionCount
except:
    TransactionCount = 1
    print TransactionCount



'''Setting Variables'''



#Testing variables:
OrderNumber = 50
OrderAccount = "***"
OrderType = "Instant"
TradingFeeProfit = 0



cursor.execute("""SELECT * FROM Users WHERE Username = "%s" """ % (OrderAccount))
UserDetails = cursor.fetchone()

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
            Price = int(Price)
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
            Volume = int(Volume)
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
        CompletelyFulfilled = False
        ExistingOrderFulfillmentList = []
        InstantOrderFulfillmentList = []
        FullOrderList = []
        PartialOrderList = []
        PartialTransactionInstantOrderVolumeList = []
        FullTransactionInstantOrderVolumeList = []
        print ""
        print ""
        print ""
        TransactionPriceTicker = 0
        RemainingInstantOrderVolume = Volume
        if OrderAction == "BUY":
            print "Orders:"
            while RemainingInstantOrderVolume > 0:
                QueueLoop = 0
                for Order in PriceSortedSellOrderQueue:
                    SellOrderVolume = Order[3]
                    print ""
                    #print QueueLoop
                    print Order
                    BuyOrderVolume = RemainingInstantOrderVolume
                    if SellOrderVolume > RemainingInstantOrderVolume:
                        TransactionPriceTicker += (Order[2] * RemainingInstantOrderVolume)
                        PartialTransactionInstantOrderVolume = RemainingInstantOrderVolume
                        NewOrderVolume = Order[3] - RemainingInstantOrderVolume
                        RemainingInstantOrderVolume = 0
                        print "INSTANT BUY ORDER FULLY FULFILLED"
                        print "EXISTING SELL ORDER PARTIALLY FULFILLED"
                        print "Transaction Price Ticker: " + str(TransactionPriceTicker)
                        print "Remaining Volume: " + str(RemainingInstantOrderVolume)
                        PartialTransactionInstantOrderVolumeList.append(PartialTransactionInstantOrderVolume)
                        PartialOrderList.append(Order)
                        ExistingOrderFulfillmentList.append("Partial")
                        InstantOrderFulfillmentList.append("Full")
                        LastOrderCompletion = "Partial"
                        break;
                    elif SellOrderVolume < RemainingInstantOrderVolume:
                        TransactionPriceTicker += (Order[2] * Order[3])
                        FullTransactionInstantOrderVolume = RemainingInstantOrderVolume
                        RemainingInstantOrderVolume -= Order[3]
                        print "INSTANT BUY ORDER PARTIALLY FULFILLED"
                        print "EXISTING SELL ORDER FULLY FULFILLED"
                        print "Transaction Price Ticker: " + str(TransactionPriceTicker)
                        print "Remaining Volume: " + str(RemainingInstantOrderVolume)
                        FullTransactionInstantOrderVolumeList.append(FullTransactionInstantOrderVolume)
                        FullOrderList.append(Order)
                        ExistingOrderFulfillmentList.append("Full")
                        InstantOrderFulfillmentList.append("Partial")
                        LastOrderCompletion = "Full"
                    else:
                        TransactionPriceTicker += (Order[2] * Order[3])
                        FullTransactionInstantOrderVolume = RemainingInstantOrderVolume
                        RemainingInstantOrderVolume -= Order[3]
                        print "INSTANT BUY ORDER FULLY FULFILLED"
                        print "EXISTING SELL ORDER FULLY FULFILLED"
                        print "Transaction Price Ticker: " + str(TransactionPriceTicker)
                        print "Remaining Volume: " + str(RemainingInstantOrderVolume)
                        FullTransactionInstantOrderVolumeList.append(FullTransactionInstantOrderVolume)
                        FullOrderList.append(Order)
                        ExistingOrderFulfillmentList.append("Full")
                        InstantOrderFulfillmentList.append("Full")
                        LastOrderCompletion = "Full"
                        break;
                    QueueLoop += 1
                #print ""
                #print "Full Order List:"
                #print FullOrderList
                #print "Partial Order List:"
                #print PartialOrderList
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
                    BuyOrderVolume = Order[3]
                    print ""
                    print Order
                    if BuyOrderVolume > RemainingInstantOrderVolume:
                        TransactionPriceTicker += (Order[2] * RemainingInstantOrderVolume)
                        PartialTransactionInstantOrderVolume = RemainingInstantOrderVolume
                        NewOrderVolume = Order[3] - RemainingInstantOrderVolume
                        RemainingInstantOrderVolume = 0
                        print "EXISTING BUY ORDER PARTIALLY FULFILLED"
                        print "INSTANT SELL ORDER FULLY FULFILLED"
                        print "Transaction Price Ticker: " + str(TransactionPriceTicker)
                        print "Remaining Volume: " + str(RemainingInstantOrderVolume)
                        PartialTransactionInstantOrderVolumeList.append(PartialTransactionInstantOrderVolume)
                        PartialOrderList.append(Order)
                        ExistingOrderFulfillmentList.append("Partial")
                        InstantOrderFulfillmentList.append("Full")
                        LastOrderCompletion = "Partial"
                        break;
                    elif BuyOrderVolume < RemainingInstantOrderVolume:
                        TransactionPriceTicker += (Order[2] * Order[3])
                        FullTransactionInstantOrderVolume = RemainingInstantOrderVolume
                        RemainingInstantOrderVolume -= Order[3]
                        print "EXISTING BUY ORDER FULLY FULFILLED"
                        print "INSTANT SELL ORDER PARTIALLY FULFILLED"
                        print "Transaction Price Ticker: " + str(TransactionPriceTicker)
                        print "Remaining Volume: " + str(RemainingInstantOrderVolume)
                        FullTransactionInstantOrderVolumeList.append(FullTransactionInstantOrderVolume)
                        FullOrderList.append(Order)
                        ExistingOrderFulfillmentList.append("Full")
                        InstantOrderFulfillmentList.append("Partial")
                        LastOrderCompletion = "Full"
                    else:
                        TransactionPriceTicker += (Order[2] * Order[3])
                        FullTransactionInstantOrderVolume = RemainingInstantOrderVolume
                        RemainingInstantOrderVolume -= Order[3]
                        print "EXISTING BUY ORDER FULLY FULFILLED"
                        print "INSTANT SELL ORDER FULLY FULFILLED"
                        print "Transaction Price Ticker: " + str(TransactionPriceTicker)
                        print "Remaining Volume: " + str(RemainingInstantOrderVolume)
                        FullTransactionInstantOrderVolumeList.append(FullTransactionInstantOrderVolume)
                        FullOrderList.append(Order)
                        ExistingOrderFulfillmentList.append("Full")
                        InstantOrderFulfillmentList.append("Full")
                        LastOrderCompletion = "Full"
                        break;
                #print ""
                #print "Full Order List:"
                #print FullOrderList
                #print "Partial Order List:"
                #print PartialOrderList
                if RemainingInstantOrderVolume == 0:
                    CompletelyFulfilled = True
                else:
                    print ""
                    print "Not enough orders to fulfill"
                break;
        print ""
        BoughtVolume = Volume - RemainingInstantOrderVolume
        if BoughtVolume == 0:
            print "No orders to fulfill"
            break;
        else:
            print "Amount to Exchange: " + str(BoughtVolume)
            print "Current Price: " + str(TransactionPriceTicker)
            if BoughtVolume != 0:
                AveragePrice = TransactionPriceTicker / BoughtVolume
                print "Average Price Per BTC: " + str(AveragePrice)
            TransactionVolumeTicker = BoughtVolume
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
        CompletelyFulfilled = False
        ExistingOrderFulfillmentList = []
        InstantOrderFulfillmentList = []
        FullOrderList = []
        PartialOrderList = []
        PartialTransactionInstantOrderBalanceList = []
        PartialTransactionInstantOrderVolumeList = []
        FullTransactionInstantOrderBalanceList = []
        print ""
        print ""
        print ""
        TransactionVolumeTicker = 0
        TransactionPriceTicker = 0
        RemainingInstantOrderBalance = Price
        if OrderAction == "BUY":
            print "Orders:"
            while RemainingInstantOrderBalance > 0:
                QueueLoop = 0
                for Order in PriceSortedSellOrderQueue:
                    SellOrderTotal = Order[3] * Order[2]
                    print ""
                    #print QueueLoop
                    print Order
                    BuyOrderBalance = RemainingInstantOrderBalance
                    if SellOrderTotal > RemainingInstantOrderBalance:
                        PartialTransactionInstantOrderVolume = (RemainingInstantOrderBalance / Order[2])
                        TransactionVolumeTicker += (RemainingInstantOrderBalance / Order[2])
                        TransactionPriceTicker += RemainingInstantOrderBalance
                        PartialTransactionInstantOrderBalance = RemainingInstantOrderBalance
                        NewOrderVolume = Order[3] - (RemainingInstantOrderBalance / Order[2])
                        RemainingInstantOrderBalance = 0
                        print "INSTANT BUY ORDER FULLY FULFILLED"
                        print "EXISTING SELL ORDER PARTIALLY FULFILLED"
                        print "Transaction Volume Ticker: " + str(TransactionVolumeTicker)
                        print "Transaction Price Ticker: " + str(TransactionPriceTicker)
                        print "Remaining Balance: " + str(RemainingInstantOrderBalance)
                        PartialTransactionInstantOrderVolumeList.append(PartialTransactionInstantOrderVolume)
                        PartialTransactionInstantOrderBalanceList.append(PartialTransactionInstantOrderBalance)
                        PartialOrderList.append(Order)
                        ExistingOrderFulfillmentList.append("Partial")
                        InstantOrderFulfillmentList.append("Full")
                        LastOrderCompletion = "Partial"
                        break;
                    elif SellOrderTotal < RemainingInstantOrderBalance:
                        TransactionVolumeTicker += long(Order[3])
                        TransactionPriceTicker += (Order[2] * Order[3])
                        FullTransactionInstantOrderBalance = RemainingInstantOrderBalance
                        RemainingInstantOrderBalance -= Order[2] * Order[3]
                        print "INSTANT BUY ORDER PARTIALLY FULFILLED"
                        print "EXISTING SELL ORDER FULLY FULFILLED"
                        print "Transaction Volume Ticker: " + str(TransactionVolumeTicker)
                        print "Transaction Price Ticker: " + str(TransactionPriceTicker)
                        print "Remaining Balance: " + str(RemainingInstantOrderBalance)
                        FullTransactionInstantOrderBalanceList.append(FullTransactionInstantOrderBalance)
                        FullOrderList.append(Order)
                        ExistingOrderFulfillmentList.append("Full")
                        InstantOrderFulfillmentList.append("Partial")
                        LastOrderCompletion = "Full"
                    else:
                        TransactionVolumeTicker += long(Order[3])
                        TransactionPriceTicker += (Order[2] * Order[3])
                        FullTransactionInstantOrderBalance = RemainingInstantOrderBalance
                        RemainingInstantOrderBalance -= Order[3]
                        print "INSTANT BUY ORDER FULLY FULFILLED"
                        print "EXISTING SELL ORDER FULLY FULFILLED"
                        print "Transaction Volume Ticker: " + str(TransactionVolumeTicker)
                        print "Transaction Price Ticker: " + str(TransactionPriceTicker)
                        print "Remaining Balance: " + str(RemainingInstantOrderBalance)
                        FullTransactionInstantOrderBalanceList.append(FullTransactionInstantOrderBalance)
                        FullOrderList.append(Order)
                        ExistingOrderFulfillmentList.append("Full")
                        InstantOrderFulfillmentList.append("Full")
                        LastOrderCompletion = "Full"
                        break;
                    QueueLoop += 1
                #print ""
                #print "Full Order List:"
                #print FullOrderList
                #print "Partial Order List:"
                #print PartialOrderList
                #print "Full Transaction Instant Order Balance List:"
                #print FullTransactionInstantOrderBalanceList
                #print "Partial Transaction Instant Order Balance List:"
                #print PartialTransactionInstantOrderBalanceList
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
                    BuyOrderTotal = Order[3] * Order[2]
                    print ""
                    print Order
                    if BuyOrderTotal > RemainingInstantOrderBalance:
                        PartialTransactionInstantOrderVolume = (RemainingInstantOrderBalance / Order[2])
                        TransactionVolumeTicker += (RemainingInstantOrderBalance / Order[2])
                        TransactionPriceTicker += Order[2] * (RemainingInstantOrderBalance / Order[2])
                        PartialTransactionInstantOrderBalance = RemainingInstantOrderBalance
                        NewOrderVolume = Order[3] - (RemainingInstantOrderBalance / Order[2])
                        RemainingInstantOrderBalance = 0
                        print "EXISTING BUY ORDER PARTIALLY FULFILLED"
                        print "INSTANT SELL ORDER FULLY FULFILLED"
                        print "Transaction Volume Ticker: " + str(TransactionVolumeTicker)
                        print "Transaction Price Ticker: " + str(TransactionPriceTicker)
                        print "Remaining Balance: " + str(RemainingInstantOrderBalance)
                        PartialTransactionInstantOrderVolumeList.append(PartialTransactionInstantOrderVolume)
                        PartialTransactionInstantOrderBalanceList.append(PartialTransactionInstantOrderBalance)
                        PartialOrderList.append(Order)
                        ExistingOrderFulfillmentList.append("Partial")
                        InstantOrderFulfillmentList.append("Full")
                        LastOrderCompletion = "Partial"
                        break;
                    elif BuyOrderTotal < RemainingInstantOrderBalance:
                        TransactionVolumeTicker += Order[3]
                        TransactionPriceTicker += (Order[2] * Order[3])
                        FullTransactionInstantOrderBalance = RemainingInstantOrderBalance
                        RemainingInstantOrderBalance -= Order[2] * Order[3]
                        print "EXISTING BUY ORDER FULLY FULFILLED"
                        print "INSTANT SELL ORDER PARTIALLY FULFILLED"
                        print "Transaction Volume Ticker: " + str(TransactionVolumeTicker)
                        print "Transaction Price Ticker: " + str(TransactionPriceTicker)
                        print "Remaining Balance: " + str(RemainingInstantOrderBalance)
                        FullTransactionInstantOrderBalanceList.append(FullTransactionInstantOrderBalance)
                        FullOrderList.append(Order)
                        ExistingOrderFulfillmentList.append("Full")
                        InstantOrderFulfillmentList.append("Partial")
                        LastOrderCompletion = "Full"
                    else:
                        TransactionVolumeTicker += Order[3]
                        TransactionPriceTicker += (Order[2] * Order[3])
                        FullTransactionInstantOrderVolume = RemainingInstantOrderBalance
                        RemainingInstantOrderBalance -= Order[2]
                        print "EXISTING BUY ORDER FULLY FULFILLED"
                        print "INSTANT SELL ORDER FULLY FULFILLED"
                        print "Transaction Volume Ticker: " + str(TransactionVolumeTicker)
                        print "Transaction Price Ticker: " + str(TransactionPriceTicker)
                        print "Remaining Balance: " + str(RemainingInstantOrderBalance)
                        FullTransactionInstantOrderBalanceList.append(FullTransactionInstantOrderBalance)
                        FullOrderList.append(Order)
                        ExistingOrderFulfillmentList.append("Full")
                        InstantOrderFulfillmentList.append("Full")
                        LastOrderCompletion = "Full"
                        break;
                #print ""
                #print "Full Order List:"
                #print FullOrderList
                #print "Partial Order List:"
                #print PartialOrderList
                #print "Full Transaction Instant Order Balance List:"
                #print FullTransactionInstantOrderBalanceList
                #print "Partial Transaction Instant Order Balance List:"
                #print PartialTransactionInstantOrderBalanceList
                '''
                if TransactionVolumeTicker > UserDetails[4]:
                    print ""
                    print "Volume higher than balance. Defaulting to current balance."
                    BoughtVolume = TransactionVolumeTicker
                    TransactionVolumeTicker = UserDetails[4]
                    print "TransactionVolumeTicker: " + str(TransactionVolumeTicker)
                    RemainingInstantOrderVolume = 0
                    print LastOrderCompletion
                    if LastOrderCompletion == "Full":
                        print FullTransactionInstantOrderBalanceList[-1:]
                        print FullOrderList[-1:]
                        print FullOrderList[-1:][0][3]
                        FullOrderList[-1:][0][3] = BoughtVolume - TransactionVolumeTicker
                        print FullOrderList[-1:][0][3]
                    if LastOrderCompletion == "Partial":
                        print PartialTransactionInstantOrderBalanceList[-1:]
                        print PartialOrderList
                '''
                if RemainingInstantOrderBalance == 0:
                    CompletelyFulfilled = True
                else:
                    print ""
                    print "Not enough orders to fulfill"
                break;
        print ""



        '''Prompts User Confirmation'''



        BoughtVolume = TransactionVolumeTicker
        '''
        if OrderAction == "SELL":
            if BoughtVolume > UserDetails[4]:
                print "Volume higher than balance. Defaulting to current balance."
                BoughtVolume = UserDetails[4]
                TransactionVolumeTicker = UserDetails[4]
                print "TransactionVolumeTicker: " + str(TransactionVolumeTicker)
        if OrderAction == "BUY":
            if TransactionPriceTicker > UserDetails[3]:
                print "Price higher than balance. Defaulting to current balance."
                TransactionPriceTicker = UserDetails[3]
                print "TransactionPriceTicker: " + str(TransactionPriceTicker)
        '''
        if BoughtVolume == 0:
            print "No orders to fulfill"
            break;
        else:
            print "Amount to Exchange: " + str(TransactionVolumeTicker)
            print "Current Price: " + str(TransactionPriceTicker)
            if BoughtVolume != 0:
                AveragePrice = TransactionPriceTicker / TransactionVolumeTicker
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
print "Full Order List"
print FullOrderList
for Order in FullOrderList:
    print "Order Deleted: " + str(Order[0])
    #cursor.execute("""DELETE FROM BasicOrderBook WHERE OrderNumber = %s""" % (Order[0]))
    #db.commit()
print ""
print "Partial Order List"
print PartialOrderList
for Order in PartialOrderList:
    print "Order Updated: " + str(Order[0])
    print "Volume Updated: " + str(NewOrderVolume)
    cursor.execute("""UPDATE BasicOrderBook SET Volume = %s WHERE OrderNumber = %s""" % (NewOrderVolume, Order[0]))
    db.commit()



'''Logs Transactions'''

print ""
print "Existing Order Fulfillment List:"
print ExistingOrderFulfillmentList
print ""
print "Instant Order Fulfillment List:"
print InstantOrderFulfillmentList
print ""


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



for Index, Order in enumerate(FullOrderList):

    #print "Index: " + str(Index)
    #print "TransactionCount: " + str(TransactionCount)
    TransactionPrice = Order[2]
    TransactionVolume = Order[3]
    TransactionTotal = TransactionPrice * TransactionVolume
    SpreadProfit = 0
    TotalProfit = SpreadProfit + TradingFeeProfit
    if OrderAction == "BUY":
        print "Full Sell"
        BuyOrderAccount = OrderAccount
        BuyOrderNumber = OrderNumber
        BuyOrderPrice = Order[2]
        BuyOrderVolume = TransactionVolumeTicker
        BuyOrderType = "Instant"
        BuyOrderCompletion = InstantOrderFulfillmentList[Index]
        SellOrderAccount = Order[1]
        SellOrderNumber = Order[0]
        SellOrderPrice = Order[2]
        SellOrderVolume = Order[3]
        SellOrderType = Order[4]
        SellOrderCompletion = "Full"
        print "BuyCompletion: " + str(BuyOrderCompletion)
        print "SellCompletion: " + str(SellOrderCompletion)
    if OrderAction == "SELL":
        print "Full Buy"
        BuyOrderAccount = Order[1]
        BuyOrderNumber = Order[0]
        BuyOrderPrice = Order[2]
        BuyOrderVolume = Order[3]
        BuyOrderType = Order[4]
        BuyOrderCompletion = "Full"
        SellOrderAccount = OrderAccount
        SellOrderNumber = OrderNumber
        SellOrderPrice = Order[2]
        SellOrderVolume = TransactionVolumeTicker
        SellOrderType = "Instant"
        SellOrderCompletion = InstantOrderFulfillmentList[Index]
        #print "BuyCompletion: " + str(BuyOrderCompletion)
        #print "SellCompletion: " + str(SellOrderCompletion)

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
    print "Buy Order Type: " + BuyOrderType
    print "Buy Order Completion: " + BuyOrderCompletion
    print ""
    print "Sell Order Number: " + str(SellOrderNumber)
    print "Sell Order Account: " + SellOrderAccount
    print "Sell Order Price: " + str(SellOrderPrice)
    print "Sell Order Volume: " + str(SellOrderVolume)
    print "Sell Order Type: " + SellOrderType
    print "Sell Order Completion: " + SellOrderCompletion
    print ""
    print SellOrderAccount + ": +$" + str(TransactionTotal) + " and -" + str(TransactionVolume) + " BTC"
    print BuyOrderAccount + ": -$" + str(TransactionTotal) + " and +" + str(TransactionVolume) + " BTC"
    print ""

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
    log.write("Buy Order Type: " + BuyOrderType + "\n")
    log.write("Buy Order Completion: " + BuyOrderCompletion + "\n" + "\n")

    log.write("Sell Order Number: " + str(SellOrderNumber) + "\n")
    log.write("Sell Order Account: " + SellOrderAccount + "\n")
    log.write("Sell Order Price: " + str(SellOrderPrice) + "\n")
    log.write("Sell Order Volume: " + str(SellOrderVolume) + "\n")
    log.write("Sell Order Type: " + SellOrderType + "\n")
    log.write("Sell Order Completion: " + SellOrderCompletion + "\n" + "\n")

    log.write(OrderAccount + ": +$" + str(TransactionTotal) + " and -" + str(TransactionVolume) + " BTC" + "\n")
    log.write(Order[1] + ": -$" + str(TransactionTotal) + " and +" + str(TransactionVolume) + " BTC" + "\n")

    log.close()

    cursor.execute("""INSERT INTO TransactionLog(TransactionNumber, TransactionDate, TransactionPrice, TransactionVolume, TransactionTotal, TradingFeeProfit, SpreadProfit, TotalProfit, BuyOrderNumber, BuyOrderAccount, BuyOrderPrice, BuyOrderVolume, BuyOrderType, BuyOrderCompletion, SellOrderNumber, SellOrderAccount, SellOrderPrice, SellOrderVolume, SellOrderType, SellOrderCompletion) VALUES (%d, "%s", %d, %d, %d, %d, %d, %d, %d, "%s", %d, %d, "%s", "%s", %d, "%s", %d, %d, "%s", "%s")""" % (TransactionCount, FormattedDateTime, TransactionPrice, TransactionVolume, TransactionTotal, TradingFeeProfit, SpreadProfit, TotalProfit, BuyOrderNumber, BuyOrderAccount, BuyOrderPrice, BuyOrderVolume, BuyOrderType, BuyOrderCompletion, SellOrderNumber, SellOrderAccount, SellOrderPrice, SellOrderVolume, SellOrderType, SellOrderCompletion))
    db.commit()
    print "Transaction Logged"

    TransactionCount += 1



for Index, Order in enumerate(PartialOrderList):

    #print "Index: " + str(Index)
    #print "TransactionCount: " + str(TransactionCount)
    TransactionPrice = Order[2]
    TransactionVolume = PartialTransactionInstantOrderVolumeList[Index]
    TransactionTotal = TransactionPrice * TransactionVolume
    SpreadProfit = 0
    TotalProfit = SpreadProfit + TradingFeeProfit
    if OrderAction == "BUY":
        print "Partial Sell"
        BuyOrderAccount = OrderAccount
        BuyOrderNumber = OrderNumber
        BuyOrderPrice = Order[2]
        BuyOrderVolume = TransactionVolumeTicker
        BuyOrderType = "Instant"
        BuyOrderCompletion = InstantOrderFulfillmentList[Index - 1]
        SellOrderAccount = Order[1]
        SellOrderNumber = Order[0]
        SellOrderPrice = Order[2]
        SellOrderVolume = Order[3]
        SellOrderType = Order[4]
        SellOrderCompletion = "Partial"
        print "BuyCompletion: " + str(BuyOrderCompletion)
        print "SellCompletion: " + str(SellOrderCompletion)
    if OrderAction == "SELL":
        print "Partial Buy"
        BuyOrderAccount = Order[1]
        BuyOrderNumber = Order[0]
        BuyOrderPrice = Order[2]
        BuyOrderVolume = Order[3]
        BuyOrderType = Order[4]
        BuyOrderCompletion = "Partial"
        SellOrderAccount = OrderAccount
        SellOrderNumber = OrderNumber
        SellOrderPrice = Order[2]
        SellOrderVolume = float(TransactionVolumeTicker)
        SellOrderType = "Instant"
        SellOrderCompletion = InstantOrderFulfillmentList[Index]
        #print "BuyCompletion: " + str(BuyOrderCompletion)
        #print "SellCompletion: " + str(SellOrderCompletion)

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
    print "Buy Order Type: " + BuyOrderType
    print "Buy Order Completion: " + BuyOrderCompletion
    print ""
    print "Sell Order Number: " + str(SellOrderNumber)
    print "Sell Order Account: " + SellOrderAccount
    print "Sell Order Price: " + str(SellOrderPrice)
    print "Sell Order Volume: " + str(SellOrderVolume)
    print "Sell Order Type: " + SellOrderType
    print "Sell Order Completion: " + SellOrderCompletion
    print ""
    print SellOrderAccount + ": +$" + str(TransactionTotal) + " and -" + str(TransactionVolume) + " BTC"
    print BuyOrderAccount + ": -$" + str(TransactionTotal) + " and +" + str(TransactionVolume) + " BTC"
    print ""

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
    log.write("Buy Order Type: " + BuyOrderType + "\n")
    log.write("Buy Order Completion: " + BuyOrderCompletion + "\n" + "\n")

    log.write("Sell Order Number: " + str(SellOrderNumber) + "\n")
    log.write("Sell Order Account: " + SellOrderAccount + "\n")
    log.write("Sell Order Price: " + str(SellOrderPrice) + "\n")
    log.write("Sell Order Volume: " + str(SellOrderVolume) + "\n")
    log.write("Sell Order Type: " + SellOrderType + "\n")
    log.write("Sell Order Completion: " + SellOrderCompletion + "\n" + "\n")

    log.write(OrderAccount + ": +$" + str(TransactionTotal) + " and -" + str(TransactionVolume) + " BTC" + "\n")
    log.write(Order[1] + ": -$" + str(TransactionTotal) + " and +" + str(TransactionVolume) + " BTC" + "\n")

    log.close()

    cursor.execute("""INSERT INTO TransactionLog(TransactionNumber, TransactionDate, TransactionPrice, TransactionVolume, TransactionTotal, TradingFeeProfit, SpreadProfit, TotalProfit, BuyOrderNumber, BuyOrderAccount, BuyOrderPrice, BuyOrderVolume, BuyOrderType, BuyOrderCompletion, SellOrderNumber, SellOrderAccount, SellOrderPrice, SellOrderVolume, SellOrderType, SellOrderCompletion) VALUES (%d, "%s", %d, %d, %d, %d, %d, %d, %d, "%s", %d, %d, "%s", "%s", %d, "%s", %d, %d, "%s", "%s")""" % (TransactionCount, FormattedDateTime, TransactionPrice, TransactionVolume, TransactionTotal, TradingFeeProfit, SpreadProfit, TotalProfit, BuyOrderNumber, BuyOrderAccount, BuyOrderPrice, BuyOrderVolume, BuyOrderType, BuyOrderCompletion, SellOrderNumber, SellOrderAccount, SellOrderPrice, SellOrderVolume, SellOrderType, SellOrderCompletion))
    db.commit()
    print "Transaction Logged"

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
