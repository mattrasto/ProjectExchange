#-------------------------------------------------------------------------------
# Name:        DBSearchLoanBook
# Version:     1.0
# Purpose:
#
# Author:      Matthew
#
# Created:     05/31/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    05/31/2014
#-------------------------------------------------------------------------------

import MySQLdb

db = MySQLdb.connect("localhost","root","***","exchangedatabase")

cursor = db.cursor()

cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data

ContractHeaderPrinted = False
ContractFound = False

SearchParameter = raw_input("Search by: ")
SearchParameter = SearchParameter.upper()
ParameterCheck = "DESCRIBE LoanBook"
try:
    cursor.execute(ParameterCheck)
    TableDescription = cursor.fetchall()
    for Row in TableDescription:
        TargetParameter = Row[0]
        if TargetParameter.upper() == SearchParameter or SearchParameter == "CONTRACT NUMBER" or SearchParameter == "DATE ENTERED" or SearchParameter == "INTEREST COMPOUND RATE" or SearchParameter == "INTEREST RATE" or SearchParameter == "END POINT" or SearchParameter == "DIVIDEND TYPE" or SearchParameter == "MINIMUM BORROWER CONSTRAINTS" or SearchParameter == "USER INTERVENTION CONSTRAINTS" or SearchParameter == "USER REQUESTS":
            break;
    while TargetParameter.upper() != SearchParameter and SearchParameter != "CONTRACT NUMBER" and SearchParameter != "DATE ENTERED" and SearchParameter != "INTEREST COMPOUND RATE" and SearchParameter != "INTEREST RATE" and SearchParameter != "END POINT" and SearchParameter != "DIVIDEND TYPE" and SearchParameter != "MINIMUM BORROWER CONSTRAINTS" and SearchParameter != "USER INTERVENTION CONSTRAINTS" and SearchParameter != "USER REQUESTS":
        print "Cannot search by that attribute. Please enter again:"
        print "Choices: " + str([Row[0] for Row in TableDescription])
        SearchParameter = raw_input("Search by: ")
        SearchParameter = SearchParameter.upper()
        for Row in TableDescription:
            TargetParameter = Row[0]
            if TargetParameter.upper() == SearchParameter or SearchParameter == "CONTRACT NUMBER" or SearchParameter == "DATE ENTERED" or SearchParameter == "INTEREST COMPOUND RATE" or SearchParameter == "INTEREST RATE" or SearchParameter == "END POINT" or SearchParameter == "DIVIDEND TYPE" or SearchParameter == "MINIMUM BORROWER CONSTRAINTS" or SearchParameter == "USER INTERVENTION CONSTRAINTS" or SearchParameter == "USER REQUESTS":
                    break;
except:
    print "ERROR: Database execution unsuccessful"



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



if SearchParameter == "CONTRACT NUMBER":
    SearchValue = int(SearchValue)
    try:
        sql = "SELECT * FROM LoanBook WHERE ContractNumber = %d" % (SearchValue)
        cursor.execute(sql)
        Contract = cursor.fetchall()
        print ""
        if Contract != ():
            Contract = Contract[0]
            print "Contract Number: " + str(Contract[0])
            print "Username: " + Contract[1]
            print "Type: Loan"
            print "Action: " + Contract[4]
            print "Medium: " + str(Contract[2])
            print "Volume: " + str(Contract[3])
            print "Date Entered: " + str(Contract[13])
            ContractFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "USERNAME":
    SearchValue = str(SearchValue.capitalize())
    try:
        sql = """SELECT * FROM LoanBook WHERE Username = "%s" """ % (SearchValue)
        cursor.execute(sql)
        ContractList = cursor.fetchall()
        for Contract in ContractList:
            if ContractHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                ContractHeaderPrinted = True
            print ""
            print "Contract Number: " + str(Contract[0])
            print "Username: " + Contract[1]
            print "Type: Loan"
            print "Action: " + Contract[4]
            print "Medium: " + str(Contract[2])
            print "Volume: " + str(Contract[3])
            print "Date Entered: " + str(Contract[13])
            ContractFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "MEDIUM":
    SearchValue = str(SearchValue)
    try:
        sql = """SELECT * FROM LoanBook WHERE Medium = "%s" """ % (SearchValue)
        cursor.execute(sql)
        ContractList = cursor.fetchall()
        for Contract in ContractList:
            if ContractHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                ContractHeaderPrinted = True
            print ""
            print "Contract Number: " + str(Contract[0])
            print "Username: " + Contract[1]
            print "Type: Loan"
            print "Action: " + Contract[4]
            print "Medium: " + str(Contract[2])
            print "Volume: " + str(Contract[3])
            print "Date Entered: " + str(Contract[13])
            ContractFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "VOLUME":
    SearchValue = float(SearchValue)
    try:
        sql = "SELECT * FROM LoanBook WHERE Volume = %f" % (SearchValue)
        cursor.execute(sql)
        ContractList = cursor.fetchall()
        for Contract in ContractList:
            if ContractHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                ContractHeaderPrinted = True
            print ""
            print "Contract Number: " + str(Contract[0])
            print "Username: " + Contract[1]
            print "Type: Loan"
            print "Action: " + Contract[4]
            print "Medium: " + str(Contract[2])
            print "Volume: " + str(Contract[3])
            print "Date Entered: " + str(Contract[13])
            ContractFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "ACTION":
    SearchValue = str(SearchValue.capitalize())
    try:
        sql = """SELECT * FROM LoanBook WHERE Action = "%s" """ % (SearchValue)
        cursor.execute(sql)
        ContractList = cursor.fetchall()
        for Contract in ContractList:
            if ContractHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                ContractHeaderPrinted = True
            print ""
            print "Contract Number: " + str(Contract[0])
            print "Username: " + Contract[1]
            print "Type: Loan"
            print "Action: " + Contract[4]
            print "Medium: " + str(Contract[2])
            print "Volume: " + str(Contract[3])
            print "Date Entered: " + str(Contract[13])
            ContractFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "INTEREST COMPOUND RATE":
    SearchValueInterval = str(SearchValueInterval.upper())
    SearchValueValue = float(SearchValueValue)
    SearchValue = str(SearchValueValue) + " " + SearchValueInterval
    #print "Interest Compound Rate: " + str(SearchValue)
    try:
        sql = """SELECT * FROM LoanBook WHERE InterestCompoundRate = "%s" """ % (SearchValue)
        cursor.execute(sql)
        ContractList = cursor.fetchall()
        for Contract in ContractList:
            if ContractHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                ContractHeaderPrinted = True
            print ""
            print "Contract Number: " + str(Contract[0])
            print "Username: " + Contract[1]
            print "Type: MTC"
            print "Action: " + Contract[4]
            print "Medium: " + str(Contract[2])
            print "Volume: " + str(Contract[3])
            print "Date Entered: " + str(Contract[13])
            ContractFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "INTEREST RATE":
    SearchValue = float(SearchValue)
    try:
        sql = "SELECT * FROM LoanBook WHERE InterestRate = %f" % (SearchValue)
        cursor.execute(sql)
        ContractList = cursor.fetchall()
        for Contract in ContractList:
            if ContractHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                ContractHeaderPrinted = True
            print ""
            print "Contract Number: " + str(Contract[0])
            print "Username: " + Contract[1]
            print "Type: Loan"
            print "Action: " + Contract[4]
            print "Medium: " + str(Contract[2])
            print "Volume: " + str(Contract[3])
            print "Date Entered: " + str(Contract[13])
            ContractFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "DURATION":
    SearchValueInterval = str(SearchValueInterval.upper())
    SearchValueValue = float(SearchValueValue)
    SearchValue = str(SearchValueValue) + " " + SearchValueInterval
    #print "Duration: " + str(SearchValue)
    try:
        sql = """SELECT * FROM LoanBook WHERE Duration = "%s" """ % (SearchValue)
        cursor.execute(sql)
        ContractList = cursor.fetchall()
        for Contract in ContractList:
            if ContractHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                ContractHeaderPrinted = True
            print ""
            print "Contract Number: " + str(Contract[0])
            print "Username: " + Contract[1]
            print "Type: MTC"
            print "Action: " + Contract[4]
            print "Medium: " + str(Contract[2])
            print "Volume: " + str(Contract[3])
            print "Date Entered: " + str(Contract[13])
            ContractFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "DIVIDEND TYPE":
    SearchValue = str(SearchValue.capitalize())
    try:
        sql = """SELECT * FROM LoanBook WHERE DividendType = "%s" """ % (SearchValue)
        cursor.execute(sql)
        ContractList = cursor.fetchall()
        for Contract in ContractList:
            if ContractHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                ContractHeaderPrinted = True
            print ""
            print "Contract Number: " + str(Contract[0])
            print "Username: " + Contract[1]
            print "Type: MTC"
            print "Action: " + Contract[4]
            print "Medium: " + str(Contract[2])
            print "Volume: " + str(Contract[3])
            print "Date Entered: " + str(Contract[13])
            ContractFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "MINIMUM BORROWER CONSTRAINTS":
    SearchValue = int(SearchValue)
    sql = "SELECT * FROM LoanBook WHERE MinimumBorrowerConstraints = %d" % (SearchValue)
    try:
        cursor.execute(sql)
        ContractList = cursor.fetchall()
        for Contract in ContractList:
            if ContractHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                ContractHeaderPrinted = True
            print ""
            print "Contract Number: " + str(Contract[0])
            print "Username: " + Contract[1]
            print "Type: Loan"
            print "Action: " + Contract[4]
            print "Medium: " + str(Contract[2])
            print "Volume: " + str(Contract[3])
            print "Date Entered: " + str(Contract[13])
            ContractFound = True
    except:
        print "ERROR: Database fetch exception"



if SearchParameter == "USER INTERVENTION CONSTRAINTS":
    SearchValue = int(SearchValue)
    sql = "SELECT * FROM LoanBook WHERE UserInterventionConstraints = %d" % (SearchValue)
    try:
        cursor.execute(sql)
        ContractList = cursor.fetchall()
        for Contract in ContractList:
            if ContractHeaderPrinted != True:
                print ""
                print "Contracts that meet search criteria: "
                ContractHeaderPrinted = True
            print ""
            print "Contract Number: " + str(Contract[0])
            print "Username: " + Contract[1]
            print "Type: Loan"
            print "Action: " + Contract[4]
            print "Medium: " + str(Contract[2])
            print "Volume: " + str(Contract[3])
            print "Date Entered: " + str(Contract[13])
            ContractFound = True
    except:
        print "ERROR: Database fetch exception"



#Test SQL Checking After FormattedDate

if SearchParameter == "DATEENTERED" or SearchParameter == "DATE ENTERED":
    try:
        sql = "SELECT * FROM LoanBook"
        cursor.execute(sql)
        ContractList = cursor.fetchall()
        for Contract in ContractList:
            if DateSearchYearOmit == True:
                YearValue = ""
                for Character in str(Contract[13])[:4]:
                    YearValue += str(Character)
                DateSearchYear = YearValue
                
            if DateSearchMonthOmit == True:
                MonthValue = ""
                for Character in str(Contract[13])[5:7]:
                    MonthValue += str(Character)
                DateSearchMonth = MonthValue
                
            if DateSearchDayOmit == True:
                DayValue = ""
                for Character in str(Contract[13])[8:10]:
                    DayValue += str(Character)
                DateSearchDay = DayValue
                
            if DateSearchHourOmit == True:
                HourValue = ""
                for Character in str(Contract[13])[11:13]:
                    HourValue += str(Character)
                DateSearchHour = HourValue
                
            if DateSearchMinuteOmit == True:
                MinuteValue = ""
                for Character in str(Contract[13])[14:16]:
                    MinuteValue += str(Character)
                DateSearchMinute = MinuteValue
            
            if DateSearchSecondOmit == True:
                SecondValue = ""
                for Character in str(Contract[13])[17:19]:
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
            
            if str(DateSearchYear) == str(Contract[13])[:4] and str(DateSearchMonth) == str(Contract[13])[5:7] and str(DateSearchDay) == str(Contract[13])[8:10] and str(DateSearchHour) == str(Contract[13])[11:13] and str(DateSearchMinute) == str(Contract[13])[14:16] and str(DateSearchSecond) == str(Contract[13])[17:19]:
                if ContractHeaderPrinted != True:
                    ContractHeaderPrinted = True
                    print ""
                    print "Orders that meet search parameters:"
                print ""
                print "Contract Number: " + str(Contract[0])
                print "Username: " + Contract[1]
                print "Type: Loan"
                print "Action: " + Contract[4]
                print "Price: " + str(Contract[2])
                print "Volume: " + str(Contract[3])
                print "Date Entered: " + str(Contract[13])
                ContractFound = True
    except:
        print "ERROR: Database fetch exception"



if ContractFound != True:
    print ""
    print "No orders meet search criteria"



db.close()