#-------------------------------------------------------------------------------
# Name:        DBUpdateMTC
# Version:     3.0
# Purpose:     Updates MTC's specified attribute with specified value
#
# Author:      Matthew
#
# Created:     05/26/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    10/05/2014
#-------------------------------------------------------------------------------

#Only log record/control if update passes
#Add support for MTC logging when contract number is changed

import time
import MySQLdb
import sys



def main(MTCNumber, Attribute, NewValue):
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    
    
    '''Verifying Order'''
    
    
    
    print ""
    #Exits if MTCNumber is not an integer
    if not isinstance(MTCNumber, int):
        print "CRITICAL ERROR: MTC Number not an integer"
        sys.exit()
    MTCSearch = "SELECT * FROM MTCBook WHERE MTCNumber = %d" % (MTCNumber)
    try:
        cursor.execute(MTCSearch)
        MTC = cursor.fetchone()
        if MTC != None:
            #print "MTC Found"
            pass
        else:
            print "CRITICAL ERROR: MTC not found"
            sys.exit()
    except SystemExit:
        sys.exit()
    except:
        print "ERROR: Database fetch exception"
        print ""
    
    
    
    '''Defining/Executing SQL Statements'''
    
    
    
    #Updates specified contracts's MTCNumber
    if Attribute == "MTC NUMBER":
        #Converts ContractNumber value to integer type
        try:
            NewValue = integer(NewValue)
        except:
            print "CRITICAL ERROR: MTC Number unable to be converted to integer"
            sys.exit()
        #Attempts to change IDNumber to new desired value
        try:
            cursor.execute("UPDATE IDBook SET IDNumber = %d WHERE IDNumber = %d" % (NewValue, TradeNumber))
        except:
            cursor.execute("""SELECT * FROM IDBook WHERE IDNumber = %d""" % (NewValue))
            ExistingIDs = cursor.fetchall()
            if ExistingIDs == None:
                print "CRITICAL ERROR: IDBook unable to change IDNumber to specified value"
            else:
                print "CRITICAL ERROR: Specified TradeNumber is unavailable in IDBook"
            sys.exit()
        #Attempts to change MTCNumber to new desired value
        try:
            cursor.execute("UPDATE MTCBook SET MTCNumber = %d WHERE MTCNumber = %d" % (NewValue, MTCNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "MTC Modified: " + str(MTCNumber)
            print "Attribute Modified: MTC Number"
            print "New Value: " + str(NewValue)
        except:
            #If unsuccessful, searches for existing contracts and displays any if found
            db.rollback()
            print "ERROR: Update Unsuccessful"
            cursor.execute("SELECT * FROM MTCBook WHERE MTCNumber = %d" % (NewValue))
            ExistingOrders = cursor.fetchall()
            if ExistingOrders != ():
                print "ERROR: MTC Number is already in use:"
                print ""
                print ExistingOrders
    
    
    
    #Updates specified contracts's Username
    if Attribute == "USERNAME":
        #Converts Username value to string type and capitalizes
        try:
            NewValue = str(NewValue.title())
        except:
            print "CRITICAL ERROR: Username unable to be converted to string"
            sys.exit()
        #Attempts to change Username to new desired value
        try:
            cursor.execute("""UPDATE MTCBook SET Username = "%s" WHERE MTCNumber = %d""" % (NewValue, MTCNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "MTC Modified: " + str(MTCNumber)
            print "Attribute Modified: Username"
            print "New Value: " + NewValue
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contracts's Price
    if Attribute == "PRICE":
        #Converts Price value to float type
        try:
            NewValue = float(NewValue)
        except:
            print "CRITICAL ERROR: Price unable to be converted to float"
            sys.exit()
        #Attempts to change Price to new desired value
        try:
            cursor.execute("UPDATE MTCBook SET Price = %f WHERE MTCNumber = %d" % (NewValue, MTCNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "MTC Modified: " + str(MTCNumber)
            print "Attribute Modified: Price"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contracts's Volume
    if Attribute == "VOLUME":
        #Converts Volume value to float type
        try:
            NewValue = float(NewValue)
        except:
            print "CRITICAL ERROR: Volume unable to be converted to float"
            sys.exit()
        #Attempts to change Volume to new desired value
        try:
            cursor.execute("UPDATE MTCBook SET Volume = %f WHERE MTCNUmber = %d" % (NewValue, MTCNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "MTC Modified: " + str(MTCNumber)
            print "Attribute Modified: Volume"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contracts's Action
    if Attribute == "ACTION":
        #Converts Price value to string type and capitalizes
        try:
            NewValue = str(NewValue.capitalize())
        except:
            print "CRITICAL ERROR: Action unable to be converted to string"
            sys.exit()
        #Attempts to change Action to new desired value
        try:
            cursor.execute("""UPDATE MTCBook SET Action = "%s" WHERE MTCNUmber = %d""" % (NewValue, MTCNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "MTC Modified: " + str(MTCNumber)
            print "Attribute Modified: Action"
            print "New Value: " + NewValue
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contracts's InterestCompoundRate
    if Attribute == "INTEREST COMPOUND RATE":
        #Attempts to change Interest Compound Rate to new desired value
        try:
            cursor.execute("""UPDATE MTCBook SET InterestCompoundRate = "%s" WHERE MTCNumber = %d """ % (NewValue, MTCNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "MTC Modified: " + str(MTCNumber)
            print "Attribute Modified: Interest Compound Rate"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contracts's InterestRate
    if Attribute == "INTEREST RATE":
        #Converts InterestRate value to float type
        try:
            NewValue = float(NewValue)
        except:
            print "CRITICAL ERROR: Interest Rate unable to be converted to float"
            sys.exit()
        #Attempts to change InterestRate to new desired value
        try:
            cursor.execute("""UPDATE MTCBook SET InterestRate = %f WHERE MTCNumber = %d """ % (NewValue, MTCNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "MTC Modified: " + str(MTCNumber)
            print "Attribute Modified: Interest Rate"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contracts's StopLossPrice
    if Attribute == "STOP LOSS PRICE":
        #Converts StopLossPrice value to float type
        try:
            NewValue = float(NewValue)
        except:
            print "CRITICAL ERROR: Stop Loss Price unable to be converted to float"
            sys.exit()
        #Attempts to change StopLossPrice to new desired value
        try:
            cursor.execute("""UPDATE MTCBook SET StopLossPrice = %f WHERE MTCNumber = %d """ % (NewValue, MTCNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "MTC Modified: " + str(MTCNumber)
            print "Attribute Modified: Stop Loss Price"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contracts's FulfillmentPrice
    if Attribute == "FULFILLMENT PRICE":
        #Converts FulfillmentPrice value to float type
        try:
            NewValue = float(NewValue)
        except:
            print "CRITICAL ERROR: Fulfillment unable to be converted to float"
            sys.exit()
        #Attempts to change FulfillmentPrice to new desired value
        try:
            cursor.execute("""UPDATE MTCBook SET FulfillmentPrice = %f WHERE MTCNumber = %d """ % (NewValue, MTCNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "MTC Modified: " + str(MTCNumber)
            print "Attribute Modified: Fulfillment Price"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contracts's Duration
    if Attribute == "DURATION":
        #Attempts to change Duration to new desired value
        try:
            cursor.execute("""UPDATE MTCBook SET Duration = "%s" WHERE MTCNumber = %d """ % (NewValue, MTCNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "MTC Modified: " + str(MTCNumber)
            print "Attribute Modified: Duration"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contracts's DividendType
    if Attribute == "DIVIDEND TYPE":
        #Converts DividendType value to string type and capitalizes
        try:
            NewValue = str(NewValue.capitalize())
        except:
            print "CRITICAL ERROR: Dividend Type unable to be converted to string"
            sys.exit()
        #Attempts to change DividendType to new desired value
        try:
            cursor.execute("""UPDATE MTCBook SET DividendType = "%s" WHERE MTCNumber = %d """ % (NewValue, MTCNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "MTC Modified: " + str(MTCNumber)
            print "Attribute Modified: Dividend Type"
            print "New Value: " + NewValue
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contracts's MinimumBorrowerConstraints
    if Attribute == "MINIMUM BORROWER CONSTRAINTS":
        #Converts MinimumBorrowerConstraints value to integer type
        try:
            NewValue = int(NewValue)
        except:
            print "CRITICAL ERROR: Minimum Borrower Constraints unable to be converted to integer"
            sys.exit()
        #Attempts to change MinimumBorrowerConstraints to new desired value
        try:
            cursor.execute("UPDATE MTCBook SET MinimumBorrowerConstraints = %d WHERE MTCNumber = %d" % (NewValue, MTCNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "MTC Modified: " + str(MTCNumber)
            print "Attribute Modified: Minimum Borrower Constraints"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contracts's UserInterventionConstraints
    if Attribute == "USER INTERVENTION CONSTRAINTS":
        #Converts UserInterventionConstraints value to integer type
        try:
            NewValue = int(NewValue)
        except:
            print "CRITICAL ERROR: User Intervention Constraints unable to be converted to integer"
            sys.exit()
        #Attempts to change UserInterventionConstraints to new desired value
        try:
            cursor.execute("UPDATE MTCBook SET UserInterventionConstraints = %d WHERE MTCNumber = %d" % (NewValue, MTCNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "MTC Modified: " + str(MTCNumber)
            print "Attribute Modified: User Intervention Constraints"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contracts's UserRequests
    if Attribute == "USER REQUESTS":
        #Converts UserRequests value to integer type
        try:
            NewValue = int(NewValue)
        except:
            print "CRITICAL ERROR: User Requests Constraints unable to be converted to integer"
            sys.exit()
        #Attempts to change UserRequests to new desired value
        try:
            cursor.execute("UPDATE MTCBook SET UserRequests = %d WHERE MTCNumber = %d" % (NewValue, MTCNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "MTC Modified: " + str(MTCNumber)
            print "Attribute Modified: User Requests"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contracts's DateEntered
    if Attribute == "DATE ENTERED":
        
        #Gathers current DateEntered and separates into date/time components
        try:
            cursor.execute("""SELECT DateEntered FROM MTCBook WHERE MTCNumber = "%s" """ % (MTCNumber))
            CurrentJoinDate = cursor.fetchall()[0]
            if CurrentJoinDate != ():
                CurrentJoinDate = str(CurrentJoinDate[0])
                
                CurrentJoinDateYear = CurrentJoinDate[:4]
                CurrentJoinDateMonth = CurrentJoinDate[5:7]
                CurrentJoinDateDay = CurrentJoinDate[8:10]
                CurrentJoinDateHour = CurrentJoinDate[11:13]
                CurrentJoinDateMinute = CurrentJoinDate[14:16]
                CurrentJoinDateSecond = CurrentJoinDate[17:19]
            else:
                print "CRITICAL ERROR: MTC has no current date entered"
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
            NewYear = CurrentJoinDateYear
        if NewMonth == "":
            NewMonth = CurrentJoinDateMonth
        if NewDay == "":
            NewDay = CurrentJoinDateDay
        if NewHour == "":
            NewHour = CurrentJoinDateHour
        if NewMinute == "":
            NewMinute = CurrentJoinDateMinute
        if NewSecond == "":
            NewSecond = CurrentJoinDateSecond
        
        
        
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
            cursor.execute("""UPDATE MTCBook SET DateEntered = "%s" WHERE MTCNumber = %d""" % (NewValue, MTCNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "MTC Modified: " + str(MTCNumber)
            print "Attribute Modified: Date Entered"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    '''Creating Logging Record'''
    
    
    
    #Inserts record of order with changes into MTCLog
    cursor.execute("""SELECT MAX(VersionNumber) FROM MTCLog WHERE MTCNumber = %d""" % (MTCNumber))
    OldMaxVersion = int(cursor.fetchone()[0])
    NewVersion = OldMaxVersion + 1
    cursor.execute("""INSERT INTO MTCLog(MTCNumber, VersionNumber, LastModified, Username, Price, Volume, Action, InterestCompoundRate, InterestRate, StopLossPrice, FulfillmentPrice, Duration, DividendType, MinimumBorrowerConstraints, UserInterventionConstraints, DateEntered) SELECT MTCNumber, %d, "%s", Username, Price, Volume, Action, InterestCompoundRate, InterestRate, StopLossPrice, FulfillmentPrice, Duration, DividendType, MinimumBorrowerConstraints, UserInterventionConstraints, DateEntered FROM MTCBook WHERE MTCNumber = %d""" % (NewVersion, Attribute.title(), MTCNumber))
    db.commit()
    
    
    
    '''Logging Control'''
    
    
    
    #Assigns static variables for logging control
    #Note: "Employee" value changes based on user submitting manual control
    Employee = "***333"
    MTCID = "MTC " + str(MTCNumber)
    Comment = "Updated MTC"
    
    
    
    #Inserts record of MTC update into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update MTC", MTCID, Attribute.title(), Comment))
        db.commit()
        print "Control Successfully Logged"
    except:
        print "ERROR: Control Unsuccessfully Logged"
    
    
    
    #Adds ControlLog record for EndPoint if the Duration was updated
    if Attribute == "DURATION":
        try:
            print ""
            cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update MTC", MTCID, "End Point", Comment))
            db.commit()
            print "Control Successfully Logged"
        except:
            print "ERROR: Control Unsuccessfully Logged"
    
    
    
    #Adds ControlLog record for Duration if the EndPoint was updated
    if Attribute == "END POINT":
        try:
            print ""
            cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update MTC", MTCID, "Duration", Comment))
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
    
    
    
    '''Setting Variables'''
        
    
    
    #Requests ContractNumber and verifies that it is valid
    while 1 == 1:
        MTCNumber = raw_input("Update MTC Number: ")
        #Checks for integer type
        while 1 == 1:
            try:
                MTCNumber = int(MTCNumber)
                break;
            except:
                print "MTC Number must be an integer. Please enter again: "
                MTCNumber = raw_input("MTC Number: ")
        try:
            cursor.execute("""SELECT * FROM MTCBook WHERE MTCNumber = %d""" % (MTCNumber))
            MTC = cursor.fetchone()
            if MTC != None:
                break;
            else:
                print "MTC not found. Please search again:"
        except:
            print "ERROR: Database fetch exception"
    
    
    
    '''Setting Attribute'''
    
    
    
    #Requests attribute to update and verifies that it is valid
    
    Attribute = raw_input("Changing Attribute: ")
    Attribute = Attribute.upper()
    
    #Gathers column titles from LoanBook
    cursor.execute("SHOW COLUMNS FROM MTCBook")
    FieldList = cursor.fetchall()
    #Iterates column names and matches entered Attribute against existing names
    for Field in FieldList:
        TargetAttribute = Field[0]
        if TargetAttribute.upper() == Attribute or Attribute == "MTC NUMBER" or Attribute == "DATE ENTERED" or Attribute == "INTEREST COMPOUND RATE" or Attribute == "INTEREST RATE" or Attribute == "STOP LOSS PRICE" or Attribute == "FULFILLMENT PRICE" or Attribute == "END POINT" or Attribute == "DIVIDEND TYPE" or Attribute == "MINIMUM BORROWER CONSTRAINTS" or Attribute == "USER INTERVENTION CONSTRAINTS" or Attribute == "USER REQUESTS":
            break;
    #Retrying until valid input is given
    while TargetAttribute.upper() != Attribute and Attribute != "MTC NUMBER" and Attribute != "DATE ENTERED" and Attribute != "INTEREST COMPOUND RATE" and Attribute != "INTEREST RATE" and Attribute != "STOP LOSS PRICE" and Attribute != "FULFILLMENT PRICE" and Attribute != "END POINT" and Attribute != "DIVIDEND TYPE" and Attribute != "MINIMUM BORROWER CONSTRAINTS" and Attribute != "USER INTERVENTION CONSTRAINTS" and Attribute != "USER REQUESTS":
        print "Attribute is invalid. Please enter again:"
        print "Choices: " + str([Field[0] for Field in FieldList])
        Attribute = raw_input("Changing Attribute: ")
        Attribute = Attribute.upper()
        for Field in FieldList:
            TargetAttribute = Field[0]
            if TargetAttribute.upper() == Attribute or Attribute == "MTC NUMBER" or Attribute == "DATE ENTERED" or Attribute == "INTEREST COMPOUND RATE" or Attribute == "INTEREST RATE" or Attribute == "STOP LOSS PRICE" or Attribute == "FULFILLMENT PRICE" or Attribute == "END POINT" or Attribute == "DIVIDEND TYPE" or Attribute == "MINIMUM BORROWER CONSTRAINTS" or Attribute == "USER INTERVENTION CONSTRAINTS" or Attribute == "USER REQUESTS":
                    break;
    
    
    
    '''Standardizing Parameter Names'''
    
    
    
    if Attribute == "MTCNUMBER":
        Attribute = "MTC NUMBER"
        print "Updating: MTC Number"
    
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
        print "Updating: Dividend Type"
    
    elif Attribute == "MINIMUMBORROWERCONSTRAINTS":
        Attribute = "MINIMUM BORROWER CONSTRAINTS"
        print "Updating: Minimum Borrower Constraints"
    
    elif Attribute == "USERINTERVENTIONCONSTRAINTS":
        Attribute = "USER INTERVENTION CONSTRAINTS"
        print "Updating: User Intervention Constraints"
    
    elif Attribute == "DATEENTERED":
        Attribute = "DATE ENTERED"
        print "Updating: Date Entered"
    
    else:
        print "Updating: " + Attribute.title()
    
    
    
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
    main(MTCNumber, Attribute, NewValue)


