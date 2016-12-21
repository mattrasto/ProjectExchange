#-------------------------------------------------------------------------------
# Name:        ExchangeEngineCollaborative
# Version:     3.0
# Purpose:     Prepares and executes exchange between two viable Basic Orders
#
# Author:      Matthew
#
# Created:     05/04/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/15/2014
#-------------------------------------------------------------------------------

#Add support for partial/full fulfillment preferences
#Add check in eligibility for whether the order should be full or not
#Full > Partial

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

import time
import MySQLdb



#Initializing database
db = MySQLdb.connect("localhost","root","***","exchange")
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
Data = cursor.fetchone()[0]
print "Database Version: " + str(Data)



'''Defining Functions'''



#Checks highest number in TransactionLog, then assigns said number + 1 to TransactionCount

def TransactionNumberCheck():
    try:
        global TransactionCount
        db.commit()
        cursor.execute("""SELECT MAX(TransactionNumber)+1 FROM TransactionLog""")
        TransactionCount = cursor.fetchone()[0]
        if TransactionCount == None:
            TransactionCount = 1
    except:
        TransactionCount = 1



#Checks current bid price in BasicOrderBook

def BidPriceChecker():
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
    return BidPrice



#Checks current ask price in BasicOrderBook

def AskPriceChecker():
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
    return AskPrice



def main(Loops):

    #Defining variables for recording
    global TransactionCount
    global LoopCount
    global TransactionsProcessed
    global SuccessfulLogs
    LoopCount = 0
    TransactionsProcessed = 0
    SuccessfulLogs = 0

    #Performs transactions until Loops reaches LoopCount
    #In production versions, this will be replaced by a loop that occurs until no transactions are possible
    while LoopCount < Loops:

        #Initializing database
        db = MySQLdb.connect("localhost","root","***","exchange")
        cursor = db.cursor()
        cursor.execute("SELECT VERSION()")
        Data = cursor.fetchone()[0]
        print "Database Version: " + str(Data)



        '''Setting Mechanism Variables'''



        TopBuyOrderFound = False
        TopSellOrderFound = False
        TransactionPossible = False

        print ""
        print ""
        print ""
        print "----------Starting Round: " + str(LoopCount + 1) + "----------"
        print ""
        print ""

        TransactionNumberCheck()
        print ""
        BidPrice = BidPriceChecker()
        #print BidPrice
        AskPrice = AskPriceChecker()
        #print AskPrice

        print ""
        TopBuyOrderFound = False
        TopSellOrderFound = False
        TransactionPossible = False



        '''Order Refinement Mechanism'''



        try:
            cursor.execute("""SELECT * FROM BasicOrderBook WHERE Action = "Buy" AND Price >= %f  AND Active = 1 ORDER BY Price""" % (AskPrice))
            BuyOrderQueue = cursor.fetchall()
            #Checks for negative spread
            if BuyOrderQueue == ():
                print "No Negative Spread Buy Orders"
            else:

                #print "Buy Order Queue:"
                #print BuyOrderQueue

                #Sorts negative spread BuyOrderQueue by Volume
                VolumeSortedBuyOrderQueue = sorted(BuyOrderQueue, key = lambda tup: tup[3], reverse = True)

                #print ""
                #print "Volume Sorted Buy Order Queue:"
                #print VolumeSortedBuyOrderQueue

                #Sorts negative spread BuyOrderQueue by type
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

                #Sorts negative spread BuyOrderQueue by price
                PriceSortedBuyOrderQueue = sorted(TypeSortedBuyOrderQueue, key = lambda tup: tup[2], reverse = True)

                #print ""
                #print "Price Sorted Buy Order Queue:"
                #print PriceSortedBuyOrderQueue

                TopBuyOrderFound = True
        except:
            print ""
            print "ERROR: Database Fetch Exception"
            print "Possible Cause: No Ask Price"



        try:
            cursor.execute("""SELECT * FROM BasicOrderBook WHERE Action = "Sell" AND Price <= %f  AND Active = 1 ORDER BY Price""" % (BidPrice))
            SellOrderQueue = cursor.fetchall()
            if SellOrderQueue == ():
                print ""
                print "No Negative Spread Sell Orders"
            else:

                #print ""
                #print "Sell Order Queue:"
                #print SellOrderQueue

                #Sorts negative spread SellOrderQueue by volume
                VolumeSortedSellOrderQueue = sorted(SellOrderQueue, key = lambda tup: tup[3], reverse = True)

                #print ""
                #print "Volume Sorted Sell Order Queue:"
                #print VolumeSortedSellOrderQueue

                #Sorts negative spread SellOrderQueue by type
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

                #Sorts negative spread SellOrderQueue by price
                PriceSortedSellOrderQueue = sorted(TypeSortedSellOrderQueue, key = lambda tup: tup[2])

                #print ""
                #print "Price Sorted Sell Order Queue:"
                #print PriceSortedSellOrderQueue

                TopSellOrderFound = True
        except:
            print ""
            print "ERROR: Database Fetch Exception"
            print "Possible Cause: No Bid Price"



        '''Order Matching Mechanism'''



        #Checks each order in BuyOrderQueue against each order in SellOrderQueue for match

        if TopBuyOrderFound == True and TopSellOrderFound == True:
            for BuyOrder in PriceSortedBuyOrderQueue:
                for SellOrder in PriceSortedSellOrderQueue:
                    #Checks if price of top order in BuyOrderQueue is more than that of SellOrderQueue
                    if BuyOrder[2] >= SellOrder[2]:

                        #Gets account balance values from users
                        cursor.execute("""SELECT USDCredit FROM UserBook WHERE Username = "%s" """ % (BuyOrder[1]))
                        BuyOrderUSDBalance = cursor.fetchall()[0][0]
                        cursor.execute("""SELECT BTCCredit FROM UserBook WHERE Username = "%s" """ % (SellOrder[1]))
                        SellOrderBTCBalance = cursor.fetchall()[0][0]

                        #Gets trading fee values from users
                        cursor.execute("""SELECT TradingFee FROM UserBook WHERE Username = "%s" """ % (BuyOrder[1]))
                        BuyOrderTradingFeeRate = cursor.fetchall()[0][0]
                        cursor.execute("""SELECT TradingFee FROM UserBook WHERE Username = "%s" """ % (SellOrder[1]))
                        SellOrderTradingFeeRate = cursor.fetchall()[0][0]



                        BuyerEnoughFunds = False
                        SellerEnoughFunds = False
                        if (BuyOrder[2] + (BuyOrder[2] * BuyOrderTradingFeeRate)) > BuyOrderUSDBalance:
                            print "CRITICAL ERROR: Buyer's balance is too low to apply trading fees"
                        else:
                            BuyerEnoughFunds = True
                        if (SellOrder[3] + (SellOrder[3] * SellOrderTradingFeeRate)) > SellOrderBTCBalance:
                            print "CRITICAL ERROR: Seller's balance is too low to apply trading fees"
                        else:
                            SellerEnoughFunds = True



                        '''ADD ANY EXTRA TRANSACTION ELIGIBILITY CHECKING HERE'''



                        #Checks to make sure both the buyer and seller have enough funds and are not the same person
                        if BuyerEnoughFunds == True and SellerEnoughFunds == True and BuyOrder[1] != SellOrder[1]:
                            print ""
                            print "Transaction possible. Initializing transaction process."
                            print ""
                            print "Transacting Orders:"
                            print "Buy: " + str(BuyOrder[0]) + " (" + str(BuyOrder[4]) + ")"
                            print "Sell: " + str(SellOrder[0]) + " (" + str(SellOrder[4]) + ")"
                            print ""
                            #Assigning static variables for reference
                            TopBuyOrder = BuyOrder
                            TopSellOrder = SellOrder
                            TransactionPossible = True
                            break;
                        else:
                            print "Transaction not possible due to insufficient funds or same-user trading. Reassessing prices."
                    else:
                        print "Transaction not possible due to negative price difference. Reassessing prices."
                if TransactionPossible == True:
                    break;



        '''Transaction Mechanism'''



        if TransactionPossible == True:

            #Gets and formats current time into readable and database-acceptable forms
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

            #Assigns order number static variables
            print ""
            TopBuyOrderNumber = TopBuyOrder[0]
            TopSellOrderNumber = TopSellOrder[0]
            #Assigns price at which transaction occurs, which is the sell price
            TransactionPrice = TopSellOrder[2]

            #Performs volume calculations and updates volumes
            if TopBuyOrder[3] == TopSellOrder[3]:
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
                cursor.execute("""UPDATE BasicOrderBook SET Volume = %f WHERE OrderNumber = %d""" % (NewBuyOrderVolume, TopBuyOrderNumber))
                db.commit()
                print "Order " + str(TopBuyOrder[0]) + " Volume Updated To " + str(NewBuyOrderVolume)
            elif TopBuyOrder[3] < TopSellOrder[3]:
                BuyOrderCompletion = "Full"
                SellOrderCompletion = "Partial"
                FulfilledOrderList.append(TopBuyOrder[0])
                NewSellOrderVolume = TopSellOrder[3] - TopBuyOrder[3]
                TransactionVolume = TopBuyOrder[3]
                cursor.execute("""UPDATE BasicOrderBook SET Volume = %f WHERE OrderNumber = %d""" % (NewSellOrderVolume, TopSellOrderNumber))
                db.commit()
                print "Order " + str(TopSellOrder[0]) + " Volume Updated To " + str(NewSellOrderVolume)



            '''Setting Transaction Variables'''


            #Defines buy order volume and sell order prices adjusted for trading fee differences
            print ""
            AdjustedBuyOrderVolume = TransactionVolume - (TransactionVolume * BuyOrderTradingFeeRate)
            AdjustedSellOrderPrice = TopSellOrder[2] - (TopSellOrder[2] * SellOrderTradingFeeRate)
            print "Trading Fee Adjusted Buy Order Volume: " + str(AdjustedBuyOrderVolume)
            print "Trading Fee Adjusted Sell Order Price: " + str(AdjustedSellOrderPrice)

            #Calculates transaction total and exchange profit
            TransactionTotal = TransactionPrice * TransactionVolume
            AdjustedSellOrderTotal = AdjustedSellOrderPrice * TransactionVolume
            TradingFeeProfit = ((TransactionVolume - AdjustedBuyOrderVolume) * TransactionPrice) + (TransactionTotal - (TransactionVolume * AdjustedSellOrderPrice))
            SpreadProfitPerBTC = TopBuyOrder[2] - TopSellOrder[2] #Calculates profit gained by Bid/Ask spread
            SpreadProfit = SpreadProfitPerBTC * TransactionVolume
            TotalProfit = TradingFeeProfit + SpreadProfit
            print ""

            #Assigns buy and sell order static variables
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

            TransactionsProcessed += 1



            '''Printing Transaction Statistics'''



            print ""
            print "------------------------------"
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
            print "------------------------------"
            print ""



            '''Logging Transaction (Database)'''



            try:
                cursor.execute("""INSERT INTO TransactionLog(TransactionNumber, TransactionDate, TransactionPrice, TransactionVolume, TransactionTotal, TradingFeeProfit, SpreadProfit, TotalProfit, BuyOrderNumber, BuyOrderAccount, BuyOrderPrice, BuyOrderVolume, BuyOrderType, BuyOrderCompletion, SellOrderNumber, SellOrderAccount, SellOrderPrice, SellOrderVolume, SellOrderType, SellOrderCompletion) VALUES (%d, "%s", %f, %f, %f, %f, %f, %f, %d, "%s", %f, %f, "%s", "%s", %d, "%s", %f, %f, "%s", "%s")""" % (TransactionCount, FormattedDateTime, TransactionPrice, TransactionVolume, TransactionTotal, TradingFeeProfit, SpreadProfit, TotalProfit, BuyOrderNumber, BuyOrderAccount, BuyOrderPrice, BuyOrderVolume, BuyOrderType, BuyOrderCompletion, SellOrderNumber, SellOrderAccount, SellOrderPrice, SellOrderVolume, SellOrderType, SellOrderCompletion))
                db.commit()
                print "Transaction Successfully Logged"
                SuccessfulLogs += 1
            except:
                print "ERROR: Transaction Unsuccessfully Logged"



            '''Updating Account Volumes'''


            #Gets volume of buy order account
            cursor.execute("""SELECT Volume FROM UserBook WHERE Username = "%s" """ % (BuyOrderAccount))
            BuyOrderAccountVolume = cursor.fetchall()[0][0]

            #Gets volume of sell order account
            cursor.execute("""SELECT Volume FROM UserBook WHERE Username = "%s" """ % (SellOrderAccount))
            SellOrderAccountVolume = cursor.fetchall()[0][0]

            #Calculates new volume of accounts
            NewBuyOrderAccountVolume = BuyOrderAccountVolume + TransactionVolume
            NewSellOrderAccountVolume = SellOrderAccountVolume + TransactionVolume

            try:
                print ""
                print "Updating Account Volumes:"
                print BuyOrderAccount + ": +" + str(TransactionVolume) + " BTC"
                print SellOrderAccount + ": +" + str(TransactionVolume) + " BTC"
                cursor.execute("""UPDATE UserBook SET Volume = %f WHERE Username = "%s" """ % (NewBuyOrderAccountVolume, BuyOrderAccount))
                cursor.execute("""UPDATE UserBook SET Volume = %f WHERE Username = "%s" """ % (NewSellOrderAccountVolume, SellOrderAccount))
                db.commit()
                print "Account Volumes Successfully Updated"
            except:
                print "ERROR: Account Volumes Unsuccessfully Updated"



            '''Updating Credits'''


            #Gets credit values of buy order account
            cursor.execute("""SELECT USDCredit, BTCCredit FROM UserBook WHERE Username = "%s" """ % (BuyOrderAccount))
            BuyOrderAccountCredits = cursor.fetchall()[0]
            BuyOrderAccountUSDCredit = BuyOrderAccountCredits[0]
            BuyOrderAccountBTCCredit = BuyOrderAccountCredits[1]

            #Gets credit values of sell order account
            cursor.execute("""SELECT USDCredit, BTCCredit FROM UserBook WHERE Username = "%s" """ % (SellOrderAccount))
            SellOrderAccountCredits = cursor.fetchall()[0]
            SellOrderAccountUSDCredit = SellOrderAccountCredits[0]
            SellOrderAccountBTCCredit = SellOrderAccountCredits[1]

            #Calculates new credit values of accounts
            NewBuyOrderAccountUSDCredit = BuyOrderAccountUSDCredit - TransactionTotal
            NewBuyOrderAccountBTCCredit = BuyOrderAccountBTCCredit + AdjustedBuyOrderVolume
            NewSellOrderAccountUSDCredit = SellOrderAccountUSDCredit + AdjustedSellOrderTotal
            NewSellOrderAccountBTCCredit = SellOrderAccountBTCCredit - TransactionVolume

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



            '''Deleting Fulfilled Orders'''



            print ""
            print "Fulfilled Order List:"
            print FulfilledOrderList
            for OrderNumber in FulfilledOrderList:
                print ""
                print "Deleting Order: " + str(OrderNumber)
                cursor.execute("""UPDATE BasicOrderLog SET TransactionNumber = %s, TransactionDate = %s, TerminationReason = "Fulfilled", TerminationDate = %s WHERE OrderNumber = %s""", (TransactionCount, FormattedDateTime, FormattedDateTime, OrderNumber))
                cursor.execute("""DELETE FROM BasicOrderBook WHERE OrderNumber = %d""" % (OrderNumber))
                db.commit()
                print "Order Successfully Deleted"



            '''Logging Transaction (Text)'''



            log = open("Transaction" + str(TransactionCount) + ".txt", "a")
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

            log.write(BuyOrderAccount + ": -$" + str(TransactionTotal) + " and +" + str(AdjustedBuyOrderVolume) + " BTC" + "\n")
            log.write(SellOrderAccount + ": +$" + str(AdjustedSellOrderTotal) + " and -" + str(TransactionVolume) + " BTC" + "\n")
            log.write("------------------------------")
            print ""

            #Checks for new TransactionCount value
            TransactionNumberCheck();

        else:
            print ""
            print "Transaction not possible. Reassessing prices."
            print ""


        #Checks for new bid and ask prices
        BidPriceChecker()
        AskPriceChecker()
        print ""

        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #Assigns Limit and Conditional orders to active if a transaction is possible
        #WARNING: ONLY FOR TESTING; MUST BE REMOVED IN PRODUCTION VERSIONS
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        if BidPrice != None and AskPrice != None and TransactionPossible == True:
            cursor.execute("""UPDATE BasicOrderBook SET Active = 1 WHERE Type = "Limit" AND Action = "Buy" AND PRICE >= %f AND Price <= %f""" % (BidPrice, TransactionPrice))
            db.commit()
            cursor.execute("""UPDATE BasicOrderBook SET Active = 1 WHERE Type = "Limit" AND Action = "Sell" AND PRICE <= %f AND Price >= %f""" % (AskPrice, TransactionPrice))
            db.commit()



        LoopCount += 1

        #Commits any remaining database changes and closes the connection
        db.commit()
        db.close()



if __name__ == "__main__":
    main(1)
