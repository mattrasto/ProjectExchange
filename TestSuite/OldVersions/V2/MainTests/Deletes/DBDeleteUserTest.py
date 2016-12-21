#-------------------------------------------------------------------------------
# Name:        DBDeleteUserTest
# Version:     2.0
# Purpose:     Load and Remote Testing for DBDeleteUser
#
# Author:      Matthew
#
# Created:     08/13/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    08/20/2014
#-------------------------------------------------------------------------------

import time
import sys
import MySQLdb



#Starts timer
TimerStart = time.clock()

#Defines project path
sys.path.insert(0, "C:\Programming\ExchangeMechanisms\Development")

#Imports main module
import DatabaseScripts.Users.DBDeleteUser as Mod

print ""
print "Mod Finished Importing"
print ""


#Option for user deletion
#Note: 0 for specific user deletion, 1 for username iteration deletion (Username0 - Username[#]), 2 for smart deletion

Option = 2

#Option 0 settings
#To add more, create variable and add to list

Username1 = "Username12"
Username2 = "Username3"
UsernameList = [Username1, Username2]

#Option 1 settings
#To add more, change number
#Note: This operation starts user deletion from "Username0" and goes until "Username[Loops - 1]"

OptionOneLoops = 10

#Option 2 settings
#To add more, change number
#Note: This operation automatically detects active users and deletes randomly

OptionTwoLoops = 3



#Execute

if Option == 0:
    for Index, Username in enumerate(UsernameList):
        print ""
        print "----------Starting Round: " + str(Index + 1) + "----------"
        print ""
        Mod.main(Username)



if Option == 1:
    for x in range(0, OptionOneLoops):
        print ""
        print "----------Starting Round: " + str(x + 1) + "----------"
        print ""
        Username = "Username" + str(x)
        Mod.main(Username)



#WARNING: Query uses "ORDER BY RAND()": This uses full table scan and is very slow for large table

if Option == 2:
    
    #Initializes database
    db = MySQLdb.connect("localhost","root","***","exchange")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Data = cursor.fetchone()[0]
    print "Database Version: " + str(Data)
    
    cursor.execute("""SELECT Username FROM UserBook ORDER BY RAND() LIMIT %d """ % (OptionTwoLoops))
    Usernames = cursor.fetchall()
    if Usernames != ():
        for Index, Username in enumerate(Usernames):
            print ""
            print "----------Starting Round: " + str(Index + 1) + "----------"
            print ""
            Username = Username[0]
            Mod.main(Username)
    else:
        print ""
        print "No users found"
        



#Ends timer
TimerEnd = time.clock()
TimePassed = TimerEnd - TimerStart

print ""
print "Run Time: " + str(TimePassed) + " Seconds"


