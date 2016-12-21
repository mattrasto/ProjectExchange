#-------------------------------------------------------------------------------
# Name:        DBSearchBasicOrderBook
# Version:     1.0
# Purpose:
#
# Author:      Matthew
#
# Created:     05/17/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    05/30/2014
#-------------------------------------------------------------------------------

#CHECK IF FOR AUTOMATIC SQL ITERATION USING "WHERE" FUNCTION

import MySQLdb

db = MySQLdb.connect("localhost","root","***","exchangedatabase")

cursor = db.cursor()

cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data

OrderHeaderPrinted = False
OrderFound = False

SearchParameter = raw_input("Search by: ")
SearchParameter = SearchParameter.upper()
ParameterCheck = "DESCRIBE BasicOrderBook"
try:
    cursor.execute(ParameterCheck)
    TableDescription = cursor.fetchall()
    for Row in TableDescription:
        TargetParameter = Row[0]
        if TargetParameter.upper() == SearchParameter or SearchParameter == "ORDER NUMBER" or SearchParameter == "DATE ENTERED" or SearchParameter == "TRIGGER TYPE" or SearchParameter == "TRIGGER VALUE":
            break;
    while TargetParameter.upper() != SearchParameter and SearchParameter != "ORDER NUMBER" and SearchParameter != "DATE ENTERED" and SearchParameter != "TRIGGER TYPE" and SearchParameter != "TRIGGER VALUE":
        print "Cannot search by that attribute. Please enter again:"
        print "Choices: " + str([Row[0] for Row in TableDescription])
        SearchParameter = raw_input("Search by: ")
        SearchParameter = SearchParameter.upper()
        for Row in TableDescription:
            TargetParameter = Header[0]
            if TargetParameter.upper() == SearchParameter or SearchParameter == "ORDER NUMBER" or SearchParameter == "DATE ENTERED" or SearchParameter == "TRIGGER TYPE" or SearchParameter == "TRIGGER VALUE":
                break;
except:
    "ERROR: Database execution unsuccessful"



if SearchParameter == "ORDERNUMBER":
    SearchParameter = "ORDER NUMBER"
    print "Searching by: Order Number"
    
elif SearchParameter == "Trigger Type":
    SearchParameter = "TRIGGER TYPE"
    print "Searching by: Date Entered"
    
elif SearchParameter == "Trigger Value":
    SearchParameter = "TRIGGER VALUE"
    print "Searching by: Date Entered"
    
elif SearchParameter == "DATEENTERED":
    SearchParameter = "DATE ENTERED"
    print "Searching by: Date Entered"
    
else:
    print "Searching by: " + SearchParameter.title()



if SearchParameter != "DATEENTERED" and SearchParameter != "DATE ENTERED":
    SearchValue = raw_input("Search for value: ")
else:
    DateSearchYear = raw_input("Search Year: ")
    try:
        DateSearchYear = int(DateSearchYear)
        DateSearchYearOmit = False
    except:
        if DateSearchYear == "":
            DateSearchYearOmit = True
        else:
            DateSearchYearOmit = False
            
    DateSearchMonth = raw_input("Search Month: ")
    try:
        DateSearchMonth = int(DateSearchMonth)
        DateSearchMonthOmit = False
    except:
        if DateSearchMonth == "":
            DateSearchMonthOmit = True
        else:
            DateSearchMonthOmit = False
            
    DateSearchDay = raw_input("Search Day: ")
    try:
        DateSearchDay = int(DateSearchDay)
        DateSearchDayOmit = False
    except:
        if DateSearchDay == "":
            DateSearchDayOmit = True
        else:
            DateSearchDayOmit = False
            
    DateSearchHour = raw_input("Search Hour: ")
    try:
        DateSearchHour = int(DateSearchHour)
        DateSearchHourOmit = False
    except:
        if DateSearchHour == "":
            DateSearchHourOmit = True
        else:
            DateSearchHourOmit = False
            
    DateSearchMinute = raw_input("Search Minute: ")
    try:
        DateSearchMinute = int(DateSearchMinute)
        DateSearchMinuteOmit = False
    except:
        if DateSearchMinute == "":
            DateSearchMinuteOmit = True
        else:
            DateSearchMinuteOmit = False
            
    DateSearchSecond = raw_input("Search Second: ")
    try:
        DateSearchSecond = int(DateSearchSecond)
        DateSearchSecondOmit = False
    except:
        if DateSearchSecond == "":
            DateSearchSecondOmit = True
        else:
            DateSearchSecondOmit = False



'''Checking Parameters'''



if SearchParameter == "ORDER NUMBER":
    SearchValue = int(SearchValue)
    sql = "SELECT * FROM BasicOrderBook WHERE OrderNumber = %d" % (SearchValue)
    try:
        cursor.execute(sql)
        Order = cursor.fetchall()
        print ""
        if Order != ():
            print "Order Number: " + str(Order[0])
            print "Username: " + str(Order[1])
            print "Price: " + str(Order[2])
            print "Volume: " + str(Order[3])
            print "Type: " + str(Order[4])
            print "Action: " + str(Order[5])
            print "Trigger Type: " + str(Order[6])
            print "Trigger Action: " + str(Order[7])
            print "Date Entered: " + str(Order[8])
            print ""
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "USERNAME":
    SearchValue = str(SearchValue.capitalize())
try:
    sql = """SELECT * FROM BasicOrderBook WHERE Username = "%s" """ % (SearchValue)
    cursor.execute(sql)
    OrderList = cursor.fetchall()
    for Order in OrderList:
        if OrderHeaderPrinted != True:
            print ""
            print "Orders that meet search parameters:"
            OrderHeaderPrinted = True
        print ""
        print "Order Number: " + str(Order[0])
        print "Username: " + str(Order[1])
        print "Price: " + str(Order[2])
        print "Volume: " + str(Order[3])
        print "Type: " + str(Order[4])
        print "Action: " + str(Order[5])
        print "Trigger Type: " + str(Order[6])
        print "Trigger Action: " + str(Order[7])
        print "Date Entered: " + str(Order[8])
        print ""
        OrderFound = True
except:
    print "ERROR: Database fetch exception"



if SearchParameter == "PRICE":
    SearchValue = float(SearchValue)
    try:
        sql = "SELECT * FROM BasicOrderBook WHERE Price = %f" % (SearchValue)
        cursor.execute(sql)
        OrderList = cursor.fetchall()
        for Order in OrderList:
            if OrderHeaderPrinted != True:
                OrderHeaderPrinted = True
                print ""
                print "Orders that meet search parameters:"
            print ""
            print "Order Number: " + str(Order[0])
            print "Username: " + str(Order[1])
            print "Price: " + str(Order[2])
            print "Volume: " + str(Order[3])
            print "Type: " + str(Order[4])
            print "Action: " + str(Order[5])
            print "Trigger Type: " + str(Order[6])
            print "Trigger Action: " + str(Order[7])
            print "Date Entered: " + str(Order[8])
            print ""
            OrderFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "VOLUME":
    SearchValue = float(SearchValue)
    try:
        sql = "SELECT * FROM BasicOrderBook WHERE Volume = %f" % (SearchValue)
        cursor.execute(sql)
        OrderList = cursor.fetchall()
        for Order in OrderList:
            if OrderHeaderPrinted != True:
                OrderHeaderPrinted = True
                print ""
                print "Orders that meet search parameters:"
            print ""
            print "Order Number: " + str(Order[0])
            print "Username: " + str(Order[1])
            print "Price: " + str(Order[2])
            print "Volume: " + str(Order[3])
            print "Type: " + str(Order[4])
            print "Action: " + str(Order[5])
            print "Trigger Type: " + str(Order[6])
            print "Trigger Action: " + str(Order[7])
            print "Date Entered: " + str(Order[8])
            print ""
            OrderFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "TYPE":
    SearchValue = str(SearchValue.capitalize())
    try:
        sql = """SELECT * FROM BasicOrderBook WHERE Type = "%s" """ % (SearchValue)
        cursor.execute(sql)
        OrderList = cursor.fetchall()
        for Order in OrderList:
            if OrderHeaderPrinted != True:
                OrderHeaderPrinted = True
                print ""
                print "Orders that meet search parameters:"
            print ""
            print "Order Number: " + str(Order[0])
            print "Username: " + str(Order[1])
            print "Price: " + str(Order[2])
            print "Volume: " + str(Order[3])
            print "Type: " + str(Order[4])
            print "Action: " + str(Order[5])
            print "Trigger Type: " + str(Order[6])
            print "Trigger Action: " + str(Order[7])
            print "Date Entered: " + str(Order[8])
            print ""
            OrderFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "ACTION":
    SearchValue = str(SearchValue.capitalize())
    try:
        sql = """SELECT * FROM BasicOrderBook WHERE Action = "%s" """ % (SearchValue)
        cursor.execute(sql)
        OrderList = cursor.fetchall()
        for Order in OrderList:
            if OrderHeaderPrinted != True:
                OrderHeaderPrinted = True
                print ""
                print "Orders that meet search parameters:"
                print ""
            print "Order Number: " + str(Order[0])
            print "Username: " + str(Order[1])
            print "Price: " + str(Order[2])
            print "Volume: " + str(Order[3])
            print "Type: " + str(Order[4])
            print "Action: " + str(Order[5])
            print "Trigger Type: " + str(Order[6])
            print "Trigger Action: " + str(Order[7])
            print "Date Entered: " + str(Order[8])
            print ""
            OrderFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "TRIGGER TYPE":
    SearchValue = str(SearchValue.capitalize())
    try:
        sql = """SELECT * FROM BasicOrderBook WHERE TriggerType = "%s" """ % (SearchValue)
        cursor.execute(sql)
        OrderList = cursor.fetchall()
        for Order in OrderList:
            if OrderHeaderPrinted != True:
                OrderHeaderPrinted = True
                print ""
                print "Orders that meet search parameters:"
                print ""
            print "Order Number: " + str(Order[0])
            print "Username: " + str(Order[1])
            print "Price: " + str(Order[2])
            print "Volume: " + str(Order[3])
            print "Type: " + str(Order[4])
            print "Action: " + str(Order[5])
            print "Trigger Type: " + str(Order[6])
            print "Trigger Action: " + str(Order[7])
            print "Date Entered: " + str(Order[8])
            print ""
            OrderFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "TRIGGER VALUE":
    SearchValue = float(SearchValue)
    try:
        sql = """SELECT * FROM BasicOrderBook WHERE TriggerValue = %f """ % (SearchValue)
        cursor.execute(sql)
        OrderList = cursor.fetchall()
        for Order in OrderList:
            if OrderHeaderPrinted != True:
                OrderHeaderPrinted = True
                print ""
                print "Orders that meet search parameters:"
                print ""
            print "Order Number: " + str(Order[0])
            print "Username: " + str(Order[1])
            print "Price: " + str(Order[2])
            print "Volume: " + str(Order[3])
            print "Type: " + str(Order[4])
            print "Action: " + str(Order[5])
            print "Trigger Type: " + str(Order[6])
            print "Trigger Action: " + str(Order[7])
            print "Date Entered: " + str(Order[8])
            print ""
            OrderFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "DATE ENTERED":
    try:
        sql = "SELECT * FROM BasicOrderBook"
        cursor.execute(sql)
        OrderBookOrders = cursor.fetchall()
        for Order in OrderBookOrders:
            if DateSearchYearOmit == True:
                YearValue = ""
                for Character in str(Order[8])[:4]:
                    YearValue += str(Character)
                DateSearchYear = YearValue
                
            if DateSearchMonthOmit == True:
                MonthValue = ""
                for Character in str(Order[8])[5:7]:
                    MonthValue += str(Character)
                DateSearchMonth = MonthValue
                
            if DateSearchDayOmit == True:
                DayValue = ""
                for Character in str(Order[8])[8:10]:
                    DayValue += str(Character)
                DateSearchDay = DayValue
                
            if DateSearchHourOmit == True:
                HourValue = ""
                for Character in str(Order[8])[11:13]:
                    HourValue += str(Character)
                DateSearchHour = HourValue
                
            if DateSearchMinuteOmit == True:
                MinuteValue = ""
                for Character in str(Order[8])[14:16]:
                    MinuteValue += str(Character)
                DateSearchMinute = MinuteValue
            
            if DateSearchSecondOmit == True:
                SecondValue = ""
                for Character in str(Order[8])[17:19]:
                    SecondValue += str(Character)
                DateSearchSecond = SecondValue
            
            if DateSearchMonth < 10:
                DateSearchMonth = "0" + str(DateSearchMonth)
            if DateSearchDay < 10:
                DateSearchDay = "0" + str(DateSearchDay)
            if DateSearchHour < 10:
                DateSearchHour = "0" + str(DateSearchHour)
            if DateSearchMinute < 10:
                DateSearchMinute = "0" + str(DateSearchMinute)
            if DateSearchSecond < 10:
                DateSearchSecond = "0" + str(DateSearchSecond)
            
            if str(DateSearchYear) == str(Order[8])[:4] and str(DateSearchMonth) == str(Order[8])[5:7] and str(DateSearchDay) == str(Order[8])[8:10] and str(DateSearchHour) == str(Order[8])[11:13] and str(DateSearchMinute) == str(Order[8])[14:16] and str(DateSearchSecond) == str(Order[8])[17:19]:
                if OrderHeaderPrinted != True:
                    OrderHeaderPrinted = True
                    print ""
                    print "Orders that meet search parameters:"
                    print ""
                print "Order Number: " + str(Order[0])
                print "Username: " + str(Order[1])
                print "Price: " + str(Order[2])
                print "Volume: " + str(Order[3])
                print "Type: " + str(Order[4])
                print "Action: " + str(Order[5])
                print "Trigger Type: " + str(Order[6])
                print "Trigger Action: " + str(Order[7])
                print "Date Entered: " + str(Order[8])
                print ""
                OrderFound = True
    except:
        print "ERROR: Database fetch exception"

if OrderFound != True:
    print ""
    print "No orders meet search criteria"



db.close()