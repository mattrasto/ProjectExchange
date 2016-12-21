#-------------------------------------------------------------------------------
# Name:        DBSearchPrivateTradeBook
# Version:     1.0
# Purpose:
#
# Author:      Matthew
#
# Created:     06/01/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    06/01/2014
#-------------------------------------------------------------------------------

#CHECK IF FOR AUTOMATIC SQL ITERATION USING "WHERE" FUNCTION

import MySQLdb

db = MySQLdb.connect("localhost","root","***","exchangedatabase")

cursor = db.cursor()

cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data

TradeHeaderPrinted = False
TradeFound = False

SearchParameter = raw_input("Search by: ")
SearchParameter = SearchParameter.upper()
ParameterCheck = "DESCRIBE PrivateTradeBook"
try:
    cursor.execute(ParameterCheck)
    TableDescription = cursor.fetchall()
    for Row in TableDescription:
        TargetParameter = Row[0]
        if TargetParameter.upper() == SearchParameter or SearchParameter == "TRADE NUMBER" or SearchParameter == "DATE ENTERED" or SearchParameter == "USER REQUESTS":
            break;
    while TargetParameter.upper() != SearchParameter and SearchParameter != "TRADE NUMBER" and SearchParameter != "DATE ENTERED" and SearchParameter != "USER REQUESTS":
        print "Cannot search by that attribute. Please enter again:"
        print "Choices: " + str([Row[0] for Row in TableDescription])
        SearchParameter = raw_input("Search by: ")
        SearchParameter = SearchParameter.upper()
        for Row in TableDescription:
            TargetParameter = Header[0]
            if TargetParameter.upper() == SearchParameter or SearchParameter == "TRADE NUMBER" or SearchParameter == "DATE ENTERED" or SearchParameter == "USER REQUESTS":
                break;
except:
    "ERROR: Database execution unsuccessful"



if SearchParameter == "TRADENUMBER":
    SearchParameter = "TRADE NUMBER"
    print "Searching by: Trade Number"

elif SearchParameter == "USERREQUESTS":
    SearchParameter = "USER REQUESTS"
    print "Searching by: User Requests"

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



if SearchParameter == "TRADE NUMBER":
    SearchValue = int(SearchValue)
    sql = "SELECT * FROM PrivateTradeBook WHERE TradeNumber = %d" % (SearchValue)
    try:
        cursor.execute(sql)
        Trade = cursor.fetchall()[0]
        print ""
        if Trade != ():
            print "Trade Number: " + str(Trade[0])
            print "Username: " + str(Trade[1])
            print "Price: " + str(Trade[2])
            print "Volume: " + str(Trade[3])
            print "Action: " + str(Trade[4])
            print "Date Entered: " + str(Trade[6])
            print ""
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "USERNAME":
    SearchValue = str(SearchValue.capitalize())
    try:
        sql = """SELECT * FROM PrivateTradeBook WHERE Username = "%s" """ % (SearchValue)
        cursor.execute(sql)
        TradeList = cursor.fetchall()
        for Trade in TradeList:
            if TradeHeaderPrinted != True:
                print ""
                print "Trades that meet search parameters:"
                TradeHeaderPrinted = True
            print ""
            print "Trade Number: " + str(Trade[0])
            print "Username: " + str(Trade[1])
            print "Price: " + str(Trade[2])
            print "Volume: " + str(Trade[3])
            print "Action: " + str(Trade[4])
            print "Date Entered: " + str(Trade[6])
            print ""
            TradeFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "PRICE":
    SearchValue = float(SearchValue)
    try:
        sql = "SELECT * FROM PrivateTradeBook WHERE Price = %f" % (SearchValue)
        cursor.execute(sql)
        TradeList = cursor.fetchall()
        for Trade in TradeList:
            if TradeHeaderPrinted != True:
                TradeHeaderPrinted = True
                print ""
                print "Trades that meet search parameters:"
            print ""
            print "Trade Number: " + str(Trade[0])
            print "Username: " + str(Trade[1])
            print "Price: " + str(Trade[2])
            print "Volume: " + str(Trade[3])
            print "Action: " + str(Trade[4])
            print "Date Entered: " + str(Trade[6])
            print ""
            TradeFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "VOLUME":
    SearchValue = float(SearchValue)
    try:
        sql = "SELECT * FROM PrivateTradeBook WHERE Volume = %f" % (SearchValue)
        cursor.execute(sql)
        TradeList = cursor.fetchall()
        for Trade in TradeList:
            if TradeHeaderPrinted != True:
                TradeHeaderPrinted = True
                print ""
                print "Trades that meet search parameters:"
            print ""
            print "Trade Number: " + str(Trade[0])
            print "Username: " + str(Trade[1])
            print "Price: " + str(Trade[2])
            print "Volume: " + str(Trade[3])
            print "Action: " + str(Trade[4])
            print "Date Entered: " + str(Trade[6])
            print ""
            TradeFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "ACTION":
    SearchValue = str(SearchValue.capitalize())
    try:
        sql = """SELECT * FROM PrivateTradeBook WHERE Action = "%s" """ % (SearchValue)
        cursor.execute(sql)
        TradeList = cursor.fetchall()
        for Trade in TradeList:
            if TradeHeaderPrinted != True:
                TradeHeaderPrinted = True
                print ""
                print "Trades that meet search parameters:"
                print ""
            print "Trade Number: " + str(Trade[0])
            print "Username: " + str(Trade[1])
            print "Price: " + str(Trade[2])
            print "Volume: " + str(Trade[3])
            print "Action: " + str(Trade[4])
            print "Date Entered: " + str(Trade[6])
            print ""
            TradeFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "USER REQUESTS":
    SearchValue = int(SearchValue)
    try:
        sql = "SELECT * FROM PrivateTradeBook WHERE UserRequests = %d" % (SearchValue)
        cursor.execute(sql)
        TradeList = cursor.fetchall()
        for Trade in TradeList:
            if TradeHeaderPrinted != True:
                TradeHeaderPrinted = True
                print ""
                print "Trades that meet search parameters:"
            print ""
            print "Trade Number: " + str(Trade[0])
            print "Username: " + str(Trade[1])
            print "Price: " + str(Trade[2])
            print "Volume: " + str(Trade[3])
            print "Action: " + str(Trade[4])
            print "Date Entered: " + str(Trade[6])
            print ""
            TradeFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "DATE ENTERED":
    try:
        sql = "SELECT * FROM PrivateTradeBook"
        cursor.execute(sql)
        TradeBookTrades = cursor.fetchall()
        for Trade in TradeBookTrades:
            if DateSearchYearOmit == True:
                YearValue = ""
                for Character in str(Trade[6])[:4]:
                    YearValue += str(Character)
                DateSearchYear = YearValue
               
            if DateSearchMonthOmit == True:
                MonthValue = ""
                for Character in str(Trade[6])[5:7]:
                    MonthValue += str(Character)
                DateSearchMonth = MonthValue
               
            if DateSearchDayOmit == True:
                DayValue = ""
                for Character in str(Trade[6])[8:10]:
                    DayValue += str(Character)
                DateSearchDay = DayValue
               
            if DateSearchHourOmit == True:
                HourValue = ""
                for Character in str(Trade[6])[11:13]:
                    HourValue += str(Character)
                DateSearchHour = HourValue
               
            if DateSearchMinuteOmit == True:
                MinuteValue = ""
                for Character in str(Trade[6])[14:16]:
                    MinuteValue += str(Character)
                DateSearchMinute = MinuteValue
           
            if DateSearchSecondOmit == True:
                SecondValue = ""
                for Character in str(Trade[6])[17:19]:
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
           
            if str(DateSearchYear) == str(Trade[6])[:4] and str(DateSearchMonth) == str(Trade[6])[5:7] and str(DateSearchDay) == str(Trade[6])[8:10] and str(DateSearchHour) == str(Trade[6])[11:13] and str(DateSearchMinute) == str(Trade[6])[14:16] and str(DateSearchSecond) == str(Trade[6])[17:19]:
                if TradeHeaderPrinted != True:
                    TradeHeaderPrinted = True
                    print ""
                    print "Trades that meet search parameters:"
                    print ""
                print "Trade Number: " + str(Trade[0])
                print "Username: " + str(Trade[1])
                print "Price: " + str(Trade[2])
                print "Volume: " + str(Trade[3])
                print "Action: " + str(Trade[4])
                print "Date Entered: " + str(Trade[6])
                print ""
                TradeFound = True
    except:
       print "ERROR: Database fetch exception"

if TradeFound != True:
    print ""
    print "No trades meet search criteria"



db.close()