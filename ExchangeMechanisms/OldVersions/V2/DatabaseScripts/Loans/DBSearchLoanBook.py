#-------------------------------------------------------------------------------
# Name:        DBSearchLoanBook
# Version:     2.0
# Purpose:
#
# Author:      Matthew
#
# Created:     05/31/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/05/2014
#-------------------------------------------------------------------------------

import MySQLdb



def ContractPrint(Contracts):
    
    #Prints all contracts matched with search query
    
    print "Contracts that meet search parameters:"
    print ""
    for Contract in Contracts:
        print "------------------------------"
        print ""
        print "Contract Number: " + str(Contract[0])
        print "Username: " + str(Contract[1])
        print "Medium: " + str(Contract[2])
        print "Volume: " + str(Contract[3])
        print "Action: " + str(Contract[4])
        print "Interest Compound Rate: " + str(Contract[5])
        print "Interest Rate: " + str(Contract[6])
        print "Duration: " + str(Contract[7])
        print "End Point: " + str(Contract[8])
        print "Dividend Type: " + str(Contract[9])
        print "Minimum Borrower Constraints: " + str(Contract[10])
        print "User Intervention Constraints: " + str(Contract[11])
        print "User Requests: " + str(Contract[12])
        print "Date Entered: " + str(Contract[13])
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
    
    #Searches for contracts with specific ContractNumber
    if SearchParameter == "CONTRACT NUMBER":
        #Converts OrderNumber value to integer type
        try:
            SearchValue = int(SearchValue)
        except:
            print "CRITICAL ERROR: Contract Number unable to be converted to integer"
            sys.exit()
        try:
            ContractNumberSearch = "SELECT * FROM LoanBook WHERE ContractNumber = %d" % (SearchValue)
            cursor.execute(ContractNumberSearch)
            Contracts = cursor.fetchall()
            #If atleast 1 contract is found, passes list to print function
            if Contracts != ():
                ContractPrint(Contracts)
            else:
                print "No contracts meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for contracts under specific Username
    if SearchParameter == "USERNAME":
        #Converts Username value to string type and capitalizes
        try:
            SearchValue = str(SearchValue.capitalize())
        except:
            print "CRITICAL ERROR: Username unable to be converted to string"
            sys.exit()
        try:
            UsernameSearch = """SELECT * FROM LoanBook WHERE Username = "%s" """ % (SearchValue)
            cursor.execute(UsernameSearch)
            Contracts = cursor.fetchall()
            #If atleast 1 contract is found, passes list to print function
            if Contracts != ():
                ContractPrint(Contracts)
            else:
                print "No contracts meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for contracts with specific Medium
    if SearchParameter == "MEDIUM":
        #Converts Medium value to string type and capitalizes
        try:
            SearchValue = str(SearchValue.capitalize())
        except:
            print "CRITICAL ERROR: Medium unable to be converted to string"
            sys.exit()
        try:
            Medium = """SELECT * FROM LoanBook WHERE Medium = "%s" """ % (SearchValue)
            cursor.execute(MediumSearch)
            Contracts = cursor.fetchall()
            #If atleast 1 contract is found, passes list to print function
            if Contracts != ():
                ContractPrint(Contracts)
            else:
                print "No contracts meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for contracts with specific Volume
    if SearchParameter == "VOLUME":
        #Converts Volume value to float type
        try:
            SearchValue = float(SearchValue)
        except:
            print "CRITICAL ERROR: Volume unable to be converted to float"
            sys.exit()
        try:
            VolumeSearch = "SELECT * FROM LoanBook WHERE Volume = %f" % (SearchValue)
            cursor.execute(VolumeSearch)
            Contracts = cursor.fetchall()
            #If atleast 1 contract is found, passes list to print function
            if Contracts != ():
                ContractPrint(Contracts)
            else:
                print "No contracts meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for contracts with specific Action
    if SearchParameter == "ACTION":
        #Converts Action value to string type and capitalizes
        try:
            SearchValue = str(SearchValue.capitalize())
        except:
            print "CRITICAL ERROR: Action unable to be converted to string"
            sys.exit()
        try:
            ActionSearch = """SELECT * FROM LoanBook WHERE Action = "%s" """ % (SearchValue)
            cursor.execute(ActionSearch)
            Contracts = cursor.fetchall()
            #If atleast 1 contract is found, passes list to print function
            if Contracts != ():
                ContractPrint(Contracts)
            else:
                print "No contracts meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for contracts with specific InterestCompoundRate
    if SearchParameter == "INTEREST COMPOUND RATE":
        #Converts InterestCompoundRate value to string type
        try:
            SearchValue = str(SearchValue)
        except:
            print "CRITICAL ERROR: Interest Compound Rate unable to be converted to string"
            sys.exit()
        try:
            InterestCompoundRateSearch = """SELECT * FROM LoanBook WHERE InterestCompoundRate = "%s" """ % (SearchValue)
            cursor.execute(InterestCompoundRateSearch)
            Contracts = cursor.fetchall()
            #If atleast 1 contract is found, passes list to print function
            if Contracts != ():
                ContractPrint(Contracts)
            else:
                print "No contracts meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for contracts with specific InterestRate
    if SearchParameter == "INTEREST RATE":
        #Converts InterestRate value to float type
        try:
            SearchValue = float(SearchValue)
        except:
            print "CRITICAL ERROR: Interest Rate unable to be converted to float"
            sys.exit()
        try:
            InterestRateSearch = "SELECT * FROM LoanBook WHERE InterestRate = %f" % (SearchValue)
            cursor.execute(InterestRateSearch)
            Contracts = cursor.fetchall()
            #If atleast 1 contract is found, passes list to print function
            if Contracts != ():
                ContractPrint(Contracts)
            else:
                print "No contracts meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for contracts with specific Duration
    if SearchParameter == "DURATION":
        #Converts Duration value to string type
        try:
            SearchValue = str(SearchValue)
        except:
            print "CRITICAL ERROR: Duration unable to be converted to string"
            sys.exit()
        try:
            DurationSearch = """SELECT * FROM LoanBook WHERE Duration = "%s" """ % (SearchValue)
            cursor.execute(DurationSearch)
            Contracts = cursor.fetchall()
            #If atleast 1 contract is found, passes list to print function
            if Contracts != ():
                ContractPrint(Contracts)
            else:
                print "No contracts meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for contracts with specific EndPoint
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
        
        
        
        #Uses "LIKE" operator to compare value with wildcards, which replaces value with an "ANY" search in contract to search for current value if input was left blank
        EndPointSearch = """SELECT * FROM LoanBook WHERE (YEAR(EndPoint) LIKE "%s") AND (MONTH(EndPoint) LIKE "%s") AND (DAY(EndPoint) LIKE "%s") AND (HOUR(EndPoint) LIKE "%s") AND (MINUTE(EndPoint) LIKE "%s") AND (SECOND(EndPoint) LIKE "%s")""" % (YearParameter, MonthParameter, DayParameter, HourParameter, MinuteParameter, SecondParameter)
        try:
            cursor.execute(EndPointSearch)
            Contracts = cursor.fetchall()
            #If atleast 1 contract is found, passes list to print function
            if Contracts != ():
                ContractPrint(Contracts)
            else:
                print ""
                print "No users meet search parameters"
        except:
            "ERROR: Database Fetch Exception"
    
    
    
    #Searches for contracts with specific DividendType
    if SearchParameter == "DIVIDEND TYPE":
        #Converts DividendType value to string type and capitalizes
        try:
            SearchValue = str(SearchValue.capitalize())
        except:
            print "CRITICAL ERROR: Dividend Type unable to be converted to string"
            sys.exit()
        try:
            DividendtypeSearch = """SELECT * FROM LoanBook WHERE DividendType = "%s" """ % (SearchValue)
            cursor.execute(DividendTypeSearch)
            Contracts = cursor.fetchall()
            #If atleast 1 contract is found, passes list to print function
            if Contracts != ():
                ContractPrint(Contracts)
            else:
                print "No contracts meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for contracts with specific amount of MinimumBorrowerConstraints
    if SearchParameter == "MINIMUM BORROWER CONSTRAINTS":
        #Converts MinimumBorrowerConstraints value to integer type
        try:
            SearchValue = int(SearchValue)
        except:
            print "CRITICAL ERROR: Minimum Borrower Constraints unable to be converted to integer"
            sys.exit()
        try:
            MinimumBorrowerConstraintsSearch = "SELECT * FROM LoanBook WHERE MinimumBorrowerConstraints = %d" % (SearchValue)
            cursor.execute(MinimumBorrowerConstraintsSearch)
            Contracts = cursor.fetchall()
            #If atleast 1 contract is found, passes list to print function
            if Contracts != ():
                ContractPrint(Contracts)
            else:
                print "No contracts meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for contracts with specific amount of UserInterventionConstraints
    if SearchParameter == "USER INTERVENTION CONSTRAINTS":
        #Converts UserInterventionConstraints value to integer type
        try:
            SearchValue = int(SearchValue)
        except:
            print "CRITICAL ERROR: User Intervention Constraints unable to be converted to integer"
            sys.exit()
        try:
            UserInterventionConstraintsSearch = "SELECT * FROM LoanBook WHERE UserInterventionConstraints = %d" % (SearchValue)
            cursor.execute(UserInterventionConstraintsSearch)
            Contracts = cursor.fetchall()
            #If atleast 1 contract is found, passes list to print function
            if Contracts != ():
                ContractPrint(Contracts)
            else:
                print "No contracts meet search criteria"
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
            UserRequestsSearch = "SELECT * FROM LoanBook WHERE UserRequests = %d" % (SearchValue)
            cursor.execute(UserRequestsSearch)
            Contracts = cursor.fetchall()
            #If atleast 1 contract is found, passes list to print function
            if Contracts != ():
                ContractPrint(Contracts)
            else:
                print "No contracts meet search criteria"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    #Searches for contracts with specific DateEntered
    if SearchParameter == "DATEENTERED" or SearchParameter == "DATE ENTERED":
        
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
        DateEnteredSearch = """SELECT * FROM LoanBook WHERE (YEAR(DateEntered) LIKE "%s") AND (MONTH(DateEntered) LIKE "%s") AND (DAY(DateEntered) LIKE "%s") AND (HOUR(DateEntered) LIKE "%s") AND (MINUTE(DateEntered) LIKE "%s") AND (SECOND(DateEntered) LIKE "%s")""" % (YearParameter, MonthParameter, DayParameter, HourParameter, MinuteParameter, SecondParameter)
        try:
            cursor.execute(DateEnteredSearch)
            Contracts = cursor.fetchall()
            #If atleast 1 contract is found, passes list to print function
            if Contracts != ():
                ContractPrint(Contracts)
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
    ParameterCheck = "SHOW COLUMNS FROM LoanBook"
    
    
    
    #Checking if search parameter is valid
    try:
        cursor.execute(ParameterCheck)
        FieldList = cursor.fetchall()
        for Field in FieldList:
            TargetParameter = Field[0]
            if TargetParameter.upper() == SearchParameter or SearchParameter == "CONTRACT NUMBER" or SearchParameter == "DATE ENTERED" or SearchParameter == "INTEREST COMPOUND RATE" or SearchParameter == "INTEREST RATE" or SearchParameter == "END POINT" or SearchParameter == "DIVIDEND TYPE" or SearchParameter == "MINIMUM BORROWER CONSTRAINTS" or SearchParameter == "USER INTERVENTION CONSTRAINTS" or SearchParameter == "USER REQUESTS":
                break;
        
        #Retrying until valid input is given
        while TargetParameter.upper() != SearchParameter and SearchParameter != "CONTRACT NUMBER" and SearchParameter != "DATE ENTERED" and SearchParameter != "INTEREST COMPOUND RATE" and SearchParameter != "INTEREST RATE" and SearchParameter != "END POINT" and SearchParameter != "DIVIDEND TYPE" and SearchParameter != "MINIMUM BORROWER CONSTRAINTS" and SearchParameter != "USER INTERVENTION CONSTRAINTS" and SearchParameter != "USER REQUESTS":
            
            print "Cannot search by that attribute. Please enter again:"
            print "Choices: " + str([Field[0] for Field in FieldList])
            SearchParameter = raw_input("Search by: ")
            SearchParameter = SearchParameter.upper()
            for Field in FieldList:
                TargetParameter = Field[0]
                if TargetParameter.upper() == SearchParameter or SearchParameter == "CONTRACT NUMBER" or SearchParameter == "DATE ENTERED" or SearchParameter == "INTEREST COMPOUND RATE" or SearchParameter == "INTEREST RATE" or SearchParameter == "END POINT" or SearchParameter == "DIVIDEND TYPE" or SearchParameter == "MINIMUM BORROWER CONSTRAINTS" or SearchParameter == "USER INTERVENTION CONSTRAINTS" or SearchParameter == "USER REQUESTS":
                    break;
                    
    except:
        "ERROR: Database Execution Unsuccessful"
    
    
    
    '''Standardizing Parameter Names'''
    
    
    
    if SearchParameter == "CONTRACTNUMBER":
        SearchParameter = "CONTRACT NUMBER"
        print "Searching by: Contract Number"
    
    elif SearchParameter == "INTERESTCOMPOUNDRATE":
        SearchParameter = "INTEREST COMPOUND RATE"
        print "Searching by: Interest Compound Rate"
    
    elif SearchParameter == "INTERESTRATE":
        SearchParameter = "INTEREST RATE"
        print "Searching by: Interest Rate"
    
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
    
    elif SearchParameter == "USERREQUESTS":
        SearchParameter = "USER REQUESTS"
        print "Searching by: User Requests"
    
    elif SearchParameter == "DATEENTERED":
        SearchParameter = "DATE ENTERED"
        print "Searching by: Date Entered"
    
    elif SearchParameter == "USERREQUESTS":
        SearchParameter = "USER REQUESTS"
        print "Searching by: User Requests"
    
    else:
        print "Searching by: " + SearchParameter.title()
    
    
    
    '''Setting Search Value'''
    
    
    
    #Requests interval/value input if correct field
    if SearchParameter == "INTEREST COMPOUND RATE" or SearchParameter == "DURATION":
        SearchValueInterval = raw_input("Search for interval: ")
        SearchValueValue = raw_input("Search for value: ")
        
        SearchValueInterval = str(SearchValueInterval.upper())
        SearchValueValue = int(SearchValueValue)
        SearchValue = str(SearchValueValue) + " " + SearchValueInterval
    
    #Requests basic input value if not a date field
    elif SearchParameter != "DATE ENTERED" and SearchParameter != "END POINT":
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
                        print DateSearchYear
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
                        print DateSearchMonth
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
                        print DateSearchDay
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
                        print DateSearchHour
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
                        print DateSearchMinute
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
                        print DateSearchSecond
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
    
    
    