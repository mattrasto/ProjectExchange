#-------------------------------------------------------------------------------
# Name:        EFInstantOrder-v0.0
# Purpose:
#
# Author:      Matthew
#
# Created:     05/04/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    10/04/2014
#-------------------------------------------------------------------------------

import heapq
import time

nlargest = 1
global nlargest

nsmallest = 1
global nsmallest

transaction_count = 1
global transaction_count

limit_order_transaction_count = 1
global limit_order_transaction_count

buy_book = {}

sell_book = {}

class Order(object):

    def __init__(self, useraccount, x, y):
        self.useraccount = useraccount
        self.x = x
        self.y = y

    def add_buy_book_order(self): #Adds buy order to buy_book
        order_count = 0
        for i in buy_book:
            order_count += 1
        for i in sell_book:
            order_count += 1
        #print "order_count: " + str(order_count)
        order_number = order_count + 1 #Counts current number of orders and adds 1
        #print "order_number: " + str(order_number)
        order = "Order" + str(order_number) #Assigns order number to string as "Order#"
        #print "order: " + order
        buy_book[order] = [self.useraccount, self.x, self.y] #Adds to buy_book

    def add_sell_book_order(self): #Adds sell order to sell_book
        order_count = 0
        for i in buy_book:
            order_count += 1
        for i in sell_book:
            order_count += 1
        #print "order_count: " + str(order_count)
        order_number = order_count + 1 #Counts current number of orders and adds 1
        #print "order_number: " + str(order_number)
        order = "Order" + str(order_number) #Assigns order number to string as "Order#"
        #print "order: " + order
        sell_book[order] = [self.useraccount, self.x, self.y] #Adds to sell_book

#All things above this line are for testing

class InstantOrder(object):

    def __init__(self, account, volume, order_type):
        self.account = account
        self.volume = volume
        self.order_type = order_type

    def sell_price_check(self, nlargest):
        self.nlargest = nlargest
        sell_book_value_list = []
        buy_price_list = []
        for i in sell_book:
            sell_book_value_list = sell_book[i] #Creates list of orders in sell_book
            #print sell_book_value_list
            buy_price_list.append(sell_book_value_list[1]) #Creates list of prices in sell_book
        if buy_price_list == []:
            self.sell_price = "None"
            print "Buy Price: None below sell price."
        else:
            if nlargest > len(buy_price_list):
                print "Not enough bitcoins for sale."
                self.buy_price = 0
            else:
                self.buy_price_list = heapq.nlargest(nlargest, buy_price_list) #Finds maximum price in list
                #print buy_price_list
                self.buy_price = self.buy_price_list[nlargest-1]
                #print "Buy Price: " + str(self.buy_price)  + " - Number: " + str(self.nlargest)

    def buy_price_check(self, nsmallest):
        self.nsmallest = nsmallest
        buy_book_value_list = []
        sell_price_list = []
        for i in buy_book:
            buy_book_value_list = buy_book[i] #Creates list of orders in buy_book
            #print buy_book_value_list
            sell_price_list.append(buy_book_value_list[1]) #Creates list of prices in sell_book
        if sell_price_list == []:
            self.sell_price = "None"
            print "Sell Price: None above buy price."
        else:
            if nsmallest > len(sell_price_list):
                print "Not enough bitcoins to buy."
                self.sell_price = 0
            else:
                self.sell_price_list = heapq.nsmallest(nsmallest, sell_price_list) #Finds minimum price in list
                #print sell_price_list
                self.sell_price = self.sell_price_list[nsmallest-1]
                #print "Sell Price: " + str(self.sell_price) + " - Number: " + str(self.nsmallest)

    def sell_volume_check(self):
        buy_price_order_volumes = []
        for i in sell_book.values():
            if i[1] == self.buy_price:
                buy_price_order_volumes.append(i[2]) #Makes a list of volumes of orders in price range
        if buy_price_order_volumes == []:
            print "Buy Order Volume: None"
        else:
            #print "Buy Price Order Volumes: " + str(buy_price_order_volumes)
            self.buy_order_volume = max(1, buy_price_order_volumes) #Sets maximum value in list of volumes at certain price
            #print "Buy Order Volume: " + str(self.buy_order_volume[0])

    def buy_volume_check(self):
        sell_price_order_volumes = []
        for i in buy_book.values():
            if i[1] == self.sell_price:
                sell_price_order_volumes.append(i[2]) #Makes a list of volumes of orders in price range
        #print "Sell Price Order Volumes: " + str(sell_price_order_volumes)
        if sell_price_order_volumes == []:
            print "Sell Order Volume: None"
        else:
            self.sell_order_volume = max(1, sell_price_order_volumes) #Sets maximum value in list of volumes at certain price
            #print "Sell Order Volume: " + str(self.sell_order_volume)

    def sell_top_order_check(self): #Labels account number and account of top buy order
        for i in range(len(sell_book)):
            #print sell_book.values();
            #print i;
            #print self.buy_price;
            #print self.buy_order_volume[0];
            if sell_book.values()[i][1] == self.buy_price and sell_book.values()[i][2] == self.buy_order_volume[0]:
                self.sell_top_order_number = sell_book.keys()[i]
                self.sell_top_order_account = sell_book.values()[i][0]
                break;
            else:
                #print "Buy Order Check Else"
                self.sell_top_order_number = 0
                self.sell_top_order_account = 0
        if self.sell_top_order_number == 0 or self.sell_top_order_account == 0:
            print "No top order account."
        else:
            #print "Sell Top Order Number: " + str(self.sell_top_order_number)
            #print "Sell Top Order Account: " + str(self.sell_top_order_account)
            self.sell_order_numbers.append(self.sell_top_order_number)
            self.sell_order_accounts.append(self.sell_top_order_account)
            #print "Sell Order Numbers: " + str(self.sell_order_numbers);
            #print "Sell Order Accounts: " + str(self.sell_order_accounts);

    def buy_top_order_check(self): #Labels account number and account of top sell order
        for i in range(len(buy_book)):
            #print buy_book.values();
            #print i;
            #print self.sell_price;
            #print self.sell_order_volume[0];
            if buy_book.values()[i][1] == self.sell_price and buy_book.values()[i][2] == self.sell_order_volume[0]:
                self.buy_top_order_number = buy_book.keys()[i]
                self.buy_top_order_account = buy_book.values()[i][0]
                break;
            else:
                #print "Sell Order Check Else"
                self.buy_top_order_number = 0
                self.buy_top_order_account = 0
        if self.buy_top_order_number == 0 or self.buy_top_order_account == 0:
            print "No top order account."
        else:
            #print "Buy Top Order Number: " + str(self.buy_top_order_number)
            #print "Buy Top Order Account: " + str(self.buy_top_order_account)
            self.buy_order_numbers.append(self.buy_top_order_number)
            self.buy_order_accounts.append(self.buy_top_order_account)
            #print "Buy Order Numbers: " + str(self.buy_order_numbers)
            #print "Buy Order Accounts: " + str(self.buy_order_accounts);

    def price_estimator(self):
        self.average_sum = 0
        self.instant_order_volume = self.volume
        self.sell_order_price_list = []
        self.buy_order_price_list = []
        self.sell_order_volume_list = []
        self.buy_order_volume_list = []
        self.sell_top_order_type = []
        self.buy_top_order_type = []
        self.sell_order_numbers = []
        self.sell_order_accounts = []
        self.buy_order_numbers = []
        self.buy_order_accounts = []
        self.transaction_price_ticker = 0
        if self.order_type == 0:
            #self.sell_price_check(nlargest);
            self.sell_volume_check();
            #print "Instant Order Volume: " + str(self.volume)
            if self.buy_order_volume[0] >= self.volume:
                self.transaction_price_ticker = self.buy_price * self.volume
                #print "Buy Transaction Price Ticker: " + str(self.transaction_price_ticker)
            elif self.buy_order_volume[0] < self.volume:
                self.sell_price_check(nlargest); #USE heapq.nlargest(#, list) FOR PRICE CHECKING
                self.sell_volume_check();
                while self.volume > 0:
                    #print "Initiating Top Sell Order Check"
                    self.sell_top_order_check();
                    self.volume_difference = self.buy_order_volume[0] - self.volume
                    #print "Volume Difference: " + str(self.volume_difference)
                    if self.volume_difference > 0:
                        self.sell_top_order_type.append("PARTIAL SELL")
                        #self.sell_top_order_check();
                        break;
                    if self.buy_price == 0:
                        print self.sell_order_price_list
                        break;
                    self.sell_order_price_list.append(self.buy_price)
                    self.sell_order_volume_list.append(self.buy_order_volume)
                    self.transaction_price_ticker += self.buy_price * self.buy_order_volume[0]
                    #print "Buy Transaction Price Ticker: " + str(self.transaction_price_ticker)
                    self.volume -= self.buy_order_volume[0]
                    #print "Instant Order Volume: " + str(self.volume)
                    #print "nlargest: " + str(self.nlargest)
                    self.nlargest += 1
                    self.sell_price_check(self.nlargest); #USE heapq.nlargest(#, list) FOR PRICE CHECKING
                    self.sell_volume_check();
                    self.sell_top_order_type.append("FULL SELL")
                self.transaction_price_ticker += self.buy_price * self.volume
                self.average = self.transaction_price_ticker / self.instant_order_volume
                self.sell_order_volume_list.append(self.volume)
                self.sell_order_price_list.append(self.buy_price)
                #print "Instant Order Volume: " + str(self.volume)
                #print "Buy Transaction Price Ticker: " + str(self.transaction_price_ticker)
            else:
                print "Buy else"
        elif self.order_type == 1:
            #self.buy_price_check(nsmallest);
            self.buy_volume_check();
            #print "Instant Order Volume: " + str(self.volume)
            if self.sell_order_volume[0] >= self.volume:
                self.transaction_price_ticker = self.sell_price * self.volume
                #print "Buy Transaction Price Ticker: " + str(self.transaction_price_ticker)
            elif self.sell_order_volume[0] < self.volume:
                self.buy_price_check(nsmallest); #USE heapq.nsmallest(#, list) FOR PRICE CHECKING
                self.buy_volume_check();
                while self.volume > 0:
                    #print "Initiating Top Sell Order Check"
                    self.buy_top_order_check();
                    self.volume_difference = self.sell_order_volume[0] - self.volume
                    #print "Volume Difference: " + str(self.volume_difference)
                    if self.volume_difference > 0:
                        self.buy_top_order_type.append("PARTIAL BUY")
                        #self.buy_top_order_check();
                        break;
                    if self.sell_price == 0:
                        print self.buy_order_price_list
                        break;
                    self.buy_order_price_list.append(self.sell_price)
                    self.buy_order_volume_list.append(self.sell_order_volume)
                    self.transaction_price_ticker += self.sell_price * self.sell_order_volume[0]
                    #print "Buy Transaction Price Ticker: " + str(self.transaction_price_ticker)
                    self.volume -= self.sell_order_volume[0]
                    #print "Instant Order Volume: " + str(self.volume)
                    #print "nsmallest: " + str(self.smallest)
                    self.nsmallest += 1
                    self.buy_price_check(self.nsmallest); #USE heapq.nsmallest(#, list) FOR PRICE CHECKING
                    self.buy_volume_check();
                    self.buy_top_order_type.append("FULL BUY")
                self.transaction_price_ticker += self.sell_price * self.volume
                self.average = self.transaction_price_ticker / self.instant_order_volume
                self.buy_order_volume_list.append(self.volume)
                self.buy_order_price_list.append(self.sell_price)
                #print "Instant Order Volume: " + str(self.volume)
                #print "Sell Transaction Price Ticker: " + str(self.transaction_price_ticker)
            else:
                print "Sell else"

    def transaction(self):
        global transaction_count
        global limit_order_transaction_count
        self.limit_order_transaction_list = []
        self.price_estimator();
        localtime = time.localtime(time.time())
        local_time_minutes = localtime[4]
        local_time_seconds = localtime[5]
        if local_time_minutes < 10:
            local_time_minutes = "0" + str(local_time_minutes)
        if local_time_seconds < 10:
            local_time_seconds = "0" + str(local_time_seconds)
        self.formatted_date = str(localtime[1]) + "/" +  str(localtime[2]) + "/" +  str(localtime[0])
        self.formatted_time = str(localtime[3]) + ":" +  str(local_time_minutes) + ":" +  str(local_time_seconds)
        #print "Transaction Date: " + self.formatted_date
        #print "Transaction Time: " + self.formatted_time
        #print "Orders being transacted:"
        #print "--------------------"
        if self.order_type == 0:
            #print "Buy Order Logging"
            for i in range(len(self.sell_order_numbers)):
                self.limit_sell_order_account = self.sell_order_accounts[i];
                #print "Limit Order Account: " + self.limit_sell_order_account;
                self.limit_sell_order_number = self.sell_order_numbers[i];
                #print "Limit Order Number: " + self.limit_sell_order_number;
                self.limit_sell_order_type = self.sell_top_order_type[i]
                #print "Transaction Type: " + self.limit_sell_order_type;
                self.limit_sell_order_price = self.sell_order_price_list[i];
                #print "Transaction Price: " + str(self.limit_sell_order_price);
                if self.sell_top_order_type[i] == "FULL SELL":
                    self.limit_sell_order_volume = self.sell_order_volume_list[i][0]
                    #print "Transaction Volume: " + str(self.limit_sell_order_volume);
                    del_sell_book_order(self.sell_order_numbers[i]);
                else:
                    self.limit_sell_order_volume = self.sell_order_volume_list[i]
                    #print "Transaction Volume: " + str(self.limit_buy_order_volume);
                    self.new_sell_order_volume = self.buy_order_volume[0] - self.volume
                    sell_book[str(self.sell_order_numbers[i])][2] = self.new_sell_order_volume
                self.limit_sell_order_total = self.limit_sell_order_price * self.limit_sell_order_volume
                #print "Transaction Total: " + self.limit_sell_order_total
                self.limit_order_transaction_print();
                self.limit_order_transaction_log();
                self.limit_order_transaction_list.append(transaction_count)
                transaction_count += 1
                limit_order_transaction_count += 1
                #print "--------------------"
            #print sell_book;
            #print "Buy Order Logging Done"
            self.instant_order_transaction_print();
            self.instant_order_transaction_log();
        elif self.order_type == 1:
            #print "Buy Order Logging"
            for i in range(len(self.buy_order_numbers)):
                self.limit_buy_order_account = self.buy_order_accounts[i];
                #print "Limit Order Account: " + self.limit_buy_order_account;
                self.limit_buy_order_number = self.buy_order_numbers[i];
                #print "Limit Order Number: " + self.limit_buy_order_number;
                self.limit_buy_order_type = self.buy_top_order_type[i]
                #print "Transaction Type: " + self.limit_buy_order_type;
                self.limit_buy_order_price = self.buy_order_price_list[i];
                #print "Transaction Price: " + str(self.limit_buy_order_price);
                if self.buy_top_order_type[i] == "FULL BUY":
                    self.limit_buy_order_volume = self.buy_order_volume_list[i][0]
                    #print "Transaction Volume: " + str(self.limit_buy_order_volume);
                    del_buy_book_order(self.buy_order_numbers[i]);
                else:
                    self.limit_buy_order_volume = self.buy_order_volume_list[i]
                    #print "Transaction Volume: " + str(self.limit_buy_order_volume);
                    self.new_buy_order_volume = self.sell_order_volume[0] - self.volume
                    buy_book[str(self.buy_order_numbers[i])][2] = self.new_buy_order_volume
                self.limit_buy_order_total = self.limit_buy_order_price * self.limit_buy_order_volume
                #print "Transaction Total: " + self.limit_buy_order_total
                self.limit_order_transaction_print();
                self.limit_order_transaction_log();
                self.limit_order_transaction_list.append(transaction_count)
                transaction_count += 1
                limit_order_transaction_count += 1
                #print "--------------------"
            #print buy_book;
            #print "Buy Order Logging Done"
            self.instant_order_transaction_print();
            self.instant_order_transaction_log();
        else:
            print "Exception"

    def limit_order_transaction_print(self):
        print "Limit Order Transaction " + str(limit_order_transaction_count) + ":"
        print "--------------------"
        if self.order_type == 0:
            print "Transaction Details:"
            print "Transaction Date: " + self.formatted_date
            print "Transaction Time: " + self.formatted_time
            print "Transaction Number: " + str(transaction_count)
            print "Order Type: " + str(self.limit_sell_order_type)
            print "Limit Order Number: " + str(self.limit_sell_order_number)
            #print "Instant Order Number: " + str(transaction_count)
            print "Buy Account: " + self.account
            print "Sell Account: " + self.limit_sell_order_account
            print "Transaction Volume: " + str(self.limit_sell_order_volume)
            print "Transaction Price: " + str(self.limit_sell_order_price)
            print "Transaction Total: " + str(self.limit_sell_order_total)
            print ""
            print "Account Crediting:"
            print self.limit_sell_order_account + ": +$" + str(self.limit_sell_order_total) + " and -" + str(self.limit_sell_order_volume) + " BTC"
            print "--------------------"
        elif self.order_type == 1:
            print "Transaction Details:"
            print "Transaction Date: " + self.formatted_date
            print "Transaction Time: " + self.formatted_time
            print "Transaction Number: " + str(transaction_count)
            print "Order Type: " + str(self.limit_buy_order_type)
            print "Limit Order Number: " + str(self.limit_buy_order_number)
            #print "Instant Order Number: " + str(transaction_count)
            print "Buy Account: " + self.limit_buy_order_account
            print "Sell Account: " + self.account
            print "Transaction Volume: " + str(self.limit_buy_order_volume)
            print "Transaction Price: " + str(self.limit_buy_order_price)
            print "Transaction Total: " + str(self.limit_buy_order_total)
            print ""
            print "Account Crediting:"
            print self.limit_buy_order_account + ": -$" + str(self.limit_buy_order_total) + " and +" + str(self.limit_buy_order_volume) + " BTC"
            print "--------------------"
        else:
            print "Invalid Order Type"

    def instant_order_transaction_print(self):
        print "Instant Order Transaction:"
        print "--------------------"
        print "Transaction Date: " + self.formatted_date
        print "Transaction Time: " + self.formatted_time
        print "Transaction Number: "+ str(transaction_count)
        print "Instant Order Volume: " + str(self.instant_order_volume)
        print "Instant Order Average Price: " + str(self.average)
        print "Transaction Total: " + str(self.transaction_price_ticker)
        print ""
        print "Fulfilled Orders:"
        print ""
        #self.limit_order_transaction_print();
        if self.order_type == 0:
            if len(self.sell_order_price_list) > len(self.limit_order_transaction_list):
                del self.sell_order_price_list[-1]
            for i in range(len(self.sell_order_volume_list)):
                print "Transaction Number: " + str(self.limit_order_transaction_list[i])
                print "Order Number: " + str(self.sell_order_numbers[i])
                print "Account Number: " + str(self.sell_order_accounts[i])
                if type(self.sell_order_volume_list[i]) is list:
                    print "Transaction Volume: " + str(self.sell_order_volume_list[i][0])
                else:
                    print "Transaction Volume: " + str(self.sell_order_volume_list[i])
                print "Transaction Price: " + str(self.sell_order_price_list[i])
                print ""
        elif self.order_type == 1:
            if len(self.buy_order_price_list) > len(self.limit_order_transaction_list):
                del self.buy_order_price_list[-1]
            for i in range(len(self.buy_order_price_list)):
                print "Transaction Number: " + str(self.limit_order_transaction_list[i])
                print "Order Number: " + str(self.buy_order_numbers[i])
                print "Account Number: " + str(self.buy_order_accounts[i])
                if type(self.buy_order_volume_list[i]) is list:
                    print "Transaction Volume: " + str(self.buy_order_volume_list[i][0])
                else:
                    print "Transaction Volume: " + str(self.buy_order_volume_list[i])
                print "Transaction Price: " + str(self.buy_order_price_list[i])
                print ""
        else:
            print "Invalid Order Type"
        print "--------------------"

    def limit_order_transaction_log(self):
        log = open("LimitOrders.txt", "a") #Defines log file open variable
        log.write("Limit Order Transaction " + str(limit_order_transaction_count) + ":" + "\n")
        log.write("--------------------" + "\n")
        if self.order_type == 0:
            log.write("Transaction Details:" + "\n" + "\n")
            log.write("Transaction Date: " + self.formatted_date + "\n")
            log.write("Transaction Time: " + self.formatted_time + "\n")
            log.write("Transaction Number: " + str(transaction_count) + "\n")
            log.write("Order Type: " + str(self.limit_sell_order_type) + "\n")
            log.write("Limit Order Number: " + str(self.limit_sell_order_number) + "\n")
            #log.write("Instant Order Number: " + str(transaction_count) + "\n")
            log.write("Buy Account: " + self.account + "\n")
            log.write("Sell Account: " + self.limit_sell_order_account + "\n")
            log.write("Transaction Volume: " + str(self.limit_sell_order_volume) + "\n")
            log.write("Transaction Price: " + str(self.limit_sell_order_price) + "\n")
            log.write("Transaction Total: " + str(self.limit_sell_order_total) + "\n" + "\n")
            log.write("Account Crediting:" + "\n" + "\n")
            log.write(self.limit_sell_order_account + ": +$" + str(self.limit_sell_order_total) + " and -" + str(self.limit_sell_order_volume) + " BTC" + "\n")
            log.write("--------------------" + "\n")
        elif self.order_type == 1:
            log.write("Transaction Details:" + "\n" + "\n")
            log.write("Transaction Date: " + self.formatted_date + "\n")
            log.write("Transaction Time: " + self.formatted_time + "\n")
            log.write("Transaction Number: " + str(transaction_count) + "\n")
            log.write("Order Type: " + str(self.limit_buy_order_type) + "\n")
            log.write("Limit Order Number: " + str(self.limit_buy_order_number) + "\n")
            #log.write("Instant Order Number: " + str(transaction_count) + "\n")
            log.write("Buy Account: " + self.limit_buy_order_account + "\n")
            log.write("Sell Account: " + self.account + "\n")
            log.write("Transaction Volume: " + str(self.limit_buy_order_volume) + "\n")
            log.write("Transaction Price: " + str(self.limit_buy_order_price) + "\n")
            log.write("Transaction Total: " + str(self.limit_buy_order_total) + "\n" + "\n")
            log.write("Account Crediting:" + "\n" + "\n")
            log.write(self.limit_buy_order_account + ": -$" + str(self.limit_buy_order_total) + " and +" + str(self.limit_buy_order_volume) + " BTC" + "\n")
            log.write("--------------------" + "\n")
        log.close()
    
    def instant_order_transaction_log(self):
        log = open("InstantOrders.txt", "a") #Defines log file open variable
        log.write("Instant Order Transaction " + str(transaction_count) + ":" + "\n")
        log.write("--------------------" + "\n")
        log.write("Transaction Date: " + self.formatted_date + "\n")
        log.write("Transaction Time: " + self.formatted_time + "\n")
        log.write("Transaction Number: "+ str(transaction_count) + "\n")
        log.write("Instant Order Volume: " + str(self.instant_order_volume) + "\n")
        log.write("Instant Order Average Price: " + str(self.average) + "\n")
        log.write("Transaction Total: " + str(self.transaction_price_ticker) + "\n" + "\n")
        log.write("Fulfilled Orders:" + "\n" + "\n")
        #self.limit_order_transaction_print();
        if self.order_type == 0:
            if len(self.sell_order_price_list) > len(self.limit_order_transaction_list):
                del self.sell_order_price_list[-1]
            for i in range(len(self.sell_order_volume_list)):
                log.write("Transaction Number: " + str(self.limit_order_transaction_list[i]) + "\n")
                log.write("Order Number: " + str(self.sell_order_numbers[i]) + "\n")
                log.write("Account Number: " + str(self.sell_order_accounts[i]) + "\n")
                if type(self.sell_order_volume_list[i]) is list:
                    log.write("Transaction Volume: " + str(self.sell_order_volume_list[i][0]) + "\n")
                else:
                    log.write("Transaction Volume: " + str(self.sell_order_volume_list[i]) + "\n")
                log.write("Transaction Price: " + str(self.sell_order_price_list[i]) + "\n" + "\n")
        elif self.order_type == 1:
            if len(self.buy_order_price_list) > len(self.limit_order_transaction_list):
                del self.buy_order_price_list[-1]
            for i in range(len(self.buy_order_price_list)):
                log.write("Transaction Number: " + str(self.limit_order_transaction_list[i]) + "\n")
                log.write("Order Number: " + str(self.buy_order_numbers[i]) + "\n")
                log.write("Account Number: " + str(self.buy_order_accounts[i]) + "\n")
                if type(self.buy_order_volume_list[i]) is list:
                    log.write("Transaction Volume: " + str(self.buy_order_volume_list[i][0]) + "\n")
                else:
                    log.write("Transaction Volume: " + str(self.buy_order_volume_list[i]) + "\n")
                log.write("Transaction Price: " + str(self.buy_order_price_list[i]) + "\n" + "\n")
        log.close()
        

def del_sell_book_order(order):
    del sell_book[order]

def del_buy_book_order(order):
    del buy_book[order]



#All things below this line are for testing

#order_type: buy = 0, sell = 1

UserOrder1 = Order("Account1", 520, 7)
UserOrder2 = Order("Account2", 540, 5)
UserOrder3 = Order("Account3", 720, 8)
UserOrder4 = Order("Account4", 410, 2)
UserOrder5 = Order("Account5", 600, 7)
Order1 = InstantOrder("Account6", 10, 0)
UserOrder1.add_sell_book_order()
UserOrder2.add_sell_book_order()
UserOrder3.add_buy_book_order()
UserOrder4.add_buy_book_order()
UserOrder5.add_sell_book_order()

Order1.buy_price_check(nsmallest)
Order1.sell_price_check(nsmallest)
Order1.transaction()