#-------------------------------------------------------------------------------
# Name:        ExchangeEngineCollaborative-v0.0
# Purpose:     Refines orders and transacts according to order priority
#              NOTE: DEFECTIVE. DO NOT USE
#
# Author:      Matthew
#
# Created:     05/04/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    29/04/2014
#-------------------------------------------------------------------------------

#Add scaling "TemporaryBidPrice" and "TemporaryAskPrice" to check each limit/conditional order against to ensure that all orders are accounted for
#OR make "TemporaryBidPrice" and "TemporaryAskprice" the actual BidPrice and AskPrice

#Possible method: Determine TopBuyOrder and check against each eligible sell order, then go down BuyOrderQueue until match found

import os
print os.path.exists("DBDeleteBasicOrderBook-v1_1.py")
#from subprocess import call
#call(["python","DBDeleteBasicOrderBook-v1_1.py"])
import time
import MySQLdb

db = MySQLdb.connect("localhost","root","***","exchangedatabase")

cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data



cursor.execute("""SELECT MIN(Price) FROM BasicOrderBook WHERE Action = "Sell" """)
MinOrderList = cursor.fetchall()
#print MinOrderList
MinOrder = MinOrderList[0]
#print MinOrder
AskPrice = MinOrder[0]
print "Ask Price: " + str(AskPrice)



cursor.execute("""SELECT MAX(Price) FROM BasicOrderBook WHERE Action = "Buy" """)
MinOrderList = cursor.fetchall()
#print MinOrderList
MinOrder = MinOrderList[0]
#print MinOrder
BidPrice = MinOrder[0]
print "Bid Price: " + str(BidPrice)



TopBuyOrderFound = False
TopSellOrderFound = False
LoopCount = 0
TransactionCount = 1



while LoopCount < 2:
    BuyCheckRound = 0
    cursor.execute("""SELECT * FROM BasicOrderBook WHERE Action = "Buy" AND Price >= %d  AND Active = 1 ORDER BY Price""" % (AskPrice))
    BuyOrderQueue = cursor.fetchall()
    print ""
    print ""
    print "Buy Order Queue: " + str(BuyOrderQueue)
    while TopBuyOrderFound != True:
        if BuyOrderQueue != ():
            print ""
            print "Negative spread detected. Initiating order refinement."
            print "Initiating Round " + str(BuyCheckRound)
            BuyOrderHighestPriceList = []
            BuyOrderQueue = sorted(BuyOrderQueue, key = lambda tup: tup[2], reverse = True)
            print ""
            print "Sorted BuyOrderQueue"
            print BuyOrderQueue
            if BuyCheckRound >= len(BuyOrderQueue):
                break;
            if BuyOrderQueue[BuyCheckRound][2] >= AskPrice:
                print ""
                print "Eligible Order"
                print BuyOrderQueue[BuyCheckRound]
                BuyOrderHighestPriceList.append(BuyOrderQueue[BuyCheckRound])
            print ""
            print "BuyOrderHighestPriceList"
            print BuyOrderHighestPriceList
            BuyLimitOrderHighestPriceList = []
            OrderFound = False
            for Order in BuyOrderHighestPriceList:
                if Order[4] == "Liquid":
                    BuyLimitOrderHighestPriceList.append(Order)
                    OrderFound = True
            if OrderFound != True:
                for Order in BuyOrderHighestPriceList:
                    if Order[4] == "Limit":
                        if Order[2] == AskPrice:
                            BuyLimitOrderHighestPriceList.append(Order)
                            OrderFound = True
                        else:
                            print "Limit order not within price threshold"
            if OrderFound != True:
                for Order in BuyOrderHighestPriceList:
                    if Order[4] == "Conditional":
                        if Order[8] == True:
                            BuyLimitOrderHighestPriceList.append(Order)
                            OrderFound = True
            if OrderFound == True:
                print ""
                print "BuyLimitOrderHighestPriceList"
                print BuyLimitOrderHighestPriceList
                BuyLimitOrderHighestPriceHighestVolume = []
                MaxVolume = 0
                for Order in BuyLimitOrderHighestPriceList:
                    if Order[3] > MaxVolume:
                        MaxVolume = Order[3]
                        BuyLimitOrderHighestPriceHighestVolume = [Order]
                    elif Order[3] == MaxVolume:
                        BuyLimitOrderHighestPriceHighestVolume.append(Order)
                print ""
                print "BuyLimitOrderHighestPriceHighestPrice"
                print BuyLimitOrderHighestPriceHighestVolume
                if BuyLimitOrderHighestPriceHighestVolume != []:
                    TopBuyOrder = BuyLimitOrderHighestPriceHighestVolume[0]
                    print ""
                    print "TopBuyOrder"
                    print TopBuyOrder
                    TopBuyOrderFound = True
                else:
                    print ""
                    print "No TopBuyOrder"
                    TopBuyOrderFound = False
            else:
                print ""
                print "No eligible buy orders found. Reassessing prices."
                BuyCheckRound += 1
        else:
            print "Positive spread detected. Reassessing prices."


    SellCheckRound = 0
    cursor.execute("""SELECT * FROM BasicOrderBook WHERE Action = "Sell" AND Price <= %d  AND Active = 1 ORDER BY Price""" % (BidPrice))
    SellOrderQueue = cursor.fetchall()
    print ""
    print ""
    print "Sell Order Queue: " + str(SellOrderQueue)
    while TopSellOrderFound != True:
        if SellOrderQueue != ():
            print ""
            print "Negative spread detected. Initiating order refinement."
            print "Initiating Round " + str(SellCheckRound)
            SellOrderLowestPriceList = []
            SellOrderQueue = sorted(SellOrderQueue, key = lambda tup: tup[2])
            print ""
            print "Sorted SellOrderQueue"
            print SellOrderQueue
            if SellCheckRound >= len(SellOrderQueue):
                break;
            if SellOrderQueue[SellCheckRound][2] <= BidPrice:
                print ""
                print "Eligible Order"
                SellOrderLowestPriceList.append(SellOrderQueue[SellCheckRound])
            print ""
            print "SellOrderLowestPriceList"
            print SellOrderLowestPriceList
            SellLimitOrderLowestPriceList = []
            OrderFound = False
            for Order in SellOrderLowestPriceList:
                if Order[4] == "Liquid":
                    SellLimitOrderLowestPriceList.append(Order)
                    OrderFound = True
            if OrderFound != True:
                for Order in SellOrderLowestPriceList:
                    if Order[4] == "Limit":
                        if Order[2] == BidPrice:
                            SellLimitOrderLowestPriceList.append(Order)
                            OrderFound = True
                        else:
                            print "Limit order not within price threshold"
            if OrderFound != True:
                for Order in SellOrderLowestPriceList:
                    if Order[4] == "Conditional":
                        if Order[8] == True:
                            SellLimitOrderLowestPriceList.append(Order)
                            OrderFound = True
                        else:
                            print "Conditional not active."
            if OrderFound == True:
                print ""
                print "SellLimitOrderLowestPriceList"
                print SellLimitOrderLowestPriceList
                SellLimitOrderLowestPriceHighestVolume = []
                MaxVolume = 0
                for Order in SellLimitOrderLowestPriceList:
                    if Order[3] > MaxVolume:
                        MaxVolume = Order[3]
                        SellLimitOrderLowestPriceHighestVolume = [Order]
                    elif Order[3] == MaxVolume:
                        SellLimitOrderLowestPriceHighestVolume.append(Order)
                print ""
                print "SellLimitOrderLowestPriceHighestVolume"
                print SellLimitOrderLowestPriceHighestVolume
                if SellLimitOrderLowestPriceHighestVolume != []:
                    TopSellOrder = SellLimitOrderLowestPriceHighestVolume[0]
                    print ""
                    print "TopSellOrder"
                    print TopSellOrder
                    TopSellOrderFound = True
                else:
                    print ""
                    print "No TopSellOrder"
                    TopSellOrderFound = False
            else:
                print ""
                print "No eligible sell orders found. Reassessing prices."
                SellCheckRound += 1
        else:
            print "Positive spread detected. Reassessing prices."



    if TopSellOrderFound == True and TopBuyOrderFound == True:
        if TopBuyOrder[2] >= TopSellOrder[2]:
            print ""
            print "Top orders:"
            print "Buy:"
            print TopBuyOrder
            print "Sell:"
            print TopSellOrder
            print ""


            LocalTime = time.localtime(time.time())
            LocalTimeMinutes = LocalTime[4]
            LocalTimeSeconds = LocalTime[5]
            if LocalTimeMinutes < 10:
                LocalTimeMinutes = "0" + str(LocalTimeMinutes)
            if LocalTimeSeconds < 10:
                LocalTimeSeconds = "0" + str(LocalTimeSeconds)
            FormattedDate = str(LocalTime[1]) + "/" +  str(LocalTime[2]) + "/" +  str(LocalTime[0])
            FormattedTime = str(LocalTime[3]) + ":" +  str(LocalTimeMinutes) + ":" +  str(LocalTimeSeconds)
            print "Transaction Date: " + FormattedDate
            print "Transaction Time: " + FormattedTime
            print "Transaction Number: " + str(TransactionCount)
            print "Transacted Sell Order: " + str(TopSellOrder[0])
            print "Transacted Buy Order: " + str(TopBuyOrder[0])
            TransactionPrice = max(TopBuyOrder[2], TopBuyOrder[2]) #Assigns price at which transaction occurs with maximum profit
            print "Transaction Price: " + str(TransactionPrice)
            SpreadProfitPerBTC = TopBuyOrder[2] - TopSellOrder[2] #Calculates profit gained by Bid/Ask spread
            print "Spread Profit Per BTC: " + str(SpreadProfitPerBTC)
            if TopBuyOrder[3] == TopSellOrder[3]: #Performs volume calculations and reassignment
                SpreadProfit = SpreadProfitPerBTC * TopSellOrder[3]
                cursor.execute("""DELETE FROM BasicOrderBook WHERE OrderNumber = %d""" % (TopSellOrder[0]))
                #db.commit()
                print "After 1st delete"
                cursor.execute("""DELETE FROM BasicOrderBook WHERE OrderNumber = %d""" % (TopBuyOrder[0]))
                #db.commit()
                print "After 2nd delete"
                TransactionVolume = TopSellOrder[3]
                print "Transaction Volume: " + str(TransactionVolume)
                TransactionTotal = TransactionPrice * TransactionVolume
                print "Transaction Total: " + str(TransactionTotal)
            elif TopBuyOrder[3] > TopSellOrder[3]:
                NewBuyOrderVolume = TopBuyOrder[3] - TopSellOrder[3]
                cursor.execute("""DELETE FROM BasicOrderBook WHERE OrderNumber = %d""" % (TopSellOrder[0]))
                #db.commit()
                print "After 3rd delete"
                TransactionVolume = TopSellOrder[3]
                print "Transaction Volume: " + str(TransactionVolume)
                SpreadProfit = SpreadProfitPerBTC * TransactionVolume
                #Update TopBuyOrder to have new volume NewBuyOrderVolume
                TransactionTotal = TransactionPrice * TransactionVolume
                print "Transaction Total: " + str(TransactionTotal)
            elif TopBuyOrder[3] < TopSellOrder[3]:
                NewSellOrderVolume = TopSellOrder[3] - TopBuyOrder[3]
                cursor.execute("""DELETE FROM BasicOrderBook WHERE OrderNumber = %d""" % (TopBuyOrder[0]))
                #db.commit()
                print "After 4th delete"
                TransactionVolume = TopBuyOrder[3]
                print "Transaction Volume: " + str(TransactionVolume)
                SpreadProfit = SpreadProfitPerBTC * TransactionVolume
                #Update TopSellOrder to have new volume NewSellOrderVolume
                TransactionTotal = TransactionPrice * TransactionVolume
                print "Transaction Total: " + str(TransactionTotal)
            print "Spread Profit: " + str(SpreadProfit)
            TransactionCount += 1
            LoopCount += 1

        else:
            print ""
            print "No transaction possible. Reassessing prices."
            LoopCount += 1
    else:
        print ""
        print "No transaction possible. Reassessing prices."
        LoopCount += 1

db.rollback()
