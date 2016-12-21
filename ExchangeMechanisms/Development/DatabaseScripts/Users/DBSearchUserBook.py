#-------------------------------------------------------------------------------
# Name:        DBSearchUserBook
# Version:     3.0
# Purpose:     Searches UserBook with specified constraints
#
# Author:      Matthew
#
# Created:     04/04/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    08/28/2014
#-------------------------------------------------------------------------------

#Add more options/functionality

import MySQLdb
import sys



def UserPrint(Users):
    
    #Prints all users matched with search query
    
    print "Users that meet search parameters:"
    print ""
    for User in Users:
        print "------------------------------"
        print ""
        print "Username: " + str(User[0])
        print "Password: " + str(User[1])
        print "Email: " + str(User[2])
        print "USD: " + str(User[3])
        print "BTC: " + str(User[4])
        print "Join Date: " + str(User[5])
        print "First Name: " + str(User[6])
        print "Last Name: " + str(User[7])
        print "Bank: " + str(User[8])
        print "Address: " + str(User[9])
        print "Verified: " + str(User[10])
        print "Trading Fee: " + str(User[11])
        print "Volume: " + str(User[12])
        print ""
    print "------------------------------"



def main(SearchParameter, SearchValue):
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    
    
    #Contains all search functions
    #Note: In V2 all search functions are specific; This is planned to change
    #Each search simply checks the database for all users with the assigned SearchValue and then passes "Users" list to be printed
    
    
    
    print ""
    
    #Searches for users with specific Username
    if SearchParameter == "USERNAME":
        #Converts Username value to string type and capitalizes
        SearchValue = str(SearchValue.capitalize())
        UsernameSearch = """SELECT * FROM UserBook WHERE Username = "%s" """ % (SearchValue)
        try:
            cursor.execute(UsernameSearch)
            Users = cursor.fetchall()
            #If atleast 1 user is found, passes list to print function
            if Users != ():
                UserPrint(Users)
            else:
                print "No users meet search parameters"
        except:
            "ERROR: Database Fetch Exception"
    
    
    
    #Searches for users with specific Password
    if SearchParameter == "PASSWORD":
        #Converts Password value to string type and capitalizes
        SearchValue = str(SearchValue.capitalize())
        PasswordSearch = """SELECT * FROM UserBook WHERE Password = "%s" """ % (SearchValue)
        try:
            cursor.execute(PasswordSearch)
            Users = cursor.fetchall()
            #If atleast 1 user is found, passes list to print function
            if Users != ():
                UserPrint(Users)
            else:
                print "No users meet search parameters"
        except:
            "ERROR: Database Fetch Exception"
    
    
    
    #Searches for users with specific Email
    if SearchParameter == "EMAIL":
        #Converts Email value to string type and capitalizes
        SearchValue = str(SearchValue.capitalize())
        EmailSearch = """SELECT * FROM UserBook WHERE Email = "%s" """ % (SearchValue)
        try:
            cursor.execute(EmailSearch)
            Users = cursor.fetchall()
            #If atleast 1 user is found, passes list to print function
            if Users != ():
                UserPrint(Users)
            else:
                print "No users meet search parameters"
        except:
            "ERROR: Database Fetch Exception"
    
    
    
    #Searches for users with specific USDCredit
    if SearchParameter == "USD CREDIT":
        #Converts USDCredit value to float type
        while type(SearchValue) != float:
            try:
                SearchValue = float(SearchValue)
            except:
                print "You may only enter numbers for this parameter:"
                SearchValue = raw_input("Search for value: ")
        USDCreditSearch = """SELECT * FROM UserBook WHERE USDCredit = %f""" (SearchValue)
        try:
            cursor.execute(USDCreditSearch)
            Users = cursor.fetchall()
            #If atleast 1 user is found, passes list to print function
            if Users != ():
                UserPrint(Users)
            else:
                print "No users meet search parameters"
        except:
            "ERROR: Database Fetch Exception"
    
    
    
    #Searches for users with specific BTCCredit
    if SearchParameter == "BTC CREDIT":
        #Converts BTCCredit value to float type
        while type(SearchValue) != float:
            try:
                SearchValue = float(SearchValue)
            except:
                print "You may only enter numbers for this parameter:"
                SearchValue = raw_input("Search for value: ")
        BTCCreditSearch = """SELECT * FROM UserBook WHERE BTCCredit = %f""" (SearchValue)
        try:
            cursor.execute(BTCCreditSearch)
            Users = cursor.fetchall()
            #If atleast 1 user is found, passes list to print function
            if Users != ():
                UserPrint(Users)
            else:
                print "No users meet search parameters"
        except:
            "ERROR: Database Fetch Exception"
    
    
    
    #Searches for users with specific JoinDate
    if SearchParameter == "JOIN DATE":
        
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
        JoinDateSearch = """SELECT * FROM UserBook WHERE (YEAR(JoinDate) LIKE "%s") AND (MONTH(JoinDate) LIKE "%s") AND (DAY(JoinDate) LIKE "%s") AND (HOUR(JoinDate) LIKE "%s") AND (MINUTE(JoinDate) LIKE "%s") AND (SECOND(JoinDate) LIKE "%s")""" % (YearParameter, MonthParameter, DayParameter, HourParameter, MinuteParameter, SecondParameter)
        try:
            cursor.execute(JoinDateSearch)
            Users = cursor.fetchall()
            #If atleast 1 user is found, passes list to print function
            if Users != ():
                UserPrint(Users)
            else:
                print ""
                print "No users meet search parameters"
        except:
            print "ERROR: Database Fetch Exception"
    
    
    
    #Searches for users with specific FirstName
    if SearchParameter == "FIRST NAME":
        #Converts FirstName value to string type and capitalizes
        SearchValue = str(SearchValue.capitalize())
        FirstNameSearch = """SELECT * FROM UserBook WHERE FirstName = "%s" """ % (SearchValue)
        try:
            cursor.execute(FirstNameSearch)
            Users = cursor.fetchall()
            #If atleast 1 user is found, passes list to print function
            if Users != ():
                UserPrint(Users)
            else:
                print "No users meet search parameters"
        except:
            "ERROR: Database Fetch Exception"
    
    
    
    #Searches for users with specific LastName
    if SearchParameter == "LAST NAME":
        #Converts LastName value to string type and capitalizes
        SearchValue = str(SearchValue.capitalize())
        LastNameSearch = """SELECT * FROM UserBook WHERE LastName = "%s" """ % (SearchValue)
        try:
            cursor.execute(LastNameSearch)
            Users = cursor.fetchall()
            #If atleast 1 user is found, passes list to print function
            if Users != ():
                UserPrint(Users)
            else:
                print "No users meet search parameters"
        except:
            "ERROR: Database Fetch Exception"
    
    
    
    #Searches for users with specific BankName
    if SearchParameter == "BANK NAME":
        #Converts BankName value to string type and capitalizes
        SearchValue = str(SearchValue.capitalize())
        BankNameSearch = """SELECT * FROM UserBook WHERE BankName = "%s" """ % (SearchValue)
        try:
            cursor.execute(BankNameSearch)
            Users = cursor.fetchall()
            #If atleast 1 user is found, passes list to print function
            if Users != ():
                UserPrint(Users)
            else:
                print "No users meet search parameters"
        except:
            "ERROR: Database Fetch Exception"
    
    
    
    #Searches for users with specific Address
    if SearchParameter == "ADDRESS":
        #Converts Address value to string type and capitalizes
        SearchValue = str(SearchValue.capitalize())
        AddressSearch = """SELECT * FROM UserBook WHERE Address = "%s" """ % (SearchValue)
        try:
            cursor.execute(AddressSearch)
            Users = cursor.fetchall()
            #If atleast 1 user is found, passes list to print function
            if Users != ():
                UserPrint(Users)
            else:
                print "No users meet search parameters"
        except:
            "ERROR: Database Fetch Exception"
    
    
    
    #Searches for users with specific Verified status
    if SearchParameter == "VERIFIED":
        #Converts Verified value to integer type
        SearchValue = int(SearchValue)
        VerifiedSearch = """SELECT * FROM UserBook WHERE Verified = %d""" % (SearchValue)
        try:
            cursor.execute(VerifiedSearch)
            Users = cursor.fetchall()
            #If atleast 1 user is found, passes list to print function
            if Users != ():
                UserPrint(Users)
            else:
                print "No users meet search parameters"
        except:
            "ERROR: Database Fetch Exception"
    
    
    
    #Searches for users with specific TradingFee
    if SearchParameter == "TRADING FEE":
        #Converts TradingFee value to float type
        while type(SearchValue) != float:
            try:
                SearchValue = float(SearchValue.capitalize())
            except:
                print "You may only enter numbers for this parameter:"
                SearchValue = raw_input("Search for value: ")
        TradingFeeSearch = """SELECT * FROM UserBook WHERE TradingFee = %f""" % (SearchValue)
        try:
            cursor.execute(TradingFeeSearch)
            Users = cursor.fetchall()
            #If atleast 1 user is found, passes list to print function
            if Users != ():
                UserPrint(Users)
            else:
                print "No users meet search parameters"
        except:
            "ERROR: Database Fetch Exception"
    
    
    
    #Searches for users with specific Volume
    if SearchParameter == "VOLUME":
        #Converts Volume value to float type
        while type(SearchValue) != float:
            try:
                SearchValue = float(SearchValue)
            except:
                print "You may only enter numbers for this parameter:"
                SearchValue = raw_input("Search for value: ")
        VolumeSearch = """SELECT * FROM UserBook WHERE Volume = %f""" % (SearchValue)
        try:
            cursor.execute(VolumeSearch)
            Users = cursor.fetchall()
            #If atleast 1 user is found, passes list to print function
            if Users != ():
                UserPrint(Users)
            else:
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
    ParameterCheck = "SHOW COLUMNS FROM UserBook"
    
    
    
    #Checking if search parameter is valid
    try:
        cursor.execute(ParameterCheck)
        FieldList = cursor.fetchall()
        for Field in FieldList:
            TargetParameter = Field[0]
            if TargetParameter.upper() == SearchParameter or SearchParameter == "USD CREDIT" or SearchParameter == "BTC CREDIT" or SearchParameter == "JOIN DATE" or SearchParameter == "FIRST NAME" or SearchParameter == "LAST NAME" or SearchParameter == "BANK NAME" or SearchParameter == "TRADING FEE":
                    break;
        
        #Retrying until valid input is given
        while TargetParameter.upper() != SearchParameter and SearchParameter != "USD CREDIT" and SearchParameter != "BTC CREDIT" and SearchParameter != "JOIN DATE" and SearchParameter != "FIRST NAME" and SearchParameter != "LAST NAME" and SearchParameter != "BANK NAME" and SearchParameter != "TRADING FEE":
            
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
    
    
    
    if SearchParameter == "USDCREDIT":
        SearchParameter = "USD CREDIT"
        print "Searching by: USD Credit"
    
    elif SearchParameter == "BTCCREDIT":
        SearchParameter = "BTC CREDIT"
        print "Searching by: BTC Credit"
    
    elif SearchParameter == "JOINDATE":
        SearchParameter = "JOIN DATE"
        print "Searching by: Join Date"
    
    elif SearchParameter == "FIRSTNAME":
        SearchParameter = "FIRST NAME"
        print "Searching by: First Name"
    
    elif SearchParameter == "LASTNAME":
        SearchParameter = "LAST NAME"
        print "Searching by: Last Name"
    
    elif SearchParameter == "BANKNAME":
        SearchParameter = "BANK NAME"
        print "Searching by: Bank Name"
    
    elif SearchParameter == "TRADINGFEE":
        SearchParameter = "TRADING FEE"
        print "Searching by: Trading Fee"
    
    else:
        print "Searching by: " + SearchParameter.title()
    
    
    
    '''Setting Search Value'''
    
    
    
    #Prompting for basic input value if not a date field
    if SearchParameter != "JOIN DATE":
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


