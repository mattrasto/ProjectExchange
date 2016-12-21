#-------------------------------------------------------------------------------
# Name:        ExchangeEngineCollaborative
# Version:     1.2
# Purpose:     Improved version of ExchangeEngineCollaborative-v1.0
#
# Author:      Matthew
#
# Created:     05/04/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    07/17/2014
#-------------------------------------------------------------------------------

#Add Credit Updating

import time
import MySQLdb

db = MySQLdb.connect("localhost","root","***","exchangedatabase")

cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data



'''Defining Functions'''



def TransactionNumberCheck():
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
    else:
        print "Ask Price: " + str(AskPrice)



'''Setting Mechanism Variables'''



TopBuyOrderFound = False
TopSellOrderFound = False
TransactionPossible = False
LoopCount = 0
TransactionNumberCheck()



while LoopCount < 1:
    print ""
    print ""
    print ""
    print "Beginning Round " + str(LoopCount + 1)
    print ""
    print ""

    TransactionNumberCheck();
    BidPriceChecker();
    #print BidPrice
    AskPriceChecker();
    #print AskPrice

    print ""
    TopBuyOrderFound = False
    TopSellOrderFound = False
    TransactionPossible = False



    '''Order Refinement Mechanism'''



    try:
        cursor.execute("""SELECT * FROM BasicOrderBook WHERE Action = "Buy" AND Price >= %d  AND Active = 1 ORDER BY Price""" % (AskPrice))
        BuyOrderQueue = cursor.fetchall()
        if BuyOrderQueue == ():
            print "No Negative Spread Buy Orders"
        else:
            print "Buy Order Queue:"
            print BuyOrderQueue
            VolumeSortedBuyOrderQueue = sorted(BuyOrderQueue, key = lambda tup: tup[3], reverse = True)
            print ""
            print "Volume Sorted Buy Order Queue:"
            print VolumeSortedBuyOrderQueue
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
            print ""
            print "Type Sorted Buy Order Queue:"
            print TypeSortedBuyOrderQueue
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
        cursor.execute("""SELECT * FROM BasicOrderBook WHERE Action = "Sell" AND Price <= %d  AND Active = 1 ORDER BY Price""" % (BidPrice))
        SellOrderQueue = cursor.fetchall()
        if SellOrderQueue == ():
            print ""
            print "No Negative Spread Sell Orders"
        else:
            print ""
            print "Sell Order Queue:"
            print SellOrderQueue
            VolumeSortedSellOrderQueue = sorted(SellOrderQueue, key = lambda tup: tup[3], reverse = True)
            print ""
            print "Volume Sorted Sell Order Queue:"
            print VolumeSortedSellOrderQueue
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
            print ""
            print "Type Sorted Sell Order Queue:"
            print TypeSortedSellOrderQueue
            PriceSortedSellOrderQueue = sorted(TypeSortedSellOrderQueue, key = lambda tup: tup[2])
            print ""
            print "Price Sorted Sell Order Queue:"
            print PriceSortedSellOrderQueue
            TopSellOrderFound = True
    except:
        print ""
        print "ERROR: Database Fetch Exception"
        print "Possible Cause: No Bid Price"



    '''Order Matching Mechanism'''



    if TopBuyOrderFound == True and TopSellOrderFound == True:
        for BuyOrder in PriceSortedBuyOrderQueue:
            for SellOrder in PriceSortedSellOrderQueue:
                if BuyOrder[2] >= SellOrder[2]:
                    print ""
                    print "Transaction possible. Initializing transaction process."
                    print ""
                    print "Transacting Orders:"
                    print "Buy: " + str(BuyOrder[0]) + " (" + str(BuyOrder[4]) + ")"
                    print "Sell: " + str(SellOrder[0]) + " (" + str(SellOrder[4]) + ")"
                    print ""
                    TopBuyOrder = BuyOrder
                    TopSellOrder = SellOrder
                    TransactionPossible = True
                    break;
                else:
                    print "Transaction not possible. Reassessing prices."
            if TransactionPossible == True:
                break;



    '''Transaction Mechanism'''



    if TransactionPossible == True:

        LocalTime = time.localtime(time.time())
        LocalTimeMinutes = LocalTime[4]
        LocalTimeSeconds = LocalTime[5]
        if LocalTimeMinutes < 10:
            LocalTimeMinutes = "0" + str(LocalTimeMinutes)
        if LocalTimeSeconds < 10:
            LocalTimeSeconds = "0" + str(LocalTimeSeconds)
        FormattedDatabaseDate = str(LocalTime[0]) + "-" +  str(LocalTime[1]) + "-" +  str(LocalTime[2])
        FormattedDate = str(LocalTime[1]) + "/" +  str(LocalTime[2]) + "/" +  str(LocalTime[0])
        FormattedTime = str(LocalTime[3]) + ":" +  str(LocalTimeMinutes) + ":" +  str(LocalTimeSeconds)
        FormattedDateTime = str(FormattedDatabaseDate) + " " + str(FormattedTime)

        FulfilledOrderList = []

        cursor.execute("""SELECT TradingFee FROM UserBook WHERE Username = "%s" """ % (TopBuyOrder[1]))
        BuyOrderTradingFeeRate = cursor.fetchall()[0][0]
        cursor.execute("""SELECT TradingFee FROM UserBook WHERE Username = "%s" """ % (TopSellOrder[1]))
        SellOrderTradingFeeRate = cursor.fetchall()[0][0]
        print "Buy Order Trading Fee Rate: " + str(BuyOrderTradingFeeRate)
        print "Sell Order Trading Fee Rate: " + str(SellOrderTradingFeeRate)

        print ""
        TopBuyOrderNumber = TopBuyOrder[0]
        TopSellOrderNumber = TopSellOrder[0]
        TransactionPrice = TopSellOrder[2] #Assigns price at which transaction occurs

        if TopBuyOrder[3] == TopSellOrder[3]: #Performs volume calculations and reassignment
            BuyOrderCompletion = "Full"
            SellOrderCompletion = "Full"
            FulfilledOrderList.append(TopBuyOrder[0])
            FulfilledOrderList.append(TopSellOrder[0])
            TransactionVolume = TopSellOrder[3]
        elif TopBuyOrder[3] > TopSellOrder[3]:
            BuyOrderCompletion = "Partial"
            SellOrderCompletion = "Full"
            FulfilledOrderList.append(TopSellOrder[0])
            NewBuyOrderVolume = TopBuyOrder[3] - TopSellOrder[3]
            TransactionVolume = TopSellOrder[3]
            cursor.execute("""UPDATE BasicOrderBook SET Volume = %d WHERE OrderNumber = %d""" % (NewBuyOrderVolume, TopBuyOrderNumber))
            db.commit()
            print "Order " + str(TopBuyOrder[0]) + " Volume Updated To " + str(NewBuyOrderVolume)
        elif TopBuyOrder[3] < TopSellOrder[3]:
            BuyOrderCompletion = "Full"
            SellOrderCompletion = "Partial"
            FulfilledOrderList.append(TopBuyOrder[0])
            NewSellOrderVolume = TopSellOrder[3] - TopBuyOrder[3]
            TransactionVolume = TopBuyOrder[3]
            cursor.execute("""UPDATE BasicOrderBook SET Volume = %d WHERE OrderNumber = %d""" % (NewSellOrderVolume, TopSellOrderNumber))
            db.commit()
            print "Order " + str(TopSellOrder[0]) + " Volume Updated To " + str(NewSellOrderVolume)



        '''Setting Transaction Variables'''



        print ""
        AdjustedBuyOrderVolume = TransactionVolume - (TransactionVolume * BuyOrderTradingFeeRate)
        AdjustedSellOrderPrice = TopSellOrder[2] - (TopSellOrder[2] * SellOrderTradingFeeRate)
        print "Trading Fee Adjusted Buy Order Volume: " + str(AdjustedBuyOrderVolume)
        print "Trading Fee Adjusted Sell Order Price: " + str(AdjustedSellOrderPrice)

        TransactionTotal = TransactionPrice * TransactionVolume
        AdjustedSellOrderTotal = AdjustedSellOrderPrice * TransactionVolume
        TradingFeeProfit = ((TransactionVolume - AdjustedBuyOrderVolume) * TransactionPrice) + (TransactionTotal - (TransactionVolume * AdjustedSellOrderPrice))
        SpreadProfitPerBTC = TopBuyOrder[2] - TopSellOrder[2] #Calculates profit gained by Bid/Ask spread
        SpreadProfit = SpreadProfitPerBTC * TransactionVolume
        TotalProfit = TradingFeeProfit + SpreadProfit
        print ""

        BuyOrderAccount = TopBuyOrder[1]
        BuyOrderNumber = TopBuyOrder[0]
        BuyOrderPrice = TopBuyOrder[2]
        BuyOrderVolume = TopBuyOrder[3]
        BuyOrderType = TopBuyOrder[4]
        SellOrderAccount = TopSellOrder[1]
        SellOrderNumber = TopSellOrder[0]
        SellOrderPrice = TopSellOrder[2]
        SellOrderVolume = TopSellOrder[3]
        SellOrderType = TopSellOrder[4]



        '''Printing Transaction Statistics'''



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
            print BuyOrderAccount + ": +" + str(TransactionVolume) + " BTC"
            print SellOrderAccount + ": +" + str(TransactionVolume) + " BTC"
            cursor.execute("""UPDATE UserBook SET Volume = %d WHERE Username = "%s" """ % (NewBuyOrderAccountVolume, BuyOrderAccount))
            cursor.execute("""UPDATE UserBook SET Volume = %d WHERE Username = "%s" """ % (NewSellOrderAccountVolume, SellOrderAccount))
            db.commit()
            print "Account Volumes Successfully Updated"
        except:
            print "ERROR: Account Volumes Unsuccessfully Updated"



        '''Updating Credits'''



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



        '''Deleting Fulfilled Orders'''



        print ""
        print "Fulfilled Order List"
        print FulfilledOrderList
        for OrderNumber in FulfilledOrderList:
            print ""
            print "Deleting Order: " + str(OrderNumber)
            cursor.execute("""UPDATE BasicOrderLog SET TransactionNumber = %s, TransactionDate = %s, TerminationReason = "Fulfilled", TerminationDate = %s WHERE OrderNumber = %s""", (TransactionCount, FormattedDateTime, FormattedDateTime, OrderNumber))
            #cursor.execute("""DELETE FROM BasicOrderBook WHERE OrderNumber = %d""" % (OrderNumber))
            db.commit()
            print "Order Successfully Deleted"



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

        log.write(BuyOrderAccount + ": -$" + str(TransactionTotal) + " and +" + str(AdjustedBuyOrderVolume) + " BTC" + "\n")
        log.write(SellOrderAccount + ": +$" + str(AdjustedSellOrderTotal) + " and -" + str(TransactionVolume) + " BTC")
        print ""

        TransactionNumberCheck();

    else:
        print ""
        print "Transaction not possible. Reassessing prices."
        print ""



    BidPriceChecker()
    AskPriceChecker()
    if BidPrice != None and AskPrice != None and TransactionPossible == True:
        cursor.execute("""UPDATE BasicOrderBook SET Active = 1 WHERE Type = "Limit" AND Action = "Buy" AND PRICE >= %d AND Price <= %s""" % (BidPrice, TransactionPrice))
        db.commit()
        cursor.execute("""UPDATE BasicOrderBook SET Active = 1 WHERE Type = "Limit" AND Action = "Sell" AND PRICE <= %d AND Price >= %s""" % (AskPrice, TransactionPrice))
        db.commit()



    LoopCount += 1



'''
Variables Index:

Transaction: (Within each loop)
-Number: TransactionCount
-Date: FormattedDate
-Time: FormattedTime
-Price: TransactionPrice
-Volume: TransactionVolume
-Total: TransactionTotal
-Buy Order Number: TopBuyOrderNumber |or| TopBuyOrder[0]
-Buy Order Account: TopBuyOrder[1]
-Buy Order Price: TopBuyOrder[2]
-Buy Order Volume: TopBuyOrder[3]
-Buy Order Adjusted Volume: AdjustedBuyOrderVolume
-Buy Order Trading Fee Rate: BuyOrderTradingFeeRate
-Buy Order Type: TopBuyOrder[4]
-Sell Order Number: TopSellOrderNumber |or| TopSellOrder[0]
-Sell Order Price: TopSellOrder[2]
-Sell Order Trading Fee Rate: SellOrderTradingFeeRate
-Sell Order Adjusted Price: AdjustedSellOrderPrice
-Sell Order Volume: TopSellOrder[3]
-Sell Order Account: TopSellOrder[1]
-Sell Order Type: TopSellOrder[4]
-Spread Profit Per BTC: SpreadProfitPerBTC
-Total Spread Profit: SpreadProfit
'''


db.close()
