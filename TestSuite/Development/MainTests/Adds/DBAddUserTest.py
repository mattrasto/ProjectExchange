#-------------------------------------------------------------------------------
# Name:        DBAddUserTest
# Version:     2.0
# Purpose:     Load and Remote Testing for DBAddUser
#
# Author:      Matthew
#
# Created:     07/16/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    08/12/2014
#-------------------------------------------------------------------------------

import time
import sys

#Starts timer
TimerStart = time.clock()

#Defines project path
# Linux
# sys.path.insert(0, "/home/mal/Programming/ExchangeMechanisms/Development")
# Windows
sys.path.insert(0, "C:/Programming/ProjectExchange/ExchangeMechanisms/Development")

#Imports main module
import DatabaseScripts.Users.DBAddUser as Mod

print ""
print "Mod Finished Importing"



#Number of users to add
Loops = 2



#Execute

for x in range(0, Loops):
    print ""
    print "----------Starting Round: " + str(x + 1) + "----------"
    print ""
    Username = "Username" + str(x)
    Password = "Password" + str(x)
    Email = "Email" + str(x)
    FirstName = "FirstName" + str(x)
    LastName = "LastName" + str(x)
    Mod.main(Username, Password, Email, FirstName, LastName);



#Ends timer
TimerEnd = time.clock()
TimePassed = TimerEnd - TimerStart

print ""
print "Run Time: " + str(TimePassed) + " Seconds"


