#-------------------------------------------------------------------------------
# Name:        DBUpdateLoan
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

#ErrorHandling
#Check Input Types/Values
#Cascade DateEntered Update To Also Update Duration

import time
import MySQLdb

db = MySQLdb.connect("localhost","root","***","exchangedatabase")

cursor = db.cursor()

cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data



'''Setting Variables'''



ContractNumber = raw_input("Modified Contract: ")
ContractNumber = int(ContractNumber)
while 1 == 1:
    try:
        cursor.execute("""SELECT * FROM LoanBook WHERE ContractNumber = %d""" % (ContractNumber))
        ContractList = cursor.fetchall()
        if ContractList != ():
            print "Contract found"
            break;
        else:
            print "Contract not found. Please enter again:"
            ContractNumber = raw_input("Modified Contract: ")
            ContractNumber = int(ContractNumber)
    except:
        print "ERROR: Database fetch exception"



Attribute = raw_input("Changing Attribute: ")
Attribute = Attribute.upper()
ParameterCheck = "DESCRIBE LoanBook"
try:
    cursor.execute(ParameterCheck)
    TableDescription = cursor.fetchall()
    for Row in TableDescription:
        TargetAttribute = Row[0]
        if TargetAttribute.upper() == Attribute or Attribute == "CONTRACT NUMBER" or Attribute == "DATE ENTERED" or Attribute == "INTEREST COMPOUND RATE" or Attribute == "INTEREST RATE" or Attribute == "END POINT" or Attribute == "DIVIDEND TYPE" or Attribute == "MINIMUM BORROWER CONSTRAINTS" or Attribute == "USER INTERVENTION CONSTRAINTS" or Attribute == "USER REQUESTS":
            break;
    while TargetAttribute.upper() != Attribute and Attribute != "CONTRACT NUMBER" and Attribute != "DATE ENTERED" and Attribute != "INTEREST COMPOUND RATE" and Attribute != "INTEREST RATE" and Attribute != "END POINT" and Attribute != "DIVIDEND TYPE" and Attribute != "MINIMUM BORROWER CONSTRAINTS" and Attribute != "USER INTERVENTION CONSTRAINTS" and Attribute != "USER REQUESTS":
        print "Attribute is invalid. Please enter again:"
        print "Choices: " + str([Row[0] for Row in TableDescription])
        Attribute = raw_input("Changing Attribute: ")
        Attribute = Attribute.upper()
        for Row in TableDescription:
            TargetAttribute = Row[0]
            if TargetAttribute.upper() == Attribute or Attribute == "CONTRACT NUMBER" or Attribute == "DATE ENTERED" or Attribute == "INTEREST COMPOUND RATE" or Attribute == "INTEREST RATE" or Attribute == "END POINT" or Attribute == "DIVIDEND TYPE" or Attribute == "MINIMUM BORROWER CONSTRAINTS" or Attribute == "USER INTERVENTION CONSTRAINTS" or Attribute == "USER REQUESTS":
                    break;
except:
    print "ERROR: Database execution unsuccessful"



if Attribute != "DATEENTERED" and Attribute != "DATE ENTERED" and Attribute != "INTERESTCOMPOUNDRATE" and Attribute != "INTEREST COMPOUND RATE" and Attribute != "DURATION" and Attribute != "ENDPOINT" and Attribute != "END POINT":
    NewValue = raw_input("New Value: ")
    while NewValue == "":
        print "Value is invalid. Please enter again:"
        NewValue = raw_input("New Value: ")
        NewValue = NewValue.upper()



Comment = raw_input("Administrative Comment: ")



'''Standardizing Parameter Names'''



if Attribute == "CONTRACTNUMBER":
    Attribute = "CONTRACT NUMBER"

elif Attribute == "INTERESTCOMPOUNDRATE":
    Attribute = "INTEREST COMPOUND RATE"

elif Attribute == "INTERESTRATE":
    Attribute = "INTEREST RATE"

elif Attribute == "STOPLOSSPRICE":
    Attribute = "STOP LOSS PRICE"

elif Attribute == "FULFILLMENTPRICE":
    Attribute = "FULFILLMENT PRICE"
    
elif Attribute == "ENDPOINT":
    Attribute = "END POINT"
    
elif Attribute == "DIVIDENDTYPE":
    Attribute = "DIVIDEND TYPE"
    
elif Attribute == "MINIMUMBORROWERCONSTRAINTS":
    Attribute = "MINIMUM BORROWER CONSTRAINTS"
    
elif Attribute == "USERINTERVENTIONCONSTRAINTS":
    Attribute = "USER INTERVENTION CONSTRAINTS"
    
elif Attribute == "DATEENTERED":
    Attribute = "DATE ENTERED"



'''Defining/Executing SQL Statements'''



print ""

if Attribute == "CONTRACT NUMBER":
    NewValue = int(NewValue)
    try:
        cursor.execute("UPDATE LoanBook SET ContractNumber = %d WHERE ContractNumber = %d" % (NewValue, ContractNumber))
        db.commit()
        print "Update Successful"
        print ""
        print "Contract modified: " + str(ContractNumber)
        print "Attribute modified: Contract Number"
        print "New value: " + str(NewValue)
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "USERNAME":
    try:
        cursor.execute("""UPDATE LoanBook SET Username = "%s" WHERE ContractNumber = %d""" % (NewValue, ContractNumber))
        db.commit()
        print "Update Successful"
        print ""
        print "Contract modified: " + str(ContractNumber)
        print "Attribute modified: Username"
        print "New value: " + NewValue
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "MEDIUM":
    NewValue = str(NewValue)
    try:
        cursor.execute("""UPDATE LoanBook SET Medium = "%s" WHERE ContractNumber = %d""" % (NewValue, ContractNumber))
        db.commit()
        print "Update Successful"
        print ""
        print "Contract modified: " + str(ContractNumber)
        print "Attribute modified: Medium"
        print "New value: " + str(NewValue)
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "VOLUME":
    NewValue = float(NewValue)
    try:
        cursor.execute("UPDATE LoanBook SET Volume = %s WHERE ContractNUmber = %d" % (NewValue, ContractNumber))
        db.commit()
        print "Update Successful"
        print ""
        print "Contract modified: " + str(ContractNumber)
        print "Attribute modified: Volume"
        print "New value: " + str(NewValue)
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "ACTION":
    try:
        cursor.execute("""UPDATE LoanBook SET Action = "%s" WHERE ContractNUmber = %d""" % (NewValue, ContractNumber))
        db.commit()
        print "Update Successful"
        print ""
        print "Contract modified: " + str(ContractNumber)
        print "Attribute modified: Action"
        print "New value: " + NewValue
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "INTEREST COMPOUND RATE":
    NewInterval = raw_input("New Interval: ")
    NewValue = float(raw_input("New Value: "))
    NewRate = str(NewValue) + " " + NewInterval.upper()
    try:
        cursor.execute("""UPDATE LoanBook SET InterestCompoundRate = "%s" WHERE ContractNumber = %d """ % (NewRate, ContractNumber))
        db.commit()
        print "Update Successful"
        print ""
        print "Contract modified: " + str(ContractNumber)
        print "Attribute modified: Interest Compound Rate"
        print "New value: " + NewRate
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "INTEREST RATE":
    NewValue = float(NewValue)
    try:
        cursor.execute("""UPDATE LoanBook SET InterestRate = %f WHERE ContractNumber = %d """ % (NewValue, ContractNumber))
        db.commit()
        print "Update Successful"
        print ""
        print "Contract modified: " + str(ContractNumber)
        print "Attribute modified: Interest Rate"
        print "New value: " + str(NewValue)
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "DURATION":
    NewInterval = raw_input("New Interval: ")
    NewValue = float(raw_input("New Value: "))
    NewRate = str(NewValue) + " " + NewInterval.upper()
    try:
        cursor.execute("""UPDATE LoanBook SET Duration = "%s" WHERE ContractNumber = %d """ % (NewRate, ContractNumber))
        db.commit()
        print "Update Successful"
        print ""
        print "Contract modified: " + str(ContractNumber)
        print "Attribute modified: Duration"
        print "New value: " + NewRate
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



    DurationTuple = (NewValue, NewInterval.upper())
    print "Duration Tuple: " + str(DurationTuple)

    try:
        cursor.execute("""SELECT DateEntered FROM LoanBook WHERE ContractNumber = %d""" % (ContractNumber))
        Date = cursor.fetchall()[0][0]
    except:
        print "ERROR: Date Unsuccessfully Retrieved"

    LocalTime = str(Date)
    
    LocalTimeYears = int(LocalTime[:4])
    #print LocalTimeYears
    LocalTimeMonths = int(LocalTime[5:7])
    #print LocalTimeMonths
    LocalTimeDays = int(LocalTime[8:10])
    #print LocalTimeDays
    LocalTimeHours = int(LocalTime[11:13])
    #print LocalTimeHours
    LocalTimeMinutes = int(LocalTime[14:16])
    #print LocalTimeMinutes
    LocalTimeSeconds = int(LocalTime[17:19])
    #print LocalTimeSeconds
    
    if DurationTuple[1] == "SECOND":
        LocalTimeSeconds = int(int(LocalTimeSeconds) + DurationTuple[0])
    elif DurationTuple[1] == "MINUTE":
        LocalTimeMinutes = int(int(LocalTimeMinutes) + DurationTuple[0])
    elif DurationTuple[1] == "HOUR":
        LocalTimeHours = int(int(LocalTimeHours) + DurationTuple[0])
    elif DurationTuple[1] == "DAY":
        LocalTimeDays = int(int(LocalTimeDays) + DurationTuple[0])
        print ""
        print LocalTimeDays
    
    if LocalTimeSeconds > 60:
        LocalTimeSecondsRemainder = (LocalTimeSeconds % 60)
        LocalTimeSecondsCarry = int(round(LocalTimeSeconds / 60))
        LocalTimeMinutes += LocalTimeSecondsCarry
        LocalTimeSeconds = LocalTimeSecondsRemainder
    
    if LocalTimeMinutes > 60:
        LocalTimeMinutesRemainder = (LocalTimeMinutes % 60)
        LocalTimeMinutesCarry = int(round(LocalTimeMinutes / 60))
        LocalTimeHours += LocalTimeMinutesCarry
        LocalTimeMinutes = LocalTimeMinutesRemainder
    
    if LocalTimeHours > 24:
        LocalTimeHoursRemainder = (LocalTimeHours % 24)
        LocalTimeHoursCarry = int(round(LocalTimeHours / 24))
        LocalTimeDays += LocalTimeHoursCarry
        LocalTimeHours = LocalTimeHoursRemainder
    
    while 1 == 1:
    
        if LocalTimeMonths == 1 or LocalTimeMonths == 3 or LocalTimeMonths == 5 or LocalTimeMonths == 7 or LocalTimeMonths == 8 or LocalTimeMonths == 10 or LocalTimeMonths == 12:
            DaysCeiling = 31
        elif LocalTimeMonths == 4 or LocalTimeMonths == 6 or LocalTimeMonths == 9 or LocalTimeMonths == 11:
            DaysCeiling = 30
        else:
            DaysCeiling = 28
        
        if LocalTimeDays > DaysCeiling:
            LocalTimeDaysRemainder = LocalTimeDays - DaysCeiling
            LocalTimeDaysCarry = 1
            LocalTimeMonths += LocalTimeDaysCarry
            LocalTimeDays = LocalTimeDaysRemainder
        else:
            break;
            
        if LocalTimeMonths > 12:
            LocalTimeMonthsRemainder = (LocalTimeMonths % 12)
            LocalTimeMonthsCarry = int(round(LocalTimeMonths / 12))
            LocalTimeYears += LocalTimeMonthsCarry
            LocalTimeMonths = LocalTimeMonthsRemainder
    
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
    
    FormattedDatabaseDurationDate = str(LocalTimeYears) + "-" +  str(LocalTimeMonths) + "-" +  str(LocalTimeDays)
    FormattedDurationDate = str(LocalTimeMonths) + "/" +  str(LocalTimeDays) + "/" +  str(LocalTimeHours)
    FormattedDurationTime = str(LocalTimeHours) + ":" +  str(LocalTimeMinutes) + ":" +  str(LocalTimeSeconds)
    FormattedDurationDateTime = str(FormattedDatabaseDurationDate) + " " + str(FormattedDurationTime)
    
    try:
        print ""
        cursor.execute("""UPDATE LoanBook SET EndPoint = "%s" WHERE ContractNumber = %d """ % (FormattedDurationDateTime, ContractNumber))
        db.commit()
        print "Update Successful"
        print ""
        print "Contract modified: " + str(ContractNumber)
        print "Attribute modified: End Point"
        print "New value: " + FormattedDurationDateTime
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "END POINT":

    Year = raw_input("Year: ")
    try:
        Year = int(Year)
        while Year > 2016 or Year <= 2013:
            print "Year not valid. Please enter again:"
            Year = raw_input("Year: ")
            try:
                Year = int(Year)
            except:
                while type(Year) != "int":
                    print "Value must be an integer. Please enter again:"
                    Year = raw_input("Year: ")
                    try:
                        Year = int(Year)
                        break;
                    except:
                        pass;
        DateSearchYearOmit = False
    except:
        if Year == "":
            DateSearchYearOmit = True
        while type(Year) != "int" and Year != "":
            print "Value must be an integer. Please enter again:"
            Year = raw_input("Year: ")
            try:
                Year = int(Year)
                break;
            except:
                pass;
        while (Year > 2016 or Year <= 2013) and Year != "":
            print "Year not valid. Please enter again:"
            Year = raw_input("Year: ")
            try:
                Year = int(Year)
            except:
                while type(Year) != "int":
                    print "Value must be an integer. Please enter again:"
                    Year = raw_input("Year: ")
                    try:
                        Year = int(Year)
                        break;
                    except:
                        pass;
        if Year != "":
            DateSearchYearOmit = False
            


    Month = raw_input("Month: ")
    try:
        Month = int(Month)
        while Month > 12 or Month <= 0:
            print "Month not valid. Please enter again:"
            Month = raw_input("Month: ")
            try:
                Month = int(Month)
            except:
                while type(Month) != "int":
                    print "Value must be an integer. Please enter again:"
                    Month = raw_input("Month: ")
                    try:
                        Month = int(Month)
                        break;
                    except:
                        pass;
        DateSearchMonthOmit = False
    except:
        if Month == "":
            DateSearchMonthOmit = True
        while type(Month) != "int" and Month != "":
            print "Value must be an integer. Please enter again:"
            Month = raw_input("Month: ")
            try:
                Month = int(Month)
                break;
            except:
                pass;
        while (Month > 12 or Month <= 0) and Month != "":
            print "Month not valid. Please enter again:"
            Month = raw_input("Month: ")
            try:
                Month = int(Month)
            except:
                while type(Month) != "int":
                    print "Value must be an integer. Please enter again:"
                    Month = raw_input("Month: ")
                    try:
                        Month = int(Month)
                        break;
                    except:
                        pass;
        if Month != "":
            DateSearchMonthOmit = False

    Day = raw_input("Day: ")
    try:
        Day = int(Day)
        while Day > 31 or Day <= 0:
            print "Day not valid. Please enter again:"
            Day = raw_input("Day: ")
            try:
                Day = int(Day)
            except:
                while type(Day) != "int":
                    print "Value must be an integer. Please enter again:"
                    Day = raw_input("Day: ")
                    try:
                        Day = int(Day)
                        break;
                    except:
                        pass;
        DateSearchDayOmit = False
    except:
        if Day == "":
            DateSearchDayOmit = True
        while type(Day) != "int" and Day != "":
            print "Value must be an integer. Please enter again:"
            Day = raw_input("Year: ")
            try:
                Day = int(Day)
                break;
            except:
                pass;
        while (Day > 31 or Day <= 0) and Day != "":
            print "Day not valid. Please enter again:"
            Day = raw_input("Day: ")
            try:
                Day = int(Day)
            except:
                while type(Day) != "int":
                    print "Value must be an integer. Please enter again:"
                    Day = raw_input("Day: ")
                    try:
                        Day = int(Day)
                        break;
                    except:
                        pass;
        if Day != "":
            DateSearchDayOmit = False

    Hour = raw_input("Hour: ")
    try:
        Hour = int(Hour)
        while Hour > 24 or Hour < 0:
            print "Hour not valid. Please enter again:"
            Hour = raw_input("Hour: ")
            try:
                Hour = int(Hour)
            except:
                while type(Hour) != "int":
                    print "Value must be an integer. Please enter again:"
                    Hour = raw_input("Hour: ")
                    try:
                        Hour = int(Hour)
                        break;
                    except:
                        pass;
        DateSearchHourOmit = False
    except:
        if Hour == "":
            DateSearchHourOmit = True
        while type(Hour) != "int" and Hour != "":
            print "Value must be an integer. Please enter again:"
            Hour = raw_input("Hour: ")
            try:
                Hour = int(Hour)
                break;
            except:
                pass;
        while (Hour > 24 or Hour < 0) and Hour != "":
            print "Hour not valid. Please enter again:"
            Hour = raw_input("Hour: ")
            try:
                Hour = int(Hour)
            except:
                while type(Hour) != "int":
                    print "Value must be an integer. Please enter again:"
                    Hour = raw_input("Hour: ")
                    try:
                        Hour = int(Hour)
                        break;
                    except:
                        pass;
        if Hour != "":
            DateSearchHourOmit = False

    Minute = raw_input("Minute: ")
    try:
        Minute = int(Minute)
        while Minute > 60 or Minute < 0:
            print "Minute not valid. Please enter again:"
            Minute = raw_input("Minute: ")
            try:
                Minute = int(Minute)
            except:
                while type(Minute) != "int":
                    print "Value must be an integer. Please enter again:"
                    Minute = raw_input("Minute: ")
                    try:
                        Minute = int(Minute)
                        break;
                    except:
                        pass;
        DateSearchMinuteOmit = False
    except:
        if Minute == "":
            DateSearchMinuteOmit = True
        while type(Minute) != "int" and Minute != "":
            print "Value must be an integer. Please enter again:"
            Minute = raw_input("Minute: ")
            try:
                Minute = int(Minute)
                break;
            except:
                pass;
        while (Minute > 60 or Minute < 0) and Minute != "":
            print "Minute not valid. Please enter again:"
            Minute = raw_input("Minute: ")
            try:
                Minute = int(Minute)
            except:
                while type(Minute) != "int":
                    print "Value must be an integer. Please enter again:"
                    Minute = raw_input("Minute: ")
                    try:
                        Year = int(Minute)
                        break;
                    except:
                        pass;
        if Minute != "":
            DateSearchMinuteOmit = False

    Second = raw_input("Second: ")
    try:
        Second = int(Second)
        while Second > 60 or Second < 0:
            print "Second not valid. Please enter again:"
            Second = raw_input("Second: ")
            try:
                Second = int(Second)
            except:
                while type(Second) != "int":
                    print "Value must be an integer. Please enter again:"
                    Second = raw_input("Second: ")
                    try:
                        Second = int(Second)
                        break;
                    except:
                        pass;
        DateSearchSecondOmit = False
    except:
        if Second == "":
            DateSearchSecondOmit = True
        while type(Second) != "int" and Second != "":
            print "Value must be an integer. Please enter again:"
            Year = raw_input("Second: ")
            try:
                Second = int(Second)
                break;
            except:
                pass;
        while (Second > 60 or Second < 0) and Second != "":
            print "Second not valid. Please enter again:"
            Second = raw_input("Second: ")
            try:
                Second = int(Second)
            except:
                while type(Second) != "int":
                    print "Value must be an integer. Please enter again:"
                    Second = raw_input("Second: ")
                    try:
                        Second = int(Second)
                        break;
                    except:
                        pass;
        if Second != "":
            DateSearchSecondOmit = False


    ContractDate = ContractList[0][13]
    CurrentEndPoint = ContractList[0][8]

    if DateSearchYearOmit == True:
        YearValue = ""
        for Character in str(CurrentEndPoint)[:4]:
            YearValue += str(Character)
        Year = YearValue
    
    if DateSearchMonthOmit == True:
        MonthValue = ""
        for Character in str(CurrentEndPoint)[5:7]:
            MonthValue += str(Character)
        Month = MonthValue
        
    if DateSearchDayOmit == True:
        DayValue = ""
        for Character in str(CurrentEndPoint)[8:10]:
            DayValue += str(Character)
        Day = DayValue
        
    if DateSearchHourOmit == True:
        HourValue = ""
        for Character in str(CurrentEndPoint)[11:13]:
            HourValue += str(Character)
        Hour = HourValue
        
    if DateSearchMinuteOmit == True:
        MinuteValue = ""
        for Character in str(CurrentEndPoint)[14:16]:
            MinuteValue += str(Character)
        Minute = MinuteValue
    
    if DateSearchSecondOmit == True:
        SecondValue = ""
        for Character in str(CurrentEndPoint)[17:19]:
            SecondValue += str(Character)
        Second = SecondValue

    if Month < 10:
        Month = "0" + str(Month)
    if Day < 10:
        Day = "0" + str(Day)
    if Hour < 10:
        Hour = "0" + str(Hour)
    if Minute < 10:
        Minute = "0" + str(Minute)
    if Second < 10:
        Second = "0" + str(Second)
    
    
    
    FormattedDateTime = str(Year) + "-" + str(Month) + "-" + str(Day) + " " + str(Hour) + ":" + str(Minute) + ":" + str(Second)
    
    '''
    print ""
    print "Current Date Entered: " + str(ContractDate)
    print "Current End Point: " + str(CurrentEndPoint)
    print "Suggested End Point: " + FormattedDateTime
    print ""
    '''
    
    print ""
    
    ContractDate = str(ContractDate)
    
    ContractDateYears = int(ContractDate[:4])
    #print ContractDateYears
    ContractDateMonths = int(ContractDate[5:7])
    #print ContractDateMonths
    ContractDateDays = int(ContractDate[8:10])
    #print ContractDateDays
    ContractDateHours = int(ContractDate[11:13])
    #print ContractDateHours
    ContractDateMinutes = int(ContractDate[14:16])
    #print ContractDateMinutes
    ContractDateSeconds = int(ContractDate[17:19])
    #print ContractDateSeconds
    
    print ""

    YearsDifference = int(Year) - ContractDateYears
    #print YearsDifference
    MonthsDifference = int(Month) - ContractDateMonths
    #print MonthsDifference
    DaysDifference = int(Day) - ContractDateDays
    #print DaysDifference
    HoursDifference = int(Hour) - ContractDateHours
    #print HoursDifference
    MinutesDifference = int(Minute) - ContractDateMinutes
    #print MinutesDifference
    SecondsDifference = int(Second) - ContractDateSeconds
    #print SecondsDifference
        
    CurrentMonth = ContractDateMonths
    SecondsTotal = 0
    MinutesTotal = 0
    HoursTotal = 0
    DaysTotal = 0
    MonthsTotal = 0
    YearsTotal = 0
    
    if SecondsDifference > 0:
        
        YearsSeconds = 31536000
        if CurrentMonth == 1 or CurrentMonth == 3 or CurrentMonth == 5 or CurrentMonth == 7 or CurrentMonth == 8 or CurrentMonth == 10 or CurrentMonth == 12:
            MonthsSeconds = 2678400
        elif CurrentMonth == 4 or CurrentMonth == 6 or CurrentMonth == 9 or CurrentMonth == 11:
            MonthsSeconds = 2592000
        else:
            MonthsSeconds = 2419200
        DaysSeconds = 86400
        HoursSeconds = 3600
        MinutesSeconds = 60
        
        while 1 == 1:
    
            if YearsDifference > 0:
                SecondsTotal += YearsSeconds * YearsDifference
                YearsDifference = 0
            if MonthsDifference > 0:
                SecondsTotal += MonthsSeconds
                MonthsDifference -= 1
                CurrentMonth += 1
            if DaysDifference > 0:
                SecondsTotal += DaysSeconds * DaysDifference
                DaysDifference = 0
            if HoursDifference > 0:
                SecondsTotal += HoursSeconds * HoursDifference
                HoursDifference = 0
            if MinutesDifference > 0:
                SecondsTotal += MinutesSeconds * MinutesDifference
                MinutesDifference = 0
            if SecondsDifference > 0:
                SecondsTotal += SecondsDifference
                SecondsDifference = 0
            
            if YearsDifference == 0 and MonthsDifference == 0 and DaysDifference == 0 and HoursDifference == 0 and MinutesDifference == 0 and SecondsDifference == 0:
                print ""
                print "Seconds Total: " + str(SecondsTotal)
                DurationTuple = (SecondsTotal, "SECOND")
                break;
    
    if MinutesDifference > 0:
        
        YearsMinutes = 525600
        if CurrentMonth == 1 or CurrentMonth == 3 or CurrentMonth == 5 or CurrentMonth == 7 or CurrentMonth == 8 or CurrentMonth == 10 or CurrentMonth == 12:
            MonthsMinutes = 44640
        elif CurrentMonth == 4 or CurrentMonth == 6 or CurrentMonth == 9 or CurrentMonth == 11:
            MonthsMinutes = 43200
        else:
            MonthsMinutes = 40320
        DaysMinutes = 1440
        HoursMinutes = 60
        
        while 1 == 1:
        
            if YearsDifference > 0:
                MinutesTotal += YearsMinutes * YearsDifference
                YearsDifference = 0
            if MonthsDifference > 0:
                MinutesTotal += MonthsMinutes
                MonthsDifference -= 1
                CurrentMonth += 1
            if DaysDifference > 0:
                MinutesTotal += DaysMinutes * DaysDifference
                DaysDifference = 0
            if HoursDifference > 0:
                MinutesTotal += HoursMinutes * HoursDifference
                HoursDifference = 0
            if MinutesDifference > 0:
                MinutesTotal += MinutesDifference
                MinutesDifference = 0
            
            if YearsDifference == 0 and MonthsDifference == 0 and DaysDifference == 0 and HoursDifference == 0 and MinutesDifference == 0 and SecondsDifference == 0:
                print ""
                print "Minutes Total: " + str(MinutesTotal)
                DurationTuple = (MinutesTotal, "MINUTE")
                break;
    
    if HoursDifference > 0:
        
        YearsHours = 8760
        if CurrentMonth == 1 or CurrentMonth == 3 or CurrentMonth == 5 or CurrentMonth == 7 or CurrentMonth == 8 or CurrentMonth == 10 or CurrentMonth == 12:
            MonthsHours = 744
        elif CurrentMonth == 4 or CurrentMonth == 6 or CurrentMonth == 9 or CurrentMonth == 11:
            MonthsHours = 720
        else:
            MonthsHours = 672
        DaysHours = 24
        
        while 1 == 1:
        
            if YearsDifference > 0:
                HoursTotal += YearsHours * YearsDifference
                YearsDifference = 0
            if MonthsDifference > 0:
                HoursTotal += MonthsHours
                MonthsDifference -= 1
                CurrentMonth += 1
            if DaysDifference > 0:
                HoursTotal += DaysHours * DaysDifference
                DaysDifference = 0
            if HoursDifference > 0:
                HoursTotal += HoursDifference
                HoursDifference = 0
            
            if YearsDifference == 0 and MonthsDifference == 0 and DaysDifference == 0 and HoursDifference == 0 and MinutesDifference == 0 and SecondsDifference == 0:
                print ""
                print "Hours Total: " + str(HoursTotal)
                DurationTuple = (HoursTotal, "HOUR")
                break;
    
    if DaysDifference > 0:
        
        YearsDays = 365
        if CurrentMonth == 1 or CurrentMonth == 3 or CurrentMonth == 5 or CurrentMonth == 7 or CurrentMonth == 8 or CurrentMonth == 10 or CurrentMonth == 12:
            MonthsDays = 31
        elif CurrentMonth == 4 or CurrentMonth == 6 or CurrentMonth == 9 or CurrentMonth == 11:
            MonthsDays = 30
        else:
            MonthsDays = 29
        
        while 1 == 1:
        
            if YearsDifference > 0:
                DaysTotal += YearsDays * YearsDifference
                YearsDifference = 0
            if MonthsDifference > 0:
                DaysTotal += MonthsDays
                MonthsDifference -= 1
                CurrentMonth += 1
            if DaysDifference > 0:
                DaysTotal += DaysDifference
                DaysDifference = 0
            
            if YearsDifference == 0 and MonthsDifference == 0 and DaysDifference == 0 and HoursDifference == 0 and MinutesDifference == 0 and SecondsDifference == 0:
                print ""
                print "Days Total: " + str(DaysTotal)
                DurationTuple = (DaysTotal, "DAY")
                break;
    
    if MonthsDifference > 0:
        
        YearsMonths = 12
        
        if YearsDifference > 0:
            MonthsTotal += YearsMonths * YearsDifference
            YearsDifference = 0
        if MonthsDifference > 0:
            MonthsTotal += MonthsDifference
            MonthsDifference = 0
        
        print ""
        print "Months Total: " + str(MonthsTotal)
        DurationTuple = (MonthsTotal, "MONTH")
    
    if YearsDifference > 0:
        
        YearsTotal += YearsDifference
        
        print ""
        print "Years Total: " + str(YearsTotal)
        DurationTuple = (YearsTotal, "YEAR")
    
    
    
    NewDuration = str(float(DurationTuple[0])) + " " + DurationTuple[1]
    print ""
    #print "Duration Tuple: " + str(DurationTuple)
    print "New Duration: " + NewDuration
    print "New End Point: " + FormattedDateTime
    
    
    
    try:
        print ""
        cursor.execute("""UPDATE LoanBook SET EndPoint = "%s" WHERE ContractNumber = %d """ % (FormattedDateTime, ContractNumber))
        db.commit()
        print "Update Successful"
        print ""
        print "Contract modified: " + str(ContractNumber)
        print "Attribute modified: End Point"
        print "New value: " + FormattedDateTime
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"
    
    try:
        print ""
        cursor.execute("""UPDATE LoanBook SET Duration = "%s" WHERE ContractNumber = %d """ % (NewDuration, ContractNumber))
        db.commit()
        print "Update Successful"
        print ""
        print "Contract modified: " + str(ContractNumber)
        print "Attribute modified: Duration"
        print "New value: " + NewDuration
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "DIVIDEND TYPE":
    try:
        cursor.execute("""UPDATE LoanBook SET DividendType = "%s" WHERE ContractNumber = %d """ % (NewValue, ContractNumber))
        db.commit()
        print "Update Successful"
        print ""
        print "Contract modified: " + str(ContractNumber)
        print "Attribute modified: Dividend Type"
        print "New value: " + NewValue
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "MINIMUM BORROWER CONSTRAINTS":
    NewValue = int(NewValue)
    try:
        cursor.execute("UPDATE LoanBook SET MinimumBorrowerConstraints = %d WHERE ContractNumber = %d" % (NewValue, ContractNumber))
        db.commit()
        print "Update Successful"
        print ""
        print "Contract modified: " + str(ContractNumber)
        print "Attribute modified: Minimum Borrower Constraints"
        print "New value: " + str(NewValue)
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "USER INTERVENTION CONSTRAINTS":
    NewValue = int(NewValue)
    try:
        cursor.execute("UPDATE LoanBook SET UserInterventionConstraints = %d WHERE ContractNumber = %d" % (NewValue, ContractNumber))
        db.commit()
        print "Update Successful"
        print ""
        print "Contract modified: " + str(ContractNumber)
        print "Attribute modified: User Intervention Constraints"
        print "New value: " + str(NewValue)
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "USER REQUESTS":
    NewValue = int(NewValue)
    try:
        cursor.execute("UPDATE LoanBook SET UserRequests = %d WHERE ContractNumber = %d" % (NewValue, ContractNumber))
        db.commit()
        print "Update Successful"
        print ""
        print "Contract modified: " + str(ContractNumber)
        print "Attribute modified: User Requests"
        print "New value: " + str(NewValue)
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "DATE ENTERED":

    Year = raw_input("Year: ")
    try:
        Year = int(Year)
        while Year > 2014 or Year <= 2013:
            print "Year not valid. Please enter again:"
            Year = raw_input("Year: ")
            try:
                Year = int(Year)
            except:
                while type(Year) != "int":
                    print "Value must be an integer. Please enter again:"
                    Year = raw_input("Year: ")
                    try:
                        Year = int(Year)
                        break;
                    except:
                        pass;
        DateSearchYearOmit = False
    except:
        if Year == "":
            DateSearchYearOmit = True
        while type(Year) != "int" and Year != "":
            print "Value must be an integer. Please enter again:"
            Year = raw_input("Year: ")
            try:
                Year = int(Year)
                break;
            except:
                pass;
        while (Year > 2014 or Year <= 2013) and Year != "":
            print "Year not valid. Please enter again:"
            Year = raw_input("Year: ")
            try:
                Year = int(Year)
            except:
                while type(Year) != "int":
                    print "Value must be an integer. Please enter again:"
                    Year = raw_input("Year: ")
                    try:
                        Year = int(Year)
                        break;
                    except:
                        pass;
        if Year != "":
            DateSearchYearOmit = False
            


    Month = raw_input("Month: ")
    try:
        Month = int(Month)
        while Month > 12 or Month <= 0:
            print "Month not valid. Please enter again:"
            Month = raw_input("Month: ")
            try:
                Month = int(Month)
            except:
                while type(Month) != "int":
                    print "Value must be an integer. Please enter again:"
                    Month = raw_input("Month: ")
                    try:
                        Month = int(Month)
                        break;
                    except:
                        pass;
        DateSearchMonthOmit = False
    except:
        if Month == "":
            DateSearchMonthOmit = True
        while type(Month) != "int" and Month != "":
            print "Value must be an integer. Please enter again:"
            Month = raw_input("Month: ")
            try:
                Month = int(Month)
                break;
            except:
                pass;
        while (Month > 12 or Month <= 0) and Month != "":
            print "Month not valid. Please enter again:"
            Month = raw_input("Month: ")
            try:
                Month = int(Month)
            except:
                while type(Month) != "int":
                    print "Value must be an integer. Please enter again:"
                    Month = raw_input("Month: ")
                    try:
                        Month = int(Month)
                        break;
                    except:
                        pass;
        if Month != "":
            DateSearchMonthOmit = False

    Day = raw_input("Day: ")
    try:
        Day = int(Day)
        while Day > 31 or Day <= 0:
            print "Day not valid. Please enter again:"
            Day = raw_input("Day: ")
            try:
                Day = int(Day)
            except:
                while type(Day) != "int":
                    print "Value must be an integer. Please enter again:"
                    Day = raw_input("Day: ")
                    try:
                        Day = int(Day)
                        break;
                    except:
                        pass;
        DateSearchDayOmit = False
    except:
        if Day == "":
            DateSearchDayOmit = True
        while type(Day) != "int" and Day != "":
            print "Value must be an integer. Please enter again:"
            Day = raw_input("Year: ")
            try:
                Day = int(Day)
                break;
            except:
                pass;
        while (Day > 31 or Day <= 0) and Day != "":
            print "Day not valid. Please enter again:"
            Day = raw_input("Day: ")
            try:
                Day = int(Day)
            except:
                while type(Day) != "int":
                    print "Value must be an integer. Please enter again:"
                    Day = raw_input("Day: ")
                    try:
                        Day = int(Day)
                        break;
                    except:
                        pass;
        if Day != "":
            DateSearchDayOmit = False

    Hour = raw_input("Hour: ")
    try:
        Hour = int(Hour)
        while Hour > 24 or Hour < 0:
            print "Hour not valid. Please enter again:"
            Hour = raw_input("Hour: ")
            try:
                Hour = int(Hour)
            except:
                while type(Hour) != "int":
                    print "Value must be an integer. Please enter again:"
                    Hour = raw_input("Hour: ")
                    try:
                        Hour = int(Hour)
                        break;
                    except:
                        pass;
        DateSearchHourOmit = False
    except:
        if Hour == "":
            DateSearchHourOmit = True
        while type(Hour) != "int" and Hour != "":
            print "Value must be an integer. Please enter again:"
            Hour = raw_input("Hour: ")
            try:
                Hour = int(Hour)
                break;
            except:
                pass;
        while (Hour > 24 or Hour < 0) and Hour != "":
            print "Hour not valid. Please enter again:"
            Hour = raw_input("Hour: ")
            try:
                Hour = int(Hour)
            except:
                while type(Hour) != "int":
                    print "Value must be an integer. Please enter again:"
                    Hour = raw_input("Hour: ")
                    try:
                        Hour = int(Hour)
                        break;
                    except:
                        pass;
        if Hour != "":
            DateSearchHourOmit = False

    Minute = raw_input("Minute: ")
    try:
        Minute = int(Minute)
        while Minute > 60 or Minute < 0:
            print "Minute not valid. Please enter again:"
            Minute = raw_input("Minute: ")
            try:
                Minute = int(Minute)
            except:
                while type(Minute) != "int":
                    print "Value must be an integer. Please enter again:"
                    Minute = raw_input("Minute: ")
                    try:
                        Minute = int(Minute)
                        break;
                    except:
                        pass;
        DateSearchMinuteOmit = False
    except:
        if Minute == "":
            DateSearchMinuteOmit = True
        while type(Minute) != "int" and Minute != "":
            print "Value must be an integer. Please enter again:"
            Minute = raw_input("Minute: ")
            try:
                Minute = int(Minute)
                break;
            except:
                pass;
        while (Minute > 60 or Minute < 0) and Minute != "":
            print "Minute not valid. Please enter again:"
            Minute = raw_input("Minute: ")
            try:
                Minute = int(Minute)
            except:
                while type(Minute) != "int":
                    print "Value must be an integer. Please enter again:"
                    Minute = raw_input("Minute: ")
                    try:
                        Year = int(Minute)
                        break;
                    except:
                        pass;
        if Minute != "":
            DateSearchMinuteOmit = False

    Second = raw_input("Second: ")
    try:
        Second = int(Second)
        while Second > 60 or Second < 0:
            print "Second not valid. Please enter again:"
            Second = raw_input("Second: ")
            try:
                Second = int(Second)
            except:
                while type(Second) != "int":
                    print "Value must be an integer. Please enter again:"
                    Second = raw_input("Second: ")
                    try:
                        Second = int(Second)
                        break;
                    except:
                        pass;
        DateSearchSecondOmit = False
    except:
        if Second == "":
            DateSearchSecondOmit = True
        while type(Second) != "int" and Second != "":
            print "Value must be an integer. Please enter again:"
            Year = raw_input("Second: ")
            try:
                Second = int(Second)
                break;
            except:
                pass;
        while (Second > 60 or Second < 0) and Second != "":
            print "Second not valid. Please enter again:"
            Second = raw_input("Second: ")
            try:
                Second = int(Second)
            except:
                while type(Second) != "int":
                    print "Value must be an integer. Please enter again:"
                    Second = raw_input("Second: ")
                    try:
                        Second = int(Second)
                        break;
                    except:
                        pass;
        if Second != "":
            DateSearchSecondOmit = False



    ContractDate = ContractList[0][13]

    if DateSearchYearOmit == True:
        YearValue = ""
        for Character in str(ContractDate)[:4]:
            YearValue += str(Character)
        Year = YearValue
    
    if DateSearchMonthOmit == True:
        MonthValue = ""
        for Character in str(ContractDate)[5:7]:
            MonthValue += str(Character)
        Month = MonthValue
        
    if DateSearchDayOmit == True:
        DayValue = ""
        for Character in str(ContractDate)[8:10]:
            DayValue += str(Character)
        Day = DayValue
        
    if DateSearchHourOmit == True:
        HourValue = ""
        for Character in str(ContractDate)[11:13]:
            HourValue += str(Character)
        Hour = HourValue
        
    if DateSearchMinuteOmit == True:
        MinuteValue = ""
        for Character in str(ContractDate)[14:16]:
            MinuteValue += str(Character)
        Minute = MinuteValue
    
    if DateSearchSecondOmit == True:
        SecondValue = ""
        for Character in str(ContractDate)[17:19]:
            SecondValue += str(Character)
        Second = SecondValue

    if Month < 10:
        Month = "0" + str(Month)
    if Day < 10:
        Day = "0" + str(Day)
    if Hour < 10:
        Hour = "0" + str(Hour)
    if Minute < 10:
        Minute = "0" + str(Minute)
    if Second < 10:
        Second = "0" + str(Second)
        
    FormattedDateTime = str(Year) + "-" + str(Month) + "-" + str(Day) + " " + str(Hour) + ":" + str(Minute) + ":" + str(Second)

    try:
        cursor.execute("""UPDATE LoanBook SET DateEntered = "%s" WHERE ContractNumber = %d""" % (FormattedDateTime, ContractNumber))
        db.commit()
        print "Update Successful"
        print ""
        print "Contract modified: " + str(ContractNumber)
        print "Attribute modified: Date Entered"
        print "New value: " + str(FormattedDateTime)
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



'''Logging Control'''


    
Employee = "***333"

ContractID = "Loan " + str(ContractNumber)

try:
    print ""
    cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update Loan", ContractID, Attribute.title(), Comment))
    db.commit()
    print "Control Successfully Logged"
except:
    print "ERROR: Control Unsuccessfully Logged"

if Attribute == "DURATION":
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update Loan", ContractID, "End Point", Comment))
        db.commit()
        print "Control Successfully Logged"
    except:
        print "ERROR: Control Unsuccessfully Logged"

if Attribute == "END POINT":
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update Loan", ContractID, "Duration", Comment))
        db.commit()
        print "Control Successfully Logged"
    except:
        print "ERROR: Control Unsuccessfully Logged"



db.close()