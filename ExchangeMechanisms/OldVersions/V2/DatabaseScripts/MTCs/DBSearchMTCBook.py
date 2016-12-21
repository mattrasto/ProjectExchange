#-------------------------------------------------------------------------------
# Name:        DBSearchMTCBook
# Version:     2.0
# Purpose:
#
# Author:      Matthew
#
# Created:     05/26/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/15/2014
#-------------------------------------------------------------------------------

import MySQLdb



def MTCPrint(MTCs):
    
    #Prints all MTC's matched with search query
    
    print "MTC's that meet search parameters:"
    print ""
    for MTC in MTCs:
        print "------------------------------"
        print ""
        print "MTC Number: " + str(MTC[0])
        print "Username: " + MTC[1]
        print "Price: " + str(MTC[2])
        print "Volume: " + str(MTC[3])
        print "Action: " + str(MTC[4])
        print "Interest Compound Rate: " + str(MTC[5])
        print "Interest Rate: " + str(MTC[6])
        print "Stop Loss Price: " + str(MTC[7])
        print "Fulfillment Price: " + str(MTC[8])
        print "Duration: " + str(MTC[9])
        print "End Point: " + str(MTC[10])
        print "Dividend Type: " + str(MTC[11])
        print "Minimum Borrower Constraints: " + str(MTC[12])
        print "User Intervention Constraints: " + str(MTC[13])
        print "User Requests: " + str(MTC[14])
        print "Date Entered: " + str(MTC[15])
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
    print "Database version: "+ str(Data)
    
    
    
    print ""
    
    #Searches for MTCs with specific MTCNumber
    if SearchParameter == "MTC NUMBER":
        #Converts MTCNumber value to integer type
        try:
            SearchValue = int(SearchValue)
        except:
            print "CRITICAL ERROR: MTC Number unable to be converted to integer"
            sys.exit()
        try:
            MTCNumberSearch = "SELECT * FROM MTCBook WHERE MTCNumber = %d" % (SearchValue)
            cursor.execute(MTCNumberSearch)
            MTCs = cursor.fetchall()
            #If atleast 1 MTC is found, passes list to print function
            if MTCs != ():
                MTCPrint(MTCs)
            else:
                print "No MTC's meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    #Searches for MTCs under specific Username
    if SearchParameter == "USERNAME":
        #Converts Username value to string type and capitalizes
        SearchValue = str(SearchValue.capitalize())
        try:
            SearchValue = str(SearchValue)
        except:
            print "CRITICAL ERROR: Username unable to be converted to string"
            sys.exit()
        try:
            UsernameSearch = """SELECT * FROM MTCBook WHERE Username = "%s" """ % (SearchValue)
            cursor.execute(UsernameSearch)
            MTCs = cursor.fetchall()
            #If atleast 1 MTC is found, passes list to print function
            if MTCs != ():
                MTCPrint(MTCs)
            else:
                print "No MTC's meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for MTCs with specific Price
    if SearchParameter == "PRICE":
        #Converts Price value to float type
        try:
            SearchValue = float(SearchValue)
        except:
            print "CRITICAL ERROR: Price unable to be converted to float"
            sys.exit()
        try:
            PriceSearch = "SELECT * FROM MTCBook WHERE Price = %f" % (SearchValue)
            cursor.execute(PriceSearch)
            MTCs = cursor.fetchall()
            #If atleast 1 MTC is found, passes list to print function
            if MTCs != ():
                MTCPrint(MTCs)
            else:
                print "No MTC's meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for MTCs with specific Volume
    if SearchParameter == "VOLUME":
        #Converts Volume value to float type
        try:
            SearchValue = float(SearchValue)
        except:
            print "CRITICAL ERROR: Volume unable to be converted to float"
            sys.exit()
        try:
            VolumeSearch = "SELECT * FROM MTCBook WHERE Volume = %f" % (SearchValue)
            cursor.execute(VolumeSearch)
            MTCs = cursor.fetchall()
            #If atleast 1 MTC is found, passes list to print function
            if MTCs != ():
                MTCPrint(MTCs)
            else:
                print "No MTC's meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for MTCs with specific Action
    if SearchParameter == "ACTION":
        #Converts Action value to string type and capitalizes
        try:
            SearchValue = str(SearchValue.capitalize())
        except:
            print "CRITICAL ERROR: Action unable to be converted to string"
            sys.exit()
        try:
            ActionSearch = """SELECT * FROM MTCBook WHERE Action = "%s" """ % (SearchValue)
            cursor.execute(ActionSearch)
            MTCs = cursor.fetchall()
            #If atleast 1 MTC is found, passes list to print function
            if MTCs != ():
                MTCPrint(MTCs)
            else:
                print "No MTC's meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for MTCs with specific InterestCompoundRate
    if SearchParameter == "INTEREST COMPOUND RATE":
        #Converts InterestCompoundRate value to string type
        try:
            SearchValue = str(SearchValue)
        except:
            print "CRITICAL ERROR: Interest Compound Rate unable to be converted to string"
            sys.exit()
        try:
            InterestCompoundRateSearch = """SELECT * FROM MTCBook WHERE InterestCompoundRate = "%s" """ % (SearchValue)
            cursor.execute(InterestCompoundRateSearch)
            MTCs = cursor.fetchall()
            #If atleast 1 MTC is found, passes list to print function
            if MTCs != ():
                MTCPrint(MTCs)
            else:
                print "No MTC's meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for MTCs with specific InterestRate
    if SearchParameter == "INTEREST RATE":
        #Converts InterestRate value to float type
        try:
            SearchValue = float(SearchValue)
        except:
            print "CRITICAL ERROR: Interest Rate unable to be converted to float"
            sys.exit()
        try:
            InterestRateSearch = "SELECT * FROM MTCBook WHERE InterestRate = %f" % (SearchValue)
            cursor.execute(InterestRateSearch)
            MTCs = cursor.fetchall()
            #If atleast 1 MTC is found, passes list to print function
            if MTCs != ():
                MTCPrint(MTCs)
            else:
                print "No MTC's meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for MTCs with specific StopLossPrice
    if SearchParameter == "STOP LOSS PRICE":
        #Converts StopLossPrice value to float type
        try:
            SearchValue = float(SearchValue)
        except:
            print "CRITICAL ERROR: Stop Loss Price unable to be converted to float"
            sys.exit()
        try:
            StopLossPriceSearch = "SELECT * FROM MTCBook WHERE StopLossPrice = %f" % (SearchValue)
            cursor.execute(StopLossPriceSearch)
            MTCs = cursor.fetchall()
            #If atleast 1 MTC is found, passes list to print function
            if MTCs != ():
                MTCPrint(MTCs)
            else:
                print "No MTC's meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for MTCs with specific FulfillmentPrice
    if SearchParameter == "FULFILLMENT PRICE":
        #Converts FulfillmentPrice value to float type
        try:
            SearchValue = float(SearchValue)
        except:
            print "CRITICAL ERROR: Fulfillment Price unable to be converted to float"
            sys.exit()
        try:
            FulfillmentPriceSearch= "SELECT * FROM MTCBook WHERE FulfillmentPrice = %f" % (SearchValue)
            cursor.execute(FulfillmentPriceSearch)
            MTCs = cursor.fetchall()
            #If atleast 1 MTC is found, passes list to print function
            if MTCs != ():
                MTCPrint(MTCs)
            else:
                print "No MTC's meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for MTCs with specific Duration
    if SearchParameter == "DURATION":
        #Converts Duration value to string type
        try:
            SearchValue = str(SearchValue)
        except:
            print "CRITICAL ERROR: Duration unable to be converted to string"
            sys.exit()
        try:
            DurationSearch = """SELECT * FROM MTCBook WHERE Duration = "%s" """ % (SearchValue)
            cursor.execute(DurationSearch)
            MTCs = cursor.fetchall()
            #If atleast 1 MTC is found, passes list to print function
            if MTCs != ():
                MTCPrint(MTCs)
            else:
                print "No MTC's meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for MTCs with specific EndPoint
    if SearchParameter == "END POINT":
        
        #Separates SearchValue variable into date/time components
        EndPointSearchYear = SearchValue[0]
        EndPointSearchMonth = SearchValue[1]
        EndPointSearchDay = SearchValue[2]
        EndPointSearchHour = SearchValue[3]
        EndPointSearchMinute = SearchValue[4]
        EndPointSearchSecond = SearchValue[5]
        
        
        
        #If user left any interval blank, turns search parameter to "%" for wildcard searching in database
        if EndPointSearchYear == "":
            YearParameter = "%"
        else:
            YearParameter = EndPointSearchYear
        if EndPointSearchMonth == "":
            MonthParameter = "%"
        else:
            MonthParameter = EndPointSearchMonth
        if EndPointSearchDay == "":
            DayParameter = "%"
        else:
            DayParameter = EndPointSearchDay
        if EndPointSearchHour == "":
            HourParameter = "%"
        else:
            HourParameter = EndPointSearchHour
        if EndPointSearchMinute == "":
            MinuteParameter = "%"
        else:
            MinuteParameter = EndPointSearchMinute
        if EndPointSearchSecond == "":
            SecondParameter = "%"
        else:
            SecondParameter = EndPointSearchSecond
        
        
        
        #Uses "LIKE" operator to compare value with wildcards, which replaces value with an "ANY" search in MTC to search for current value if input was left blank
        EndPointSearch = """SELECT * FROM MTCBook WHERE (YEAR(EndPoint) LIKE "%s") AND (MONTH(EndPoint) LIKE "%s") AND (DAY(EndPoint) LIKE "%s") AND (HOUR(EndPoint) LIKE "%s") AND (MINUTE(EndPoint) LIKE "%s") AND (SECOND(EndPoint) LIKE "%s")""" % (YearParameter, MonthParameter, DayParameter, HourParameter, MinuteParameter, SecondParameter)
        try:
            cursor.execute(EndPointSearch)
            MTCs = cursor.fetchall()
            #If atleast 1 MTC is found, passes list to print function
            print MTCs
            if MTCs != ():
                MTCPrint(MTCs)
            else:
                print ""
                print "No users meet search parameters"
        except:
            "ERROR: Database Fetch Exception"
    
    
    
    #Searches for MTCs with specific DividendType
    if SearchParameter == "DIVIDEND TYPE":
        #Converts DividendType value to string type and capitalizes
        try:
            SearchValue = str(SearchValue.capitalize())
        except:
            print "CRITICAL ERROR: Dividend Type unable to be converted to string"
            sys.exit()
        try:
            DividendtypeSearch = """SELECT * FROM MTCBook WHERE DividendType = "%s" """ % (SearchValue)
            cursor.execute(DividendTypeSearch)
            MTCs = cursor.fetchall()
            #If atleast 1 MTC is found, passes list to print function
            if MTCs != ():
                MTCPrint(MTCs)
            else:
                print "No MTC's meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for MTCs with specific amount ofMinimumBorrowerConstraints
    if SearchParameter == "MINIMUM BORROWER CONSTRAINTS":
        #Converts MinimumBorrowerConstraints value to integer type
        try:
            SearchValue = int(SearchValue)
        except:
            print "CRITICAL ERROR: Minimum Borrower Constraints unable to be converted to integer"
            sys.exit()
        try:
            MinimumBorrowerConstraintsSearch = "SELECT * FROM MTCBook WHERE MinimumBorrowerConstraints = %d" % (SearchValue)
            cursor.execute(MinimumBorrowerConstraintsSearch)
            MTCs = cursor.fetchall()
            #If atleast 1 MTC is found, passes list to print function
            if MTCs != ():
                MTCPrint(MTCs)
            else:
                print "No MTC's meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for MTCs with specific amount of UserInterventionConstraints
    if SearchParameter == "USER INTERVENTION CONSTRAINTS":
        #Converts UserInterventionConstraints value to integer type
        try:
            SearchValue = int(SearchValue)
        except:
            print "CRITICAL ERROR: User Intervention Constraints unable to be converted to integer"
            sys.exit()
        try:
            UserInterventionConstraintsSearch = "SELECT * FROM MTCBook WHERE UserInterventionConstraints = %d" % (SearchValue)
            cursor.execute(UserInterventionConstraintsSearch)
            MTCs = cursor.fetchall()
            #If atleast 1 MTC is found, passes list to print function
            if MTCs != ():
                MTCPrint(MTCs)
            else:
                print "No MTC's meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for contracts with specific amount of UserRequests
    if SearchParameter == "USER REQUESTS":
        #Converts UserRequests value to integer type
        try:
            SearchValue = int(SearchValue)
        except:
            print "CRITICAL ERROR: User Requests unable to be converted to integer"
            sys.exit()
        try:
            UserRequestsSearch = "SELECT * FROM MTCBook WHERE UserRequests = %d" % (SearchValue)
            cursor.execute(UserRequestsSearch)
            Contracts = cursor.fetchall()
            #If atleast 1 contract is found, passes list to print function
            if Contracts != ():
                ContractPrint(Contracts)
            else:
                print "No contracts meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for MTCs with specific DateEntered
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
        
        
        
        #Uses "LIKE" operator to compare value with wildcards, which replaces value with an "ANY" search in MTC to search for current value if input was left blank
        DateEnteredSearch = """SELECT * FROM MTCBook WHERE (YEAR(DateEntered) LIKE "%s") AND (MONTH(DateEntered) LIKE "%s") AND (DAY(DateEntered) LIKE "%s") AND (HOUR(DateEntered) LIKE "%s") AND (MINUTE(DateEntered) LIKE "%s") AND (SECOND(DateEntered) LIKE "%s")""" % (YearParameter, MonthParameter, DayParameter, HourParameter, MinuteParameter, SecondParameter)
        try:
            cursor.execute(DateEnteredSearch)
            MTCs = cursor.fetchall()
            #If atleast 1 MTC is found, passes list to print function
            if MTCs != ():
                MTCPrint(MTCs)
            else:
                print ""
                print "No users meet search parameters"
        except:
            "ERROR: Database Fetch Exception"
    
    
    
    db.close()



if __name__ == "__main__":
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    
    
    '''Setting Search Parameter'''
    
    
    
    SearchParameter = (raw_input("Search by: ")).upper()
    ParameterCheck = "SHOW COLUMNS FROM MTCBook"
    
    
    
    #Checking if search parameter is valid
    try:
        cursor.execute(ParameterCheck)
        FieldList = cursor.fetchall()
        print FieldList
        for Field in FieldList:
            TargetParameter = Field[0]
            if TargetParameter.upper() == SearchParameter or SearchParameter == "MTC NUMBER" or SearchParameter == "DATE ENTERED" or SearchParameter == "INTEREST COMPOUND RATE" or SearchParameter == "INTEREST RATE" or SearchParameter == "STOP LOSS PRICE" or SearchParameter == "FULFILLMENT PRICE" or SearchParameter == "END POINT" or SearchParameter == "DIVIDEND TYPE" or SearchParameter == "MINIMUM BORROWER CONSTRAINTS" or SearchParameter == "USER INTERVENTION CONSTRAINTS" or SearchParameter == "USER REQUESTS":
                break;
        
        #Retrying until valid input is given
        while TargetParameter.upper() != SearchParameter and SearchParameter != "MTC NUMBER" and SearchParameter != "DATE ENTERED" and SearchParameter != "INTEREST COMPOUND RATE" and SearchParameter != "INTEREST RATE" and SearchParameter != "STOP LOSS PRICE" and SearchParameter != "FULFILLMENT PRICE" and SearchParameter != "END POINT" and SearchParameter != "DIVIDEND TYPE" and SearchParameter != "MINIMUM BORROWER CONSTRAINTS" and SearchParameter != "USER INTERVENTION CONSTRAINTS" and SearchParameter != "USER REQUESTS":
            
            print "Cannot search by that attribute. Please enter again:"
            print "Choices: " + str([Field[0] for Field in FieldList])
            SearchParameter = raw_input("Search by: ")
            SearchParameter = SearchParameter.upper()
            for Field in FieldList:
                TargetParameter = Field[0]
                if TargetParameter.upper() == SearchParameter or SearchParameter == "MTC NUMBER" or SearchParameter == "DATE ENTERED" or SearchParameter == "INTEREST COMPOUND RATE" or SearchParameter == "INTEREST RATE" or SearchParameter == "STOP LOSS PRICE" or SearchParameter == "FULFILLMENT PRICE" or SearchParameter == "END POINT" or SearchParameter == "DIVIDEND TYPE" or SearchParameter == "MINIMUM BORROWER CONSTRAINTS" or SearchParameter == "USER INTERVENTION CONSTRAINTS" or SearchParameter == "USER REQUESTS":
                    break;  
    except:
        "ERROR: Database Execution Unsuccessful"
    
    
    
    if SearchParameter == "MTCNUMBER":
        SearchParameter = "MTC NUMBER"
        print "Searching by: MTC Number"
    elif SearchParameter == "INTERESTCOMPOUNDRATE":
        SearchParameter = "INTEREST COMPOUND RATE"
        print "Searching by: Interest Compound Rate"
    elif SearchParameter == "INTERESTRATE":
        SearchParameter = "INTEREST RATE"
        print "Searching by: Interest Rate"
    elif SearchParameter == "STOPLOSSPRICE":
        SearchParameter = "STOP LOSS PRICE"
        print "Searching by: Stop Loss Price"
    elif SearchParameter == "FULFILLMENTPRICE":
        SearchParameter = "FULFILLMENT PRICE"
        print "Searching by: Fulfillment Price"
    elif SearchParameter == "ENDPOINT":
        SearchParameter = "END POINT"
        print "Searching by: End Point"
    elif SearchParameter == "DIVIDENDTYPE":
        SearchParameter = "DIVIDEND TYPE"
        print "Searching by: Dividend Type"
    elif SearchParameter == "MINIMUMBORROWERCONSTRAINTS":
        SearchParameter = "MINIMUM BORROWER CONSTRAINTS"
        print "Searching by: Minimum Borrower Constraints"
    elif SearchParameter == "USERINTERVENTIONCONSTRAINTS":
        SearchParameter = "USER INTERVENTION CONSTRAINTS"
        print "Searching by: User Intervention Constraints"
    elif SearchParameter == "DATEENTERED":
        SearchParameter = "DATE ENTERED"
        print "Searching by: Date Entered"
    else:
        print "Searching by: " + SearchParameter.title()
    
    
    
    #Prompting for interval/value input if correct field
    if SearchParameter == "INTEREST COMPOUND RATE" or SearchParameter == "DURATION":
        SearchValueInterval = raw_input("Search for interval: ")
        SearchValueValue = raw_input("Search for value: ")
        
        SearchValueInterval = str(SearchValueInterval.upper())
        SearchValueValue = int(SearchValueValue)
        SearchValue = str(SearchValueValue) + " " + SearchValueInterval
    
    #Prompting for basic input value if not a date field
    elif SearchParameter != "DATE ENTERED" and SearchParameter != "END POINT":
        SearchValue = raw_input("Search for value: ")
        while SearchValue == "":
            print "You must enter a value to search by:"
            SearchValue = raw_input("Search for value: ")
    
    #Prompting for date input and testing values for validity
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
    
    
    