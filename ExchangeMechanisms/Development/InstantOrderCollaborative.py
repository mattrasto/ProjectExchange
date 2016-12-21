#-------------------------------------------------------------------------------
# Name:        InstantOrderCollaborative
# Version:     3.0
# Purpose:     Creates Instant Order and matches against existing Basic Orders
#
# Author:      Matthew
#
# Created:     05/04/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/15/2014
#-------------------------------------------------------------------------------

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

from __future__ import division
import time
import MySQLdb
import sys



#Initializing database
db = MySQLdb.connect("localhost","root","***","exchange")
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
Data = cursor.fetchone()[0]
print "Database Version: " + str(Data)



#Defines counting variable for test
global TransactionsProcessed
TransactionsProcessed = 0



'''Defining Functions'''



#Defines variable for transaction number

def TransactionNumberCheck():
    try:
        global TransactionCount
        db.commit()
        cursor.execute("""SELECT MAX(TransactionNumber) FROM TransactionLog""")
        MaxTransactionNumber = cursor.fetchone()[0]
        #print "Current Max Transaction: " + str(MaxTransactionNumber)
        TransactionCount = MaxTransactionNumber + 1
        #print ""
        #print "Transaction Number: " +str(TransactionCount)
    except:
        TransactionCount = 1
        #print ""
        #print "Transaction Number: " +str(TransactionCount)



#Defines variable for order number

def OrderNumberCheck():
    try:
        global OrderNumber
        db.commit()
        cursor.execute("""SELECT MAX(IDNumber) FROM IDBook""")
        MaxOrderNumber = cursor.fetchone()[0]
        OrderNumber = MaxOrderNumber + 1
        print ""
        print "Order Number: " +str(OrderNumber)
    except:
        OrderNumber = 1
        print
        print "Order Number: " +str(OrderNumber)



#Determines current bid price of BasicOrderBook

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



#Determines current ask price of BasicOrderBook

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



def main(OrderAccount, OrderAction, OrderConstraint, Price, Volume, Confirmation):
    
    #Initializing database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    
    
    '''Checking User Balances'''
    
    
    
    #Gathers details of user initiating order
    cursor.execute("""SELECT * FROM UserBook WHERE Username = "%s" """ % (OrderAccount))
    UserDetails = cursor.fetchone()
    #Assigns user's balance and volume to static variables
    InstantOrderAccountBalance = UserDetails[3]
    InstantOrderAccountVolume = UserDetails[4]
    print ""
    print "User Balance: " + str(InstantOrderAccountBalance)
    print "User Volume: " + str(InstantOrderAccountVolume)
    print ""
    OrderType = "Instant"
    
    #Calls functions to assign transaction and order numbers
    global TransactionCount
    TransactionNumberCheck()
    OrderNumberCheck()
    
    
    #Checks if there is a negative balance on initiating user and exits if so
    if (InstantOrderAccountBalance < 0) or (InstantOrderAccountVolume < 0):
        print ""
        print "CRITICAL ERROR: User has negative balance"
        print "Exiting..."
        sys.exit()
    
    
    
    '''Checking Bid/Ask Prices'''
    
    
    
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
    TransactionProcessed = False
    OrderPlace = "NO"
    
    
    
    '''Creating Buy/Sell Order Queues'''
    
    
    
    try:
        cursor.execute("""SELECT * FROM BasicOrderBook WHERE Action = "Buy" AND Active = 1 ORDER BY Price""")
        #Primitive buy order queue
        #Note: Refine/optimize query with limit and call for more if transaction not possible
        BuyOrderQueue = cursor.fetchall()
        #Tests for empty queue
        if BuyOrderQueue == ():
            print "No Buy Orders"
            PriceSortedBuyOrderQueue = []
        else:
            
            #print "Buy Order Queue:"
            #print BuyOrderQueue
            
            #Sorts BuyOrderQueue by volume
            VolumeSortedBuyOrderQueue = sorted(BuyOrderQueue, key = lambda tup: tup[3], reverse = True)
            
            #print ""
            #print "Volume Sorted Buy Order Queue:"
            #print VolumeSortedBuyOrderQueue
            
            #Sorts BuyOrderQueue by type
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
            
            #Sorts BuyOrderQueue by price
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
        #Primitive buy order queue
        #Note: Refine/optimize query with limit and call for more if transaction not possible
        SellOrderQueue = cursor.fetchall()
        #Tests for empty queue
        if SellOrderQueue == ():
            print ""
            print "No Sell Orders"
            PriceSortedSellOrderQueue = []
        else:
            
            #print ""
            #print "Sell Order Queue:"
            #print SellOrderQueue
            
            #Sorts SellOrderQueue by volume
            VolumeSortedSellOrderQueue = sorted(SellOrderQueue, key = lambda tup: tup[3], reverse = True)
            
            #print ""
            #print "Volume Sorted Sell Order Queue:"
            #print VolumeSortedSellOrderQueue
            
            #Sorts SellOrderQueue by type
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
            
            #Sorts SellOrderQueue by price
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
    
    
    
    #Checks if the instant order is defined by volume
    if OrderConstraint == "VOLUME":
        #Loops while the user has not accepted the order
        while OrderPlace != "YES":
            #Defines index lists
            OrderList = []
            ExistingOrderCompletionList = []
            InstantOrderCompletionList = []
            TransactionList = []
            #Defines ticker variables
            TransactionPriceTicker = 0
            TransactionVolumeTicker = 0
            RemainingInstantOrderVolume = Volume
            CompletelyFulfilled = False
            #Defines new account variables
            NewInstantOrderAccountBalance = InstantOrderAccountBalance
            NewInstantOrderAccountVolume = InstantOrderAccountVolume
            print ""
            print ""
            print ""
            #Checks if the instant order is a buy order
            if OrderAction == "BUY":
                print "Orders:"
                #Loops while the instant order still has volume to be fulfilled
                while RemainingInstantOrderVolume > 0:
                    #Checks against each order in SellOrderQueue
                    for Order in PriceSortedSellOrderQueue:
                        #Checks if order is owned by same person who is creating instant order
                        if Order[1] != OrderAccount:
                            #Calculates order total
                            SellOrderPrice = Order[2]
                            SellOrderVolume = Order[3]
                            SellOrderTotal = SellOrderPrice * SellOrderVolume
                            print ""
                            print Order
                            #If the sell order has a larger volume than the instant order
                            if SellOrderVolume > RemainingInstantOrderVolume:
                                #Calculates transaction/account statistics
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
                                #Updates remaining volume
                                RemainingInstantOrderVolume = 0
                            #If the sell order has a smaller volume than the instant order
                            elif SellOrderVolume < RemainingInstantOrderVolume:
                                #Calculates transaction/account statistics
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
                                #Updates remaining volume
                                RemainingInstantOrderVolume -= SellOrderVolume
                            #If the sell order has the same volume as the instant order
                            else:
                                #Calculates transaction/account statistics
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
                                #Updates remaining volume
                                RemainingInstantOrderVolume -= SellOrderVolume
                            #Appends sell order to OrderList (Used later as exchanged order index list)
                            OrderList.append(Order)
                            #Appends completion values ("Full" or "Partial") to CompletionList
                            ExistingOrderCompletionList.append(ExistingOrderCompletion)
                            InstantOrderCompletionList.append(InstantOrderCompletion)
                            #Forms list of basic transaction details
                            TransactionDetails = [TransactionPrice, TransactionVolume, TransactionTotal]
                            TransactionList.append(TransactionDetails)
                            #Breaks loop if instant order is completely fulfilled
                            if InstantOrderCompletion == "Full":
                                break;
                    #Checks if instant order has any unfulfilled volume
                    if RemainingInstantOrderVolume == 0:
                        CompletelyFulfilled = True
                    else:
                        print ""
                        print "Not enough orders to fulfill"
                    break;
            #Checks if the instant order is a sell order
            elif OrderAction == "SELL":
                print "Orders:"
                #Loops while the instant order still has volume to be fulfilled
                while RemainingInstantOrderVolume > 0:
                    #Checks against each order in BuyOrderQueue
                    for Order in PriceSortedBuyOrderQueue:
                        #Checks if order is owned by same person who is creating instant order
                        if Order[1] != OrderAccount:
                            #Calculates order total
                            BuyOrderPrice = Order[2]
                            BuyOrderVolume = Order[3]
                            BuyOrderTotal = BuyOrderPrice * BuyOrderVolume
                            print ""
                            print Order
                            #If the buy order has a larger volume than the instant order
                            if BuyOrderVolume > RemainingInstantOrderVolume:
                                #Calculates transaction/account statistics
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
                                #Updates remaining volume
                                RemainingInstantOrderVolume = 0
                            #If the buy order has a smaller volume than the instant order
                            elif BuyOrderVolume < RemainingInstantOrderVolume:
                                #Calculates transaction/account statistics
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
                                #Updates remaining volume
                                RemainingInstantOrderVolume -= BuyOrderVolume
                            #If the sell order has the same volume as the instant order
                            else:
                                #Calculates transaction/account statistics
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
                                #Updates remaining volume
                                RemainingInstantOrderVolume -= BuyOrderVolume
                            #Appends buy order to OrderList (Used later as exchanged order index list)
                            OrderList.append(Order)
                            #Appends completion values ("Full" or "Partial") to CompletionList
                            ExistingOrderCompletionList.append(ExistingOrderCompletion)
                            InstantOrderCompletionList.append(InstantOrderCompletion)
                            #Forms list of basic transaction details
                            TransactionDetails = [TransactionPrice, TransactionVolume, TransactionTotal]
                            TransactionList.append(TransactionDetails)
                            #Breaks loop if instant order is completely fulfilled
                            if InstantOrderCompletion == "Full":
                                break;
                    #Checks if instant order has any unfulfilled volume
                    if RemainingInstantOrderVolume == 0:
                        CompletelyFulfilled = True
                    else:
                        print ""
                        print "Not enough orders to fulfill"
                    break;
            
            
            print ""
            print ""
            print ""
            #Defines static transaction variables
            ExchangeVolume = TransactionVolumeTicker
            ExchangePrice = TransactionPriceTicker
            #Checks if queue is empty
            if ExchangeVolume == 0:
                print "No orders to fulfill"
                print "If order queues are not empty, cause may be same-user trading"
                break;
            else:
                print "Amount to Exchange: " + str(ExchangeVolume)
                print "Current Price: " + str(ExchangePrice)
                
                
                
                #Checks if instant order has enough funds to cover the trading fee expenses
                BuyerEnoughFunds = False
                SellerEnoughFunds = False
                #Gets account balance value and trading fee value from user if it is a buy order
                if OrderAction == "BUY":
                    cursor.execute("""SELECT USDCredit FROM UserBook WHERE Username = "%s" """ % (OrderAccount))
                    BuyOrderUSDBalance = cursor.fetchall()[0][0]
                    cursor.execute("""SELECT TradingFee FROM UserBook WHERE Username = "%s" """ % (OrderAccount))
                    BuyOrderTradingFeeRate = cursor.fetchall()[0][0]
                    if (ExchangePrice + (ExchangePrice * BuyOrderTradingFeeRate)) > BuyOrderUSDBalance:
                        print "CRITICAL ERROR: Buyer's balance is too low to apply trading fees"
                        sys.exit()
                    else:
                        BuyerEnoughFunds = True
                #Gets account balance value and trading fee value from user if it is a sell order
                if OrderAction == "SELL":
                    cursor.execute("""SELECT BTCCredit FROM UserBook WHERE Username = "%s" """ % (OrderAccount))
                    SellOrderBTCBalance = cursor.fetchall()[0][0]
                    cursor.execute("""SELECT TradingFee FROM UserBook WHERE Username = "%s" """ % (OrderAccount))
                    SellOrderTradingFeeRate = cursor.fetchall()[0][0]
                    if (ExchangeVolume + (ExchangeVolume * SellOrderTradingFeeRate)) > SellOrderBTCBalance:
                        print "CRITICAL ERROR: Seller's balance is too low to apply trading fees"
                        sys.exit()
                    else:
                        SellerEnoughFunds = True
                
                
                
                #Checks if fulfilled orders have enough funds to cover the trading fee expenses
                for Index, Order in enumerate(OrderList):
                    #Gets account balance value and trading fee value from user if it is a buy order
                    if Order[5] == "BUY":
                        cursor.execute("""SELECT USDCredit FROM UserBook WHERE Username = "%s" """ % (Order[1]))
                        BuyOrderUSDBalance = cursor.fetchall()[0][0]
                        cursor.execute("""SELECT TradingFee FROM UserBook WHERE Username = "%s" """ % (Order[1]))
                        BuyOrderTradingFeeRate = cursor.fetchall()[0][0]
                        if (TransactionList[Index][2] + (TransactionList[Index][2] * BuyOrderTradingFeeRate)) > BuyOrderBTCBalance:
                            print "CRITICAL ERROR: Buyer's balance is too low to apply trading fees"
                            sys.exit()
                        else:
                            BuyerEnoughFunds = True
                    #Gets account balance value and trading fee value from user if it is a sell order
                    if Order[5] == "SELL":
                        cursor.execute("""SELECT BTCCredit FROM UserBook WHERE Username = "%s" """ % (Order[1]))
                        SellOrderBTCBalance = cursor.fetchall()[0][0]
                        cursor.execute("""SELECT TradingFee FROM UserBook WHERE Username = "%s" """ % (Order[1]))
                        SellOrderTradingFeeRate = cursor.fetchall()[0][0]
                        if (TransactionList[Index][1] + (TransactionList[Index][1] * SellOrderTradingFeeRate)) > SellOrderBTCBalance:
                            print "CRITICAL ERROR: Seller's balance is too low to apply trading fees"
                            sys.exit()
                        else:
                            SellerEnoughFunds = True
                
                
                
                #Checks if any orders are owned by the same user creating the instant order
                for Order in OrderList:
                    if Order[1] == OrderAccount:
                        print "CRITICAL ERROR: User attempted to transact with themselves"
                        sys.exit()
                
                
                
                #Calculates average price per BTC
                if ExchangeVolume != 0:
                    AveragePrice = ExchangePrice / ExchangeVolume
                    print "Average Price Per BTC: " + str(AveragePrice)
                #Checks if testing for manual user confirmation
                if Confirmation == "YES":
                    OrderPlace = raw_input("Accept (Yes/No): ")
                    OrderPlace = OrderPlace.upper()
                    while OrderPlace != "YES" and OrderPlace != "NO":
                        print "Incorrect option. Please enter again:"
                        OrderPlace = raw_input("Accept (Yes/No): ")
                        OrderPlace = OrderPlace.upper()
                    if OrderPlace == "YES":
                        break;
                else:
                    OrderPlace = "YES"
                print "Performing Transaction With Orders:"
    
    
           
    #Checks if the instant order is defined by price
    elif OrderConstraint == "PRICE":
        #Loops while the user has not accepted the order
        while OrderPlace != "YES":
            #Defines index lists
            OrderList = []
            ExistingOrderCompletionList = []
            InstantOrderCompletionList = []
            TransactionList = []
            #Defines ticker variables
            TransactionPriceTicker = 0
            TransactionVolumeTicker = 0
            RemainingInstantOrderBalance = Price
            CompletelyFulfilled = False
            #Defines new account variables
            NewInstantOrderAccountBalance = InstantOrderAccountBalance
            NewInstantOrderAccountVolume = InstantOrderAccountVolume
            print ""
            print ""
            print ""
            #Checks if the instant order is a buy order
            if OrderAction == "BUY":
                print "Orders:"
                #Loops while the instant order still has volume to be fulfilled
                while RemainingInstantOrderBalance > 0:
                    #Checks against each order in SellOrderQueue
                    for Order in PriceSortedSellOrderQueue:
                        #Checks if order is owned by same person who is creating instant order
                        if Order[1] != OrderAccount:
                            #Calculates order total
                            SellOrderPrice = Order[2]
                            SellOrderVolume = Order[3]
                            SellOrderTotal = SellOrderPrice * SellOrderVolume
                            print ""
                            print Order
                            #If the sell order has a larger volume than the instant order
                            if SellOrderTotal > RemainingInstantOrderBalance:
                                #Calculates transaction/account statistics
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
                                #Updates remaining volume
                                RemainingInstantOrderBalance = 0
                            elif SellOrderTotal < RemainingInstantOrderBalance:
                                #Calculates transaction/account statistics
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
                                #Updates remaining volume
                                RemainingInstantOrderBalance -= SellOrderTotal
                            else:
                                #Calculates transaction/account statistics
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
                                #Updates remaining volume
                                RemainingInstantOrderBalance -= SellOrderTotal
                            #Appends buy order to OrderList (Used later as exchanged order index list)
                            OrderList.append(Order)
                            #Appends completion values ("Full" or "Partial") to CompletionList
                            ExistingOrderCompletionList.append(ExistingOrderCompletion)
                            InstantOrderCompletionList.append(InstantOrderCompletion)
                            #Forms list of basic transaction details
                            TransactionDetails = [TransactionPrice, TransactionVolume, TransactionTotal]
                            TransactionList.append(TransactionDetails)
                            #Breaks loop if instant order is completely fulfilled
                            if InstantOrderCompletion == "Full":
                                break;
                    #Checks if instant order has any unfulfilled volume
                    if RemainingInstantOrderBalance == 0:
                        CompletelyFulfilled = True
                    else:
                        print ""
                        print "Not enough orders to fulfill"
                    break;
            #Checks if instant order is a sell order
            elif OrderAction == "SELL":
                print "Orders:"
                #Loops while the instant order still has volume to be fulfilled
                while RemainingInstantOrderBalance > 0:
                    #Checks against each order in BuyOrderQueue
                    for Order in PriceSortedBuyOrderQueue:
                        #Checks if order is owned by same person who is creating instant order
                        if Order[1] != OrderAccount:
                            #Calculates order total
                            BuyOrderPrice = Order[2]
                            BuyOrderVolume = Order[3]
                            BuyOrderTotal = BuyOrderPrice * BuyOrderVolume
                            print ""
                            print Order
                            #If the sell order has a larger volume than the instant order
                            if BuyOrderTotal > RemainingInstantOrderBalance:
                                #Calculates transaction/account statistics
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
                                #Updates remaining volume
                                RemainingInstantOrderBalance = 0
                            #If the sell order has a larger volume than the instant order
                            elif BuyOrderTotal < RemainingInstantOrderBalance:
                                #Calculates transaction/account statistics
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
                                #Updates remaining volume
                                RemainingInstantOrderBalance -= BuyOrderTotal
                            #If the sell order has the same volume as the instant order
                            else:
                                #Calculates transaction/account statistics
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
                                #Updates remaining volume
                                RemainingInstantOrderBalance -= BuyOrderTotal
                            #Appends buy order to OrderList (Used later as exchanged order index list)
                            OrderList.append(Order)
                            #Appends completion values ("Full" or "Partial") to CompletionList
                            ExistingOrderCompletionList.append(ExistingOrderCompletion)
                            InstantOrderCompletionList.append(InstantOrderCompletion)
                            #Forms list of basic transaction details
                            TransactionDetails = [TransactionPrice, TransactionVolume, TransactionTotal]
                            TransactionList.append(TransactionDetails)
                            #Breaks loop if instant order is completely fulfilled
                            if InstantOrderCompletion == "Full":
                                break;
                    #Checks if instant order has any unfulfilled volume
                    if RemainingInstantOrderBalance == 0:
                        CompletelyFulfilled = True
                    else:
                        print ""
                        print "Not enough orders to fulfill"
                    break;
            
            
            
            print ""
            print ""
            print ""
            #Defines static transaction variables
            ExchangeVolume = TransactionVolumeTicker
            ExchangePrice = TransactionPriceTicker
            #Checks if queue is empty
            if ExchangeVolume == 0:
                print "No orders to fulfill"
                break;
            else:
                print "Amount to Exchange: " + str(ExchangeVolume)
                print "Current Price: " + str(ExchangePrice)
                
                
                
                #Checks if instant order has enough funds to cover the trading fee expenses
                BuyerEnoughFunds = False
                SellerEnoughFunds = False
                #Gets account balance value and trading fee value from user if it is a buy order
                if OrderAction == "BUY":
                    cursor.execute("""SELECT USDCredit FROM UserBook WHERE Username = "%s" """ % (OrderAccount))
                    BuyOrderUSDBalance = cursor.fetchall()[0][0]
                    cursor.execute("""SELECT TradingFee FROM UserBook WHERE Username = "%s" """ % (OrderAccount))
                    BuyOrderTradingFeeRate = cursor.fetchall()[0][0]
                    if (ExchangePrice + (ExchangePrice * BuyOrderTradingFeeRate)) > BuyOrderUSDBalance:
                        print "CRITICAL ERROR: Buyer's balance is too low to apply trading fees"
                        sys.exit()
                    else:
                        BuyerEnoughFunds = True
                #Gets account balance value and trading fee value from user if it is a sell order
                if OrderAction == "SELL":
                    cursor.execute("""SELECT BTCCredit FROM UserBook WHERE Username = "%s" """ % (OrderAccount))
                    SellOrderBTCBalance = cursor.fetchall()[0][0]
                    cursor.execute("""SELECT TradingFee FROM UserBook WHERE Username = "%s" """ % (OrderAccount))
                    SellOrderTradingFeeRate = cursor.fetchall()[0][0]
                    if (ExchangeVolume + (ExchangeVolume * SellOrderTradingFeeRate)) > SellOrderBTCBalance:
                        print "CRITICAL ERROR: Seller's balance is too low to apply trading fees"
                        sys.exit()
                    else:
                        SellerEnoughFunds = True
                
                
                
                #Checks if fulfilled orders have enough funds to cover the trading fee expenses
                for Index, Order in enumerate(OrderList):
                    #Gets account balance value and trading fee value from user if it is a buy order
                    if Order[5] == "BUY":
                        cursor.execute("""SELECT USDCredit FROM UserBook WHERE Username = "%s" """ % (Order[1]))
                        BuyOrderUSDBalance = cursor.fetchall()[0][0]
                        cursor.execute("""SELECT TradingFee FROM UserBook WHERE Username = "%s" """ % (Order[1]))
                        BuyOrderTradingFeeRate = cursor.fetchall()[0][0]
                        if (TransactionList[Index][2] + (TransactionList[Index][2] * BuyOrderTradingFeeRate)) > BuyOrderBTCBalance:
                            print "CRITICAL ERROR: Buyer's balance is too low to apply trading fees"
                            sys.exit()
                        else:
                            BuyerEnoughFunds = True
                    #Gets account balance value and trading fee value from user if it is a sell order
                    if Order[5] == "SELL":
                        cursor.execute("""SELECT BTCCredit FROM UserBook WHERE Username = "%s" """ % (Order[1]))
                        SellOrderBTCBalance = cursor.fetchall()[0][0]
                        cursor.execute("""SELECT TradingFee FROM UserBook WHERE Username = "%s" """ % (Order[1]))
                        SellOrderTradingFeeRate = cursor.fetchall()[0][0]
                        if (TransactionList[Index][1] + (TransactionList[Index][1] * SellOrderTradingFeeRate)) > SellOrderBTCBalance:
                            print "CRITICAL ERROR: Seller's balance is too low to apply trading fees"
                            sys.exit()
                        else:
                            SellerEnoughFunds = True
                
                
                
                #Checks if any orders are owned by the same user creating the instant order
                for Order in OrderList:
                    if Order[1] == OrderAccount:
                        print "CRITICAL ERROR: User attempted to transact with themselves"
                        sys.exit()
                
                
                
                #Calculates average price per BTC
                if ExchangeVolume != 0:
                    AveragePrice = ExchangePrice / ExchangeVolume
                    print "Average Price Per BTC: " + str(AveragePrice)
                #Checks if testing for manual user confirmation
                if Confirmation == "YES":
                    OrderPlace = raw_input("Accept (Yes/No): ")
                    OrderPlace = OrderPlace.upper()
                    while OrderPlace != "YES" and OrderPlace != "NO":
                        print "Incorrect option. Please enter again:"
                        OrderPlace = raw_input("Accept (Yes/No): ")
                        OrderPlace = OrderPlace.upper()
                    if OrderPlace == "YES":
                        break;
                else:
                    OrderPlace = "YES"
                print "Performing Transaction With Orders:"
    
    
    
    '''Deletes/Updates Fulfilled Orders'''
    
    
    
    print ""
    print ""
    print ""
    print "Order List"
    print OrderList
    #Cycles through OrderList for fulfilled orders
    for Index, Order in enumerate(OrderList):
        #Checks corresponding index in CompletionLists for completion type
        #Order is deleted if completely fulfilled
        if ExistingOrderCompletionList[Index] == "Full":
            print "Order Deleted: " + str(Order[0])
            cursor.execute("""DELETE FROM BasicOrderBook WHERE OrderNumber = %s""" % (Order[0]))
            db.commit()
        #Order is updated to new volume if partially fulfilled
        elif ExistingOrderCompletionList[Index] == "Partial":
            print "Order Updated: " + str(Order[0])
            print "Volume Updated: " + str(NewExistingOrderVolume)
            cursor.execute("""UPDATE BasicOrderBook SET Volume = %s WHERE OrderNumber = %s""" % (NewExistingOrderVolume, Order[0]))
            db.commit()
    
    #print ""
    #print "Existing Order Completion List"
    #print ExistingOrderCompletionList
    #print ""
    #print "Instant Order Completion List"
    #print InstantOrderCompletionList
    #print ""
    #print "Transaction List"
    #print TransactionList
    
    
    
    '''Logs Transactions'''
    
    
    
    if CompletelyFulfilled != True:
        print ""
        print "Not enough orders to fulfill"
    #Gets current datetime and formats into human readable and database acceptable forms
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
    
    
    
    #Cycles through each fulfilled order
    for Index, Order in enumerate(OrderList):
        
        #Checks each account's trading fee rate
        cursor.execute("""SELECT TradingFee FROM UserBook WHERE Username = "%s" """ % (OrderAccount))
        InstantOrderTradingFeeRate = cursor.fetchall()[0][0]
        cursor.execute("""SELECT TradingFee FROM UserBook WHERE Username = "%s" """ % (Order[1]))
        ExistingOrderTradingFeeRate = cursor.fetchall()[0][0]
        
        #print "Instant Order Trading Fee Rate: " + str(InstantOrderTradingFeeRate)
        #print "Existing Order Trading Fee Rate: " + str(ExistingOrderTradingFeeRate)
        
        #print ""
        #print "Index: " + str(Index)
        #print "TransactionCount: " + str(TransactionCount)
        
        #Assigns transaction details from TransactionList to static variables
        TransactionPrice = TransactionList[Index][0]
        TransactionVolume = TransactionList[Index][1]
        TransactionTotal = TransactionList[Index][2]
        
        #Checks if instant order is a buy order
        if OrderAction == "BUY":
            #Assigns Buy/Sell specific static variables
            #Note: Adjusted price variables are the values of the transaction price reduced by the trading fee value
            
            #print str(ExistingOrderCompletionList[Index]) + " Sell"
            
            BuyOrderAccount = OrderAccount
            BuyOrderNumber = OrderNumber
            BuyOrderPrice = Order[2]
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
            
            #print "BuyCompletion: " + str(BuyOrderCompletion)
            #print "SellCompletion: " + str(SellOrderCompletion)
        
        #Checks if instant order is a sell order
        if OrderAction == "SELL":
            #Assigns Buy/Sell specific static variables
            #Note: Adjusted price variables are the values of the transaction price reduced by the trading fee value
            
            #print str(ExistingOrderCompletionList[Index]) + " Buy"
            
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
            
            #print "BuyCompletion: " + str(BuyOrderCompletion)
            #print "SellCompletion: " + str(SellOrderCompletion)
        
        print ""
        print "Trading Fee Adjusted Buy Order Volume: " + str(AdjustedBuyOrderVolume)
        print "Trading Fee Adjusted Sell Order Price: " + str(AdjustedSellOrderPrice)
        
        #Calculates adjusted total
        AdjustedSellOrderTotal = AdjustedSellOrderPrice * TransactionVolume
        #Calculates profits
        TradingFeeProfit = ((TransactionVolume - AdjustedBuyOrderVolume) * TransactionPrice) + (TransactionTotal - (TransactionVolume * AdjustedSellOrderPrice))
        SpreadProfitPerBTC = BuyOrderPrice - SellOrderPrice #Calculates profit gained by Bid/Ask spread
        SpreadProfit = SpreadProfitPerBTC * TransactionVolume
        TotalProfit = TradingFeeProfit + SpreadProfit
        
        print ""
        print "------------------------------"
        print "Transaction Details:"
        print ""
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
        print "------------------------------"
        print ""
        
        #Declares that the transaction has been fully processed
        TransactionProcessed = True
        
        
        
        '''Logging Transaction'''
        
        
        
        try:
            cursor.execute("""INSERT INTO TransactionLog(TransactionNumber, TransactionDate, TransactionPrice, TransactionVolume, TransactionTotal, TradingFeeProfit, SpreadProfit, TotalProfit, BuyOrderNumber, BuyOrderAccount, BuyOrderPrice, BuyOrderVolume, BuyOrderType, BuyOrderCompletion, SellOrderNumber, SellOrderAccount, SellOrderPrice, SellOrderVolume, SellOrderType, SellOrderCompletion) VALUES (%d, "%s", %f, %f, %f, %f, %f, %f, %d, "%s", %f, %f, "%s", "%s", %d, "%s", %f, %f, "%s", "%s")""" % (TransactionCount, FormattedDateTime, TransactionPrice, TransactionVolume, TransactionTotal, TradingFeeProfit, SpreadProfit, TotalProfit, BuyOrderNumber, BuyOrderAccount, BuyOrderPrice, BuyOrderVolume, BuyOrderType, BuyOrderCompletion, SellOrderNumber, SellOrderAccount, SellOrderPrice, SellOrderVolume, SellOrderType, SellOrderCompletion))
            db.commit()
            print "Transaction Successfully Logged"
        except:
            print "ERROR: Transaction Unsuccessfully Logged"
        
        
        
        '''Updating Account Volumes'''
        
        
        #Gathers buy order account's trading volume
        cursor.execute("""SELECT Volume FROM UserBook WHERE Username = "%s" """ % (BuyOrderAccount))
        BuyOrderAccountVolume = cursor.fetchall()[0][0]
        
        #Gathers sell order account's trading volume
        cursor.execute("""SELECT Volume FROM UserBook WHERE Username = "%s" """ % (SellOrderAccount))
        SellOrderAccountVolume = cursor.fetchall()[0][0]
        
        #Calculates new trading volume of accounts
        NewBuyOrderAccountVolume = BuyOrderAccountVolume + TransactionVolume
        NewSellOrderAccountVolume = SellOrderAccountVolume + TransactionVolume
        
        try:
            print ""
            print "Updating Account Volumes:"
            print BuyOrderAccount + ": +" + str(TransactionVolume) + " BTC"
            print SellOrderAccount + ": +" + str(TransactionVolume) + " BTC"
            
            #print "New Buy Order Account Volume: " +str(NewBuyOrderAccountVolume)
            #print "New Sell Order Account Volume: " +str(NewSellOrderAccountVolume)
            
            cursor.execute("""UPDATE UserBook SET Volume = %d WHERE Username = "%s" """ % (NewBuyOrderAccountVolume, BuyOrderAccount))
            cursor.execute("""UPDATE UserBook SET Volume = %d WHERE Username = "%s" """ % (NewSellOrderAccountVolume, SellOrderAccount))
            db.commit()
            print "Account Volumes Successfully Updated"
        except:
            print "ERROR: Account Volumes Unsuccessfully Updated"
        
        
        
        '''Updating Account Credits'''
        
        
        #Gathers USD and BTC credit of buy order account
        cursor.execute("""SELECT USDCredit, BTCCredit FROM UserBook WHERE Username = "%s" """ % (BuyOrderAccount))
        BuyOrderAccountCredits = cursor.fetchall()[0]
        BuyOrderAccountUSDCredit = BuyOrderAccountCredits[0]
        BuyOrderAccountBTCCredit = BuyOrderAccountCredits[1]
        
        #Gathers USD and BTC credit of sell order account
        cursor.execute("""SELECT USDCredit, BTCCredit FROM UserBook WHERE Username = "%s" """ % (SellOrderAccount))
        SellOrderAccountCredits = cursor.fetchall()[0]
        SellOrderAccountUSDCredit = SellOrderAccountCredits[0]
        SellOrderAccountBTCCredit = SellOrderAccountCredits[1]
        
        #Calculates new credits of accounts
        NewBuyOrderAccountUSDCredit = BuyOrderAccountUSDCredit - TransactionTotal
        NewBuyOrderAccountBTCCredit = BuyOrderAccountBTCCredit + AdjustedBuyOrderVolume
        NewSellOrderAccountUSDCredit = SellOrderAccountUSDCredit + AdjustedSellOrderTotal
        NewSellOrderAccountBTCCredit = SellOrderAccountBTCCredit - TransactionVolume
        
        #print ""
        #print "New Buy Order Account USD Credit: " + str(NewBuyOrderAccountUSDCredit)
        #print "New Buy Order Account BTC Credit: " + str(NewBuyOrderAccountBTCCredit)
        #print "New Sell Order Account USD Credit: " + str(NewSellOrderAccountUSDCredit)
        #print "New Sell Order Account BTC Credit: " + str(NewSellOrderAccountBTCCredit)
        
        try:
            print ""
            print "Updating Account Credits:"
            cursor.execute("""UPDATE UserBook SET USDCredit = %f, BTCCredit = %f WHERE Username = "%s" """ % (NewBuyOrderAccountUSDCredit, NewBuyOrderAccountBTCCredit, BuyOrderAccount))
            cursor.execute("""UPDATE UserBook SET USDCredit = %f, BTCCredit = %f WHERE Username = "%s" """ % (NewSellOrderAccountUSDCredit, NewSellOrderAccountBTCCredit, SellOrderAccount))
            db.commit()
            print BuyOrderAccount + ": -$" + str(TransactionTotal) + " and +" + str(AdjustedBuyOrderVolume) + " BTC"
            print SellOrderAccount + ": +$" + str(AdjustedSellOrderTotal) + " and -" + str(TransactionVolume) + " BTC"
            print "Account Credits Successfully Updated"
        except:
            print "ERROR: Account Credits Unsuccessfully Updated"
        
        
        
        '''Logging Transaction Statistics'''
        
        
        
        #Opens new text file and logs transaction and order statistics
        log = open("Transaction" + str(TransactionCount) + ".txt", "a") #Defines log file open variable
        log.write("------------------------------" + "\n" + "Transaction Details:" + "\n" + "\n")
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
        log.write("Buy Order Trading Fee Rate: " + str(BuyOrderTradingFeeRate) + "\n")
        log.write("Buy Order Adjusted Volume: " + str(AdjustedBuyOrderVolume) + "\n")
        log.write("Buy Order Type: " + BuyOrderType + "\n")
        log.write("Buy Order Completion: " + BuyOrderCompletion + "\n" + "\n")
    
        log.write("Sell Order Number: " + str(SellOrderNumber) + "\n")
        log.write("Sell Order Account: " + SellOrderAccount + "\n")
        log.write("Sell Order Price: " + str(SellOrderPrice) + "\n")
        log.write("Sell Order Trading Fee Rate: " + str(SellOrderTradingFeeRate) + "\n")
        log.write("Sell Order Adjusted Price: " + str(AdjustedSellOrderPrice) + "\n")
        log.write("Sell Order Volume: " + str(SellOrderVolume) + "\n")
        log.write("Sell Order Type: " + SellOrderType + "\n")
        log.write("Sell Order Completion: " + SellOrderCompletion + "\n" + "\n")
        
        log.write(BuyOrderAccount + ": +$" + str(TransactionTotal) + " and -" + str(AdjustedBuyOrderVolume) + " BTC" + "\n")
        log.write(SellOrderAccount + ": -$" + str(AdjustedSellOrderTotal) + " and +" + str(TransactionVolume) + " BTC" + "\n")
        log.write("------------------------------")
        
        log.close()
        
        #Adds one to the transaction count for the current instant order
        TransactionCount += 1
    
    
    
    '''Adding Virtual Order to BasicOrderLog'''
    
    
    
    #Note: Possibly migrate instant orders to separate table
    
    #Assigns undefined variables to transaction-defined values
    if TransactionProcessed == True:
        if OrderConstraint == "PRICE":
            Volume = TransactionVolume
        elif OrderConstraint == "VOLUME":
            Price = TransactionPrice
        
        #Inserts record into IDBook to ensure no duplicate entries
        db.commit()
        cursor.execute("""INSERT INTO IDBook(IDNumber, Type, Action) VALUES(%d, "%s", "%s")""" % (OrderNumber, OrderType.capitalize(), OrderAction.capitalize()))
        db.commit()
        
        try:
            
            #print "Price: " + str(Price)
            #print "Volume: " +str(Volume)
            
            #Inserts record into BasicOrderLog
            db.commit()
            cursor.execute("""INSERT INTO BasicOrderLog(OrderNumber, Username, Price, Volume, Type, Action) VALUES(%d, "%s", %f, %f, "%s", "%s")""" % (OrderNumber, OrderAccount, TransactionPrice, Volume, OrderType.capitalize(), OrderAction.capitalize()))
            db.commit()
            print ""
            print "Order Successfully Logged"
        except:
            print "ERROR: Database Log Insert Failure"
        
        
    
        db.commit()
        db.close()
        return OrderNumber
    
    else:
        return False



if __name__ == "__main__":
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print "Database version : %s " % data
    
    global TransactionCount
    
    
    
    '''Setting Variables'''
    
    
    
    #Prompts for user to put instant order under
    print ""
    OrderAccount = raw_input("Username: ")
    OrderAccount = OrderAccount.capitalize()
    UserFound = False
    #Checks to see if user exists
    while UserFound != True:
        cursor.execute("""SELECT * FROM UserBook WHERE Username = "%s" """ % (OrderAccount))
        UserDetails = cursor.fetchone()
        if UserDetails != None:
            print "User found"
            UserFound = True
        else:
            print "User not found. Please enter again: "
            OrderAccount = raw_input("Username: ")
            OrderAccount = OrderAccount.capitalize()
    #Gathers user's balance and volume
    cursor.execute("""SELECT * FROM UserBook WHERE Username = "%s" """ % (OrderAccount))
    UserDetails = cursor.fetchone()
    InstantOrderAccountBalance = UserDetails[3]
    InstantOrderAccountVolume = UserDetails[4]
    print ""
    print "User Balance: " + str(InstantOrderAccountBalance)
    print "User Volume: " + str(InstantOrderAccountVolume)
    print ""
    
    #Checks if there is a negative balance on initiating user and exits if so
    if (InstantOrderAccountBalance < 0) or (InstantOrderAccountVolume < 0):
        print "CRITICAL ERROR: User has negative balance"
        print "Exiting..."
        sys.exit()
    
    
    
    #Prompts for action ("BUY" or "SELL") of instant order
    OrderAction = raw_input("Action (Buy/Sell): ")
    OrderAction = OrderAction.upper()
    while OrderAction != "BUY" and OrderAction != "SELL":
        print "Incorrect action. Please enter again:"
        OrderAction = raw_input("Action (Buy/Sell): ")
        OrderAction = OrderAction.upper()
    
    
    
    #Prompts for constraint ("PRICE" or "VOLUME") of instant order
    OrderConstraint = raw_input("Place By (Price/Volume): ")
    OrderConstraint = OrderConstraint.upper()
    while OrderConstraint != "PRICE" and OrderConstraint != "VOLUME":
        print "Incorrect order constraint. Please enter again:"
        OrderConstraint = raw_input("Place By (Price/Volume): ")
        OrderConstraint = OrderConstraint.upper()
    
    
    
    #Prompts for proper price value if OrderConstraint is set to price
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
    else:
        Price = None
    
    
    
    #Prompts for proper volume value if OrderConstraint is set to volume
    if OrderConstraint == "VOLUME":
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
        if OrderAction == "SELL":
            if Volume > UserDetails[4]:
                print "Volume higher than balance. Defaulting to current balance."
                Volume = UserDetails[4]
            print "Volume: " + str(Volume)
    else:
        Volume = None
    
    
    
    #Defines manual confirmation before order is transacted
    Confirmation = "YES"
    
    #Execute
    if Price != None or Volume != None:
        main(OrderAccount, OrderAction, OrderConstraint, Price, Volume, Confirmation)
    else:
        print ""
        print "ERROR: Price or Volume are undefined"


