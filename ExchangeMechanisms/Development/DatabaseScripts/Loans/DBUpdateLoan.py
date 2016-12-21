#-------------------------------------------------------------------------------
# Name:        DBUpdateLoan
# Version:     3.0
# Purpose:     Updates Loan's specified attribute with specified value
#
# Author:      Matthew
#
# Created:     05/31/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    10/05/2014
#-------------------------------------------------------------------------------

#Only log record/control if update passes
#Add support for contract logging when contract number is changed

import time
import MySQLdb
import sys



def main(ContractNumber, Attribute, NewValue):
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    
    
    '''Verifying Order'''
    
    
    
    print ""
    #Exits if ContractNumber is not an integer
    if not isinstance(ContractNumber, int):
        print "CRITICAL ERROR: Contract Number not an integer"
        sys.exit()
    ContractSearch = "SELECT * FROM LoanBook WHERE ContractNumber = %d" % (ContractNumber)
    try:
        cursor.execute(ContractSearch)
        Contract = cursor.fetchone()
        if Contract != None:
            #print "Contract Found"
            pass
        else:
            print "CRITICAL ERROR: Contract not found"
            sys.exit()
    except SystemExit:
        sys.exit()
    except:
        print "ERROR: Database fetch exception"
        print ""
    
    
    
    '''Defining/Executing SQL Statements'''
    
    
    
    #Updates specified contracts's ContractNumber
    if Attribute == "CONTRACT NUMBER":
        #Converts ContractNumber value to integer type
        try:
            NewValue = int(NewValue)
        except:
            print "CRITICAL ERROR: Contract Number unable to be converted to integer"
            sys.exit()
        #Attempts to change IDNumber to new desired ContractNumber
        try:
            cursor.execute("UPDATE IDBook SET IDNumber = %d WHERE IDNumber = %d" % (NewValue, ContractNumber))
        except:
            cursor.execute("""SELECT * FROM IDBook WHERE IDNumber = %d""" % (NewValue))
            ExistingIDs = cursor.fetchall()
            if ExistingIDs == None:
                print "CRITICAL ERROR: IDBook unable to change IDNumber to specified value"
            else:
                print "CRITICAL ERROR: Specified ContractNumber is unavailable in IDBook"
            sys.exit()
        #Attempts to change ContractNumber to new desired ContractNumber
        try:
            cursor.execute("UPDATE LoanBook SET ContractNumber = %d WHERE ContractNumber = %d" % (NewValue, ContractNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Contract Modified: " + str(ContractNumber)
            print "Attribute Modified: Contract Number"
            print "New Value: " + str(NewValue)
        except:
            #If unsuccessful, searches for existing contracts and displays any if found
            db.rollback()
            print "ERROR: Update Unsuccessful"
            cursor.execute("SELECT * FROM LoanBook WHERE ContractNumber = %d" % (NewValue))
            ExistingOrders = cursor.fetchall()
            if ExistingOrders != ():
                print "ERROR: Contract Number is already in use:"
                print ""
                print ExistingOrders
            
    
    
    
    #Updates specified contract's Username
    if Attribute == "USERNAME":
        #Converts Username value to string type and capitalizes
        try:
            NewValue = str(NewValue.capitalize())
        except:
            print "CRITICAL ERROR: Username unable to be converted to string"
            sys.exit()
        #Attempts to change Username to new desired value
        try:
            cursor.execute("""UPDATE LoanBook SET Username = "%s" WHERE ContractNumber = %d""" % (NewValue, ContractNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Contract Modified: " + str(ContractNumber)
            print "Attribute Modified: Username"
            print "New Value: " + NewValue
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contract's Medium
    if Attribute == "MEDIUM":
        #Converts Medium value to string type and capitalizes
        try:
            NewValue = str(NewValue.capitalize())
        except:
            print "CRITICAL ERROR: Medium unable to be converted to string"
            sys.exit()
        #Attempts to change Medium to new desired value
        try:
            cursor.execute("""UPDATE LoanBook SET Medium = "%s" WHERE ContractNumber = %d""" % (NewValue, ContractNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Contract Modified: " + str(ContractNumber)
            print "Attribute Modified: Medium"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contract's Volume
    if Attribute == "VOLUME":
        #Converts Volume value to float type
        try:
            NewValue = float(NewValue)
        except:
            print "CRITICAL ERROR: Volume unable to be converted to float"
            sys.exit()
        #Attempts to change Volume to new desired value
        try:
            cursor.execute("UPDATE LoanBook SET Volume = %f WHERE ContractNUmber = %d" % (NewValue, ContractNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Contract Modified: " + str(ContractNumber)
            print "Attribute Modified: Volume"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contract's Action
    if Attribute == "ACTION":
        #Converts Action value to string type and capitalizes
        try:
            NewValue = str(NewValue.title())
        except:
            print "CRITICAL ERROR: Action unable to be converted to string"
            sys.exit()
        #Attempts to change Action to new desired value
        try:
            cursor.execute("""UPDATE LoanBook SET Action = "%s" WHERE ContractNUmber = %d""" % (NewValue, ContractNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Contract Modified: " + str(ContractNumber)
            print "Attribute Modified: Action"
            print "New Value: " + NewValue
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contract's InterestCompoundRate
    if Attribute == "INTEREST COMPOUND RATE":
        #Attempts to change Interest Compound Rate to new desired value
        try:
            cursor.execute("""UPDATE LoanBook SET InterestCompoundRate = "%s" WHERE ContractNumber = %d """ % (NewValue, ContractNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Contract Modified: " + str(ContractNumber)
            print "Attribute Modified: Interest Compound Rate"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contract's InterestRate
    if Attribute == "INTEREST RATE":
        #Converts InterestRate value to float type
        try:
            NewValue = float(NewValue)
        except:
            print "CRITICAL ERROR: Interest Rate unable to be converted to float"
            sys.exit()
        #Attempts to change InterestRate to new desired value
        try:
            cursor.execute("""UPDATE LoanBook SET InterestRate = %f WHERE ContractNumber = %d """ % (NewValue, ContractNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Contract Modified: " + str(ContractNumber)
            print "Attribute Modified: Interest Rate"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contract's Duration
    if Attribute == "DURATION":
        #Attempts to change Duration to new desired value
        try:
            cursor.execute("""UPDATE LoanBook SET Duration = "%s" WHERE ContractNumber = %d """ % (NewValue, ContractNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Contract Modified: " + str(ContractNumber)
            print "Attribute Modified: Duration"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contract's DividendType
    if Attribute == "DIVIDEND TYPE":
        #Converts DividendType value to string type
        try:
            NewValue = str(NewValue.capitalize())
        except:
            print "CRITICAL ERROR: Dividend Type unable to be converted to string"
        #Attempts to change DividendType to new desired value
        try:
            cursor.execute("""UPDATE LoanBook SET DividendType = "%s" WHERE ContractNumber = %d """ % (NewValue, ContractNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Contract Modified: " + str(ContractNumber)
            print "Attribute Modified: Dividend Type"
            print "New Value: " + NewValue
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contract's MinimumBorrowerConstraints
    if Attribute == "MINIMUM BORROWER CONSTRAINTS":
        try:
            #Converts MinimumBorrowerConstraints value to integer type
            NewValue = int(NewValue)
        except:
            print "CRITICAL ERROR: Minimum Borrower Constraints unable to be converted to integer"
            sys.exit()
        #Attempts to change MinimumBorrowerConstraints to new desired value
        try:
            cursor.execute("UPDATE LoanBook SET MinimumBorrowerConstraints = %d WHERE ContractNumber = %d" % (NewValue, ContractNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Contract Modified: " + str(ContractNumber)
            print "Attribute Modified: Minimum Borrower Constraints"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contract's UserInterventionConstraints
    if Attribute == "USER INTERVENTION CONSTRAINTS":
        try:
            #Converts userInterventionConstraints value to integer type
            NewValue = int(NewValue)
        except:
            print "CRITICAL ERROR: User Intervention Constraints unable to be converted to integer"
            sys.exit()
        #Attempts to change UserInterventionConstraints to new desired value
        try:
            cursor.execute("UPDATE LoanBook SET UserInterventionConstraints = %d WHERE ContractNumber = %d" % (NewValue, ContractNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Contract Modified: " + str(ContractNumber)
            print "Attribute Modified: User Intervention Constraints"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contract's UserRequests
    if Attribute == "USER REQUESTS":
        try:
            #Converts UserRequests value to integer type
            NewValue = int(NewValue)
        except:
            print "CRITICAL ERROR: User Requests unable to be converted to integer"
            sys.exit()
        #Attempts to change UserRequests to new desired value
        try:
            cursor.execute("UPDATE LoanBook SET UserRequests = %d WHERE ContractNumber = %d" % (NewValue, ContractNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Contract Modified: " + str(ContractNumber)
            print "Attribute Modified: User Requests"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contract's DateEntered
    if Attribute == "DATE ENTERED":
        
        #Gathers current DateEntered and separates into date/time components
        try:
            cursor.execute("""SELECT DateEntered FROM LoanBook WHERE ContractNumber = "%s" """ % (ContractNumber))
            CurrentDateEntered = cursor.fetchall()[0]
            if CurrentDateEntered != ():
                CurrentDateEntered = str(CurrentDateEntered[0])
                
                CurrentDateEnteredYear = CurrentDateEntered[:4]
                CurrentDateEnteredMonth = CurrentDateEntered[5:7]
                CurrentDateEnteredDay = CurrentDateEntered[8:10]
                CurrentDateEnteredHour = CurrentDateEntered[11:13]
                CurrentDateEnteredMinute = CurrentDateEntered[14:16]
                CurrentDateEnteredSecond = CurrentDateEntered[17:19]
            else:
                print "CRITICAL ERROR: Contract has no current date entered"
                sys.exit()
        except:
            print "ERROR: Database fetch exception"
        
        
        
        #Separates NewValue variable into date/time components
        NewYear = NewValue[0]
        NewMonth = NewValue[1]
        NewDay = NewValue[2]
        NewHour = NewValue[3]
        NewMinute = NewValue[4]
        NewSecond = NewValue[5]
        
        
        
        #If any parameter was left blank by user, parameter is set to the current DateEntered interval value
        if NewYear == "":
            NewYear = CurrentDateEnteredYear
        if NewMonth == "":
            NewMonth = CurrentDateEnteredMonth
        if NewDay == "":
            NewDay = CurrentDateEnteredDay
        if NewHour == "":
            NewHour = CurrentDateEnteredHour
        if NewMinute == "":
            NewMinute = CurrentDateEnteredMinute
        if NewSecond == "":
            NewSecond = CurrentDateEnteredSecond
        
        
        
        #If any date/time value is under 10, converts value to string and adds a "0" before value for database compatibility
        if NewMonth < 10:
            NewMonth = "0" + str(NewMonth)
        if NewDay < 10:
            NewDay = "0" + str(NewDay)
        if NewHour < 10:
            NewHour = "0" + str(NewHour)
        if NewMinute < 10:
            NewMinute = "0" + str(NewMinute)
        if NewSecond < 10:
            NewSecond = "0" + str(NewSecond)
        
        
        
        #Forms new Duration value by converting date/time components to strings and concatenating
        NewValue = str(NewYear) + "-" + str(NewMonth) + "-" + str(NewDay) + " " + str(NewHour) + ":" + str(NewMinute) + ":" + str(NewSecond)
        
        
        
        #Attempts to change DateEntered to new desired value
        try:
            cursor.execute("""UPDATE LoanBook SET DateEntered = "%s" WHERE ContractNumber = %d""" % (NewValue, ContractNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "Contract Modified: " + str(ContractNumber)
            print "Attribute Modified: Date Entered"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    '''Creating Logging Record'''
    
    
    
    #Inserts record of order with changes into LoanLog
    cursor.execute("""SELECT MAX(VersionNumber) FROM LoanLog WHERE ContractNumber = %d""" % (ContractNumber))
    OldMaxVersion = int(cursor.fetchone()[0])
    NewVersion = OldMaxVersion + 1
    cursor.execute("""INSERT INTO LoanLog(ContractNumber, VersionNumber, LastModified, Username, Medium, Volume, Action, InterestCompoundRate, InterestRate, Duration, DividendType, MinimumBorrowerConstraints, UserInterventionConstraints, DateEntered) SELECT ContractNumber, %d, "%s", Username, Medium, Volume, Action, InterestCompoundRate, InterestRate, Duration, DividendType, MinimumBorrowerConstraints, UserInterventionConstraints, DateEntered FROM LoanBook WHERE ContractNumber = %d""" % (NewVersion, Attribute.title(), ContractNumber))
    db.commit()
    
    
    
    '''Logging Control'''
    
    
    
    #Assigns static variables for logging control
    #Note: "Employee" value changes based on user submitting manual control
    Employee = "***333"
    ContractID = "Loan " + str(ContractNumber)
    Comment = "Deleted Loan"
    
    
    
    #Inserts record of loan update into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update Loan", ContractID, Attribute.title(), Comment))
        db.commit()
        print "Control Successfully Logged"
    except:
        print "ERROR: Control Unsuccessfully Logged"
    
    
    
    #Adds ControlLog record for EndPoint if the Duration was updated
    if Attribute == "DURATION":
        try:
            print ""
            cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update Loan", ContractID, "End Point", Comment))
            db.commit()
            print "Control Successfully Logged"
        except:
            print "ERROR: Control Unsuccessfully Logged"
    
    
    
    #Adds ControlLog record for Duration if the EndPoint was updated
    if Attribute == "END POINT":
        try:
            print ""
            cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update Loan", ContractID, "Duration", Comment))
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
    
    
    
    '''Setting ContractNumber'''
    
    
    
    #Requests ContractNumber and verifies that it is valid
    while 1 == 1:
        ContractNumber = raw_input("Modified Contract: ")
        #Checks for integer type
        while 1 == 1:
            try:
                ContractNumber = int(ContractNumber)
                break;
            except:
                print "Contract Number must be an integer. Please enter again: "
                ContractNumber = raw_input("Modified Contract: ")
        try:
            cursor.execute("""SELECT * FROM LoanBook WHERE ContractNumber = %d""" % (ContractNumber))
            ContractList = cursor.fetchall()
            if ContractList != ():
                break;
            else:
                print "Contract not found. Please enter again:"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    '''Setting Attribute'''
    
    
    
    #Requests attribute to update and verifies that it is valid
    
    Attribute = raw_input("Changing Attribute: ")
    Attribute = Attribute.upper()
    
    #Gathers column titles from LoanBook
    cursor.execute("SHOW COLUMNS FROM LoanBook")
    FieldList = cursor.fetchall()
    #Iterates column names and matches entered Attribute against existing names
    for Field in FieldList:
        TargetAttribute = Field[0]
        if TargetAttribute.upper() == Attribute or Attribute == "CONTRACT NUMBER" or Attribute == "DATE ENTERED" or Attribute == "INTEREST COMPOUND RATE" or Attribute == "INTEREST RATE" or Attribute == "END POINT" or Attribute == "DIVIDEND TYPE" or Attribute == "MINIMUM BORROWER CONSTRAINTS" or Attribute == "USER INTERVENTION CONSTRAINTS" or Attribute == "USER REQUESTS":
            break;
    #Retrying until valid input is given
    while TargetAttribute.upper() != Attribute and Attribute != "CONTRACT NUMBER" and Attribute != "DATE ENTERED" and Attribute != "INTEREST COMPOUND RATE" and Attribute != "INTEREST RATE" and Attribute != "END POINT" and Attribute != "DIVIDEND TYPE" and Attribute != "MINIMUM BORROWER CONSTRAINTS" and Attribute != "USER INTERVENTION CONSTRAINTS" and Attribute != "USER REQUESTS":
        print "Attribute is invalid. Please enter again:"
        print "Choices: " + str([Field[0] for Field in FieldList])
        Attribute = raw_input("Changing Attribute: ")
        Attribute = Attribute.upper()
        for Field in FieldList:
            TargetAttribute = Field[0]
            if TargetAttribute.upper() == Attribute or Attribute == "CONTRACT NUMBER" or Attribute == "DATE ENTERED" or Attribute == "INTEREST COMPOUND RATE" or Attribute == "INTEREST RATE" or Attribute == "END POINT" or Attribute == "DIVIDEND TYPE" or Attribute == "MINIMUM BORROWER CONSTRAINTS" or Attribute == "USER INTERVENTION CONSTRAINTS" or Attribute == "USER REQUESTS":
                    break;
    
    
    
    '''Standardizing Parameter Names'''
    
    
    
    if Attribute == "CONTRACTNUMBER":
        Attribute = "CONTRACT NUMBER"
        print "Updating: Contract Number"
    
    elif Attribute == "INTERESTCOMPOUNDRATE":
        Attribute = "INTEREST COMPOUND RATE"
        print "Updating: Interest Compound Rate"
    
    elif Attribute == "INTERESTRATE":
        Attribute = "INTEREST RATE"
        print "Updating: Interest Rate"
    
    elif Attribute == "STOPLOSSPRICE":
        Attribute = "STOP LOSS PRICE"
        print "Updating: Stop Loss Price"
    
    elif Attribute == "FULFILLMENTPRICE":
        Attribute = "FULFILLMENT PRICE"
        print "Updating: Fulfillment Price"
        
    elif Attribute == "DIVIDENDTYPE":
        Attribute = "DIVIDEND TYPE"
        print "Updating: Dividend type"
        
    elif Attribute == "MINIMUMBORROWERCONSTRAINTS":
        Attribute = "MINIMUM BORROWER CONSTRAINTS"
        print "Updating: Minimum Borrower Constraints"
        
    elif Attribute == "USERINTERVENTIONCONSTRAINTS":
        Attribute = "USER INTERVENTION CONSTRAINTS"
        print "Updating: User Intervention Constraints"
        
    elif Attribute == "DATEENTERED":
        Attribute = "DATE ENTERED"
        print "Updating: Date Entered"
    
    
    
    '''Setting NewValue'''
    
    
    
    #Requesting basic input value if not a date field or rate field
    if Attribute != "DATE ENTERED" and Attribute != "INTEREST COMPOUND RATE" and Attribute != "DURATION" and Attribute != "END POINT":
        NewValue = raw_input("New Value: ")
        while NewValue == "":
            print "Value is invalid. Please enter again:"
            NewValue = raw_input("New Value: ")
            NewValue = NewValue.upper()
    #Requesting rate input values if not a date field or basic input field
    elif Attribute == "INTEREST COMPOUND RATE" or Attribute == "DURATION":
        NewIntervalValue = raw_input("New Interval Value: ")
        while 1 == 1:
            try:
                NewIntervalValue = int(NewIntervalValue)
                if NewIntervalValue == 0:
                    print "New Interval Value cannot be zero. Please select a positive value:"
                    NewIntervalValue = raw_input("New Interval Value: ")
                else:
                    break;
            except:
                print "New Interval Value must be an integer. Please enter again: "
                NewIntervalValue = raw_input("New New Value: ")
        
        NewInterval = (raw_input("New Interval: ")).upper()
        while 1 == 1:
            if NewInterval != "SECOND" and NewInterval != "MINUTE" and NewInterval != "HOUR" and NewInterval != "DAY":
                print "Value is invalid. Please enter again:"
                print "Choices: [SECOND, MINUTE, HOUR, DAY]"
                NewInterval = (raw_input("New Interval: ")).upper()
            else:
                break;
        
        if NewInterval == "SECOND":
            NewValue = "00:00:%d" % (NewValue)
        if NewInterval == "MINUTE":
            NewValue = "00:%d:00" % (NewValue)
        if NewInterval == "HOUR":
            NewValue = "%d:00:00" % (NewValue)
        if NewInterval == "DAY":
            NewValue = DurationValue * 24
            NewValue = "%d:00:00" % (NewValue)
        print "Duration: " + str(Duration)
    #Requesting date input values if not a rate field or basic input field
    else:
        
        YearValid = False
        MonthValid = False
        DayValid = False
        HourValid = False
        MinuteValid = False
        SecondValid = False
        
        
        
        while YearValid != True:
            DateUpdateYear = raw_input("Update Year: ")
            if DateUpdateYear != "":
                try:
                    DateUpdateYear = int(DateUpdateYear)
                    if DateUpdateYear >= 2014 and DateUpdateYear <= 2015:
                        #print DateUpdateYear
                        YearValid = True
                    else:
                        print "Update parameter must be between 2014 and 2015. Please enter again:"
                except:
                    print "Update parameter must be an integer or blank. Please enter again:"
            else:
                YearValid = True
        
        
        
        while MonthValid != True:
            DateUpdateMonth = raw_input("Update Month: ")
            if DateUpdateMonth != "":
                try:
                    DateUpdateMonth = int(DateUpdateMonth)
                    if DateUpdateMonth >= 1 and DateUpdateMonth <= 12:
                        #print DateUpdateMonth
                        MonthValid = True
                    else:
                        print "Update parameter must be between 1 and 12. Please enter again:"
                except:
                    print "Update parameter must be an integer or blank. Please enter again:"
            else:
                MonthValid = True
        
        
        
        while DayValid != True:
            DateUpdateDay = raw_input("Update Day: ")
            if DateUpdateDay != "":
                try:
                    DateUpdateDay = int(DateUpdateDay)
                    if DateUpdateDay >= 1 and DateUpdateDay <= 365:
                        #print DateUpdateDay
                        DayValid = True
                    else:
                        print "Update parameter must be between 1 and 365. Please enter again:"
                except:
                    print "Update parameter must be an integer or blank. Please enter again:"
            else:
                DayValid = True
        
        
        
        while HourValid != True:
            DateUpdateHour = raw_input("Update Hour: ")
            if DateUpdateHour != "":
                try:
                    DateUpdateHour = int(DateUpdateHour)
                    if DateUpdateHour >= 0 and DateUpdateHour <= 23:
                        #print DateUpdateHour
                        HourValid = True
                    else:
                        print "Update parameter must be between 0 and 23. Please enter again:"
                except:
                    print "Update parameter must be an integer or blank. Please enter again:"
            else:
                HourValid = True
        
        
        
        while MinuteValid != True:
            DateUpdateMinute = raw_input("Update Minute: ")
            if DateUpdateMinute != "":
                try:
                    DateUpdateMinute = int(DateUpdateMinute)
                    if DateUpdateMinute >= 0 and DateUpdateMinute <= 59:
                        #print DateUpdateMinute
                        MinuteValid = True
                    else:
                        print "Update parameter must be between 0 and 59. Please enter again:"
                except:
                    print "Update parameter must be an integer or blank. Please enter again:"
            else:
                MinuteValid = True
        
        
        
        while SecondValid != True:
            DateUpdateSecond = raw_input("Update Second: ")
            if DateUpdateSecond != "":
                try:
                    DateUpdateSecond = int(DateUpdateSecond)
                    if DateUpdateSecond >= 0 and DateUpdateSecond <= 59:
                        #print DateUpdateSecond
                        SecondValid = True
                    else:
                        print "Update parameter must be between 0 and 59. Please enter again:"
                except:
                    print "Update parameter must be an integer or blank. Please enter again:"
            else:
                SecondValid = True
        
        
        
        #Combines all date/time component values into a list for passing to main()
        NewValue = [DateUpdateYear, DateUpdateMonth, DateUpdateDay, DateUpdateHour, DateUpdateMinute, DateUpdateSecond]
    
    
    
    #Execute
    main(ContractNumber, Attribute, NewValue)


