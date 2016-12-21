#-------------------------------------------------------------------------------
# Name:        DBAddMTC
# Version:     1.0
# Purpose:     
#
# Author:      Matthew
#
# Created:     05/07/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    05/29/2014
#-------------------------------------------------------------------------------



#Enable User Requests
#Enable Credit Checking
#Enable Events



import time
import MySQLdb

db = MySQLdb.connect("localhost","root","***","exchangedatabase")

cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data



'''Setting Required Variables'''



Username = raw_input("Username: ")
Username = Username.capitalize()
UserFound = False
while UserFound != True:
    cursor.execute("""SELECT * FROM UserBook WHERE Username = "%s" """ % (Username))
    UsernameList = cursor.fetchall()
    for User in UsernameList:
        if Username == User[0]:
            print "User found"
            UserFound = True
            break;
    else:
        print "User not found. Please enter again: "
        Username = raw_input("Username: ")
        Username = Username.capitalize()



print ""
OrderAction = raw_input("Action (Loan/Borrow): ")
OrderAction = OrderAction.upper()
while OrderAction != "LOAN" and OrderAction != "BORROW":
    print "Incorrect order action. Please enter again:"
    OrderAction = raw_input("Action (Loan/Borrow): ")
    OrderAction = OrderAction.upper()

OrderType = "MTC"



Price = raw_input("Price: ")
while 1 == 1:
    try:
        Price = float(Price)
        break;
    except:
        print "Price must be an integer. Please enter again: "
        Price = raw_input("Price: ")

Volume = raw_input("Volume: ")
while 1 == 1:
    try:
        Volume = float(Volume)
        break;
    except:
        print "Volume must be an integer. Please enter again: "
        Volume = raw_input("Volume: ")

ContractTotal = Price * Volume
print OrderAction.title() + " Total: " + str(ContractTotal)



InterestCompoundRateValue = raw_input("Interest Compound Rate Value: ")
while 1 == 1:
    try:
        InterestCompoundRateValue = float(InterestCompoundRateValue)
        break;
    except:
        print "Interest Compound Rate must be an integer. Please enter again: "
        InterestCompoundRateValue = raw_input("Interest Compound Rate Value: ")

if InterestCompoundRateValue != 0:
    InterestCompoundRateInterval = raw_input("Interest Compound Rate Interval (Second, Minute, Hour, Day): ")
    InterestCompoundRateInterval = InterestCompoundRateInterval.upper()
    while 1 == 1:
        if InterestCompoundRateInterval != "SECOND" and InterestCompoundRateInterval != "MINUTE" and InterestCompoundRateInterval != "HOUR" and InterestCompoundRateInterval != "DAY":
            print "Interest Compound Rate Interval must be either SECOND, MINUTE, HOUR, or DAY. Please enter again: "
            InterestCompoundRateInterval = raw_input("Interest Compound Rate Interval: ")
            InterestCompoundRateInterval = InterestCompoundRateInterval.upper()
        else:
            break;

    InterestCompoundRate = str(InterestCompoundRateValue) + " " + InterestCompoundRateInterval
    InterestCompoundRateTuple = (InterestCompoundRateValue, InterestCompoundRateInterval)
else:
    InterestCompoundRate = 0

print "Interest Compound Rate: " + str(InterestCompoundRate)



InterestRate = raw_input("Interest Rate: ")
while 1 == 1:
    try:
        InterestRate = float(InterestRate)
        break;
    except:
        print "Interest Rate must be an integer. Please enter again: "
        InterestRate = raw_input("InterestRate: ")



DurationValue = raw_input("Duration Value: ")
while 1 == 1:
    try:
        DurationValue = float(DurationValue)
        if DurationValue == 0:
            print "Duration Value cannot be zero. Please select a positive value:"
            DurationValue = raw_input("Duration Value: ")
        else:
            break;
    except:
        print "Duration Value must be an integer. Please enter again: "
        DurationValue = raw_input("Duration Value: ")

DurationInterval = raw_input("Duration Interval (Second, Minute, Hour, Day): ")
DurationInterval = DurationInterval.upper()
while 1 == 1:
    if DurationInterval != "SECOND" and DurationInterval != "MINUTE" and DurationInterval != "HOUR" and DurationInterval != "DAY":
        print "Duration Interval must be either SECOND, MINUTE, HOUR, or DAY. Please enter again: "
        DurationInterval = raw_input("Duration Interval: ")
        DurationInterval = DurationInterval.upper()
    else:
        break;

Duration = str(DurationValue) + " " + DurationInterval
DurationTuple = (DurationValue, DurationInterval)
print "Duration: " + str(Duration)
print "Duration Tuple: " + str(DurationTuple)



LocalTime = time.localtime(time.time())

LocalTimeYears = int(LocalTime[0])
LocalTimeMonths = int(LocalTime[1])
LocalTimeDays = int(LocalTime[2])
LocalTimeHours = int(LocalTime[3])
LocalTimeMinutes = int(LocalTime[4])
LocalTimeSeconds = int(LocalTime[5])

if DurationTuple[1] == "SECOND":
    LocalTimeSeconds = int(int(LocalTimeSeconds) + DurationTuple[0])
elif DurationTuple[1] == "MINUTE":
    LocalTimeMinutes = int(int(LocalTimeMinutes) + DurationTuple[0])
elif DurationTuple[1] == "HOUR":
    LocalTimeHours = int(int(LocalTimeHours) + DurationTuple[0])
elif DurationTuple[1] == "DAY":
    LocalTimeDays = int(int(LocalTimeDays) + DurationTuple[0])

if LocalTimeSeconds > 60:
    #print ""
    #print "Initial Seconds: " + str(LocalTimeSeconds)
    LocalTimeSecondsRemainder = (LocalTimeSeconds % 60)
    #print "Seconds Remainder (Final Seconds): " + str(LocalTimeSecondsRemainder)
    LocalTimeSecondsCarry = int(round(LocalTimeSeconds / 60))
    #print "Seconds Carry: " + str(LocalTimeSecondsCarry)
    #print "Initial Minutes: " + str(LocalTimeMinutes)
    LocalTimeMinutes += LocalTimeSecondsCarry
    #print "Final Minutes: " + str(LocalTimeMinutes)
    LocalTimeSeconds = LocalTimeSecondsRemainder

if LocalTimeMinutes > 60:
    #print ""
    #print "Initial Minutes: " + str(LocalTimeMinutes)
    LocalTimeMinutesRemainder = (LocalTimeMinutes % 60)
    #print "Minutes Remainder (Final Minutes): " + str(LocalTimeMinutesRemainder)
    LocalTimeMinutesCarry = int(round(LocalTimeMinutes / 60))
    #print "Minutes Carry: " + str(LocalTimeMinutesCarry)
    #print "Initial Hours: " + str(LocalTimeHours)
    LocalTimeHours += LocalTimeMinutesCarry
    #print "Final Hours: " + str(LocalTimeHours)
    LocalTimeMinutes = LocalTimeMinutesRemainder

if LocalTimeHours > 24:
    #print ""
    #print "Initial Hours: " + str(LocalTimeHours)
    LocalTimeHoursRemainder = (LocalTimeHours % 24)
    #print "Hours Remainder (Final Hours): " + str(LocalTimeHoursRemainder)
    LocalTimeHoursCarry = int(round(LocalTimeHours / 24))
    #print "Hours Carry: " + str(LocalTimeHoursCarry)
    #print "Initial Days: " + str(LocalTimeDays)
    LocalTimeDays += LocalTimeHoursCarry
    #print "Final Days: " + str(LocalTimeDays)
    LocalTimeHours = LocalTimeHoursRemainder

while 1 == 1:

    if LocalTimeMonths == 1 or LocalTimeMonths == 3 or LocalTimeMonths == 5 or LocalTimeMonths == 7 or LocalTimeMonths == 8 or LocalTimeMonths == 10 or LocalTimeMonths == 12:
        DaysCeiling = 31
    elif LocalTimeMonths == 4 or LocalTimeMonths == 6 or LocalTimeMonths == 9 or LocalTimeMonths == 11:
        DaysCeiling = 30
    else:
        DaysCeiling = 28
    
    #print ""
    #print "Month: " + str(LocalTimeMonths)
    #print "Days Ceiling: " + str(DaysCeiling)
    
    if LocalTimeDays > DaysCeiling:
        #print ""
        #print "Initial Days: " + str(LocalTimeDays)
        LocalTimeDaysRemainder = LocalTimeDays - DaysCeiling
        #print "Days Remainder (Final Days): " + str(LocalTimeDaysRemainder)
        LocalTimeDaysCarry = 1
        #print "Days Carry (Months Add): " + str(LocalTimeDaysCarry)
        #print "Initial Months: " + str(LocalTimeMonths)
        LocalTimeMonths += LocalTimeDaysCarry
        #print "Final Months: " + str(LocalTimeMonths)
        LocalTimeDays = LocalTimeDaysRemainder
    else:
        break;
        
    if LocalTimeMonths > 12:
        #print ""
        #print "Initial Months: " + str(LocalTimeMonths)
        LocalTimeMonthsRemainder = (LocalTimeMonths % 12)
        #print "Months Remainder (Final Months): " + str(LocalTimeMonthsRemainder)
        LocalTimeMonthsCarry = int(round(LocalTimeMonths / 12))
        #print "Months Carry (Years Add): " + str(LocalTimeMonthsCarry)
        #print "Initial Years: " + str(LocalTimeYears)
        LocalTimeYears += LocalTimeMonthsCarry
        #print "Final Years: " + str(LocalTimeYears)
        LocalTimeMonths = LocalTimeMonthsRemainder

FormattedDatabaseDurationDate = str(LocalTimeYears) + "-" +  str(LocalTimeMonths) + "-" +  str(LocalTimeDays)
FormattedDurationDate = str(LocalTimeMonths) + "/" +  str(LocalTimeDays) + "/" +  str(LocalTimeHours)
FormattedDurationTime = str(LocalTimeHours) + ":" +  str(LocalTimeMinutes) + ":" +  str(LocalTimeSeconds)
FormattedDurationDateTime = str(FormattedDatabaseDurationDate) + " " + str(FormattedDurationTime)

print "Formatted Duration Date Time: " + FormattedDurationDateTime



DividendType = raw_input("Dividend Type(Flat/Percent): ")
DividendType = DividendType.upper()
while DividendType != "FLAT" and DividendType != "PERCENT":
    print "Incorrect dividend type. Please enter again:"
    DividendType = raw_input("Dividend Type(Flat/Percent): ")
    DividendType = DividendType.upper()



Comment = raw_input("Administrative Comment: ")



'''Setting Optional Variables: Barrier Prices'''


StopLossPricePresent = False
StopLossPrice = raw_input("Stop Loss Price: ")
while 1 == 1:
    if StopLossPrice == "":
        break;
    try:
        StopLossPrice = float(StopLossPrice)
        StopLossPricePresent = True
        break;
    except:
        print "Stop Loss Price must be an integer. Please enter again: "
        StopLossPrice = raw_input("Stop Loss Price: ")

FulfillmentPricePresent = False
FulfillmentPrice = raw_input("Fulfillment Price: ")
while 1 == 1:
    if FulfillmentPrice == "":
        break;
    try:
        FulfillmentPrice = float(FulfillmentPrice)
        FulfillmentPricePresent = True
        break;
    except:
        print "Fulfillment Price must be an integer. Please enter again: "
        FulfillmentPrice = raw_input("Fulfillment Price: ")



'''Setting Optional Variables: Constraints'''



MinimumBorrowerConstraintPresent = raw_input("Minimum Borrower Constraint (Yes/No):")
MinimumBorrowerConstraintPresent = MinimumBorrowerConstraintPresent.upper()
while 1 == 1:
    if MinimumBorrowerConstraintPresent == "YES":
        MinimumBorrowerConstraintPresent = True
        break;
    elif MinimumBorrowerConstraintPresent == "NO":
        MinimumBorrowerConstraintPresent = False
        break;
    else:
        print "You must choose an answer. Please enter again: "
        MinimumBorrowerConstraintPresent = raw_input("Minimum Borrower Constraint (Yes/No):")
        MinimumBorrowerConstraintPresent = MinimumBorrowerConstraintPresent.upper()

if MinimumBorrowerConstraintPresent == True:
    MinimumBorrowerConstraintType = raw_input("Minimum Borrower Constraint Type (Account Balance, Volume, Contracts, Transactions, Liquidity Value): ")
    MinimumBorrowerConstraintType = MinimumBorrowerConstraintType.upper()
    while 1 == 1:
        if MinimumBorrowerConstraintType == "":
            print "Minimum Borrower Constraint Failed"
            MinimumBorrowerConstraintPresent = False
            break;
        if MinimumBorrowerConstraintType != "ACCOUNT BALANCE" and MinimumBorrowerConstraintType != "ACCOUNTBALANCE" and MinimumBorrowerConstraintType != "VOLUME" and MinimumBorrowerConstraintType != "CONTRACTS" and MinimumBorrowerConstraintType != "TRANSACTIONS" and MinimumBorrowerConstraintType != "LIQUIDITY VALUE" and MinimumBorrowerConstraintType != "LIQUIDITYVALUE":
            print "Incorrect Minimum Borrower Constraint Type. Please enter again:"
            MinimumBorrowerConstraintType = raw_input("Minimum Borrower Constraint Type (Account Balance, Volume, Contracts, Transactions, Liquidity Value): ")
            MinimumBorrowerConstraintType = MinimumBorrowerConstraintType.upper()
        else:
            MinimumBorrowerConstraintPresent = True
            break;

if MinimumBorrowerConstraintPresent == True:    
    MinimumBorrowerConstraintValue = raw_input("Minimum Borrower Constraint Value: ")
    while 1 == 1:
        if MinimumBorrowerConstraintValue == "":
            print "Minimum Borrower Constraint Failed"
            MinimumBorrowerConstraintPresent = False
            break;
        try:
            MinimumBorrowerConstraintValue = float(MinimumBorrowerConstraintValue)
            MinimumBorrowerConstraintPresent = True
            break;
        except:
            print "Minimum Borrower Constraint Type must be a rational number. Please enter again:"
            MinimumBorrowerConstraintValue = raw_input("Minimum Borrower Constraint Value: ")



UserInterventionConstraintPresent = raw_input("User Intervention Constraint (Yes/No):")
UserInterventionConstraintPresent = UserInterventionConstraintPresent.upper()
while 1 == 1:
    if UserInterventionConstraintPresent == "YES":
        UserInterventionConstraintPresent = True
        break;
    elif UserInterventionConstraintPresent == "NO":
        UserInterventionConstraintPresent = False
        break;
    else:
        print "You must choose an answer. Please enter again: "
        UserInterventionConstraintPresent = raw_input("Minimum Borrower Constraint (Yes/No):")
        UserInterventionConstraintPresent = UserInterventionConstraintPresent.upper()

if UserInterventionConstraintPresent == True:
    UserInterventionConstraintType = raw_input("Minimum Borrower Constraint Type (Market Price, Profit Margin, Interest Rate: ")
    UserInterventionConstraintType = UserInterventionConstraintType.upper()
    while 1 == 1:
        if UserInterventionConstraintType == "":
            print "Minimum Borrower Constraint Failed"
            UserInterventionConstraintPresent = False
            break;
        if UserInterventionConstraintType != "MARKET PRICE" and UserInterventionConstraintType != "MARKETPRICE" and UserInterventionConstraintType != "PROFIT MARGIN" and UserInterventionConstraintType != "PROFITMARGIN" and UserInterventionConstraintType != "INTEREST RATE" and UserInterventionConstraintType != "INTERESTRATE":
            print "Incorrect Minimum Borrower Constraint Type. Please enter again:"
            UserInterventionConstraintType = raw_input("Minimum Borrower Constraint Type (Market Price, Profit Margin, Interest Rate): ")
            UserInterventionConstraintType = UserInterventionConstraintType.upper()
        else:
            UserInterventionConstraintPresent = True
            break;

if UserInterventionConstraintPresent == True:    
    UserInterventionConstraintValue = raw_input("Minimum Borrower Constraint Value: ")
    while 1 == 1:
        if UserInterventionConstraintValue == "":
            print "Minimum Borrower Constraint Failed"
            UserInterventionConstraintPresent = False
            break;
        try:
            UserInterventionConstraintValue = float(UserInterventionConstraintValue)
            UserInterventionConstraintPresent = True
            break;
        except:
            print "Minimum Borrower Constraint Type must be a rational number. Please enter again:"
            UserInterventionConstraintValue = raw_input("Minimum Borrower Constraint Value: ")



'''Defining/Executing SQL Statements'''

'''
#Testing Variables:

Username = "***333"
OrderType = "MTC"
OrderAction = "Loan"
Price = 200
Volume = 2
InterestCompoundRate = "4 DAY"
InterestRate = .0002
Duration = "10 DAY"
FormattedDurationDateTime = "2014-5-19 21:31:56"
DividendType = "Flat"
Comment = "Adding MTC"
'''

print ""

cursor.execute("""INSERT INTO IDBook(Type, Action) VALUES("%s", "%s")""" % (OrderType, OrderAction.capitalize()))
cursor.execute("""INSERT INTO MTCBook(Username, Price, Volume, Action, InterestCompoundRate, InterestRate, Duration, EndPoint, DividendType) VALUES("%s", %f, %f, "%s", "%s", %f, "%s", "%s", "%s")""" % (Username, Price, Volume, OrderAction.title(), InterestCompoundRate, InterestRate, Duration, FormattedDurationDateTime, DividendType.title()))
db.commit()
print ""
print "Order Successfully Added"
try:
    cursor.execute("""SELECT * FROM MTCBook ORDER BY MTCNumber DESC LIMIT 1""")
    LatestContracts = cursor.fetchall()
    for Contract in LatestContracts:
        print Contract
        print ""
        print "Order Added:"
        print ""
        MTCNumber = Contract[0]
        Username = Contract[1]
        Price = Contract[2]
        Volume = Contract[3]
        OrderAction = Contract[4]
        DateEntered = Contract[15]
        print "Order Number: " + str(MTCNumber)
        print "Type: " + str(OrderType)
        print "Action: " + str(OrderAction)
        print "Username: " + str(Username)
        print "Price: " + str(Price)
        print "Volume: " + str(Volume)
        print "Date Entered: " + str(DateEntered)
        break;
except:
    db.rollback()
    print "ERROR: Database Insert Failure"



if MinimumBorrowerConstraintPresent == True:
    if MinimumBorrowerConstraintType == "ACCOUNTBALANCE":
        MinimumBorrowerConstraintType = "ACCOUNT BALANCE"
    elif MinimumBorrowerConstraintType == "LIQUIDITYVALUE":
        MinimumBorrowerConstraintType = "LIQUIDITY VALUE"
    #print ""
    cursor.execute("""SELECT * FROM BorrowerConstraintBook WHERE ContractNumber = %s""" % (MTCNumber))
    BorrowerConstraintBookConstraints = cursor.fetchall()
    #print BorrowerConstraintBookConstraints
    if BorrowerConstraintBookConstraints == ():
        ConstraintID = str(MTCNumber) + "-1"
    else:
        OldConstraintNumber = 0
        for Constraint in BorrowerConstraintBookConstraints:
            #print ""
            #print "Previous Constraint: " + str(Constraint[0])
            ConstraintCutOff = len(str(MTCNumber)) + 1
            #print "Constraint Cut-Off: " + str(ConstraintCutOff)
            ConstraintNumber = str(Constraint[0])[ConstraintCutOff:]
            #print "Constraint Number: " + str(ConstraintNumber)
            #print "Old Constraint Number: " + str(OldConstraintNumber)
            if int(ConstraintNumber) > int(OldConstraintNumber):
                #print "Constraint Number: " + str(ConstraintNumber)
                #print "Old Constraint Number: " + str(OldConstraintNumber)
                ConstraintID = (str(MTCNumber) + "-" + str(int(ConstraintNumber) + 1))
                #print "Constraint ID: " + str(ConstraintID)
                OldConstraintNumber = ConstraintNumber
                #print "Old Constraint Number: " + str(OldConstraintNumber)
    print ""
    try:
        cursor.execute("""INSERT INTO BorrowerConstraintBook(ConstraintID, ContractNumber, Username, Type, Value) VALUES("%s", %d, "%s", "%s", %f)""" % (ConstraintID, MTCNumber, Username, MinimumBorrowerConstraintType.title(), MinimumBorrowerConstraintValue))
        cursor.execute("""INSERT INTO BorrowerConstraintLog(ConstraintID, ContractNumber, Username, Type, Value) VALUES("%s", %d, "%s", "%s", %f)""" % (ConstraintID, MTCNumber, Username, MinimumBorrowerConstraintType.title(), MinimumBorrowerConstraintValue))
        db.commit()
        print "Minimum Borrower Constraint Successfully Added"
    except:
        print "ERROR: Minimum Borrower Constraint Unsuccessfully Added"
    
    cursor.execute("""UPDATE MTCBook SET MinimumBorrowerConstraints = (MinimumBorrowerConstraints + 1) WHERE MTCNumber = %s""" % (MTCNumber))
    cursor.execute("""UPDATE MTCLog SET MinimumBorrowerConstraints = (MinimumBorrowerConstraints + 1) WHERE MTCNumber = %s""" % (MTCNumber))
    db.commit()


if UserInterventionConstraintPresent == True:
    if UserInterventionConstraintType == "MARKETPRICE":
        UserInterventionConstraintType = "MARKET PRICE"
    elif UserInterventionConstraintType == "PROFITMARGIN":
        UserInterventionConstraintType = "PROFIT MARGIN"
    elif UserInterventionConstraintType == "INTERESTRATE":
        UserInterventionConstraintType = "INTEREST RATE"
    #print ""
    cursor.execute("""SELECT * FROM InterventionConstraintBook WHERE ContractNumber = %s""" % (MTCNumber))
    InterventionConstraintBookConstraints = cursor.fetchall()
    #print InterventionConstraintBookConstraints
    if InterventionConstraintBookConstraints == ():
        ConstraintID = str(MTCNumber) + "-1"
    else:
        OldConstraintNumber = 0
        for Constraint in InterventionConstraintBookConstraints:
            #print ""
            #print "Previous Constraint: " + str(Constraint[0])
            ConstraintCutOff = len(str(MTCNumber)) + 1
            #print "Constraint Cut-Off: " + str(ConstraintCutOff)
            ConstraintNumber = str(Constraint[0])[ConstraintCutOff:]
            #print "Constraint Number: " + str(ConstraintNumber)
            #print "Old Constraint Number: " + str(OldConstraintNumber)
            if int(ConstraintNumber) > int(OldConstraintNumber):
                #print "Constraint Number: " + str(ConstraintNumber)
                #print "Old Constraint Number: " + str(OldConstraintNumber)
                ConstraintID = (str(MTCNumber) + "-" + str(int(ConstraintNumber) + 1))
                #print "Constraint ID: " + str(ConstraintID)
                OldConstraintNumber = ConstraintNumber
                #print "Old Constraint Number: " + str(OldConstraintNumber)
    print ""
    try:
        cursor.execute("""INSERT INTO InterventionConstraintBook(ConstraintID, ContractNumber, Username, Type, Value) VALUES("%s", %d, "%s", "%s", %f)""" % (ConstraintID, MTCNumber, Username, UserInterventionConstraintType.title(), UserInterventionConstraintValue))
        cursor.execute("""INSERT INTO InterventionConstraintLog(ConstraintID, ContractNumber, Username, Type, Value) VALUES("%s", %d, "%s", "%s", %f)""" % (ConstraintID, MTCNumber, Username, UserInterventionConstraintType.title(), UserInterventionConstraintValue))
        db.commit()
        print "User Intervention Constraint Successfully Added"
    except:
        print "ERROR: User Intervention Constraint Unsuccessfully Added"
    
    cursor.execute("""UPDATE MTCBook SET UserInterventionConstraints = (UserInterventionConstraints + 1) WHERE MTCNumber = %s""" % (MTCNumber))
    cursor.execute("""UPDATE MTCLog SET UserInterventionConstraints = (UserInterventionConstraints + 1) WHERE MTCNumber = %s""" % (MTCNumber))
    db.commit()



'''Logging Order'''



try:
    cursor.execute("""INSERT INTO MTCLog(MTCNumber, Username, Price, Volume, Action, InterestCompoundRate, InterestRate, Duration, EndPoint, DividendType) VALUES(%d, "%s", %f, %f, "%s", "%s", %f, "%s", "%s", "%s")""" % (MTCNumber, Username, Price, Volume, OrderAction.title(), InterestCompoundRate, InterestRate, Duration, FormattedDurationDateTime, DividendType.title()))
    db.commit()
    print ""
    print "MTC Successfully Logged"
except:
    print "ERROR: Database Log Insert Failure"



'''Adding Barrier Prices'''



if StopLossPricePresent == True:
    try:
        cursor.execute("""UPDATE MTCBook SET StopLossPrice = %f WHERE MTCNumber = %d""" % (StopLossPrice, MTCNumber))
        cursor.execute("""UPDATE MTCLog SET StopLossPrice = %f WHERE MTCNumber = %d""" % (StopLossPrice, MTCNumber))
        print ""
        print "Stop Loss Price Updated"
        db.commit()
    except:
        print "ERROR: StopLossPrice Not Updated"

if FulfillmentPricePresent == True:
    try:
        cursor.execute("""UPDATE MTCBook SET FulfillmentPrice = %f WHERE MTCNumber = %d""" % (FulfillmentPrice, MTCNumber))
        cursor.execute("""UPDATE MTCLog SET FulfillmentPrice = %f WHERE MTCNumber = %d""" % (FulfillmentPrice, MTCNumber))
        print ""
        print "Fulfillment Price Updated"
        db.commit()
    except:
        print "ERROR: FulfillmentPrice Not Updated"



'''Logging Control'''
    


Employee = "***333"

MTCID = "MTC " + str(MTCNumber)

try:
    print ""
    cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Add MTC", MTCID, "All", Comment))
    db.commit()
    print "Control Successfully Logged"
except:
    print "ERROR: Control Unsuccessfully Logged"



db.close()