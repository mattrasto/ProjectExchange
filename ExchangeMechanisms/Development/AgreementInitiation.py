#-------------------------------------------------------------------------------
# Name:        AgreementInitiation
# Version:     3.0
# Purpose:     Accepts a User Request and initiates the agreement
#
# Author:      Matthew
#
# Created:     10/05/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    10/05/2014
#-------------------------------------------------------------------------------

#Check for same-user trading
#Credit accounts once initiated



import MySQLdb
import sys
import datetime



#Initializing database
db = MySQLdb.connect("localhost","root","***","exchange")
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
Data = cursor.fetchone()[0]
print "Database Version: " + str(Data)



def main(RequestID):

    cursor.execute("""SELECT * FROM UserRequestBook WHERE RequestID = "%s" """ % (RequestID))
    UserRequestDetails = cursor.fetchone()
    if UserRequestDetails == None:
        print "CRITICAL ERROR: User Request does not exist"
        sys.exit()
    print UserRequestDetails
    ContractNumber = UserRequestDetails[1]

    cursor.execute("""SELECT * FROM MTCBook WHERE MTCNumber = %d""" % (ContractNumber))
    MTCList = cursor.fetchall()
    cursor.execute("""SELECT * FROM LoanBook WHERE ContractNumber = %d""" % (ContractNumber))
    LoanList = cursor.fetchall()
    cursor.execute("""SELECT * FROM PrivateTradeBook WHERE TradeNumber = %d""" % (ContractNumber))
    PrivateTradeList = cursor.fetchall()

    if MTCList == () and LoanList == () and PrivateTradeList == ():
        print "CRITICAL ERROR: No contracts with specified User Request!"
        sys.exit()



    #Checking if contract is already involved in an agreement
    cursor.execute("""SELECT * FROM AgreementLog WHERE ContractNumber = "%s" """ % (ContractNumber))
    AgreementList = cursor.fetchall()
    if AgreementList != ():
        print "CRITICAL ERROR: Contract already in an agreement"
        sys.exit()



    #Assigns agreement variables and creates agreement based on MTC aspects
    if MTCList != ():
        AgreementType = "MTC"
        MTC = MTCList[0]
        ContractNumber = MTC[0]
        if MTC[4] == "Loan":
            LoanAccount = MTC[1]
            BorrowAccount = UserRequestDetails[2]
        else:
            LoanAccount = UserRequestDetails[2]
            BorrowAccount = MTC[1]
        InitiationDate = datetime.datetime.now()
        AgreementDuration = MTC[9]
        EndPoint = InitiationDate + AgreementDuration
        AgreementAmount = MTC[2] * MTC[3]
        AgreementInterestRate = MTC[6]
        AgreementInterestCompoundRate = MTC[5]
        AgreementDividendType = MTC[10]
        #Will be calculated based on various contract properties
        EscrowTax = .005



        #Converts timedelta of Duration back to string format for database insertion
        DurationSeconds = AgreementDuration.seconds
        DurationDays = AgreementDuration.days

        DurationHours = DurationDays * 24
        DurationMinutes = DurationSeconds / 60
        DurationHours += DurationMinutes / 60
        DurationMinutes = (DurationMinutes % 60)
        DurationSeconds = (DurationSeconds % 60)

        AgreementDuration = "%d:%d:%d" % (DurationHours, DurationMinutes, DurationSeconds)


        #Converts timedelta of InterestCompoundRate back to string format for database insertion
        InterestCompoundRateSeconds = AgreementInterestCompoundRate.seconds
        InterestCompoundRateDays = AgreementInterestCompoundRate.days

        InterestCompoundRateHours = InterestCompoundRateDays * 24
        InterestCompoundRateMinutes = InterestCompoundRateSeconds / 60
        InterestCompoundRateHours += InterestCompoundRateMinutes / 60
        InterestCompoundRateMinutes = (InterestCompoundRateMinutes % 60)
        InterestCompoundRateSeconds = (InterestCompoundRateSeconds % 60)

        AgreementInterestCompoundRate = "%d:%d:%d" % (InterestCompoundRateHours, InterestCompoundRateMinutes, InterestCompoundRateSeconds)



        #Attempts to insert agreement record into AgreementBook
        try:
            print ""
            cursor.execute("""INSERT INTO AgreementBook(ContractNumber, LoanAccount, BorrowAccount, InitiationDate, EndPoint, AgreementDuration, AgreementType, AgreementAmount, AgreementInterestRate, AgreementInterestCompoundRate, AgreementDividendType, EscrowTax) VALUES("%d", "%s", "%s", "%s", "%s", "%s", "%s", %f, %f, "%s", "%s", %f)""" % (ContractNumber, LoanAccount, BorrowAccount, InitiationDate, EndPoint, AgreementDuration, AgreementType, AgreementAmount, AgreementInterestRate, AgreementInterestCompoundRate, AgreementDividendType, EscrowTax))
            db.commit()
            print "Agreement Successfully Added"
        except:
            print "Agreement Unsuccessfully Added"

        #Attempts to insert agreement record into AgreementLog
        try:
            print ""
            cursor.execute("""INSERT INTO AgreementLog(ContractNumber, LoanAccount, BorrowAccount, InitiationDate, EndPoint, AgreementDuration, AgreementType, AgreementAmount, AgreementInterestRate, AgreementInterestCompoundRate, AgreementDividendType, EscrowTax) VALUES("%d", "%s", "%s", "%s", "%s", "%s", "%s", %f, %f, "%s", "%s", %f)""" % (ContractNumber, LoanAccount, BorrowAccount, InitiationDate, EndPoint, AgreementDuration, AgreementType, AgreementAmount, AgreementInterestRate, AgreementInterestCompoundRate, AgreementDividendType, EscrowTax))
            db.commit()
            print "Agreement Successfully Logged"
        except:
            print "Agreement Unsuccessfully Logged"



    #Assigns agreement variables and creates agreement based on Loan aspects
    elif LoanList != ():
        AgreementType = "Loan"
        Loan = LoanList[0]
        ContractNumber = Loan[0]
        if Loan[4] == "Loan":
            LoanAccount = Loan[1]
            BorrowAccount = UserRequestDetails[2]
        else:
            LoanAccount = UserRequestDetails[2]
            BorrowAccount = Loan[1]
        AgreementMedium = Loan[2]
        InitiationDate = datetime.datetime.now()
        AgreementDuration = Loan[7]
        EndPoint = InitiationDate + AgreementDuration
        AgreementAmount = Loan[3]
        AgreementInterestRate = Loan[6]
        AgreementInterestCompoundRate = Loan[5]
        AgreementDividendType = Loan[8]
        #Will be calculated based on various contract properties
        EscrowTax = .005



        #Converts timedelta of Duration back to string format for database insertion
        DurationSeconds = AgreementDuration.seconds
        DurationDays = AgreementDuration.days

        DurationHours = DurationDays * 24
        DurationMinutes = DurationSeconds / 60
        DurationHours += DurationMinutes / 60
        DurationMinutes = (DurationMinutes % 60)
        DurationSeconds = (DurationSeconds % 60)

        AgreementDuration = "%d:%d:%d" % (DurationHours, DurationMinutes, DurationSeconds)


        #Converts timedelta of InterestCompoundRate back to string format for database insertion
        InterestCompoundRateSeconds = AgreementInterestCompoundRate.seconds
        InterestCompoundRateDays = AgreementInterestCompoundRate.days

        InterestCompoundRateHours = InterestCompoundRateDays * 24
        InterestCompoundRateMinutes = InterestCompoundRateSeconds / 60
        InterestCompoundRateHours += InterestCompoundRateMinutes / 60
        InterestCompoundRateMinutes = (InterestCompoundRateMinutes % 60)
        InterestCompoundRateSeconds = (InterestCompoundRateSeconds % 60)

        AgreementInterestCompoundRate = "%d:%d:%d" % (InterestCompoundRateHours, InterestCompoundRateMinutes, InterestCompoundRateSeconds)



        #Attempts to insert agreement record into AgreementBook
        try:
            print ""
            cursor.execute("""INSERT INTO AgreementBook(ContractNumber, LoanAccount, BorrowAccount, InitiationDate, EndPoint, AgreementMedium, AgreementDuration, AgreementType, AgreementAmount, AgreementInterestRate, AgreementInterestCompoundRate, AgreementDividendType, EscrowTax) VALUES("%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", %f, %f, "%s", "%s", %f)""" % (ContractNumber, LoanAccount, BorrowAccount, InitiationDate, EndPoint, AgreementMedium, AgreementDuration, AgreementType, AgreementAmount, AgreementInterestRate, AgreementInterestCompoundRate, AgreementDividendType, EscrowTax))
            db.commit()
            print "Agreement Successfully Added"
        except:
            print "Agreement Unsuccessfully Added"

        #Attempts to insert agreement record into AgreementLog
        try:
            print ""
            cursor.execute("""INSERT INTO AgreementLog(ContractNumber, LoanAccount, BorrowAccount, InitiationDate, EndPoint, AgreementMedium, AgreementDuration, AgreementType, AgreementAmount, AgreementInterestRate, AgreementInterestCompoundRate, AgreementDividendType, EscrowTax) VALUES("%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", %f, %f, "%s", "%s", %f)""" % (ContractNumber, LoanAccount, BorrowAccount, InitiationDate, EndPoint, AgreementMedium, AgreementDuration, AgreementType, AgreementAmount, AgreementInterestRate, AgreementInterestCompoundRate, AgreementDividendType, EscrowTax))
            db.commit()
            print "Agreement Successfully Logged"
        except:
            print "Agreement Unsuccessfully Logged"



    #Assigns agreement variables and creates agreement based on Private Trade aspects
    else:
        AgreementType = "Private Trade"
        PrivateTrade = PrivateTradeList[0]
        ContractNumber = PrivateTrade[0]
        if PrivateTrade[4] == "Loan":
            LoanAccount = PrivateTrade[1]
            BorrowAccount = UserRequestDetails[2]
        else:
            LoanAccount = UserRequestDetails[2]
            BorrowAccount = PrivateTrade[1]
        InitiationDate = datetime.datetime.now()
        AgreementAmount = PrivateTrade[2] * PrivateTrade[3]
        #Will be calculated based on various contract properties
        EscrowTax = .005

        #Attempts to insert agreement record into AgreementLog
        try:
            cursor.execute("""INSERT INTO AgreementLog(ContractNumber, LoanAccount, BorrowAccount, AgreementType, AgreementAmount, EscrowTax) VALUES("%d", "%s", "%s", "%s", %f, %f)""" % (ContractNumber, LoanAccount, BorrowAccount, AgreementType, AgreementAmount, EscrowTax))
            db.commit()
            print "Agreement Successfully Logged"
        except:
            print "Agreement Unsuccessfully Logged"








if __name__ == "__main__":

    RequestID = raw_input("RequestID: ")

    main(RequestID)
