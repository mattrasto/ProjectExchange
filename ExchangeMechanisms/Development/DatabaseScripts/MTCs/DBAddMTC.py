#-------------------------------------------------------------------------------
# Name:        DBAddMTC
# Version:     3.0
# Purpose:     Adds MTC with specified attributes to specified user
#
# Author:      Matthew
#
# Created:     05/07/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    10/05/2014
#-------------------------------------------------------------------------------

#Remove funds once MTC is added
#Check if loan amount is below account balance
#Check time inputs for InterestCompoundRate and Duration

import sys
import time
import MySQLdb
import datetime



def main(Username, Price, Volume, OrderAction, InterestCompoundRate, InterestRate, StopLossPrice, FulfillmentPrice, Duration, DividendType, MinimumBorrowerConstraintType, MinimumBorrowerConstraintValue, UserInterventionConstraintType, UserInterventionConstraintValue):
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    
    
    '''Verifies Balances'''
    
    
    
    #Checks if order exists
    cursor.execute("""SELECT * FROM UserBook WHERE Username = "%s" """ % (Username))
    UserDetails = cursor.fetchone()
    #Exits if order is not found
    if UserDetails == None:
        print ""
        print "CRITICAL ERROR: User not found"
        sys.exit()
    AccountBalance = UserDetails[3]
    AccountVolume = UserDetails[4]
    
    #Checks for negative balances and exits if found
    if (AccountBalance < 0) or (AccountVolume < 0):
        print ""
        print "CRITICAL ERROR: User has negative balance"
        print "Exiting..."
        sys.exit()
    
    
    
    '''Checking StopLossPrice/FulfillmentPrice Validity'''
    
    
    
    if (StopLossPrice != "") and (Price < StopLossPrice):
        print "CRITICAL ERROR: MTC Price is less than StopLossPrice. It will be automatically canceled."
        sys.exit()
    elif (FulfillmentPrice != "") and Price > FulfillmentPrice:
        print "CRITICAL ERROR: MTC Price is greater than FulfillmentPrice. It will be automatically canceled."
        sys.exit()
    
    
    
    '''Creating MTC'''
    
    
    
    #Sets order type
    OrderType = "MTC"
    
    #Inserts record into IDBook
    cursor.execute("""INSERT INTO IDBook(Type, Action) VALUES("%s", "%s")""" % (OrderType, OrderAction.capitalize()))
    #Inserts MTC into MTCBook
    cursor.execute("""INSERT INTO MTCBook(Username, Price, Volume, Action, InterestCompoundRate, InterestRate, Duration, DividendType) VALUES("%s", %f, %f, "%s", "%s", %f, "%s", "%s")""" % (Username, Price, Volume, OrderAction.title(), InterestCompoundRate, InterestRate, Duration, DividendType.title()))
    db.commit()
    print ""
    print "Order Successfully Added"
    try:
        #Gathers and reads MTC details
        cursor.execute("""SELECT * FROM MTCBook ORDER BY MTCNumber DESC LIMIT 1""")
        LatestContracts = cursor.fetchall()
        for Contract in LatestContracts:
            print ""
            print "Order Added:"
            print ""
            MTCNumber = Contract[0]
            Username = Contract[1]
            Price = Contract[2]
            Volume = Contract[3]
            OrderAction = Contract[4]
            DateEntered = Contract[14]
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
    
    
    
    '''Logging MTC'''
    
    
    
    #Inserts record into MTCLog
    try:
        cursor.execute("""INSERT INTO MTCLog(MTCNumber, Username, Price, Volume, Action, InterestCompoundRate, InterestRate, Duration, DividendType) VALUES(%d, "%s", %f, %f, "%s", "%s", %f, "%s", "%s")""" % (MTCNumber, Username, Price, Volume, OrderAction.title(), InterestCompoundRate, InterestRate, Duration, DividendType.title()))
        db.commit()
        print ""
        print "MTC Successfully Logged"
    except:
        print "ERROR: Database Log Insert Failure"
    
    
    
    '''Adding Minimum Borrower Constraint'''
    
    
    
    #Gathers current highest ConstraintID from log and adds one
    #NOTE: Since ConstraintID is in format "[ContractNumber]-[ConstraintNumber]", the ID must be converted to string,
    #cut off after the dash, then the ConstraintNumber must be calculated and appended to the ID again
    
    if MinimumBorrowerConstraintType != None and MinimumBorrowerConstraintValue != None:
        cursor.execute("""SELECT * FROM BorrowerConstraintBook WHERE ContractNumber = %s""" % (MTCNumber))
        BorrowerConstraintBookConstraints = cursor.fetchall()
        #If no current constraints exists, sets ID to "[ContractNumber]-1"
        if BorrowerConstraintBookConstraints == ():
            ConstraintID = str(MTCNumber) + "-1"
        else:
            
            #Iterates through each ConstraintID, changing OldConstraintNumber to reflect ConstraintNumber that was just compared,
            #then compares those values with newly assigned ConstraintID again until loop is finished
            #NOTE: This allows for skips in the log due to error, whereas counting the number of constraints and appending would not
            
            OldConstraintNumber = 0
            #Gathers ConstraintNumber from each constraint
            for Constraint in BorrowerConstraintBookConstraints:
                ConstraintCutOff = len(str(MTCNumber)) + 1
                ConstraintNumber = str(Constraint[0])[ConstraintCutOff:]
                #If new ConstraintNumber is greater than the iterated ConstraintNumber, creates new ConstraintID with +1 added to ConstraintNumber
                if int(ConstraintNumber) > int(OldConstraintNumber):
                    ConstraintID = (str(MTCNumber) + "-" + str(int(ConstraintNumber) + 1))
                    OldConstraintNumber = ConstraintNumber
        
        
        
        #Inserts constraint into BorrowerConstraintBook and record into BorrowerConstraintLog
        try:
            print ""
            cursor.execute("""INSERT INTO BorrowerConstraintBook(ConstraintID, ContractNumber, Username, Type, Value) VALUES("%s", %d, "%s", "%s", %f)""" % (ConstraintID, MTCNumber, Username, MinimumBorrowerConstraintType.title(), MinimumBorrowerConstraintValue))
            cursor.execute("""INSERT INTO BorrowerConstraintLog(ConstraintID, ContractNumber, Username, Type, Value) VALUES("%s", %d, "%s", "%s", %f)""" % (ConstraintID, MTCNumber, Username, MinimumBorrowerConstraintType.title(), MinimumBorrowerConstraintValue))
            db.commit()
            print "Minimum Borrower Constraint Successfully Added"
        except:
            print "ERROR: Minimum Borrower Constraint Unsuccessfully Added"
        
        #Updates MTCBook and MTCLog to reflect update of constraint amount
        try:
            cursor.execute("""UPDATE MTCBook SET MinimumBorrowerConstraints = (MinimumBorrowerConstraints + 1) WHERE MTCNumber = %s""" % (MTCNumber))
            cursor.execute("""UPDATE MTCLog SET MinimumBorrowerConstraints = (MinimumBorrowerConstraints + 1) WHERE MTCNumber = %s""" % (MTCNumber))
            db.commit()
        except:
            print "ERROR: User Intervention Constraint Count Unsuccessfully Updated"
    
    
    
    '''Adding User Intervention Constraint'''
    
    
    
    if UserInterventionConstraintType != None and UserInterventionConstraintValue != None:
        cursor.execute("""SELECT * FROM InterventionConstraintBook WHERE ContractNumber = %s""" % (MTCNumber))
        InterventionConstraintBookConstraints = cursor.fetchall()
        #If no current constraints exists, sets ID to "[ContractNumber]-1"
        if InterventionConstraintBookConstraints == ():
            ConstraintID = str(MTCNumber) + "-1"
        else:
            
            #Iterates through each ConstraintID, changing OldConstraintNumber to reflect ConstraintNumber that was just compared,
            #then compares those values with newly assigned ConstraintID again until loop is finished
            #NOTE: This allows for skips in the log due to error, whereas counting the number of constraints and appending would not
            
            OldConstraintNumber = 0
            #Gathers ConstraintNumber from each constraint
            for Constraint in InterventionConstraintBookConstraints:
                ConstraintCutOff = len(str(MTCNumber)) + 1
                ConstraintNumber = str(Constraint[0])[ConstraintCutOff:]
                #If new ConstraintNumber is greater than the iterated ConstraintNumber, creates new ConstraintID with +1 added to ConstraintNumber
                if int(ConstraintNumber) > int(OldConstraintNumber):
                    ConstraintID = (str(MTCNumber) + "-" + str(int(ConstraintNumber) + 1))
                    OldConstraintNumber = ConstraintNumber
        
        
        
        #Inserts constraint into InterventionConstraintBook and record into InterventionConstraintLog
        try:
            print ""
            #Inserts constraint into InterventionConstraintBook
            cursor.execute("""INSERT INTO InterventionConstraintBook(ConstraintID, ContractNumber, Username, Type, Value) VALUES("%s", %d, "%s", "%s", %f)""" % (ConstraintID, MTCNumber, Username, UserInterventionConstraintType.title(), UserInterventionConstraintValue))
            #Inserts record into InterventionConstraintLog
            cursor.execute("""INSERT INTO InterventionConstraintLog(ConstraintID, ContractNumber, Username, Type, Value) VALUES("%s", %d, "%s", "%s", %f)""" % (ConstraintID, MTCNumber, Username, UserInterventionConstraintType.title(), UserInterventionConstraintValue))
            db.commit()
            print "User Intervention Constraint Successfully Added"
        except:
            print "ERROR: User Intervention Constraint Unsuccessfully Added"
        
        #Updates LoanBook and LoanLog to reflect update of constraint amount
        try:
            cursor.execute("""UPDATE MTCBook SET UserInterventionConstraints = (UserInterventionConstraints + 1) WHERE MTCNumber = %s""" % (MTCNumber))
            cursor.execute("""UPDATE MTCLog SET UserInterventionConstraints = (UserInterventionConstraints + 1) WHERE MTCNumber = %s""" % (MTCNumber))
            db.commit()
        except:
            print "ERROR: User Intervention Constraint Count Unsuccessfully Updated"
    
    
    
    '''Adding Barrier Prices'''
    
    
    
    #Updates MTCBook and MTCLog to show StopLossPrice if one exists
    if StopLossPrice != "":
        try:
            cursor.execute("""UPDATE MTCBook SET StopLossPrice = %f WHERE MTCNumber = %d""" % (StopLossPrice, MTCNumber))
            cursor.execute("""UPDATE MTCLog SET StopLossPrice = %f WHERE MTCNumber = %d""" % (StopLossPrice, MTCNumber))
            print ""
            print "Stop Loss Price Updated"
            db.commit()
        except:
            print "ERROR: StopLossPrice Not Updated"
    
    #Updates MTCBook and MTCLog to show FulfillmentPrice if one exists
    if FulfillmentPrice != "":
        try:
            cursor.execute("""UPDATE MTCBook SET FulfillmentPrice = %f WHERE MTCNumber = %d""" % (FulfillmentPrice, MTCNumber))
            cursor.execute("""UPDATE MTCLog SET FulfillmentPrice = %f WHERE MTCNumber = %d""" % (FulfillmentPrice, MTCNumber))
            print ""
            print "Fulfillment Price Updated"
            db.commit()
        except:
            print "ERROR: FulfillmentPrice Not Updated"
    
    
    
    '''Logging Control'''
    
    
    
    #Assigns static variables for logging control
    #Note: "Employee" value changes based on user submitting manual control
    Employee = "***333"
    MTCID = "MTC " + str(MTCNumber)
    Comment = "Added MTC"
    
    #Inserts record of action into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Add MTC", MTCID, "All", Comment))
        db.commit()
        print "Control Successfully Logged"
    except:
        print "ERROR: Control Unsuccessfully Logged"
    
    
    
    db.close()



if __name__ == "__main__":
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    
    
    '''Setting Required Variables'''
    
    
    
    #Determines user to put MTC under, and checks to see if user exists
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
    
    
    
    #Determines action of MTC
    print ""
    OrderAction = raw_input("Action (Loan/Borrow): ")
    OrderAction = OrderAction.upper()
    while OrderAction != "LOAN" and OrderAction != "BORROW":
        print "Incorrect order action. Please enter again:"
        OrderAction = raw_input("Action (Loan/Borrow): ")
        OrderAction = OrderAction.upper()

    
    
    #Determines price of MTC
    Price = raw_input("Price: ")
    while 1 == 1:
        try:
            Price = float(Price)
            break;
        except:
            print "Price must be an integer. Please enter again: "
            Price = raw_input("Price: ")
    
    
    
    #Determines volume of MTC
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
    
    
    
    #Determines value of rate at which MTC interest is compounded
    InterestCompoundRateValue = raw_input("Interest Compound Rate Value: ")
    while 1 == 1:
        try:
            InterestCompoundRateValue = float(InterestCompoundRateValue)
            break;
        except:
            print "Interest Compound Rate must be an integer. Please enter again: "
            InterestCompoundRateValue = raw_input("Interest Compound Rate Value: ")
    
    
    
    #Determines interval of rate at which MTC interest is compounded
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
    
    if InterestCompoundRateInterval == "SECOND":
        InterestCompoundRate = "00:00:%d" % (InterestCompoundRateValue)
    elif InterestCompoundRateInterval == "MINUTE":
        InterestCompoundRate = "00:%d:00" % (InterestCompoundRateValue)
    elif InterestCompoundRateInterval == "HOUR":
        InterestCompoundRate = "%d:00:00" % (InterestCompoundRateValue)
    elif InterestCompoundRateInterval == "DAY":
        InterestCompoundRateValue = InterestCompoundRateValue * 24
        InterestCompoundRate = "%d:00:00" % (InterestCompoundRateValue)
    print "InterestCompoundRate: " + str(InterestCompoundRate)
    
    
    
    #Determines interest rate of MTC
    InterestRate = raw_input("Interest Rate: ")
    while 1 == 1:
        try:
            InterestRate = float(InterestRate)
            break;
        except:
            print "Interest Rate must be an integer. Please enter again: "
            InterestRate = raw_input("InterestRate: ")
    
    
    
    #Determines value for the duration of the MTC
    DurationValue = raw_input("Duration Value: ")
    while 1 == 1:
        try:
            DurationValue = int(DurationValue)
            if DurationValue == 0:
                print "Duration Value cannot be zero. Please select a positive value:"
                DurationValue = raw_input("Duration Value: ")
            else:
                break;
        except:
            print "Duration Value must be an integer. Please enter again: "
            DurationValue = raw_input("Duration Value: ")
    
    
    
    #Determines interval for the duration of the MTC
    DurationInterval = raw_input("Duration Interval (Second, Minute, Hour, Day): ")
    DurationInterval = DurationInterval.upper()
    while 1 == 1:
        if DurationInterval != "SECOND" and DurationInterval != "MINUTE" and DurationInterval != "HOUR" and DurationInterval != "DAY":
            print "Duration Interval must be either SECOND, MINUTE, HOUR, or DAY. Please enter again: "
            DurationInterval = raw_input("Duration Interval: ")
            DurationInterval = DurationInterval.upper()
        else:
            break;
    
    
    
    if DurationInterval == "SECOND":
        Duration = "00:00:%d" % (DurationValue)
    elif DurationInterval == "MINUTE":
        Duration = "00:%d:00" % (DurationValue)
    elif DurationInterval == "HOUR":
        Duration = "%d:00:00" % (DurationValue)
    elif DurationInterval == "DAY":
        DurationValue = DurationValue * 24
        Duration = "%d:00:00" % (DurationValue)
    print "Duration: " + str(Duration)
    
    
    
    #Determines dividend type of MTC
    DividendType = raw_input("Dividend Type (Flat/Percent): ")
    DividendType = DividendType.upper()
    while DividendType != "FLAT" and DividendType != "PERCENT":
        print "Incorrect dividend type. Please enter again:"
        DividendType = raw_input("Dividend Type (Flat/Percent): ")
        DividendType = DividendType.upper()
    
    
    
    '''Setting Optional Variables: Barrier Prices'''
    
    
    
    #Determines stop loss price of MTC
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
    
    
    
    #Determines fulfillment price
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
    
    
    
    '''Setting Optional Variable: Minimum Borrower Constraint'''
    
    
    
    #Checks if user wants to include a first Minimum Borrower Constraint
    while 1 == 1:
        MinimumBorrowerConstraintPresent = (raw_input("Minimum Borrower Constraint (Yes/No):")).upper()
        if MinimumBorrowerConstraintPresent == "YES":
            MinimumBorrowerConstraintPresent = True
            break;
        elif MinimumBorrowerConstraintPresent == "NO":
            MinimumBorrowerConstraintPresent = False
            break;
        else:
            print "You must choose an answer. Please enter again: "
    
    
    
    #If the user wants a constraint, requests Constraint Type and Constraint Value
    if MinimumBorrowerConstraintPresent == True:
        
        #Determines type of Minimum Borrower Constraint
        while 1 == 1:
            MinimumBorrowerConstraintType = (raw_input("Minimum Borrower Constraint Type (Account Balance, Volume, Contracts, Transactions, Liquidity Value): ")).upper()
            if MinimumBorrowerConstraintType == "":
                print "You must specify a value for the Minimum Borrower Constraint Type. Please enter again:"
            if MinimumBorrowerConstraintType != "ACCOUNT BALANCE" and MinimumBorrowerConstraintType != "ACCOUNTBALANCE" and MinimumBorrowerConstraintType != "VOLUME" and MinimumBorrowerConstraintType != "CONTRACTS" and MinimumBorrowerConstraintType != "TRANSACTIONS" and MinimumBorrowerConstraintType != "LIQUIDITY VALUE" and MinimumBorrowerConstraintType != "LIQUIDITYVALUE":
                print "Incorrect Minimum Borrower Constraint Type. Please enter again:"
            else:
                MinimumBorrowerConstraintPresent = True
                break;
        
        
        
        #Standardizes Minimum Borrower Constraint names
        if MinimumBorrowerConstraintType == "ACCOUNTBALANCE":
            MinimumBorrowerConstraintType = "ACCOUNT BALANCE"
        elif MinimumBorrowerConstraintType == "LIQUIDITYVALUE":
            MinimumBorrowerConstraintType = "LIQUIDITY VALUE"
        
        
        
        #Determines value of Minimum Borrower Constraint
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
    
    
    
    #If the user doesn't want a constraint, sets Constraint Type and Constraint Value to None
    else:
        MinimumBorrowerConstraintType = None
        MinimumBorrowerConstraintValue = None
    
    
    
    '''Setting Optional Variable: User Intervention Constraint'''
    
    
    
    #Checks if user wants to include a first User Intervention Constraint
    while 1 == 1:
        UserInterventionConstraintPresent = (raw_input("User Intervention Constraint (Yes/No):")).upper()
        if UserInterventionConstraintPresent == "YES":
            UserInterventionConstraintPresent = True
            break;
        elif UserInterventionConstraintPresent == "NO":
            UserInterventionConstraintPresent = False
            break;
        else:
            print "You must choose an answer. Please enter again: "
    
    
    
    #If the user wants a constraint, requests Constraint Type and Constraint Value
    if UserInterventionConstraintPresent == True:
        
        #Determines type of User Intervention Constraint
        while 1 == 1:
            UserInterventionConstraintType = (raw_input("User Intervention Constraint Type (Account Balance, Volume, Contracts, Transactions, Liquidity Value): ")).upper()
            if UserInterventionConstraintType == "":
                print "You must specify a value for the User Intervention Constraint Type. Please enter again:"
            if UserInterventionConstraintType != "ACCOUNT BALANCE" and UserInterventionConstraintType != "ACCOUNTBALANCE" and UserInterventionConstraintType != "VOLUME" and UserInterventionConstraintType != "CONTRACTS" and UserInterventionConstraintType != "TRANSACTIONS" and UserInterventionConstraintType != "LIQUIDITY VALUE" and UserInterventionConstraintType != "LIQUIDITYVALUE":
                print "Incorrect User Intervention Constraint Type. Please enter again:"
            else:
                UserInterventionConstraintPresent = True
                break;
        
        
        
        #Standardizes User Intervention Constraint names
        if UserInterventionConstraintType == "MARKETPRICE":
            UserInterventionConstraintType = "MARKET PRICE"
        elif UserInterventionConstraintType == "PROFITMARGIN":
            UserInterventionConstraintType = "PROFIT MARGIN"
        elif UserInterventionConstraintType == "INTERESTRATE":
            UserInterventionConstraintType = "INTEREST RATE"
        
        
        
        #Determines value of User Intervention Constraint
        UserInterventionConstraintValue = raw_input("User Intervention Constraint Value: ")
        while 1 == 1:
            if UserInterventionConstraintValue == "":
                print "User Intervention Constraint Failed"
                UserInterventionConstraintPresent = False
                break;
            try:
                UserInterventionConstraintValue = float(UserInterventionConstraintValue)
                UserInterventionConstraintPresent = True
                break;
            except:
                print "User Intervention Constraint Type must be a rational number. Please enter again:"
            UserInterventionConstraintValue = raw_input("User Intervention Constraint Value: ")
    
    
    
    #If the user doesn't want a constraint, sets Constraint Type and Constraint Value to None
    else:
        UserInterventionConstraintType = None
        UserInterventionConstraintValue = None
    
    
    #Execute
    main(Username, Price, Volume, OrderAction, InterestCompoundRate, InterestRate, StopLossPrice, FulfillmentPrice, Duration, DividendType, MinimumBorrowerConstraintType, MinimumBorrowerConstraintValue, UserInterventionConstraintType, UserInterventionConstraintValue)


