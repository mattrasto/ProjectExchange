#-------------------------------------------------------------------------------
# Name:        DBUpdateUser
# Version:     1.0
# Purpose:
#
# Author:      Matthew
#
# Created:     04/07/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    05/27/2014
#-------------------------------------------------------------------------------

import MySQLdb

db = MySQLdb.connect("localhost","root","***","exchangedatabase")

cursor = db.cursor()

cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data



'''Setting Variables'''



Username = raw_input("Modified User: ")
Username = Username.upper()
UsernameCheck = """SELECT * FROM UserBook"""
try:
    cursor.execute(UsernameCheck)
    Usernames = cursor.fetchall()
    for User in Usernames:
        TargetUsername = User[0]
        if TargetUsername.upper() == Username:
            print "User found."
            break;
    while TargetUsername.upper() != Username:
            print "User not found. Please enter again:"
            Username = raw_input("Modified User: ")
            Username = Username.upper()
            try:
                cursor.execute(UsernameCheck)
                Usernames = cursor.fetchall()
                for User in Usernames:
                    TargetUsername = User[0]
                    if TargetUsername.upper() == Username:
                        print "User found."
                        break;
            except:
                "ERROR: Database fetch exception"
except:
    print "ERROR: Database fetch exception"



Attribute = raw_input("Changing Attribute: ")
Attribute = Attribute.upper()
for Header in cursor.description:
    TargetAttribute = Header[0]
    if TargetAttribute.upper() == Attribute or Attribute == "USD CREDIT" or Attribute == "BTC CREDIT" or Attribute == "JOIN DATE" or Attribute == "FIRST NAME" or Attribute == "LAST NAME" or Attribute == "BANK NAME" or Attribute == "TRADING FEE":
        break;
while TargetAttribute.upper() != Attribute and Attribute != "USD CREDIT" and Attribute != "BTC CREDIT" and Attribute != "JOIN DATE" and Attribute != "FIRST NAME" and Attribute != "LAST NAME" and Attribute != "BANK NAME" and Attribute != "TRADING FEE":
    print "Attribute is invalid. Please enter again:"
    print "Choices: " + str([Header[0] for Header in cursor.description])
    Attribute = raw_input("Changing Attribute: ")
    Attribute = Attribute.upper()
    for Header in cursor.description:
        TargetAttribute = Header[0]
        if TargetAttribute.upper() == Attribute or Attribute == "USD CREDIT" or Attribute == "BTC CREDIT" or Attribute == "JOIN DATE" or Attribute == "FIRST NAME" or Attribute == "LAST NAME" or Attribute == "BANK NAME" or Attribute == "TRADING FEE":
            break;



if Attribute != "JOINDATE" and Attribute != "JOIN DATE":
    NewValue = raw_input("New Value: ")
    while NewValue == "":
        print "Value is invalid. Please enter again:"
        NewValue = raw_input("New Value: ")
        NewValue = NewValue.upper()



Comment = raw_input("Administrative Comment: ")



'''Defining/Executing SQL Statements'''



if Attribute == "USERNAME" or Attribute == "USER NAME":
    try:
        cursor.execute("UPDATE UserBook SET Username = %s WHERE Username = %s" % (NewValue, Username))
        db.commit()
        print "Update Successful"
        print ""
        print "User modified: " + Username.capitalize()
        print "Attribute modified: Username"
        print "New value: " + NewValue
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "PASSWORD":
    try:
        cursor.execute("UPDATE UserBook SET Password = %s WHERE Username = %s" % (NewValue, Username))
        db.commit()
        print "Update Successful"
        print ""
        print "User modified: " + Username.capitalize()
        print "Attribute modified: Password"
        print "New value: " + NewValue
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "EMAIL":
    try:
        cursor.execute("UPDATE UserBook SET Email = %s WHERE Username = %s" % (NewValue, Username))
        db.commit()
        print "Update Successful"
        print ""
        print "User modified: " + Username.capitalize()
        print "Attribute modified: Email"
        print "New value: " + NewValue
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "USDCREDIT" or Attribute == "USD CREDIT":
    try:
        cursor.execute("UPDATE UserBook SET USDCredit = %s WHERE Username = %s" % (NewValue, Username))
        db.commit()
        print "Update Successful"
        print ""
        print "User modified: " + Username.capitalize()
        print "Attribute modified: USD Credit"
        print "New value: " + NewValue
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "BTCCREDIT" or Attribute == "BTC CREDIT":
    try:
        cursor.execute("UPDATE UserBook SET BTCCredit = %s WHERE Username = %s" % (NewValue, Username))
        db.commit()
        print "Update Successful"
        print ""
        print "User modified: " + Username.capitalize()
        print "Attribute modified: BTC Credit"
        print "New value: " + NewValue
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "JOINDATE" or Attribute == "JOIN DATE":



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



    if DateSearchYearOmit == True:
        YearValue = ""
        for Character in str(User[5])[:4]:
            YearValue += str(Character)
        Year = YearValue
    
    if DateSearchMonthOmit == True:
        MonthValue = ""
        for Character in str(User[5])[5:7]:
            MonthValue += str(Character)
        Month = MonthValue
        
    if DateSearchDayOmit == True:
        DayValue = ""
        for Character in str(User[5])[8:10]:
            DayValue += str(Character)
        Day = DayValue
        
    if DateSearchHourOmit == True:
        HourValue = ""
        for Character in str(User[5])[11:13]:
            HourValue += str(Character)
        Hour = HourValue
        
    if DateSearchMinuteOmit == True:
        MinuteValue = ""
        for Character in str(User[5])[14:16]:
            MinuteValue += str(Character)
        Minute = MinuteValue
    
    if DateSearchSecondOmit == True:
        SecondValue = ""
        for Character in str(User[5])[17:19]:
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

    cursor.execute("""UPDATE UserBook SET JoinDate = "%s" WHERE Username = "%s" """ % (FormattedDateTime, Username))
    db.commit()
    print "Update Successful"
    print ""
    print "User modified: " + Username.capitalize()
    print "Attribute modified: Join Date"
    print "New value: " + str(FormattedDateTime)

    db.rollback()
    print "ERROR: Update Unsuccessful"



if Attribute == "FIRSTNAME" or Attribute == "FIRST NAME":
    try:
        cursor.execute("UPDATE UserBook SET FirstName = %s WHERE Username = %s" % (NewValue, Username))
        db.commit()
        print "Update Successful"
        print ""
        print "User modified: " + Username.capitalize()
        print "Attribute modified: First Name"
        print "New value: " + NewValue
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "LASTNAME" or Attribute == "LAST NAME":
    try:
        cursor.execute("UPDATE UserBook SET LastName = %s WHERE Username = %s" % (NewValue, Username))
        db.commit()
        print "Update Successful"
        print ""
        print "User modified: " + Username.capitalize()
        print "Attribute modified: Last Name"
        print "New value: " + NewValue
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "BANKNAME" or Attribute == "BANK NAME":
    try:
        cursor.execute("UPDATE UserBook SET BankName = %s WHERE Username = %s", (NewValue, Username))
        db.commit()
        print "Update Successful"
        print ""
        print "User modified: " + Username.capitalize()
        print "Attribute modified: Bank Name"
        print "New value: " + NewValue
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "ADDRESS":
    try:
        cursor.execute("UPDATE UserBook SET Address = %s WHERE Username = %s" % (NewValue, Username))
        db.commit()
        print "Update Successful"
        print ""
        print "User modified: " + Username.capitalize()
        print "Attribute modified: Address"
        print "New value: " + NewValue
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "VERIFIED":
    try:
        cursor.execute("UPDATE UserBook SET Verified = %s WHERE Username = %s" % (NewValue, Username))
        db.commit()
        print "Update Successful"
        print ""
        print "User modified: " + Username.capitalize()
        print "Attribute modified: Verified"
        print "New value: " + NewValue
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "TRADINGFEE" or Attribute == "TRADING FEE":
    try:
        cursor.execute("UPDATE UserBook SET TradingFee = %s WHERE Username = %s" % (NewValue, Username))
        db.commit()
        print "Update Successful"
        print ""
        print "User modified: " + Username.capitalize()
        print "Attribute modified: Trading Fee"
        print "New value: " + NewValue
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



if Attribute == "VOLUME":
    try:
        cursor.execute("UPDATE UserBook SET Volume = %s WHERE Username = %s" % (NewValue, Username))
        db.commit()
        print "Update Successful"
        print ""
        print "User modified: " + Username.capitalize()
        print "Attribute modified: Volume"
        print "New value: " + NewValue
    except:
        db.rollback()
        print "ERROR: Update Unsuccessful"



'''Logging Control'''
    

    
Employee = "***333"

try:
    print ""
    cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update User", Username.capitalize(), Attribute.title(), Comment))
    db.commit()
    print "Control Successfully Logged"
except:
    print "ERROR: Control Unsuccessfully Logged"



db.close()