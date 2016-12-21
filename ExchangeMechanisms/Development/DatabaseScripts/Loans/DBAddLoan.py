#-------------------------------------------------------------------------------
# Name:        DBAddLoan
# Version:     3.0
# Purpose:     Adds Loan with specified attributes to specified user
#
# Author:      Matthew
#
# Created:     05/28/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    10/05/2014
#-------------------------------------------------------------------------------

#Remove funds once loan is added
#Check if loan amount is below account balance
#Check time inputs for InterestCompoundRate and Duration

import time
import MySQLdb



def main(Username, ContractMedium, Volume, OrderAction, InterestCompoundRate, InterestRate, Duration, DividendType, MinimumBorrowerConstraintType, MinimumBorrowerConstraintValue, UserInterventionConstraintType, UserInterventionConstraintValue):
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()[0]
    print "Database version: " + str(data)
    
    
    
    '''Creating Loan'''
    
    
    
    #Sets order type
    OrderType = "Loan"
    
    #Inserts record into IDBook
    cursor.execute("""INSERT INTO IDBook(Type, Action) VALUES("%s", "%s")""" % (OrderType, OrderAction.capitalize()))
    #Inserts loan into LoanBook
    cursor.execute("""INSERT INTO LoanBook(Username, Medium, Volume, Action, InterestCompoundRate, InterestRate, Duration, DividendType) VALUES("%s", "%s", %f, "%s", "%s", %f, "%s", "%s")""" % (Username, ContractMedium.title(), Volume, OrderAction.title(), InterestCompoundRate, InterestRate, Duration, DividendType.title()))
    db.commit()
    print ""
    print "Order Successfully Added"
    try:
        #Gathers and reads loan details
        cursor.execute("""SELECT * FROM LoanBook ORDER BY ContractNumber DESC LIMIT 1""")
        LatestContracts = cursor.fetchall()
        for Contract in LatestContracts:
            print ""
            print "Order Added:"
            print ""
            ContractNumber = Contract[0]
            Username = Contract[1]
            ContractMedium = Contract[2]
            Volume = Contract[3]
            OrderAction = Contract[4]
            DateEntered = Contract[12]
            print "Order Number: " + str(ContractNumber)
            print "Type: " + str(OrderType)
            print "Action: " + str(OrderAction)
            print "Username: " + str(Username)
            print "Medium: " + str(ContractMedium.title())
            print "Volume: " + str(Volume)
            print "Date Entered: " + str(DateEntered)
            break;
    except:
        db.rollback()
        print "ERROR: Database Insert Failure"
    
    
    
    '''Logging Contract'''
    
    
    
    #Inserts record into LoanLog
    try:
        print ""
        cursor.execute("""INSERT INTO LoanLog(ContractNumber, Username, Medium, Volume, Action, InterestCompoundRate, InterestRate, Duration, DividendType) VALUES(%d, "%s", "%s", %f, "%s", "%s", %f, "%s", "%s")""" % (ContractNumber, Username, ContractMedium.title(), Volume, OrderAction.title(), InterestCompoundRate, InterestRate, Duration, DividendType.title()))
        db.commit()
        print "Loan Contract Successfully Logged"
    except:
        print "ERROR: Database Log Insert Failure"
    
    
    
    '''Adding Minimum Borrower Constraint'''
    
    
    
    #Gathers current highest ConstraintID from log and adds one
    #NOTE: Since ConstraintID is in format "[ContractNumber]-[ConstraintNumber]", the ID must be converted to string,
    #cut off after the dash, then the ConstraintNumber must be calculated and appended to the ID again
    
    if MinimumBorrowerConstraintType != None and MinimumBorrowerConstraintValue != None:
        cursor.execute("""SELECT * FROM BorrowerConstraintBook WHERE ContractNumber = %s""" % (ContractNumber))
        BorrowerConstraintBookConstraints = cursor.fetchall()
        #If no current constraints exists, sets ID to "[ContractNumber]-1"
        if BorrowerConstraintBookConstraints == ():
            ConstraintID = str(ContractNumber) + "-1"
        else:
            
            #Iterates through each ConstraintID, changing OldConstraintNumber to reflect ConstraintNumber that was just compared,
            #then compares those values with newly assigned ConstraintID again until loop is finished
            #NOTE: This allows for skips in the log due to error, whereas counting the number of constraints and appending would not
            
            OldConstraintNumber = 0
            #Gathers ConstraintNumber from each constraint
            for Constraint in BorrowerConstraintBookConstraints:
                ConstraintCutOff = len(str(ContractNumber)) + 1
                ConstraintNumber = str(Constraint[0])[ConstraintCutOff:]
                #If new ConstraintNumber is greater than the iterated ConstraintNumber, creates new ConstraintID with +1 added to ConstraintNumber
                if int(ConstraintNumber) > int(OldConstraintNumber):
                    ConstraintID = (str(ContractNumber) + "-" + str(int(ConstraintNumber) + 1))
                    OldConstraintNumber = ConstraintNumber
        
        
        
        #Inserts constraint into BorrowerConstraintBook and record into BorrowerConstraintLog
        try:
            print ""
            cursor.execute("""INSERT INTO BorrowerConstraintBook(ConstraintID, ContractNumber, Username, Type, Value) VALUES("%s", %d, "%s", "%s", %f)""" % (ConstraintID, ContractNumber, Username, MinimumBorrowerConstraintType.title(), MinimumBorrowerConstraintValue))
            cursor.execute("""INSERT INTO BorrowerConstraintLog(ConstraintID, ContractNumber, Username, Type, Value) VALUES("%s", %d, "%s", "%s", %f)""" % (ConstraintID, ContractNumber, Username, MinimumBorrowerConstraintType.title(), MinimumBorrowerConstraintValue))
            db.commit()
            print "Minimum Borrower Constraint Successfully Added"
        except:
            print "ERROR: Minimum Borrower Constraint Unsuccessfully Added"
        
        #Updates LoanBook and LoanLog to reflect update of constraint amount
        cursor.execute("""UPDATE LoanBook SET MinimumBorrowerConstraints = (MinimumBorrowerConstraints + 1) WHERE ContractNumber = %s""" % (ContractNumber))
        cursor.execute("""UPDATE LoanLog SET MinimumBorrowerConstraints = (MinimumBorrowerConstraints + 1) WHERE ContractNumber = %s""" % (ContractNumber))
        db.commit()
    
    
    
    '''Adding User Intervention Constraint'''
    
    
    
    #Gathers current highest ConstraintID from log and adds one
    #NOTE: Since ConstraintID is in format "[ContractNumber]-[ConstraintNumber]", the ID must be converted to string,
    #cut off after the dash, then the ConstraintNumber must be calculated and appended to the ID again
    
    if UserInterventionConstraintType != None and UserInterventionConstraintValue != None:
        cursor.execute("""SELECT * FROM InterventionConstraintBook WHERE ContractNumber = %s""" % (ContractNumber))
        InterventionConstraintBookConstraints = cursor.fetchall()
        #If no current constraints exists, sets ID to "[ContractNumber]-1"
        if InterventionConstraintBookConstraints == ():
            ConstraintID = str(ContractNumber) + "-1"
        else:
            
            #Iterates through each ConstraintID, changing OldConstraintNumber to reflect ConstraintNumber that was just compared,
            #then compares those values with newly assigned ConstraintID again until loop is finished
            #NOTE: This allows for skips in the log due to error, whereas counting the number of constraints and appending would not
            
            OldConstraintNumber = 0
            #Gathers ConstraintNumber from each constraint
            for Constraint in InterventionConstraintBookConstraints:
                ConstraintCutOff = len(str(ContractNumber)) + 1
                ConstraintNumber = str(Constraint[0])[ConstraintCutOff:]
                #If new ConstraintNumber is greater than the iterated ConstraintNumber, creates new ConstraintID with +1 added to ConstraintNumber
                if int(ConstraintNumber) > int(OldConstraintNumber):
                    ConstraintID = (str(ContractNumber) + "-" + str(int(ConstraintNumber) + 1))
                    OldConstraintNumber = ConstraintNumber
        
        
        
        #Inserts constraint into InterventionConstraintBook and record into InterventionConstraintLog
        try:
            print ""
            cursor.execute("""INSERT INTO InterventionConstraintBook(ConstraintID, ContractNumber, Username, Type, Value) VALUES("%s", %d, "%s", "%s", %f)""" % (ConstraintID, ContractNumber, Username, UserInterventionConstraintType.title(), UserInterventionConstraintValue))
            cursor.execute("""INSERT INTO InterventionConstraintLog(ConstraintID, ContractNumber, Username, Type, Value) VALUES("%s", %d, "%s", "%s", %f)""" % (ConstraintID, ContractNumber, Username, UserInterventionConstraintType.title(), UserInterventionConstraintValue))
            db.commit()
            print "User Intervention Constraint Successfully Added"
        except:
            print "ERROR: User Intervention Constraint Unsuccessfully Added"
        
        #Updates LoanBook and LoanLog to reflect update of constraint amount
        cursor.execute("""UPDATE LoanBook SET UserInterventionConstraints = (UserInterventionConstraints + 1) WHERE ContractNumber = %s""" % (ContractNumber))
        cursor.execute("""UPDATE LoanLog SET UserInterventionConstraints = (UserInterventionConstraints + 1) WHERE ContractNumber = %s""" % (ContractNumber))
        db.commit()
    
    
    
    '''Logging Control'''
        
    
    
    #Assigns static variables for logging control
    #Note: "Employee" value changes based on user submitting manual control
    Employee = "***333"
    ContractID = "Loan " + str(ContractNumber)
    Comment = "Added Loan"
    
    #Inserts record of action into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Add Loan Contract", ContractID, "All", Comment))
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
    
    
    
    #Determines user to put loan under, and checks to see if user exists
    Username = raw_input("Username: ")
    Username = Username.capitalize()
    UserFound = False
    while UserFound != True:
        cursor.execute("""SELECT * FROM UserBook WHERE Username = "%s" """ % (Username))
        UsernameList = cursor.fetchall()
        for User in UsernameList:
            if Username == User[0]:
                AccountBalance = User[3]
                AccountVolume = User[4]
                print "User found"
                UserFound = True
                break;
        else:
            print "User not found. Please enter again: "
            Username = raw_input("Username: ")
            Username = Username.capitalize()
    print ""
    print "User Balance: " + str(AccountBalance)
    print "User Volume: " + str(AccountVolume)
    print ""
    
    #Checks for negative balances and exits if found
    if (AccountBalance < 0) or (AccountVolume < 0):
        print "CRITICAL ERROR: User has negative balance"
        print "Exiting..."
        sys.exit()
    
    
    
    #Determines action of loan
    print ""
    OrderAction = raw_input("Action (Loan/Borrow): ")
    OrderAction = OrderAction.upper()
    while OrderAction != "LOAN" and OrderAction != "BORROW":
        print "Incorrect order action. Please enter again:"
        OrderAction = raw_input("Action (Loan/Borrow): ")
        OrderAction = OrderAction.upper()
    
    #Determines type of loan
    OrderType = "Loan"
    
    
    #Determines which medium the loan will be issued in
    ContractMedium = raw_input("Medium (Currency/Digital): ")
    ContractMedium = ContractMedium.upper()
    while ContractMedium != "CURRENCY" and ContractMedium != "DIGITAL":
        print "Incorrect medium type. Please enter again: "
        ContractMedium = raw_input("Medium (Currency/Digital): ")
        ContractMedium = ContractMedium.upper()
    
    
    #Determines volume of loan
    Volume = raw_input("Volume: ")
    while 1 == 1:
        try:
            Volume = float(Volume)
            break;
        except:
            print "Volume must be an integer. Please enter again: "
            Volume = raw_input("Volume: ")
    
    
    
    #Determines value for the rate at which loan interest is compounded
    InterestCompoundRateValue = raw_input("Interest Compound Rate Value: ")
    while 1 == 1:
        try:
            InterestCompoundRateValue = float(InterestCompoundRateValue)
            break;
        except:
            print "Interest Compound Rate must be an integer. Please enter again: "
            InterestCompoundRateValue = raw_input("Interest Compound Rate Value: ")
    
    
    
    #Determines interval of rate at which Loan interest is compounded
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
    
    
    
    #Determines interest rate of loan
    InterestRate = raw_input("Interest Rate: ")
    while 1 == 1:
        try:
            InterestRate = float(InterestRate)
            break;
        except:
            print "Interest Rate must be an integer. Please enter again: "
            InterestRate = raw_input("InterestRate: ")
    
    
    
    #Determines value for the duration of the loan
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
    
    
    
    #Determines interval for the duration of the loan
    DurationInterval = raw_input("Duration Interval (Second, Minute, Hour, Day): ")
    DurationInterval = DurationInterval.upper()
    while 1 == 1:
        if DurationInterval != "SECOND" and DurationInterval != "MINUTE" and DurationInterval != "HOUR" and DurationInterval != "DAY":
            print "Duration Interval must be either SECOND, MINUTE, HOUR, or DAY. Please enter again: "
            DurationInterval = (raw_input("Duration Interval: ")).upper()
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
    
    
    
    #Determines dividend type of loan
    DividendType = raw_input("Dividend Type (Flat/Percent): ")
    DividendType = DividendType.upper()
    while DividendType != "FLAT" and DividendType != "PERCENT":
        print "Incorrect dividend type. Please enter again:"
        DividendType = raw_input("Dividend Type (Flat/Percent): ")
        DividendType = DividendType.upper()
    
    
    
    #Sets comment for manual run
    Comment = raw_input("Administrative Comment: ")
    
    
    
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
    main(Username, ContractMedium, Volume, OrderAction, InterestCompoundRate, InterestRate, Duration, DividendType, MinimumBorrowerConstraintType, MinimumBorrowerConstraintValue, UserInterventionConstraintType, UserInterventionConstraintValue)


