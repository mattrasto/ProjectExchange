#-------------------------------------------------------------------------------
# Name:        DBSearchUserBook
# Version:     1.0
# Purpose:
#
# Author:      Matthew
#
# Created:     04/04/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    04/17/2014
#-------------------------------------------------------------------------------

import MySQLdb

db = MySQLdb.connect("localhost","root","***","exchangedatabase")

cursor = db.cursor()

cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data

DateSearchYearOmit = False

SearchParameter = raw_input("Search by: ")
SearchParameter = SearchParameter.upper()
ParameterCheck = "SELECT * FROM Users" #BuyBook is not specific; SellBook may also be used as they have similar columns
try:
    cursor.execute(ParameterCheck)
    for Header in cursor.description:
        TargetParameter = Header[0]
        if TargetParameter.upper() == SearchParameter or SearchParameter == "USD CREDIT" or SearchParameter == "BTC CREDIT" or SearchParameter == "JOIN DATE" or SearchParameter == "FIRST NAME" or SearchParameter == "LAST NAME" or SearchParameter == "BANK NAME" or SearchParameter == "TRADING FEE":
            if SearchParameter == "USDCREDIT":
                print "Searching by: USD Credit"
                break;
            elif SearchParameter == "BTCCREDIT":
                print "Searching by: BTC Credit"
                break;
            elif SearchParameter == "JOINDATE":
                print "Searching by: Join Date"
                break;
            elif SearchParameter == "FIRSTNAME":
                print "Searching by: First Name"
                break;
            elif SearchParameter == "LASTNAME":
                print "Searching by: Last Name"
                break;
            elif SearchParameter == "BANKNAME":
                print "Searching by: Bank Name"
                break;
            elif SearchParameter == "TRADINGFEE":
                print "Searching by: Trading Fee"
                break;
            else:
                print "Searching by: " + SearchParameter.title()
                break;
    while TargetParameter.upper() != SearchParameter and SearchParameter != "USD CREDIT" and SearchParameter != "BTC CREDIT" and SearchParameter != "JOIN DATE" and SearchParameter != "FIRST NAME" and SearchParameter != "LAST NAME" and SearchParameter != "BANK NAME" and SearchParameter != "TRADING FEE":
        print "Cannot search by that attribute. Please enter again:"
        print "Choices: " + str([Header[0] for Header in cursor.description])
        SearchParameter = raw_input("Search by: ")
        SearchParameter = SearchParameter.upper()
        for Header in cursor.description:
            TargetParameter = Header[0]
            if TargetParameter.upper() == SearchParameter or SearchParameter == "ORDER NUMBER" or SearchParameter == "DATE ENTERED":
                if SearchParameter == "USDCREDIT":
                    print "Searching by: USD Credit"
                    break;
                elif SearchParameter == "BTCCREDIT":
                    print "Searching by: BTC Credit"
                    break;
                elif SearchParameter == "JOINDATE":
                    print "Searching by: Join Date"
                    break;
                elif SearchParameter == "FIRSTNAME":
                    print "Searching by: First Name"
                    break;
                elif SearchParameter == "LASTNAME":
                    print "Searching by: Last Name"
                    break;
                elif SearchParameter == "BANKNAME":
                    print "Searching by: Bank Name"
                    break;
                elif SearchParameter == "TRADINGFEE":
                    print "Searching by: Trading Fee"
                    break;
                else:
                    print "Searching by: " + SearchParameter.title()
                    break;
except:
    "ERROR: Database execution unsuccessful"

if SearchParameter != "JOINDATE" and SearchParameter != "JOIN DATE":
    SearchValue = raw_input("Search for value: ")
    while SearchValue == "":
        print "You must enter a value to search by:"
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

if SearchParameter == "USERNAME" or SearchParameter == "USER NAME":
    SearchValue = str(SearchValue.capitalize())
    sql = "SELECT * FROM Users"
    try:
        cursor.execute(sql)
        Users = cursor.fetchall()
        for User in Users:
            if User[0] == SearchValue:
                print ""
                print "Users that meet search parameters:"
                print ""
                for User in Users:
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
                break;
        else:
            print ""
            print "No users meet search parameters"
    except:
        "ERROR: Database fetch exception"

if SearchParameter == "PASSWORD":
    SearchValue = str(SearchValue.capitalize())
    sql = "SELECT * FROM Users"
    try:
        cursor.execute(sql)
        Users = cursor.fetchall()
        for User in Users:
            if User[1] == SearchValue:
                print ""
                print "Users that meet search parameters:"
                print ""
                for User in Users:
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
                break;
        else:
            print ""
            print "No users meet search parameters"
    except:
        "ERROR: Database fetch exception"

if SearchParameter == "EMAIL":
    SearchValue = str(SearchValue.capitalize())
    sql = "SELECT * FROM Users"
    try:
        cursor.execute(sql)
        Users = cursor.fetchall()
        for User in Users:
            if User[2] == SearchValue:
                print ""
                print "Users that meet search parameters:"
                print ""
                for User in Users:
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
                break;
        else:
            print ""
            print "No users meet search parameters"
    except:
        "ERROR: Database fetch exception"

if SearchParameter == "USDCREDIT" or SearchParameter == "USD CREDIT":
    while 1 == 1:
        try:
            SearchValue = int(SearchValue.capitalize())
            break;
        except:
            print "You may only enter numbers for this parameter:"
            SearchValue = raw_input("Search for value: ")
    sql = "SELECT * FROM Users"
    try:
        cursor.execute(sql)
        Users = cursor.fetchall()
        for User in Users:
            if User[3] == SearchValue:
                print ""
                print "Users that meet search parameters:"
                print ""
                for User in Users:
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
                break;
        else:
            print ""
            print "No users meet search parameters"
    except:
        "ERROR: Database fetch exception"

if SearchParameter == "BTCCREDIT" or SearchParameter == "BTC CREDIT":
    while 1 == 1:
        try:
            SearchValue = int(SearchValue.capitalize())
            break;
        except:
            print "You may only enter numbers for this parameter:"
            SearchValue = raw_input("Search for value: ")
    sql = "SELECT * FROM Users"
    try:
        cursor.execute(sql)
        Users = cursor.fetchall()
        for User in Users:
            if User[4] == SearchValue:
                print ""
                print "Users that meet search parameters:"
                print ""
                for User in Users:
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
                break;
        else:
            print ""
            print "No users meet search parameters"
    except:
        "ERROR: Database fetch exception"

if SearchParameter == "JOINDATE" or SearchParameter == "JOIN DATE":
    sql = "SELECT * FROM Users"
    try:
        cursor.execute(sql)
        Users = cursor.fetchall()
        for User in Users:
            if DateSearchYearOmit == True:
                YearValue = ""
                for Character in str(User[5])[:4]:
                    YearValue += str(Character)
                DateSearchYear = YearValue
                
            if DateSearchMonthOmit == True:
                MonthValue = ""
                for Character in str(User[5])[5:7]:
                    MonthValue += str(Character)
                DateSearchMonth = MonthValue
                
            if DateSearchDayOmit == True:
                DayValue = ""
                for Character in str(User[5])[8:10]:
                    DayValue += str(Character)
                DateSearchDay = DayValue
                
            if DateSearchHourOmit == True:
                HourValue = ""
                for Character in str(User[5])[11:13]:
                    HourValue += str(Character)
                DateSearchHour = HourValue
                
            if DateSearchMinuteOmit == True:
                MinuteValue = ""
                for Character in str(User[5])[14:16]:
                    MinuteValue += str(Character)
                DateSearchMinute = MinuteValue
            
            if DateSearchSecondOmit == True:
                SecondValue = ""
                for Character in str(User[5])[17:19]:
                    SecondValue += str(Character)
                DateSearchSecond = SecondValue
            
            if str(DateSearchYear) == str(User[5])[:4] and str(DateSearchMonth) == str(User[5])[5:7] and str(DateSearchDay) == str(User[5])[8:10] and str(DateSearchHour) == str(User[5])[11:13] and str(DateSearchMinute) == str(User[5])[14:16] and str(DateSearchSecond) == str(User[5])[17:19]:
                print ""
                print "Users that meet search parameters:"
                print ""
                for User in Users:
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
                break;
        else:
            print ""
            print "No users meet search parameters"
    except:
        "ERROR: Database fetch exception"

if SearchParameter == "FIRSTNAME" or SearchParameter == "FIRST NAME":
    SearchValue = str(SearchValue.capitalize())
    sql = "SELECT * FROM Users"
    try:
        cursor.execute(sql)
        Users = cursor.fetchall()
        for User in Users:
            if User[6] == SearchValue:
                print ""
                print "Users that meet search parameters:"
                print ""
                for User in Users:
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
                break;
        else:
            print ""
            print "No users meet search parameters"
    except:
        "ERROR: Database fetch exception"

if SearchParameter == "LASTNAME" or SearchParameter == "LAST NAME":
    SearchValue = str(SearchValue.capitalize())
    sql = "SELECT * FROM Users"
    try:
        cursor.execute(sql)
        Users = cursor.fetchall()
        for User in Users:
            if User[7] == SearchValue:
                print ""
                print "Users that meet search parameters:"
                print ""
                for User in Users:
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
                break;
        else:
            print ""
            print "No users meet search parameters"
    except:
        "ERROR: Database fetch exception"

if SearchParameter == "BANKNAME" or SearchParameter == "BANK NAME":
    SearchValue = str(SearchValue.capitalize())
    sql = "SELECT * FROM Users"
    try:
        cursor.execute(sql)
        Users = cursor.fetchall()
        for User in Users:
            if User[8] == SearchValue:
                print ""
                print "Users that meet search parameters:"
                print ""
                for User in Users:
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
                break;
        else:
            print ""
            print "No users meet search parameters"
    except:
        "ERROR: Database fetch exception"

if SearchParameter == "ADDRESS":
    SearchValue = str(SearchValue.capitalize())
    sql = "SELECT * FROM Users"
    try:
        cursor.execute(sql)
        Users = cursor.fetchall()
        for User in Users:
            if User[9] == SearchValue:
                print ""
                print "Users that meet search parameters:"
                print ""
                for User in Users:
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
                break;
        else:
            print ""
            print "No users meet search parameters"
    except:
        "ERROR: Database fetch exception"

if SearchParameter == "VERIFIED":
    SearchValue = str(SearchValue.capitalize())
    sql = "SELECT * FROM Users"
    try:
        cursor.execute(sql)
        Users = cursor.fetchall()
        for User in Users:
            if User[10] == SearchValue:
                print ""
                print "Users that meet search parameters:"
                print ""
                for User in Users:
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
                break;
        else:
            print ""
            print "No users meet search parameters"
    except:
        "ERROR: Database fetch exception"

if SearchParameter == "TRADINGFEE" or SearchParameter == "TRADING FEE":
    while 1 == 1:
        try:
            SearchValue = int(SearchValue.capitalize())
            break;
        except:
            print "You may only enter numbers for this parameter:"
            SearchValue = raw_input("Search for value: ")
    sql = "SELECT * FROM Users"
    try:
        cursor.execute(sql)
        Users = cursor.fetchall()
        for User in Users:
            if User[11] == SearchValue:
                print ""
                print "Users that meet search parameters:"
                print ""
                for User in Users:
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
                break;
        else:
            print ""
            print "No users meet search parameters"
    except:
        "ERROR: Database fetch exception"

if SearchParameter == "VOLUME":
    while 1 == 1:
        try:
            SearchValue = int(SearchValue.capitalize())
            break;
        except:
            print "You may only enter numbers for this parameter:"
            SearchValue = raw_input("Search for value: ")
    sql = "SELECT * FROM Users"
    try:
        cursor.execute(sql)
        Users = cursor.fetchall()
        for User in Users:
            if User[12] == SearchValue:
                print ""
                print "Users that meet search parameters:"
                print ""
                for User in Users:
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
                break;
        else:
            print ""
            print "No users meet search parameters"
    except:
        "ERROR: Database fetch exception"