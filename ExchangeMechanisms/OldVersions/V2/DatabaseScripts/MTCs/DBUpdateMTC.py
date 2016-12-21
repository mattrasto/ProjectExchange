#-------------------------------------------------------------------------------
# Name:        DBUpdateMTC
# Version:     2.0
# Purpose:
#
# Author:      Matthew
#
# Created:     05/26/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/15/2014
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
        #Separates InterestCompoundRate list into values and concatenates into a string
        NewInterval = NewValue[0]
        NewIntervalValue = NewValue[1]
        NewRate = str(NewIntervalValue) + " " + str(NewInterval.upper())
        try:
            cursor.execute("""UPDATE MTCBook SET InterestCompoundRate = "%s" WHERE MTCNumber = %d """ % (NewRate, MTCNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "MTC Modified: " + str(MTCNumber)
            print "Attribute Modified: Interest Compound Rate"
            print "New Value: " + NewRate
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
        #Separates InterestCompoundRate list into values and concatenates into a string
        NewInterval = NewValue[0]
        NewIntervalValue = NewValue[1]
        NewDuration = str(NewIntervalValue) + " " + str(NewInterval.upper())
        #Attempts to change Duration to new desired value
        try:
            cursor.execute("""UPDATE MTCBook SET Duration = "%s" WHERE MTCNumber = %d """ % (NewDuration, MTCNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "MTC Modified: " + str(MTCNumber)
            print "Attribute Modified: Duration"
            print "New Value: " + str(NewDuration)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
        
        
        
        #Forms new list for duration values
        NewDurationList = (NewIntervalValue, NewInterval.upper())
        
        
        
        #Gathers current DateEntered and separates into date/time components
        try:
            cursor.execute("""SELECT DateEntered FROM MTCBook WHERE MTCNumber = %d""" % (MTCNumber))
            Date = cursor.fetchall()[0][0]
        except:
            print "ERROR: Date Unsuccessfully Retrieved"
        
        #Converts Date value to string type
        LocalTime = str(Date)
        
        #Separates LocalTime variable into date/time components
        LocalTimeYears = int(LocalTime[:4])
        LocalTimeMonths = int(LocalTime[5:7])
        LocalTimeDays = int(LocalTime[8:10])
        LocalTimeHours = int(LocalTime[11:13])
        LocalTimeMinutes = int(LocalTime[14:16])
        LocalTimeSeconds = int(LocalTime[17:19])
        
        
        
        #Adds current time intervals to duration time intervals
        if NewDurationList[1] == "SECOND":
            LocalTimeSeconds = int(int(LocalTimeSeconds) + NewDurationList[0])
        elif NewDurationList[1] == "MINUTE":
            LocalTimeMinutes = int(int(LocalTimeMinutes) + NewDurationList[0])
        elif NewDurationList[1] == "HOUR":
            LocalTimeHours = int(int(LocalTimeHours) + NewDurationList[0])
        elif NewDurationList[1] == "DAY":
            LocalTimeDays = int(int(LocalTimeDays) + NewDurationList[0])
        
        
        
        #Carries extra seconds into minutes
        if LocalTimeSeconds > 60:
            LocalTimeSecondsRemainder = (LocalTimeSeconds % 60)
            LocalTimeSecondsCarry = int(round(LocalTimeSeconds / 60))
            LocalTimeMinutes += LocalTimeSecondsCarry
            LocalTimeSeconds = LocalTimeSecondsRemainder
        
        #Carries extra minutes into hours
        if LocalTimeMinutes > 60:
            LocalTimeMinutesRemainder = (LocalTimeMinutes % 60)
            LocalTimeMinutesCarry = int(round(LocalTimeMinutes / 60))
            LocalTimeHours += LocalTimeMinutesCarry
            LocalTimeMinutes = LocalTimeMinutesRemainder
        
        #Carries extra hours into days
        if LocalTimeHours > 24:
            LocalTimeHoursRemainder = (LocalTimeHours % 24)
            LocalTimeHoursCarry = int(round(LocalTimeHours / 24))
            LocalTimeDays += LocalTimeHoursCarry
            LocalTimeHours = LocalTimeHoursRemainder
        
        #Checks if extra days value is over amount of days in month
        while 1 == 1:
            
            #Checks for proper amount of days in respective month and assigns to variable DaysCeiling
            if LocalTimeMonths == 1 or LocalTimeMonths == 3 or LocalTimeMonths == 5 or LocalTimeMonths == 7 or LocalTimeMonths == 8 or LocalTimeMonths == 10 or LocalTimeMonths == 12:
                DaysCeiling = 31
            elif LocalTimeMonths == 4 or LocalTimeMonths == 6 or LocalTimeMonths == 9 or LocalTimeMonths == 11:
                DaysCeiling = 30
            else:
                DaysCeiling = 28
            
            #Carries extra days into months
            if LocalTimeDays > DaysCeiling:
                LocalTimeDaysRemainder = LocalTimeDays - DaysCeiling
                LocalTimeDaysCarry = 1
                LocalTimeMonths += LocalTimeDaysCarry
                LocalTimeDays = LocalTimeDaysRemainder
            else:
                break;
            
            #Carries extra months into years
            if LocalTimeMonths > 12:
                LocalTimeMonthsRemainder = (LocalTimeMonths % 12)
                LocalTimeMonthsCarry = int(round(LocalTimeMonths / 12))
                LocalTimeYears += LocalTimeMonthsCarry
                LocalTimeMonths = LocalTimeMonthsRemainder
        
        
        
        #If any date/time value is under 10, converts value to string and adds a "0" before value for database compatibility
        if LocalTimeMonths < 10:
            LocalTimeMonths = "0" + str(LocalTimeMonths)
        if LocalTimeDays < 10:
            LocalTimeDays = "0" + str(LocalTimeDays)
        if LocalTimeHours < 10:
            LocalTimeHours = "0" + str(LocalTimeHours)
        if LocalTimeMinutes < 10:
            LocalTimeMinutes = "0" + str(LocalTimeMinutes)
        if LocalTimeSeconds < 10:
            LocalTimeSeconds = "0" + str(LocalTimeSeconds)
        
        
        
        #Formats timestamps
        FormattedDurationDate = str(LocalTimeYears) + "-" +  str(LocalTimeMonths) + "-" +  str(LocalTimeDays)
        FormattedDurationTime = str(LocalTimeHours) + ":" +  str(LocalTimeMinutes) + ":" +  str(LocalTimeSeconds)
        FormattedDurationDateTime = str(FormattedDurationDate) + " " + str(FormattedDurationTime)
        
        
        
        #Attempts to change EndPoint to new desired value
        try:
            print ""
            cursor.execute("""UPDATE MTCBook SET EndPoint = "%s" WHERE MTCNumber = %d """ % (FormattedDurationDateTime, MTCNumber))
            db.commit()
            print "Update Successful"
            print ""
            print "MTC Modified: " + str(MTCNumber)
            print "Attribute Modified: End Point"
            print "New Value: " + FormattedDurationDateTime
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    #Updates specified contracts's EndPoint
    if Attribute == "END POINT":
        
        #Gathers current EndPoint and separates into date/time components
        try:
            cursor.execute("""SELECT EndPoint FROM MTCBook WHERE MTCNumber = %d """ % (MTCNumber))
            CurrentEndPoint = cursor.fetchall()[0]
            if CurrentEndPoint != ():
                CurrentEndPoint = str(CurrentEndPoint[0])
                
                CurrentEndPointYear = CurrentEndPoint[:4]
                CurrentEndPointMonth = CurrentEndPoint[5:7]
                CurrentEndPointDay = CurrentEndPoint[8:10]
                CurrentEndPointHour = CurrentEndPoint[11:13]
                CurrentEndPointMinute = CurrentEndPoint[14:16]
                CurrentEndPointSecond = CurrentEndPoint[17:19]
            else:
                print "CRITICAL ERROR: MTC has no current end point"
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
        
        
        
        #If any parameter was left blank by user, parameter is set to the current EndPoint interval value
        if NewYear == "":
            NewYear = CurrentEndPointYear
        if NewMonth == "":
            NewMonth = CurrentEndPointMonth
        if NewDay == "":
            NewDay = CurrentEndPointDay
        if NewHour == "":
            NewHour = CurrentEndPointHour
        if NewMinute == "":
            NewMinute = CurrentEndPointMinute
        if NewSecond == "":
            NewSecond = CurrentEndPointSecond
        
        
        
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
        
        
        
        #Forms new EndPoint value by converting date/time components to strings and concatenating
        NewEndPoint = str(NewYear) + "-" + str(NewMonth) + "-" + str(NewDay) + " " + str(NewHour) + ":" + str(NewMinute) + ":" + str(NewSecond)
        
        
        
        #Gathers current DateEntered and separates into date/time components
        try:
            cursor.execute("""SELECT DateEntered FROM MTCBook WHERE MTCNumber = %d """ % (MTCNumber))
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
                print "CRITICAL ERROR: MTC has no current date entered"
                sys.exit()
        except:
            print "ERROR: Database fetch exception"
        
        
        
        #Calculates difference between new interval values and current interval values
        YearsDifference = int(NewYear) - int(CurrentDateEnteredYear)
        MonthsDifference = int(NewMonth) - int(CurrentDateEnteredMonth)
        DaysDifference = int(NewDay) - int(CurrentDateEnteredDay)
        HoursDifference = int(NewHour) - int(CurrentDateEnteredHour)
        MinutesDifference = int(NewMinute) - int(CurrentDateEnteredMinute)
        SecondsDifference = int(NewSecond) - int(CurrentDateEnteredSecond)
        
        
        
        #Sets static variables for looping
        CurrentMonth = int(CurrentEndPointMonth)
        SecondsTotal = 0
        MinutesTotal = 0
        HoursTotal = 0
        DaysTotal = 0
        MonthsTotal = 0
        YearsTotal = 0
        
        
        
        #Tests new EndPoint value for a past date by searching each difference for negative values that,
        #if paired with other negative difference values, would indicate a past date
        if YearsDifference < 0:
            print "CRITICAL ERROR: Negative time differences. End Point cannot be in the past."
            sys.exit()
        elif MonthsDifference < 0:
            if YearsDifference > 0:
                pass
            else:
                print "CRITICAL ERROR: Negative time differences. End Point cannot be in the past."
                sys.exit()
        elif DaysDifference < 0:
            if YearsDifference > 0 or MonthsDifference > 0:
                pass
            else:
                print "CRITICAL ERROR: Negative time differences. End Point cannot be in the past."
                sys.exit()
        elif HoursDifference < 0:
            if YearsDifference > 0 or MonthsDifference > 0 or DaysDifference > 0:
                pass
            else:
                print "CRITICAL ERROR: Negative time differences. End Point cannot be in the past."
                sys.exit()
        elif MinutesDifference < 0:
            if YearsDifference > 0 or MonthsDifference > 0 or DaysDifference > 0 or HoursDifference > 0:
                pass
            else:
                print "CRITICAL ERROR: Negative time differences. End Point cannot be in the past."
                sys.exit()
        elif SecondsDifference < 0:
            if YearsDifference > 0 or MonthsDifference > 0 or DaysDifference > 0 or HoursDifference > 0 or MinutesDifference > 0:
                pass
            else:
                print "CRITICAL ERROR: Negative time differences. End Point cannot be in the past."
                sys.exit()
        
        
        
        #If all differences equal 0, then the date is what it is currently, therefore no update is performed
        if SecondsDifference == 0 and MinutesDifference == 0 and HoursDifference == 0 and DaysDifference == 0 and MonthsDifference == 0 and YearsDifference == 0:
            print "NOTE: No change in date detected. No update performed."
        else:
            
            
            
            #Calculates the total number of seconds it takes to reach new EndPoint from DateEntered
            if SecondsDifference != 0:
                
                #Defines variables of each date/time interval converted to seconds
                YearsSeconds = 31536000
                if CurrentDateEnteredMonth == 1 or CurrentDateEnteredMonth == 3 or CurrentDateEnteredMonth == 5 or CurrentDateEnteredMonth == 7 or CurrentDateEnteredMonth == 8 or CurrentDateEnteredMonth == 10 or CurrentDateEnteredMonth == 12:
                    MonthsSeconds = 2678400
                elif CurrentDateEnteredMonth == 4 or CurrentDateEnteredMonth == 6 or CurrentDateEnteredMonth == 9 or CurrentDateEnteredMonth == 11:
                    MonthsSeconds = 2592000
                else:
                    MonthsSeconds = 2419200
                DaysSeconds = 86400
                HoursSeconds = 3600
                MinutesSeconds = 60
                
                #Loops through function until all differences are 0, adding the proper value to the SecondsTotal 
                #variable during each pass of a positive difference variable is performed
                while 1 == 1:
            
                    if YearsDifference != 0:
                        SecondsTotal += YearsSeconds * YearsDifference
                        YearsDifference = 0
                    #Months are appended once per loop, since time per month is not constant
                    #Because of this, MonthsDifference is subtracted one at a time instead of set to 0,
                    #and SecondsTotal only adds 1 MonthsSeconds value per loop
                    if MonthsDifference != 0:
                        SecondsTotal += MonthsSeconds
                        if MonthsDifference > 0:
                            MonthsDifference -= 1
                        elif MonthsDifference < 0:
                            MonthsDifference += 1
                        CurrentMonth += 1
                    if DaysDifference != 0:
                        SecondsTotal += DaysSeconds * DaysDifference
                        DaysDifference = 0
                    if HoursDifference != 0:
                        SecondsTotal += HoursSeconds * HoursDifference
                        HoursDifference = 0
                    if MinutesDifference != 0:
                        SecondsTotal += MinutesSeconds * MinutesDifference
                        MinutesDifference = 0
                    if SecondsDifference != 0:
                        SecondsTotal += SecondsDifference
                        SecondsDifference = 0
                    
                    #Exits loop if all differences are 0
                    if YearsDifference == 0 and MonthsDifference == 0 and DaysDifference == 0 and HoursDifference == 0 and MinutesDifference == 0 and SecondsDifference == 0:
                        NewDurationList = (SecondsTotal, "SECOND")
                        break;
            
            
            
            #Calculates the total number of minutes it takes to reach new EndPoint from DateEntered
            if MinutesDifference != 0:
                
                #Defines variables of each date/time interval converted to minutes
                YearsMinutes = 525600
                if CurrentDateEnteredMonth == 1 or CurrentDateEnteredMonth == 3 or CurrentDateEnteredMonth == 5 or CurrentDateEnteredMonth == 7 or CurrentDateEnteredMonth == 8 or CurrentDateEnteredMonth == 10 or CurrentDateEnteredMonth == 12:
                    MonthsMinutes = 44640
                elif CurrentDateEnteredMonth == 4 or CurrentDateEnteredMonth == 6 or CurrentDateEnteredMonth == 9 or CurrentDateEnteredMonth == 11:
                    MonthsMinutes = 43200
                else:
                    MonthsMinutes = 40320
                DaysMinutes = 1440
                HoursMinutes = 60
                
                #Loops through function until all differences are 0, adding the proper value to the MinutessTotal 
                #variable during each pass of a positive difference variable is performed
                while 1 == 1:
                
                    if YearsDifference != 0:
                        MinutesTotal += YearsMinutes * YearsDifference
                        YearsDifference = 0
                    #Months are appended once per loop, since time per month is not constant
                    #Because of this, MonthsDifference is subtracted one at a time instead of set to 0,
                    #and SecondsTotal only adds 1 MonthsSeconds value per loop
                    if MonthsDifference != 0:
                        MinutesTotal += MonthsMinutes
                        if MonthsDifference > 0:
                            MonthsDifference -= 1
                        elif MonthsDifference < 0:
                            MonthsDifference += 1
                        CurrentMonth += 1
                    if DaysDifference != 0:
                        MinutesTotal += DaysMinutes * DaysDifference
                        DaysDifference = 0
                    if HoursDifference != 0:
                        MinutesTotal += HoursMinutes * HoursDifference
                        HoursDifference = 0
                    if MinutesDifference != 0:
                        MinutesTotal += MinutesDifference
                        MinutesDifference = 0
                    
                    #Exits loop if all differences are 0
                    if YearsDifference == 0 and MonthsDifference == 0 and DaysDifference == 0 and HoursDifference == 0 and MinutesDifference == 0 and SecondsDifference == 0:
                        NewDurationList = (MinutesTotal, "MINUTE")
                        break;
            
            
            
            
            #Calculates the total number of hours it takes to reach new EndPoint from DateEntered
            if HoursDifference != 0:
                
                #Defines variables of each date/time interval converted to hours
                YearsHours = 8760
                if CurrentDateEnteredMonth == 1 or CurrentDateEnteredMonth == 3 or CurrentDateEnteredMonth == 5 or CurrentDateEnteredMonth == 7 or CurrentDateEnteredMonth == 8 or CurrentDateEnteredMonth == 10 or CurrentDateEnteredMonth == 12:
                    MonthsHours = 744
                elif CurrentDateEnteredMonth == 4 or CurrentDateEnteredMonth == 6 or CurrentDateEnteredMonth == 9 or CurrentDateEnteredMonth == 11:
                    MonthsHours = 720
                else:
                    MonthsHours = 672
                DaysHours = 24
                
                #Loops through function until all differences are 0, adding the proper value to the HoursTotal 
                #variable during each pass of a positive difference variable is performed
                while 1 == 1:
                
                    if YearsDifference != 0:
                        HoursTotal += YearsHours * YearsDifference
                        YearsDifference = 0
                    #Months are appended once per loop, since time per month is not constant
                    #Because of this, MonthsDifference is subtracted one at a time instead of set to 0,
                    #and SecondsTotal only adds 1 MonthsSeconds value per loop
                    if MonthsDifference != 0:
                        HoursTotal += MonthsHours
                        if MonthsDifference > 0:
                            MonthsDifference -= 1
                        elif MonthsDifference < 0:
                            MonthsDifference += 1
                        CurrentMonth += 1
                    if DaysDifference != 0:
                        HoursTotal += DaysHours * DaysDifference
                        DaysDifference = 0
                    if HoursDifference != 0:
                        HoursTotal += HoursDifference
                        HoursDifference = 0
                    
                    #Exits loop if all differences are 0
                    if YearsDifference == 0 and MonthsDifference == 0 and DaysDifference == 0 and HoursDifference == 0 and MinutesDifference == 0 and SecondsDifference == 0:
                        NewDurationList = (HoursTotal, "HOUR")
                        break;
            
            
            
            #Calculates the total number of days it takes to reach new EndPoint from DateEntered
            if DaysDifference != 0:
                
                #Defines variables of each date/time interval converted to days
                YearsDays = 365
                if CurrentDateEnteredMonth == 1 or CurrentDateEnteredMonth == 3 or CurrentDateEnteredMonth == 5 or CurrentDateEnteredMonth == 7 or CurrentDateEnteredMonth == 8 or CurrentDateEnteredMonth == 10 or CurrentDateEnteredMonth == 12:
                    MonthsDays = 31
                elif CurrentDateEnteredMonth == 4 or CurrentDateEnteredMonth == 6 or CurrentDateEnteredMonth == 9 or CurrentDateEnteredMonth == 11:
                    MonthsDays = 30
                else:
                    MonthsDays = 29
                
                #Loops through function until all differences are 0, adding the proper value to the DaysTotal 
                #variable during each pass of a positive difference variable is performed
                while 1 == 1:
                
                    if YearsDifference != 0:
                        DaysTotal += YearsDays * YearsDifference
                        YearsDifference = 0
                    #Months are appended once per loop, since time per month is not constant
                    #Because of this, MonthsDifference is subtracted one at a time instead of set to 0,
                    #and SecondsTotal only adds 1 MonthsSeconds value per loop
                    if MonthsDifference != 0:
                        DaysTotal += MonthsDays
                        if MonthsDifference > 0:
                            MonthsDifference -= 1
                        elif MonthsDifference < 0:
                            MonthsDifference += 1
                        CurrentMonth += 1
                    if DaysDifference != 0:
                        DaysTotal += DaysDifference
                        DaysDifference = 0
                    
                    #Exits loop if all differences are 0
                    if YearsDifference == 0 and MonthsDifference == 0 and DaysDifference == 0 and HoursDifference == 0 and MinutesDifference == 0 and SecondsDifference == 0:
                        NewDurationList = (DaysTotal, "DAY")
                        break;
            
            
            
            #Calculates the total number of months it takes to reach new EndPoint from DateEntered
            if MonthsDifference != 0:
                
                #Defines variables of each date/time interval converted to months
                YearsMonths = 12
                
                if YearsDifference != 0:
                    MonthsTotal += YearsMonths * YearsDifference
                    YearsDifference = 0
                #Months are appended once per loop, since time per month is not constant
                #Because of this, MonthsDifference is subtracted one at a time instead of set to 0,
                #and SecondsTotal only adds 1 MonthsSeconds value per loop
                if MonthsDifference != 0:
                    MonthsTotal += MonthsDifference
                    MonthsDifference = 0
                
                NewDurationList = (MonthsTotal, "MONTH")
            
            
            
            #Calculates the total number of years it takes to reach new EndPoint from DateEntered
            if YearsDifference > 0:
                
                YearsTotal += YearsDifference
                
                NewDurationList = (YearsTotal, "YEAR")
            
            
            
            #Forms new Duration value by converting date/time components to strings and concatenating
            NewDuration = str(float(NewDurationList[0])) + " " + NewDurationList[1]
            
            
            
            #Attempts to change Duration to new desired value
            try:
                cursor.execute("""UPDATE MTCBook SET Duration = "%s" WHERE MTCNumber = %d """ % (NewDuration, MTCNumber))
                db.commit()
                print "Update Successful"
                print ""
                print "MTC Modified: " + str(MTCNumber)
                print "Attribute Modified: Duration"
                print "New Value: " + NewDuration
            except:
                db.rollback()
                print "ERROR: Update Unsuccessful"
            
            
            
            #Attempts to change EndPoint to new desired value
            try:
                print ""
                cursor.execute("""UPDATE MTCBook SET EndPoint = "%s" WHERE MTCNumber = %d """ % (NewEndPoint, MTCNumber))
                db.commit()
                print "Update Successful"
                print ""
                print "MTC Modified: " + str(MTCNumber)
                print "Attribute Modified: End Point"
                print "New Value: " + str(NewEndPoint)
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
    cursor.execute("""INSERT INTO MTCLog(MTCNumber, VersionNumber, LastModified, Username, Price, Volume, Action, InterestCompoundRate, InterestRate, StopLossPrice, FulfillmentPrice, Duration, EndPoint, DividendType, MinimumBorrowerConstraints, UserInterventionConstraints, DateEntered) SELECT MTCNumber, %d, "%s", Username, Price, Volume, Action, InterestCompoundRate, InterestRate, StopLossPrice, FulfillmentPrice, Duration, EndPoint, DividendType, MinimumBorrowerConstraints, UserInterventionConstraints, DateEntered FROM MTCBook WHERE MTCNumber = %d""" % (NewVersion, Attribute.title(), MTCNumber))
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
    
    elif Attribute == "ENDPOINT":
        Attribute = "END POINT"
        print "Updating: End Point"
    
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
        NewInterval = (raw_input("New Interval: ")).upper()
        while 1 == 1:
            if NewInterval != "SECOND" and NewInterval != "MINUTE" and NewInterval != "HOUR" and NewInterval != "DAY":
                print "Value is invalid. Please enter again:"
                print "Choices: [SECOND, MINUTE, HOUR, DAY]"
                NewInterval = (raw_input("New Interval: ")).upper()
            else:
                break;
        NewIntervalValue = float(raw_input("New Value: "))
        NewValue = [NewInterval, NewIntervalValue]
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


