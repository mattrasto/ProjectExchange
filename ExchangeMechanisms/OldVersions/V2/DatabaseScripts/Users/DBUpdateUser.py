#-------------------------------------------------------------------------------
# Name:        DBUpdateUser
# Version:     2.0
# Purpose:
#
# Author:      Matthew
#
# Created:     04/07/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/15/2014
#-------------------------------------------------------------------------------

import MySQLdb



def main(Username, Attribute, NewValue):

    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    
    
    '''Verifying User'''
    
    
    
    #Exits if user does not exist
    try:
        print ""
        cursor.execute("""SELECT * FROM UserBook WHERE Username = "%s" """ % (Username))
        User = cursor.fetchone()
        if User != None:
            #print "User found"
            pass
        else:
            print "CRITICAL ERROR: User not found"
            sys.exit()
    except SystemExit:
        sys.exit()
    except:
        print "ERROR: Database fetch exception"
        sys.exit()
    
    
    
    '''Defining/Executing SQL Statements'''
    
    
    
    #Updates specified user's Username
    if Attribute == "USERNAME" or Attribute == "USER NAME":
        #Converts Username value to string type and capitalizes
        try:
            NewValue = str(NewValue.capitalize())
        except:
            print "CRITICAL ERROR: Username unable to be converted to string"
            sys.exit()
        try:
            cursor.execute("""UPDATE UserBook SET Username = "%s" WHERE Username = "%s" """ % (NewValue, Username))
            db.commit()
            print "Update Successful"
            print ""
            print "User Modified: " + Username.capitalize()
            print "Attribute Modified: Username"
            print "New Value: " + str(NewValue)
        except:
            #If unsuccessful, searches for existing users and displays any if found
            db.rollback()
            print "ERROR: Update Unsuccessful"
            cursor.execute("SELECT * FROM UserBook WHERE Username = %d" % (NewValue))
            ExistingUsers = cursor.fetchall()
            if ExistingUsers != ():
                print "ERROR: Username is already in use:"
                print ""
                print ExistingUsers
            else:
                print "Ensure that an existing user has been entered"
    
    
    
    if Attribute == "PASSWORD":
        #Converts Password value to string type
        try:
            NewValue = str(NewValue)
        except:
            print "CRITICAL ERROR: Password unable to be converted to string"
            sys.exit()
        try:
            cursor.execute("""UPDATE UserBook SET Password = "%s" WHERE Username = "%s" """ % (NewValue, Username))
            db.commit()
            print "Update Successful"
            print ""
            print "User Modified: " + Username.capitalize()
            print "Attribute Modified: Password"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    if Attribute == "EMAIL":
        #Converts Email value to string type
        try:
            NewValue = str(NewValue)
        except:
            print "CRITICAL ERROR: Email unable to be converted to string"
            sys.exit()
        try:
            cursor.execute("""UPDATE UserBook SET Email = "%s" WHERE Username = "%s" """ % (NewValue, Username))
            db.commit()
            print "Update Successful"
            print ""
            print "User Modified: " + Username.capitalize()
            print "Attribute Modified: Email"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    if Attribute == "USD CREDIT":
        #Converts USDCredit value to float type
        try:
            NewValue = float(NewValue)
        except:
            print "CRITICAL ERROR: USD Credit unable to be converted to float"
            sys.exit()
        try:
            cursor.execute("""UPDATE UserBook SET USDCredit = "%s" WHERE Username = "%s" """ % (NewValue, Username))
            db.commit()
            print "Update Successful"
            print ""
            print "User Modified: " + Username.capitalize()
            print "Attribute Modified: USD Credit"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    if Attribute == "BTC CREDIT":
        #Converts BTCCredit value to float type
        try:
            NewValue = float(NewValue)
        except:
            print "CRITICAL ERROR: BTC Credit unable to be converted to float"
            sys.exit()
        try:
            cursor.execute("""UPDATE UserBook SET BTCCredit = "%s" WHERE Username = "%s" """ % (NewValue, Username))
            db.commit()
            print "Update Successful"
            print ""
            print "User Modified: " + Username.capitalize()
            print "Attribute Modified: BTC Credit"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    if Attribute == "JOINDATE" or Attribute == "JOIN DATE":
        
        #Gathers current JoinDate and separates into date/time components
        try:
            cursor.execute("""SELECT JoinDate FROM UserBook WHERE Username = "%s" """ % (Username))
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
                print "CRITICAL ERROR: User has no current join date"
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
        
        
        
        #If user left any interval blank, turns search parameter to "%" for wildcard searching in database
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
        
        
        
        #Forms new DateEntered value by converting date/time components to strings and concatenating
        NewValue = str(NewYear) + "-" + str(NewMonth) + "-" + str(NewDay) + " " + str(NewHour) + ":" + str(NewMinute) + ":" + str(NewSecond)
        
        
        
        try:
            cursor.execute("""UPDATE UserBook SET JoinDate = "%s" WHERE Username = "%s" """ % (NewValue, Username))
            db.commit()
            print "Update Successful"
            print ""
            print "User Modified: " + Username.capitalize()
            print "Attribute Modified: Join Date"
            print "New Value: " + str(NewValue)
        except:
            print "ERROR: Database Fetch Exception"
    
    
    
    if Attribute == "FIRST NAME":
        #Converts FirstName value to string type and capitalizes
        try:
            NewValue = str(NewValue.capitalize())
        except:
            print "CRITICAL ERROR: First Name unable to be converted to string"
            sys.exit()
        try:
            cursor.execute("""UPDATE UserBook SET FirstName = "%s" WHERE Username = "%s" """ % (NewValue, Username))
            db.commit()
            print "Update Successful"
            print ""
            print "User Modified: " + Username.capitalize()
            print "Attribute Modified: First Name"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    if Attribute == "LAST NAME":
        #Converts LastName value to string type and capitalizes
        try:
            NewValue = str(NewValue.capitalize())
        except:
            print "CRITICAL ERROR: Last Name unable to be converted to string"
            sys.exit()
        try:
            cursor.execute("""UPDATE UserBook SET LastName = "%s" WHERE Username = "%s" """ % (NewValue, Username))
            db.commit()
            print "Update Successful"
            print ""
            print "User Modified: " + Username.capitalize()
            print "Attribute Modified: Last Name"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    if Attribute == "BANK NAME":
        #Converts BankName value to string type and capitalizes
        try:
            NewValue = str(NewValue.title())
        except:
            print "CRITICAL ERROR: Last Name unable to be converted to string"
            sys.exit()
        try:
            cursor.execute("""UPDATE UserBook SET BankName = "%s" WHERE Username = "%s" """ % (NewValue, Username))
            db.commit()
            print "Update Successful"
            print ""
            print "User Modified: " + Username.capitalize()
            print "Attribute Modified: Bank Name"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    if Attribute == "ADDRESS":
        #Converts Address value to string type and capitalizes
        try:
            NewValue = str(NewValue.title())
        except:
            print "CRITICAL ERROR: Address unable to be converted to string"
            sys.exit()
        try:
            cursor.execute("""UPDATE UserBook SET Address = "%s" WHERE Username = "%s" """ % (NewValue, Username))
            db.commit()
            print "Update Successful"
            print ""
            print "User Modified: " + Username.capitalize()
            print "Attribute Modified: Address"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    if Attribute == "VERIFIED":
        #Converts Verified value to integer type
        try:
            NewValue = int(NewValue)
        except:
            print "CRITICAL ERROR: Verified unable to be converted to integer"
            sys.exit()
        try:
            cursor.execute("""UPDATE UserBook SET Verified = "%s" WHERE Username = "%s" """ % (NewValue, Username))
            db.commit()
            print "Update Successful"
            print ""
            print "User Modified: " + Username.capitalize()
            print "Attribute Modified: Verified"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    if Attribute == "TRADING FEE":
        #Converts TradingFee value to float type
        try:
            NewValue = float(NewValue)
        except:
            print "CRITICAL ERROR: Trading Fee unable to be converted to float"
            sys.exit()
        try:
            cursor.execute("""UPDATE UserBook SET TradingFee = "%s" WHERE Username = "%s" """% (NewValue, Username))
            db.commit()
            print "Update Successful"
            print ""
            print "User Modified: " + Username.capitalize()
            print "Attribute Modified: Trading Fee"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    if Attribute == "VOLUME":
        #Converts Volume value to float type
        try:
            NewValue = float(NewValue)
        except:
            print "CRITICAL ERROR: Volume unable to be converted to float"
            sys.exit()
        try:
            cursor.execute("""UPDATE UserBook SET Volume = "%s" WHERE Username = "%s" """ % (NewValue, Username))
            db.commit()
            print "Update Successful"
            print ""
            print "User Modified: " + Username.capitalize()
            print "Attribute Modified: Volume"
            print "New Value: " + str(NewValue)
        except:
            db.rollback()
            print "ERROR: Update Unsuccessful"
    
    
    
    '''Creating Logging Record'''
    
    
    
    #Inserts record of order with changes into MTCLog
    cursor.execute("""SELECT MAX(VersionNumber) FROM UserLog WHERE Username = "%s" """ % (Username))
    OldMaxVersion = int(cursor.fetchone()[0])
    NewVersion = OldMaxVersion + 1
    cursor.execute("""INSERT INTO UserLog(Username, VersionNumber, LastModified, Password, Email, USDCredit, BTCCredit, JoinDate, FirstName, LastName, BankName, Address, Verified, TradingFee, Volume) SELECT Username, %d, "%s", Password, Email, USDCredit, BTCCredit, JoinDate, FirstName, LastName, BankName, Address, Verified, TradingFee, Volume FROM UserBook WHERE Username = "%s" """ % (NewVersion, Attribute.title(), Username))
    db.commit()
    
    
    
    '''Logging Control'''
        
    
        
    #Assigns static variables for logging control
    #Note: "Employee" value changes based on user submitting manual control
    Employee = "***333"
    Comment = "Updated User"
    
    
    
    #Inserts record of action into ControlLog
    try:
        print ""
        cursor.execute("""INSERT INTO ControlLog(Employee, Action, AffectedRows, AffectedAttributes, Comment) VALUES("%s", "%s", "%s", "%s", "%s")""" % (Employee, "Update User", Username.capitalize(), Attribute.title(), Comment))
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
    
    
    
    '''Setting Username'''
    
    
    
    #Requests OrderNumber and verifies that it is valid
    #Requests Username and verifies that it is valid
    while 1 == 1:
        Username = (raw_input("Username: ")).capitalize()
        cursor.execute("""SELECT * FROM UserBook WHERE Username = "%s" """ % (Username))
        Username = cursor.fetchone()
        if Username != None:
            print "User found"
            break;
        else:
            print "User not found. Please enter again: "
    
    
    
    '''Setting Attribute'''
    
    
    
    #Requests attribute to update and verifies that it is valid
    
    Attribute = (raw_input("Changing Attribute: ")).upper()
    
    #Gathers column titles from BasicOrderBook
    cursor.execute("SHOW COLUMNS FROM BasicOrderBook")
    FieldList = cursor.fetchall()
    #Iterates column names and matches entered Attribute against existing names
    for Field in FieldList:
        TargetAttribute = Field[0]
        if TargetAttribute.upper() == Attribute or Attribute == "USD CREDIT" or Attribute == "BTC CREDIT" or Attribute == "JOIN DATE" or Attribute == "FIRST NAME" or Attribute == "LAST NAME" or Attribute == "BANK NAME" or Attribute == "TRADING FEE":
            break;
    #Retrying until valid input is given
    while TargetAttribute.upper() != Attribute and Attribute != "USD CREDIT" and Attribute != "BTC CREDIT" and Attribute != "JOIN DATE" and Attribute != "FIRST NAME" and Attribute != "LAST NAME" and Attribute != "BANK NAME" and Attribute != "TRADING FEE":
        print "Attribute is invalid. Please enter again:"
        print "Choices: " + str([Header[0] for Header in cursor.description])
        Attribute = raw_input("Changing Attribute: ")
        Attribute = Attribute.upper()
        for Field in FieldList:
            TargetAttribute = Field[0]
            if TargetAttribute.upper() == Attribute or Attribute == "USD CREDIT" or Attribute == "BTC CREDIT" or Attribute == "JOIN DATE" or Attribute == "FIRST NAME" or Attribute == "LAST NAME" or Attribute == "BANK NAME" or Attribute == "TRADING FEE":
                break;
    
    
    
    '''Standardizing Parameter Names'''
    
    
    
    if Attribute == "USDCREDIT":
        Attribute = "USD CREDIT"
        print "Updating: USD Credit"
    
    elif Attribute == "BTCCREDIT":
        Attribute = "BTC CREDIT"
        print "Updating: BTC Credit"
    
    elif Attribute == "JOINDATE":
        Attribute = "JOIN DATE"
        print "Updating: Join Date"
    
    elif Attribute == "FIRSTNAME":
        Attribute = "FIRST NAME"
        print "Updating: First Name"
    
    elif Attribute == "LASTNAME":
        Attribute = "LAST NAME"
        print "Updating: Last Name"
    
    elif Attribute == "BANKNAME":
        Attribute = "BANK NAME"
        print "Updating: Bank Name"
    
    elif Attribute == "TRADINGFEE":
        Attribute = "TRADING FEE"
        print "Updating: Trading Fee"
    
    else:
        print "Updating: " + Attribute.title()
    
    
    
    '''Setting NewValue'''
    
    
    
    #Requesting basic input value if not a date field
    if Attribute != "JOINDATE" and Attribute != "JOIN DATE":
        NewValue = raw_input("New Value: ")
        while NewValue == "":
            print "Value is invalid. Please enter again:"
            NewValue = raw_input("New Value: ")
            NewValue = NewValue.upper()
    #Requesting date input values if not a basic input field
    else:
        
        YearValid = False
        MonthValid = False
        DayValid = False
        HourValid = False
        MinuteValid = False
        SecondValid = False
        
        
        
        while YearValid != True:
            NewDateYear = raw_input("New Year: ")
            if NewDateYear != "":
                try:
                    NewDateYear = int(NewDateYear)
                    if NewDateYear >= 2014 and NewDateYear <= 2015:
                        #print NewDateYear
                        YearValid = True
                    else:
                        print "New parameter must be between 2014 and 2015. Please enter again:"
                except:
                    print "New parameter must be an integer or blank. Please enter again:"
            else:
                YearValid = True
        
        
        
        while MonthValid != True:
            NewDateMonth = raw_input("New Month: ")
            if NewDateMonth != "":
                try:
                    NewDateMonth = int(NewDateMonth)
                    if NewDateMonth >= 1 and NewDateMonth <= 12:
                        #print NewDateMonth
                        MonthValid = True
                    else:
                        print "New parameter must be between 1 and 12. Please enter again:"
                except:
                    print "New parameter must be an integer or blank. Please enter again:"
            else:
                MonthValid = True
        
        
        
        while DayValid != True:
            NewDateDay = raw_input("New Day: ")
            if NewDateDay != "":
                try:
                    NewDateDay = int(NewDateDay)
                    if NewDateDay >= 1 and NewDateDay <= 365:
                        #print NewDateDay
                        DayValid = True
                    else:
                        print "New parameter must be between 1 and 365. Please enter again:"
                except:
                    print "New parameter must be an integer or blank. Please enter again:"
            else:
                DayValid = True
        
        
        
        while HourValid != True:
            NewDateHour = raw_input("New Hour: ")
            if NewDateHour != "":
                try:
                    NewDateHour = int(NewDateHour)
                    if NewDateHour >= 0 and NewDateHour <= 23:
                        #print NewDateHour
                        HourValid = True
                    else:
                        print "New parameter must be between 0 and 23. Please enter again:"
                except:
                    print "New parameter must be an integer or blank. Please enter again:"
            else:
                HourValid = True
        
        
        
        while MinuteValid != True:
            NewDateMinute = raw_input("New Minute: ")
            if NewDateMinute != "":
                try:
                    NewDateMinute = int(NewDateMinute)
                    if NewDateMinute >= 0 and NewDateMinute <= 59:
                        #print NewDateMinute
                        MinuteValid = True
                    else:
                        print "New parameter must be between 0 and 59. Please enter again:"
                except:
                    print "New parameter must be an integer or blank. Please enter again:"
            else:
                MinuteValid = True
        
        
        
        while SecondValid != True:
            NewDateSecond = raw_input("New Second: ")
            if NewDateSecond != "":
                try:
                    NewDateSecond = int(NewDateSecond)
                    if NewDateSecond >= 0 and NewDateSecond <= 59:
                        #print NewDateSecond
                        SecondValid = True
                    else:
                        print "New parameter must be between 0 and 59. Please enter again:"
                except:
                    print "New parameter must be an integer or blank. Please enter again:"
            else:
                SecondValid = True
        
        
        
        #Combines all date/time component values into a list for passing to main()
        NewValue = [NewDateYear, NewDateMonth, NewDateDay, NewDateHour, NewDateMinute, NewDateSecond]
    
    
    
    #Execute
    main(Username, Attribute, NewValue)


