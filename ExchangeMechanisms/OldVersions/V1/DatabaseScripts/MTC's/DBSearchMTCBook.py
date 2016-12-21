#-------------------------------------------------------------------------------
# Name:        DBSearchMTCBook
# Version:     1.0
# Purpose:
#
# Author:      Matthew
#
# Created:     05/26/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    05/30/2014
#-------------------------------------------------------------------------------

import MySQLdb

db = MySQLdb.connect("localhost","root","***","exchangedatabase")

cursor = db.cursor()

cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data

MTCHeaderPrinted = False
MTCFound = False

SearchParameter = raw_input("Search by: ")
SearchParameter = SearchParameter.upper()
ParameterCheck = "DESCRIBE MTCBook"
try:
    cursor.execute(ParameterCheck)
    TableDescription = cursor.fetchall()
    for Row in TableDescription:
        TargetParameter = Row[0]
        if TargetParameter.upper() == SearchParameter or SearchParameter == "MTC NUMBER" or SearchParameter == "DATE ENTERED" or SearchParameter == "INTEREST COMPOUND RATE" or SearchParameter == "INTEREST RATE" or SearchParameter == "STOP LOSS PRICE" or SearchParameter == "FULFILLMENT PRICE" or SearchParameter == "END POINT" or SearchParameter == "DIVIDEND TYPE" or SearchParameter == "MINIMUM BORROWER CONSTRAINTS" or SearchParameter == "USER INTERVENTION CONSTRAINTS" or SearchParameter == "USER REQUESTS":
            break;
    while TargetParameter.upper() != SearchParameter and SearchParameter != "MTC NUMBER" and SearchParameter != "DATE ENTERED" and SearchParameter != "INTEREST COMPOUND RATE" and SearchParameter != "INTEREST RATE" and SearchParameter != "STOP LOSS PRICE" and SearchParameter != "FULFILLMENT PRICE" and SearchParameter != "END POINT" and SearchParameter != "DIVIDEND TYPE" and SearchParameter != "MINIMUM BORROWER CONSTRAINTS" and SearchParameter != "USER INTERVENTION CONSTRAINTS" and SearchParameter != "USER REQUESTS":
        print "Cannot search by that attribute. Please enter again:"
        print "Choices: " + str([Row[0] for Row in TableDescription])
        SearchParameter = raw_input("Search by: ")
        SearchParameter = SearchParameter.upper()
        for Row in TableDescription:
            TargetParameter = Row[0]
            if TargetParameter.upper() == SearchParameter or SearchParameter == "MTC NUMBER" or SearchParameter == "DATE ENTERED" or SearchParameter == "INTEREST COMPOUND RATE" or SearchParameter == "INTEREST RATE" or SearchParameter == "STOP LOSS PRICE" or SearchParameter == "FULFILLMENT PRICE" or SearchParameter == "END POINT" or SearchParameter == "DIVIDEND TYPE" or SearchParameter == "MINIMUM BORROWER CONSTRAINTS" or SearchParameter == "USER INTERVENTION CONSTRAINTS" or SearchParameter == "USER REQUESTS":
                    break;
except:
    print "ERROR: Database execution unsuccessful"



'''Standardizing Parameter Names'''



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



'''Prompting For Extra Inputs'''



if SearchParameter == "INTEREST COMPOUND RATE" or SearchParameter == "DURATION":
    SearchValueInterval = raw_input("Search for interval: ")
    SearchValueValue = raw_input("Search for value: ")
elif SearchParameter != "DATE ENTERED":
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



if SearchParameter == "MTC NUMBER":
    SearchValue = int(SearchValue)
    sql = "SELECT * FROM MTCBook WHERE MTCNumber = %d" % (SearchValue)
    try:
        cursor.execute(sql)
        MTC = cursor.fetchall()
        print ""
        if MTC != ():
            MTC = MTC[0]
            print "MTC Number: " + str(MTC[0])
            print "Username: " + MTC[1]
            print "Type: MTC"
            print "Action: " + MTC[4]
            print "Price: " + str(MTC[2])
            print "Volume: " + str(MTC[3])
            print "Date Entered: " + str(MTC[15])
            MTCFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "USERNAME":
    SearchValue = str(SearchValue.capitalize())
    try:
        sql = """SELECT * FROM MTCBook WHERE Username = "%s" """ % (SearchValue)
        cursor.execute(sql)
        MTCList = cursor.fetchall()
        for MTC in MTCList:
            if MTCHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                MTCHeaderPrinted = True
            print ""
            print "MTC Number: " + str(MTC[0])
            print "Username: " + MTC[1]
            print "Type: MTC"
            print "Action: " + MTC[4]
            print "Price: " + str(MTC[2])
            print "Volume: " + str(MTC[3])
            print "Date Entered: " + str(MTC[15])
            MTCFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "PRICE":
    SearchValue = float(SearchValue)
    try:
        sql = "SELECT * FROM MTCBook WHERE Price = %f" % (SearchValue)
        cursor.execute(sql)
        MTCList = cursor.fetchall()
        for MTC in MTCList:
            if MTCHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                MTCHeaderPrinted = True
            print ""
            print "MTC Number: " + str(MTC[0])
            print "Username: " + MTC[1]
            print "Type: MTC"
            print "Action: " + MTC[4]
            print "Price: " + str(MTC[2])
            print "Volume: " + str(MTC[3])
            print "Date Entered: " + str(MTC[15])
            MTCFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "VOLUME":
    SearchValue = float(SearchValue)
    try:
        sql = "SELECT * FROM MTCBook WHERE Volume = %f" % (SearchValue)
        cursor.execute(sql)
        MTCList = cursor.fetchall()
        for MTC in MTCList:
            if MTCHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                MTCHeaderPrinted = True
            print ""
            print "MTC Number: " + str(MTC[0])
            print "Username: " + MTC[1]
            print "Type: MTC"
            print "Action: " + MTC[4]
            print "Price: " + str(MTC[2])
            print "Volume: " + str(MTC[3])
            print "Date Entered: " + str(MTC[15])
            MTCFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "ACTION":
    SearchValue = str(SearchValue.capitalize())
    try:
        sql = """SELECT * FROM MTCBook WHERE Action = "%s" """ % (SearchValue)
        cursor.execute(sql)
        MTCList = cursor.fetchall()
        for MTC in MTCList:
            if MTCHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                MTCHeaderPrinted = True
            print ""
            print "MTC Number: " + str(MTC[0])
            print "Username: " + MTC[1]
            print "Type: MTC"
            print "Action: " + MTC[4]
            print "Price: " + str(MTC[2])
            print "Volume: " + str(MTC[3])
            print "Date Entered: " + str(MTC[15])
            MTCFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "INTEREST COMPOUND RATE":
    SearchValueInterval = str(SearchValueInterval.upper())
    SearchValueValue = float(SearchValueValue)
    SearchValue = str(SearchValueValue) + " " + SearchValueInterval
    #print "Interest Compound Rate: " + str(SearchValue)
    try:
        sql = """SELECT * FROM MTCBook WHERE InterestCompoundRate = "%s" """ % (SearchValue)
        cursor.execute(sql)
        MTCList = cursor.fetchall()
        for MTC in MTCList:
            if MTCHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                MTCHeaderPrinted = True
            print ""
            print "MTC Number: " + str(MTC[0])
            print "Username: " + MTC[1]
            print "Type: MTC"
            print "Action: " + MTC[4]
            print "Price: " + str(MTC[2])
            print "Volume: " + str(MTC[3])
            print "Date Entered: " + str(MTC[15])
            MTCFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "INTEREST RATE":
    SearchValue = float(SearchValue)
    try:
        sql = "SELECT * FROM MTCBook WHERE InterestRate = %f" % (SearchValue)
        cursor.execute(sql)
        MTCList = cursor.fetchall()
        for MTC in MTCList:
            if MTCHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                MTCHeaderPrinted = True
            print ""
            print "MTC Number: " + str(MTC[0])
            print "Username: " + MTC[1]
            print "Type: MTC"
            print "Action: " + MTC[4]
            print "Price: " + str(MTC[2])
            print "Volume: " + str(MTC[3])
            print "Date Entered: " + str(MTC[15])
            MTCFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "STOP LOSS PRICE":
    SearchValue = float(SearchValue)
    try:
        sql = "SELECT * FROM MTCBook WHERE StopLossPrice = %f" % (SearchValue)
        cursor.execute(sql)
        MTCList = cursor.fetchall()
        for MTC in MTCList:
            if MTCHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                MTCHeaderPrinted = True
            print ""
            print "MTC Number: " + str(MTC[0])
            print "Username: " + MTC[1]
            print "Type: MTC"
            print "Action: " + MTC[4]
            print "Price: " + str(MTC[2])
            print "Volume: " + str(MTC[3])
            print "Date Entered: " + str(MTC[15])
            MTCFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "FULFILLMENT PRICE":
    SearchValue = float(SearchValue)
    try:
        sql = "SELECT * FROM MTCBook WHERE FulfillmentPrice = %f" % (SearchValue)
        cursor.execute(sql)
        MTCList = cursor.fetchall()
        for MTC in MTCList:
            if MTCHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                MTCHeaderPrinted = True
            print ""
            print "MTC Number: " + str(MTC[0])
            print "Username: " + MTC[1]
            print "Type: MTC"
            print "Action: " + MTC[4]
            print "Price: " + str(MTC[2])
            print "Volume: " + str(MTC[3])
            print "Date Entered: " + str(MTC[15])
            MTCFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "DURATION":
    SearchValueInterval = str(SearchValueInterval.upper())
    SearchValueValue = float(SearchValueValue)
    SearchValue = str(SearchValueValue) + " " + SearchValueInterval
    #print "Duration: " + str(SearchValue)
    try:
        sql = """SELECT * FROM MTCBook WHERE Duration = "%s" """ % (SearchValue)
        cursor.execute(sql)
        MTCList = cursor.fetchall()
        for MTC in MTCList:
            if MTCHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                MTCHeaderPrinted = True
            print ""
            print "MTC Number: " + str(MTC[0])
            print "Username: " + MTC[1]
            print "Type: MTC"
            print "Action: " + MTC[4]
            print "Price: " + str(MTC[2])
            print "Volume: " + str(MTC[3])
            print "Date Entered: " + str(MTC[15])
            MTCFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "DIVIDEND TYPE":
    SearchValue = str(SearchValue.capitalize())
    try:
        sql = """SELECT * FROM MTCBook WHERE DividendType = "%s" """ % (SearchValue)
        cursor.execute(sql)
        MTCList = cursor.fetchall()
        for MTC in MTCList:
            if MTCHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                MTCHeaderPrinted = True
            print ""
            print "MTC Number: " + str(MTC[0])
            print "Username: " + MTC[1]
            print "Type: MTC"
            print "Action: " + MTC[4]
            print "Price: " + str(MTC[2])
            print "Volume: " + str(MTC[3])
            print "Date Entered: " + str(MTC[15])
            MTCFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "MINIMUM BORROWER CONSTRAINTS":
    SearchValue = int(SearchValue)
    sql = "SELECT * FROM MTCBook WHERE MinimumBorrowerConstraints = %d" % (SearchValue)
    try:
        cursor.execute(sql)
        MTCList = cursor.fetchall()
        for MTC in MTCList:
            if MTCHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                MTCHeaderPrinted = True
            print ""
            print "MTC Number: " + str(MTC[0])
            print "Username: " + MTC[1]
            print "Type: MTC"
            print "Action: " + MTC[4]
            print "Price: " + str(MTC[2])
            print "Volume: " + str(MTC[3])
            print "Date Entered: " + str(MTC[15])
            MTCFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "USER INTERVENTION CONSTRAINTS":
    SearchValue = int(SearchValue)
    sql = "SELECT * FROM MTCBook WHERE UserInterventionConstraints = %d" % (SearchValue)
    try:
        cursor.execute(sql)
        MTCList = cursor.fetchall()
        for MTC in MTCList:
            if MTCHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                MTCHeaderPrinted = True
            print ""
            print "MTC Number: " + str(MTC[0])
            print "Username: " + MTC[1]
            print "Type: MTC"
            print "Action: " + MTC[4]
            print "Price: " + str(MTC[2])
            print "Volume: " + str(MTC[3])
            print "Date Entered: " + str(MTC[15])
            MTCFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "DATEENTERED" or SearchParameter == "DATE ENTERED":
    try:
        sql = "SELECT * FROM MTCBook"
        cursor.execute(sql)
        MTCList = cursor.fetchall()
        for MTC in MTCList:
            if DateSearchYearOmit == True:
                YearValue = ""
                for Character in str(MTC[15])[:4]:
                    YearValue += str(Character)
                DateSearchYear = YearValue
                
            if DateSearchMonthOmit == True:
                MonthValue = ""
                for Character in str(MTC[15])[5:7]:
                    MonthValue += str(Character)
                DateSearchMonth = MonthValue
                
            if DateSearchDayOmit == True:
                DayValue = ""
                for Character in str(MTC[15])[8:10]:
                    DayValue += str(Character)
                DateSearchDay = DayValue
                
            if DateSearchHourOmit == True:
                HourValue = ""
                for Character in str(MTC[15])[11:13]:
                    HourValue += str(Character)
                DateSearchHour = HourValue
                
            if DateSearchMinuteOmit == True:
                MinuteValue = ""
                for Character in str(MTC[15])[14:16]:
                    MinuteValue += str(Character)
                DateSearchMinute = MinuteValue
            
            if DateSearchSecondOmit == True:
                SecondValue = ""
                for Character in str(MTC[15])[17:19]:
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
            
            if str(DateSearchYear) == str(MTC[15])[:4] and str(DateSearchMonth) == str(MTC[15])[5:7] and str(DateSearchDay) == str(MTC[15])[8:10] and str(DateSearchHour) == str(MTC[15])[11:13] and str(DateSearchMinute) == str(MTC[15])[14:16] and str(DateSearchSecond) == str(MTC[15])[17:19]:
                if MTCHeaderPrinted != True:
                    MTCHeaderPrinted = True
                    print ""
                    print "Orders that meet search parameters:"
                print ""
                print "MTC Number: " + str(MTC[0])
                print "Username: " + MTC[1]
                print "Type: MTC"
                print "Action: " + MTC[4]
                print "Price: " + str(MTC[2])
                print "Volume: " + str(MTC[3])
                print "Date Entered: " + str(MTC[15])
                MTCFound = True
    except:
        print "ERROR: Database fetch exception"



if MTCFound != True:
    print ""
    print "No orders meet search criteria"



db.close()