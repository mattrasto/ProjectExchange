#-------------------------------------------------------------------------------
# Name:        EmailServer
# Version:     1.0
# Purpose:     SMTP Protocol Experimentation
#
# Author:      Matthew
#
# Created:     05/04/2014
# Copyright:   (c) Matthew 2014
# Licence:     <your licence>
# Modified:    10/04/2014
#-------------------------------------------------------------------------------

#This is a very basic layout of an SMTP server implementation. Unusable and not currently in development.

import smtplib

sender = "ExchangeName@ExchangeDomain.com"
receivers = ["matthewrastovac@yahoo.com"]

message = """
From: "Company Name" <"ExchangeName@ExchangeDomain.com">
To: "Matthew Rastovac" <"matthewrastovac@yahoo.com">
Subject: "Test"
Message: "This is a test email"

"""

try:
    smtpObj = smtplib.SMTP("localhost")
    smtpObj.sendmail(sender, receivers, message)
    print "Email sent"
except:
    print "Error: Unable to send email"