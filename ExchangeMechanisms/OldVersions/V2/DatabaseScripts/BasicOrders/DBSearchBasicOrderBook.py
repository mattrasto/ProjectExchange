#-------------------------------------------------------------------------------
# Name:        DBSearchBasicOrderBook
# Version:     2.0
# Purpose:
#
# Author:      Matthew
#
# Created:     05/17/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/04/2014
#-------------------------------------------------------------------------------

#Add more options/functionality

import MySQLdb



#Initializes database
db = MySQLdb.connect("localhost","root","***","exchange")
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
Data = cursor.fetchone()[0]
print "Database Version: " + str(Data)



def OrderPrint(Orders):
    
    #Prints all users matched with search query
    
    print "Orders that meet search parameters:"
    print ""
    for Order in Orders:
        print "------------------------------"
        print ""
        print "Order Number: " + str(Order[0])
        print "Username: " + str(Order[1])
        print "Price: " + str(Order[2])
        print "Volume: " + str(Order[3])
        print "Type: " + str(Order[4])
        print "Action: " + str(Order[5])
        print "Trigger Type: " + str(Order[6])
        print "Trigger Action: " + str(Order[7])
        print "Active: " + str(Order[8])
        print "Date Entered: " + str(Order[9])
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
    
    #Searches for orders with specific OrderNumber
    if SearchParameter == "ORDER NUMBER":
        #Converts OrderNumber value to integer type
        try:
            SearchValue = int(SearchValue)
        except:
            print "CRITICAL ERROR: Order Number unable to be converted to integer"
            sys.exit()
        #Search query
        try:
            OrderNumberSearch = """SELECT * FROM BasicOrderBook WHERE OrderNumber = %d""" % (SearchValue)
            cursor.execute(OrderNumberSearch)
            Orders = cursor.fetchall()
            #If atleast 1 order is found, passes list to print function
            if Orders != ():
                OrderPrint(Orders)
            else:
                print "No orders meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for orders under specific Username
    if SearchParameter == "USERNAME":
        #Converts Username value to string type and capitalizes
        try:
            SearchValue = str(SearchValue.capitalize())
        except:
            print "CRITICAL ERROR: Username unable to be converted to string"
            sys.exit()
        #Search query
        try:
            UsernameSearch = """SELECT * FROM BasicOrderBook WHERE Username = "%s" """ % (SearchValue)
            cursor.execute(UsernameSearch)
            Orders = cursor.fetchall()
            #If atleast 1 order is found, passes list to print function
            if Orders != ():
                OrderPrint(Orders)
            else:
                print "No orders meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for orders with specific Price
    if SearchParameter == "PRICE":
        #Converts Price value to float type
        try:
            SearchValue = float(SearchValue)
        except:
            print "CRITICAL ERROR: Price unable to be converted to float"
            sys.exit()
        #Search query
        try:
            PriceSearch = "SELECT * FROM BasicOrderBook WHERE Price = %f" % (SearchValue)
            cursor.execute(PriceSearch)
            Orders = cursor.fetchall()
            #If atleast 1 order is found, passes list to print function
            if Orders != ():
                OrderPrint(Orders)
            else:
                print "No orders meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for orders with specific Volume
    if SearchParameter == "VOLUME":
        #Converts Volume value to float type
        try:
            SearchValue = float(SearchValue)
        except:
            print "CRITICAL ERROR: Volume unable to be converted to float"
            sys.exit()
        #Search query
        try:
            VolumeSearch = "SELECT * FROM BasicOrderBook WHERE Volume = %f" % (SearchValue)
            cursor.execute(VolumeSearch)
            Orders = cursor.fetchall()
            #If atleast 1 order is found, passes list to print function
            if Orders != ():
                OrderPrint(Orders)
            else:
                print "No orders meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for orders of a specific Type (Limit, Liquid, or Conditional)
    if SearchParameter == "TYPE":
        #Converts Type value to string type and capitalizes
        try:
            SearchValue = str(SearchValue.capitalize())
        except:
            print "CRITICAL ERROR: Type unable to be converted to string"
            sys.exit()
        #Search query
        try:
            TypeSearch = """SELECT * FROM BasicOrderBook WHERE Type = "%s" """ % (SearchValue)
            cursor.execute(TypeSearch)
            Orders = cursor.fetchall()
            #If atleast 1 order is found, passes list to print function
            if Orders != ():
                OrderPrint(Orders)
            else:
                print "No orders meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for orders with specific Action (Buy or Sell)
    if SearchParameter == "ACTION":
        #Converts Action value to string type and capitalizes
        try:
            SearchValue = str(SearchValue.capitalize())
        except:
            print "CRITICAL ERROR: Action unable to be converted to string"
            sys.exit()
        #Search query
        try:
            ActionSearch = """SELECT * FROM BasicOrderBook WHERE Action = "%s" """ % (SearchValue)
            cursor.execute(ActionSearch)
            Orders = cursor.fetchall()
            #If atleast 1 order is found, passes list to print function
            if Orders != ():
                OrderPrint(Orders)
            else:
                print "No orders meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for orders with specific Trigger Type (Bid Price, Ask price, Latest Price, Average Price)
    #NOTE: Add verification
    if SearchParameter == "TRIGGER TYPE":
        #Converts Trigger Type value to string and capitalizes
        try:
            SearchValue = str(SearchValue.capitalize())
        except:
            print "CRITICAL ERROR: Trigger Type unable to be converted to string"
            sys.exit()
        #Search query
        try:
            TriggerTypeSearch = """SELECT * FROM BasicOrderBook WHERE TriggerType = "%s" """ % (SearchValue)
            cursor.execute(TriggerTypeSearch)
            Orders = cursor.fetchall()
            #If atleast 1 order is found, passes list to print function
            if Orders != ():
                OrderPrint(Orders)
            else:
                print "No orders meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for orders with specified Trigger Value
    if SearchParameter == "TRIGGER VALUE":
        #Converts Trigger Value value to float
        try:
            SearchValue = float(SearchValue)
        except:
            print "CRITICAL ERROR: Trigger Value unable to be converted to float"
            sys.exit()
        #Search query
        try:
            TriggerValueSearch = """SELECT * FROM BasicOrderBook WHERE TriggerValue = %f """ % (SearchValue)
            cursor.execute(TriggerValueSearch)
            OrderList = cursor.fetchall()
            #If atleast 1 order is found, passes list to print function
            if Orders != ():
                OrderPrint(Orders)
            else:
                print "No orders meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for orders entered on a specific date
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
        
        
        
        #Uses "LIKE" operator to compare value with wildcards, which replaces value with an "ANY" search in order to search for current value if input was left blank
        DateEnteredSearch = """SELECT * FROM BasicOrderBook WHERE (YEAR(DateEntered) LIKE "%s") AND (MONTH(DateEntered) LIKE "%s") AND (DAY(DateEntered) LIKE "%s") AND (HOUR(DateEntered) LIKE "%s") AND (MINUTE(DateEntered) LIKE "%s") AND (SECOND(DateEntered) LIKE "%s")""" % (YearParameter, MonthParameter, DayParameter, HourParameter, MinuteParameter, SecondParameter)
        try:
            cursor.execute(DateEnteredSearch)
            Orders = cursor.fetchall()
            #If atleast 1 order is found, passes list to print function
            if Orders != ():
                OrderPrint(Orders)
            else:
                print ""
                print "No users meet search parameters"
        except:
            "ERROR: Database Fetch Exception"
    
    
    
    db.close()



if __name__ == "__main__":
    
    
    
    ''''Setting Search Parameter'''
    
    
    
    SearchParameter = (raw_input("Search by: ")).upper()
    ParameterCheck = "SHOW COLUMNS FROM BasicOrderBook"
    
    
    
    #Checking if search parameter is valid
    try:
        cursor.execute(ParameterCheck)
        FieldList = cursor.fetchall()
        for Field in FieldList:
            TargetParameter = Field[0]
            if TargetParameter.upper() == SearchParameter or SearchParameter == "ORDER NUMBER" or SearchParameter == "DATE ENTERED" or SearchParameter == "TRIGGER TYPE" or SearchParameter == "TRIGGER VALUE":
                break;
        
        #Retrying until valid input is given
        while TargetParameter.upper() != SearchParameter and SearchParameter != "ORDER NUMBER" and SearchParameter != "DATE ENTERED" and SearchParameter != "TRIGGER TYPE" and SearchParameter != "TRIGGER VALUE":
            print "Cannot search by that attribute. Please enter again:"
            print "Choices: " + str([Field[0] for Field in FieldList])
            SearchParameter = raw_input("Search by: ")
            SearchParameter = SearchParameter.upper()
            for Field in FieldList:
                TargetParameter = Field[0]
                if TargetParameter.upper() == SearchParameter or SearchParameter == "ORDER NUMBER" or SearchParameter == "DATE ENTERED":
                    break;
    except:
        "ERROR: Database Execution Unsuccessful"
    
    
    
    '''Standardizing Parameter Names'''
    
    
    
    if SearchParameter == "ORDERNUMBER":
        SearchParameter = "ORDER NUMBER"
        print "Searching by: Order Number"
    
    elif SearchParameter == "TRIGGERTYPE":
        SearchParameter = "TRIGGER TYPE"
        print "Searching by: Trigger Type"
    
    elif SearchParameter == "TRIGGER VALUE":
        SearchParameter = "TRIGGER VALUE"
        print "Searching by: Trigger Value"
    
    elif SearchParameter == "DATEENTERED":
        SearchParameter = "DATE ENTERED"
        print "Searching by: Date Entered"
    
    else:
        print "Searching by: " + SearchParameter.title()
    
    
    
    '''Setting Search Value'''
    
    
    
    #Requests basic input value if not a date field
    if SearchParameter != "DATE ENTERED" and SearchParameter != "TRIGGER TYPE":
        SearchValue = raw_input("Search for value: ")
        while SearchValue == "":
            print "You must enter a value to search by:"
            SearchValue = raw_input("Search for value: ")
    elif SearchParameter == "TRIGGER TYPE":
        SearchValue = (raw_input("Search for value: ")).upper()
        while SearchValue != "BID PRICE" and SearchValue != "ASK PRICE" and SearchValue != "LATEST PRICE" and SearchValue != "AVERAGE PRICE":
            print "Invalid Trigger Type. Please enter again:"
            print "Choices: [\"Bid Price\", \"Ask Price\", \"Latest Price\", \"Average Price\"]"
            SearchValue = (raw_input("Search for value: ")).upper()
    
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
    
    
    