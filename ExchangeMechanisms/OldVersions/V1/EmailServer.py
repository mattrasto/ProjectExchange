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

import smtplib

sender = "Name@Domain.com"
receivers = ["Receiver1", "Receiver2"]

message = """From: "Company Name" <"Name@Domain.com">
To: "Person Name" <"Receiver1">
Subject: "Subject"

"Message"
"""

try:
    smtpObj = smtplib.SMTP("localhost")
    smtpObj.sendmail(sender, receivers, message)
    print "Email sent"
except:
    print "Error: Unable to send email"