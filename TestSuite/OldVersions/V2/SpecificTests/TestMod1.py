'''
Created on Jul 15, 2014

@author: Matthew
'''

import datetime

def AgePrinter(Name, Age):
    print Name
    print Age
    Variable2 = 2
    return Variable2
    Variable1 = 1
    return Variable1
    print "Test Script Complete"

Name = "Matthew"
Age = 16
AgePrinter(Name, Age)
Variable = AgePrinter(Name, Age)
print Variable

List = [0, 1, 2, 3]
List2 = [0, 1, 2, List[3]+6]
print List2

Date = datetime.datetime(1, 1, 1, 1, 1, 1)
print Date