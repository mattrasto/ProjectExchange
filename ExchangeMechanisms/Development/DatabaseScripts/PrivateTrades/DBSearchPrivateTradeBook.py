#-------------------------------------------------------------------------------
# Name:        DBSearchPrivateTradeBook
# Version:     3.0
# Purpose:     Searches PrivateTradeBook with specified constraints
#
# Author:      Matthew
#
# Created:     08/12/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/15/2014
#-------------------------------------------------------------------------------

import MySQLdb
    


def PrivateTradePrint(PrivateTrades):
    
    #Prints all private trades matched with search query
    
    print "Private Trades that meet search parameters:"
    print ""
    for PrivateTrade in PrivateTrades:
        print "------------------------------"
        print ""
        print "Trade Number: " + str(PrivateTrade[0])
        print "Username: " + str(PrivateTrade[1])
        print "Price: " + str(PrivateTrade[2])
        print "Volume: " + str(PrivateTrade[3])
        print "Action: " + str(PrivateTrade[4])
        print "Date Entered: " + str(PrivateTrade[6])
        print ""
    print "------------------------------"



def main(SearchParameter, SearchValue):
    
    #Contains all search functions
    #Note: In V2 all search functions are specific; This is planned to change
    #Each search simply checks the database for all users with the assigned SearchValue and then passes "Users" list to be printed
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    
    
    print ""
    
    #Searches for trades with specific TradeNumber
    if SearchParameter == "TRADE NUMBER":
        #Converts TradeNumber value to integer type
        try:
            SearchValue = int(SearchValue)
        except:
            print "CRITICAL ERROR: Trade Number unable to be converted to integer"
            sys.exit()
        try:
            TradeNumberSearch = "SELECT * FROM PrivateTradeBook WHERE TradeNumber = %d" % (SearchValue)
            cursor.execute(TradeNumberSearch)
            PrivateTrades = cursor.fetchall()
            #If atleast 1 trade is found, passes list to print function
            if PrivateTrades != ():
                PrivateTradePrint(PrivateTrades)
            else:
                print "No private trades meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for trades under specific Username
    if SearchParameter == "USERNAME":
        #Converts Username value to integer type and capitalizes
        try:
            SearchValue = str(SearchValue.capitalize())
        except:
            print "CRITICAL ERROR: Username unable to be converted to string"
            sys.exit()
        try:
            UsernameSearch = """SELECT * FROM PrivateTradeBook WHERE Username = "%s" """ % (SearchValue)
            cursor.execute(UsernameSearch)
            PrivateTrades = cursor.fetchall()
            #If atleast 1 trade is found, passes list to print function
            if PrivateTrades != ():
                PrivateTradePrint(PrivateTrades)
            else:
                print "No private trades meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for trades with specific Price
    if SearchParameter == "PRICE":
        #Converts Price value to float type
        try:
            SearchValue = float(SearchValue)
        except:
            print "CRITICAL ERROR: Price unable to be converted to float"
            sys.exit()
        try:
            PriceSearch = "SELECT * FROM PrivateTradeBook WHERE Price = %f" % (SearchValue)
            cursor.execute(PriceSearch)
            PrivateTrades = cursor.fetchall()
            #If atleast 1 trade is found, passes list to print function
            if PrivateTrades != ():
                PrivateTradePrint(PrivateTrades)
            else:
                print "No private trades meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for trades with specific Volume
    if SearchParameter == "VOLUME":
        #Converts Volume value to float type
        try:
            SearchValue = float(SearchValue)
        except:
            print "CRITICAL ERROR: Volume unable to be converted to float"
            sys.exit()
        try:
            VolumeSearch = "SELECT * FROM PrivateTradeBook WHERE Volume = %f" % (SearchValue)
            cursor.execute(VolumeSearch)
            PrivateTrades = cursor.fetchall()
            #If atleast 1 trade is found, passes list to print function
            if PrivateTrades != ():
                PrivateTradePrint(PrivateTrades)
            else:
                print "No private trades meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for trades with specific Action
    if SearchParameter == "ACTION":
        #Converts Action value to string type and capitalizes
        try:
            SearchValue = str(SearchValue.capitalize())
        except:
            print "CRITICAL ERROR: Action unable to be converted to string"
            sys.exit()
        try:
            ActionSearch = """SELECT * FROM PrivateTradeBook WHERE Action = "%s" """ % (SearchValue)
            cursor.execute(ActionSearch)
            PrivateTrades = cursor.fetchall()
            #If atleast 1 trade is found, passes list to print function
            if PrivateTrades != ():
                PrivateTradePrint(PrivateTrades)
            else:
                print "No private trades meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for trades with specific amount of UserRequests
    if SearchParameter == "USER REQUESTS":
        #Converts UserRequests value to integer type
        try:
            SearchValue = int(SearchValue)
        except:
            print "CRITICAL ERROR: User Requests unable to be converted to integer"
            sys.exit()
        try:
            UserRequestsSearch = "SELECT * FROM PrivateTradeBook WHERE UserRequests = %d" % (SearchValue)
            cursor.execute(userRequestsSearch)
            PrivateTrades = cursor.fetchall()
            #If atleast 1 trade is found, passes list to print function
            if PrivateTrades != ():
                PrivateTradePrint(PrivateTrades)
            else:
                print "No private trades meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for trades with specific DateEntered
    if SearchParameter == "DATE ENTERED":
        
        #Separates SearchValue variable into date/time components
        DateSearchYear = SearchValue[0]
        DateSearchMonth = SearchValue[1]
        DateSearchDay = SearchValue[2]
        DateSearchHour = SearchValue[3]
        DateSearchMinute = SearchValue[4]
        DateSearchSecond = SearchValue[5]
        
        
        
        #If user left any interval blank, turns search parameter to "%" for wildcard searching in database
        if DateSearchYear == "":
            YearParameter = "%"
        else:
            YearParameter = DateSearchYear
        if DateSearchMonth == "":
            MonthParameter = "%"
        else:
            MonthParameter = DateSearchMonth
        if DateSearchDay == "":
            DayParameter = "%"
        else:
            DayParameter = DateSearchDay
        if DateSearchHour == "":
            HourParameter = "%"
        else:
            HourParameter = DateSearchHour
        if DateSearchMinute == "":
            MinuteParameter = "%"
        else:
            MinuteParameter = DateSearchMinute
        if DateSearchSecond == "":
            SecondParameter = "%"
        else:
            SecondParameter = DateSearchSecond
        
        
        
        #Uses "LIKE" operator to compare value with wildcards, which replaces value with an "ANY" search in contract to search for current value if input was left blank
        DateEnteredSearch = """SELECT * FROM PrivateTradeBook WHERE (YEAR(DateEntered) LIKE "%s") AND (MONTH(DateEntered) LIKE "%s") AND (DAY(DateEntered) LIKE "%s") AND (HOUR(DateEntered) LIKE "%s") AND (MINUTE(DateEntered) LIKE "%s") AND (SECOND(DateEntered) LIKE "%s")""" % (YearParameter, MonthParameter, DayParameter, HourParameter, MinuteParameter, SecondParameter)
        try:
            cursor.execute(DateEnteredSearch)
            PrivateTrades = cursor.fetchall()
            #If atleast 1 trade is found, passes list to print function
            if PrivateTrades != ():
                PrivateTradePrint(PrivateTrades)
            else:
                print ""
                print "No users meet search parameters"
        except:
            "ERROR: Database Fetch Exception"



if __name__ == "__main__":
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    
    
    '''Setting Search Parameter'''
    
    
    
    SearchParameter = (raw_input("Search by: ")).upper()
    ParameterCheck = "SHOW COLUMNS FROM PrivateTradeBook"
    
    
    
    #Checking if search parameter is valid
    try:
        cursor.execute(ParameterCheck)
        FieldList = cursor.fetchall()
        for Field in FieldList:
            TargetParameter = Field[0]
            if TargetParameter.upper() == SearchParameter or SearchParameter == "TRADE NUMBER" or SearchParameter == "DATE ENTERED" or SearchParameter == "USER REQUESTS":
                    break;
        
        #Retrying until valid input is given
        while TargetParameter.upper() != SearchParameter and SearchParameter != "TRADE NUMBER" and SearchParameter != "DATE ENTERED" and SearchParameter != "USER REQUESTS":
            
            print "Cannot search by that attribute. Please enter again:"
            print "Choices: " + str([Field[0] for Field in FieldList])
            SearchParameter = raw_input("Search by: ")
            SearchParameter = SearchParameter.upper()
            for Field in FieldList:
                TargetParameter = Field[0]
                if TargetParameter.upper() == SearchParameter or SearchParameter == "TRADE NUMBER" or SearchParameter == "DATE ENTERED" or SearchParameter == "USER REQUESTS":
                        break;
    except:
        "ERROR: Database Execution Unsuccessful"
    
    
    
    '''Standardizing Parameter Names'''
    
    
    
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
    
    
    
    '''Setting Search Value'''
    
    
    
    #Requests basic input value if not a date field
    if SearchParameter != "DATE ENTERED":
        SearchValue = raw_input("Search for value: ")
        while SearchValue == "":
            print "You must enter a value to search by:"
            SearchValue = raw_input("Search for value: ")
    
    #Requests date input and tests values for validity
    else:
        
        YearValid = False
        MonthValid = False
        DayValid = False
        HourValid = False
        MinuteValid = False
        SecondValid = False
        
        
        
        while YearValid != True:
            DateSearchYear = raw_input("Search Year: ")
            if DateSearchYear != "":
                try:
                    DateSearchYear = int(DateSearchYear)
                    if DateSearchYear >= 2014 and DateSearchYear <= 2015:
                        #print DateSearchYear
                        YearValid = True
                    else:
                        print "Search parameter must be between 2014 and 2015. Please enter again:"
                except:
                    print "Search parameter must be an integer or blank. Please enter again:"
            else:
                YearValid = True
        
        
        
        while MonthValid != True:
            DateSearchMonth = raw_input("Search Month: ")
            if DateSearchMonth != "":
                try:
                    DateSearchMonth = int(DateSearchMonth)
                    if DateSearchMonth >= 1 and DateSearchMonth <= 12:
                        #print DateSearchMonth
                        MonthValid = True
                    else:
                        print "Search parameter must be between 1 and 12. Please enter again:"
                except:
                    print "Search parameter must be an integer or blank. Please enter again:"
            else:
                MonthValid = True
        
        
        
        while DayValid != True:
            DateSearchDay = raw_input("Search Day: ")
            if DateSearchDay != "":
                try:
                    DateSearchDay = int(DateSearchDay)
                    if DateSearchDay >= 1 and DateSearchDay <= 365:
                        #print DateSearchDay
                        DayValid = True
                    else:
                        print "Search parameter must be between 1 and 365. Please enter again:"
                except:
                    print "Search parameter must be an integer or blank. Please enter again:"
            else:
                DayValid = True
        
        
        
        while HourValid != True:
            DateSearchHour = raw_input("Search Hour: ")
            if DateSearchHour != "":
                try:
                    DateSearchHour = int(DateSearchHour)
                    if DateSearchHour >= 0 and DateSearchHour <= 23:
                        #print DateSearchHour
                        HourValid = True
                    else:
                        print "Search parameter must be between 0 and 23. Please enter again:"
                except:
                    print "Search parameter must be an integer or blank. Please enter again:"
            else:
                HourValid = True
        
        
        
        while MinuteValid != True:
            DateSearchMinute = raw_input("Search Minute: ")
            if DateSearchMinute != "":
                try:
                    DateSearchMinute = int(DateSearchMinute)
                    if DateSearchMinute >= 0 and DateSearchMinute <= 59:
                        #print DateSearchMinute
                        MinuteValid = True
                    else:
                        print "Search parameter must be between 0 and 59. Please enter again:"
                except:
                    print "Search parameter must be an integer or blank. Please enter again:"
            else:
                MinuteValid = True
        
        
        
        while SecondValid != True:
            DateSearchSecond = raw_input("Search Second: ")
            if DateSearchSecond != "":
                try:
                    DateSearchSecond = int(DateSearchSecond)
                    if DateSearchSecond >= 0 and DateSearchSecond <= 59:
                        #print DateSearchSecond
                        SecondValid = True
                    else:
                        print "Search parameter must be between 0 and 59. Please enter again:"
                except:
                    print "Search parameter must be an integer or blank. Please enter again:"
            else:
                SecondValid = True
        
        
        
        #Combines all date/time component values into a list for passing to main()
        SearchValue = [DateSearchYear, DateSearchMonth, DateSearchDay, DateSearchHour, DateSearchMinute, DateSearchSecond]
    
    
    
    #Execute
    main(SearchParameter, SearchValue)
    
    
    