#-------------------------------------------------------------------------------
# Name:        DBFullClear
# Version:     2.0
# Purpose:     Deletes all records from every table in database
#
# Author:      Matthew
#
# Created:     07/29/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    09/01/2014
#-------------------------------------------------------------------------------

import time
import MySQLdb

#Starts timer
TimerStart = time.clock()

#Initializes database
db = MySQLdb.connect("localhost","root","***","exchange")
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
Data = cursor.fetchone()[0]
print "Database Version: " + str(Data)



#Clear Tables:
#Note: 1 for clearing, 0 for not
UserBook = 1
UserLog = 1
IDBook = 1
BasicOrderBook = 1
BasicOrderLog = 1
MTCBook = 1
MTCLog = 1
LoanBook = 1
LoanLog = 1
PrivateTradeBook = 1
PrivateTradeLog = 1
BorrowerConstraintBook = 1
BorrowerConstraintLog = 1
InterventionConstraintBook = 1
InterventionConstraintLog = 1
TransactionLog = 1
AgreementLog = 1
UserRequestBook = 1
UserRequestLog = 1
ControlLog = 1



TotalTests = 0
PassedTests = 0
FailedTests = 0



#User tables

print ""
if UserBook:
    TotalTests += 1
    try:
        cursor.execute("""DELETE FROM UserBook""")
        db.commit()
        print "UserBook Cleared"
        PassedTests += 1
    except:
        print "ERROR: UserBook Not Cleared"
        FailedTests += 1
if UserLog:
    TotalTests += 1
    try:
        cursor.execute("""DELETE FROM UserLog""")
        db.commit()
        print "UserLog Cleared"
        PassedTests += 1
    except:
        print "ERROR: UserLog Not Cleared"
        FailedTests += 1

#IDBook table

print ""
if IDBook:
    TotalTests += 2
    try:
        cursor.execute("""DELETE FROM IDBook""")
        db.commit()
        print "IDBook Cleared"
        PassedTests += 1
    except:
        print "ERROR: IDBook Not Cleared"
        FailedTests += 1
    try:
        cursor.execute("""ALTER TABLE IDBook AUTO_INCREMENT = 1""")
        db.commit()
        print "IDBook Auto-Increment Reset"
        PassedTests += 1
    except:
        print "ERROR: IDBook Auto-Increment Not Reset"
        FailedTests += 1
        
#Basic Order tables

print ""
if BasicOrderBook:
    TotalTests += 1
    try:
        cursor.execute("""DELETE FROM BasicOrderBook""")
        db.commit()
        print "BasicOrderBook Cleared"
        PassedTests += 1
    except:
        print "ERROR: BasicOrderBook Not Cleared"
        FailedTests += 1
if BasicOrderLog:
    TotalTests += 1
    try:
        cursor.execute("""DELETE FROM BasicOrderLog""")
        db.commit()
        print "BasicOrderLog Cleared"
        PassedTests += 1
    except:
        print "ERROR: BasicOrderLog Not Cleared"
        FailedTests += 1

#MTC tables

print ""
if MTCBook:
    TotalTests += 1
    try:
        cursor.execute("""DELETE FROM MTCBook""")
        db.commit()
        print "MTCBook Cleared"
        PassedTests += 1
    except:
        print "ERROR: MTCBook Not Cleared"
        FailedTests += 1
if MTCLog:
    TotalTests += 1
    try:
        cursor.execute("""DELETE FROM MTCLog""")
        db.commit()
        print "MTCLog Cleared"
        PassedTests += 1
    except:
        print "ERROR: MTCLog Not Cleared"
        FailedTests += 1

#Loan tables

print ""
if LoanBook:
    TotalTests += 1
    try:
        cursor.execute("""DELETE FROM LoanBook""")
        db.commit()
        print "LoanBook Cleared"
        PassedTests += 1
    except:
        print "ERROR: LoanBook Not Cleared"
        FailedTests += 1
if LoanLog:
    TotalTests += 1
    try:
        cursor.execute("""DELETE FROM LoanLog""")
        db.commit()
        print "LoanLog Cleared"
        PassedTests += 1
    except:
        print "ERROR: LoanLog Not Cleared"
        FailedTests += 1

#Private Trade tables

print ""
if PrivateTradeBook:
    TotalTests += 1
    try:
        cursor.execute("""DELETE FROM PrivateTradeBook""")
        db.commit()
        print "PrivateTradeBook Cleared"
        PassedTests += 1
    except:
        print "ERROR: UserBook Not Cleared"
        FailedTests += 1
if PrivateTradeLog:
    TotalTests += 1
    try:
        cursor.execute("""DELETE FROM PrivateTradeLog""")
        db.commit()
        print "PrivateTradeLog Cleared"
        PassedTests += 1
    except:
        print "ERROR: PrivateTradeLog Not Cleared"
        FailedTests += 1

#Minimum Borrower Constraint Tables

print ""
if BorrowerConstraintBook:
    TotalTests += 1
    try:
        cursor.execute("""DELETE FROM BorrowerConstraintBook""")
        db.commit()
        print "BorrowerConstraintBook Cleared"
        PassedTests += 1
    except:
        print "ERROR: BorrowerConstraintBook Not Cleared"
        FailedTests += 1
if UserLog:
    TotalTests += 1
    try:
        cursor.execute("""DELETE FROM BorrowerConstraintLog""")
        db.commit()
        print "BorrowerConstraintLog Cleared"
        PassedTests += 1
    except:
        print "ERROR: BorrowerConstraintLog Not Cleared"
        FailedTests += 1

#User Intervention Constraint Tables

print ""
if InterventionConstraintBook:
    TotalTests += 1
    try:
        cursor.execute("""DELETE FROM InterventionConstraintBook""")
        db.commit()
        print "InterventionConstraintBook Cleared"
        PassedTests += 1
    except:
        print "ERROR: InterventionConstraintBook Not Cleared"
        FailedTests += 1
if UserLog:
    TotalTests += 1
    try:
        cursor.execute("""DELETE FROM InterventionConstraintLog""")
        db.commit()
        print "InterventionConstraintLog Cleared"
        PassedTests += 1
    except:
        print "ERROR: BorrowerConstraintLog Not Cleared"
        FailedTests += 1

#TransactionLog

print ""
if TransactionLog:
    TotalTests += 2
    try:
        cursor.execute("""DELETE FROM TransactionLog""")
        db.commit()
        print "TransactionLog Cleared"
        PassedTests += 1
    except:
        print "ERROR: TransactionLog Not Cleared"
        FailedTests += 1
    try:
        cursor.execute("""ALTER TABLE TransactionLog AUTO_INCREMENT = 1""")
        db.commit()
        print "TransactionLog Auto-Increment Reset"
        PassedTests += 1
    except:
        print "ERROR: TransactionLog Auto-Increment Not Reset"
        FailedTests += 1

#AgreementLog

print ""
if AgreementLog:
    TotalTests += 2
    try:
        cursor.execute("""DELETE FROM AgreementLog""")
        db.commit()
        print "AgreementLog Cleared"
        PassedTests += 1
    except:
        print "ERROR: AgreementLog Not Cleared"
        FailedTests += 1
    try:
        cursor.execute("""ALTER TABLE AgreementLog AUTO_INCREMENT = 1""")
        db.commit()
        print "AgreementLog Auto-Increment Reset"
        PassedTests += 1
    except:
        print "ERROR: AgreementLog Auto-Increment Not Reset"
        FailedTests += 1

#User Request Tables

print ""
if UserRequestBook:
    TotalTests += 1
    try:
        cursor.execute("""DELETE FROM UserRequestBook""")
        db.commit()
        print "UserRequestBook Cleared"
        PassedTests += 1
    except:
        print "ERROR: UserRequestBook Not Cleared"
        FailedTests += 1
if UserRequestLog:
    TotalTests += 1
    try:
        cursor.execute("""DELETE FROM UserRequestLog""")
        db.commit()
        print "UserRequestLog Cleared"
        PassedTests += 1
    except:
        print "ERROR: UserRequestLog Not Cleared"
        FailedTests += 1

#ControlLog

print ""
if ControlLog:
    TotalTests += 2
    try:
        cursor.execute("""DELETE FROM ControlLog""")
        db.commit()
        print "ControlLog Cleared"
        PassedTests += 1
    except:
        print "ERROR: ControlLog Not Cleared"
        FailedTests += 1
    try:
        cursor.execute("""ALTER TABLE ControlLog AUTO_INCREMENT = 1""")
        db.commit()
        print "ControlLog Auto-Increment Reset"
        PassedTests += 1
    except:
        print "ERROR: ControlLog Auto-Increment Not Reset"
        FailedTests += 1



print ""
print "Tests Run: " + str(TotalTests)
print "Tests Passed: " + str(PassedTests)
print "Tests Failed: " + str(FailedTests)

#Ends timer
TimerEnd = time.clock()
TimePassed = TimerEnd - TimerStart

print ""
print "Run Time: " + str(TimePassed) + " Seconds"


