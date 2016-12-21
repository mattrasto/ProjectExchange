# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.


# NOTE 1:
# For foreign keys:
# Use "related_name=[Access Name]" to specify access name (For unique database link names)
# Use "to_field=[Field Name in Models]" to specify field to be connected with in models


# NOTE 2:
# When accessing object NAMES from "models.[Class].objects.all()" in DB API, a "__unicode__" function must be
# specified within said class


# NOTE 3:
# To access object in DB API, use "models.[Class].objects.get([Filter])"


# NOTE 4:
# When accessing foreign keys that return "<[Class] Object>" or line of equivalent syntax,
# append ".[Attribute of Foreign Key Object]" to access value


# TO DO:
# -Find way to automatically associate foreign key values to attributes instead of method stated in Note 4
#    -ForeignKey vs. OneToOne
#    -ForeignKey returns object upon access
#    -OneToOne returns value upon access
# -Find way to use MySQL default values instead of defining each in models



from __future__ import unicode_literals

from django.db import models

from datetime import datetime


class Agreementlog(models.Model):
    agreementnumber = models.IntegerField(db_column='AgreementNumber', primary_key=True)  # Field name made lowercase.
    initiationdate = models.DateTimeField(db_column='InitiationDate')  # Field name made lowercase.
    terminationdate = models.DateTimeField(db_column='TerminationDate', blank=True, null=True)  # Field name made lowercase.
    agreementtype = models.CharField(db_column='AgreementType', max_length=10)  # Field name made lowercase.
    agreementamount = models.FloatField(db_column='AgreementAmount')  # Field name made lowercase.
    agreementamountreturned = models.FloatField(db_column='AgreementAmountReturned')  # Field name made lowercase.
    agreementinterestrate = models.FloatField(db_column='AgreementInterestRate')  # Field name made lowercase.
    agreementinterestcompoundrate = models.FloatField(db_column='AgreementInterestCompoundRate')  # Field name made lowercase.
    agreementdividendtype = models.CharField(db_column='AgreementDividendType', max_length=20)  # Field name made lowercase.
    agreementterminationtype = models.CharField(db_column='AgreementTerminationType', max_length=50)  # Field name made lowercase.
    escrowtax = models.FloatField(db_column='EscrowTax')  # Field name made lowercase.
    spreadprofit = models.FloatField(db_column='SpreadProfit')  # Field name made lowercase.
    totalprofit = models.FloatField(db_column='TotalProfit')  # Field name made lowercase.
    loancontractnumber = models.IntegerField(db_column='LoanContractNumber')  # Field name made lowercase.
    loancontractaccount = models.CharField(db_column='LoanContractAccount', max_length=20)  # Field name made lowercase.
    loancontractamount = models.FloatField(db_column='LoanContractAmount')  # Field name made lowercase.
    loancontractdifference = models.FloatField(db_column='LoanContractDifference')  # Field name made lowercase.
    borrowcontractnumber = models.IntegerField(db_column='BorrowContractNumber')  # Field name made lowercase.
    borrowcontractaccount = models.CharField(db_column='BorrowContractAccount', max_length=20)  # Field name made lowercase.
    borrowcontractamount = models.FloatField(db_column='BorrowContractAmount')  # Field name made lowercase.
    borrowcontractdifference = models.FloatField(db_column='BorrowContractDifference')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AgreementLog'


class Basicorderbook(models.Model):
    ordernumber = models.ForeignKey('Idbook', db_column='OrderNumber', related_name='BasicOrder_IDNumber', primary_key=True)  # Field name made lowercase.
    username = models.ForeignKey('Userbook', db_column='Username', to_field='username', related_name='BasicOrder_Username')  # Field name made lowercase.
    price = models.FloatField(db_column='Price')  # Field name made lowercase.
    volume = models.FloatField(db_column='Volume')  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=20)  # Field name made lowercase.
    action = models.CharField(db_column='Action', max_length=10)  # Field name made lowercase.
    triggertype = models.CharField(db_column='TriggerType', max_length=20, blank=True)  # Field name made lowercase.
    triggervalue = models.FloatField(db_column='TriggerValue', blank=True, null=True)  # Field name made lowercase.
    active = models.IntegerField(db_column='Active', blank=True, null=True)  # Field name made lowercase.
    dateentered = models.DateTimeField(db_column='DateEntered')  # Field name made lowercase.

    def __unicode__(self):
        return unicode(self.ordernumber.idnumber)

    class Meta:
        managed = False
        db_table = 'BasicOrderBook'


class Basicorderlog(models.Model):
    recordid = models.CharField(db_column='RecordID', primary_key=True, max_length=20)  # Field name made lowercase.
    ordernumber = models.IntegerField(db_column='OrderNumber')  # Field name made lowercase.
    versionnumber = models.IntegerField(db_column='VersionNumber')  # Field name made lowercase.
    lastmodified = models.CharField(db_column='LastModified', max_length=30, blank=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=20)  # Field name made lowercase.
    price = models.FloatField(db_column='Price')  # Field name made lowercase.
    volume = models.FloatField(db_column='Volume')  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=20)  # Field name made lowercase.
    action = models.CharField(db_column='Action', max_length=10)  # Field name made lowercase.
    triggertype = models.CharField(db_column='TriggerType', max_length=20, blank=True)  # Field name made lowercase.
    triggervalue = models.FloatField(db_column='TriggerValue', blank=True, null=True)  # Field name made lowercase.
    dateentered = models.DateTimeField(db_column='DateEntered')  # Field name made lowercase.
    transactionnumber = models.ForeignKey('Transactionlog', db_column='TransactionNumber', related_name='BasicOrder_TransactionNumber', blank=True, null=True)  # Field name made lowercase.
    transactiondate = models.DateTimeField(db_column='TransactionDate', blank=True, null=True)  # Field name made lowercase.
    terminationreason = models.CharField(db_column='TerminationReason', max_length=50, blank=True)  # Field name made lowercase.
    terminationdate = models.DateTimeField(db_column='TerminationDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BasicOrderLog'


class Borrowerconstraintbook(models.Model):
    constraintid = models.CharField(db_column='ConstraintID', primary_key=True, max_length=10)  # Field name made lowercase.
    contractnumber = models.IntegerField(db_column='ContractNumber')  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=20)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=20)  # Field name made lowercase.
    value = models.FloatField(db_column='Value')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BorrowerConstraintBook'


class Borrowerconstraintlog(models.Model):
    constraintid = models.CharField(db_column='ConstraintID', primary_key=True, max_length=10)  # Field name made lowercase.
    contractnumber = models.IntegerField(db_column='ContractNumber')  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=20)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=20)  # Field name made lowercase.
    value = models.FloatField(db_column='Value')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BorrowerConstraintLog'


class Controllog(models.Model):
    actionnumber = models.IntegerField(db_column='ActionNumber', primary_key=True)  # Field name made lowercase.
    employee = models.CharField(db_column='Employee', max_length=20)  # Field name made lowercase.
    action = models.CharField(db_column='Action', max_length=50)  # Field name made lowercase.
    affectedrows = models.CharField(db_column='AffectedRows', max_length=50)  # Field name made lowercase.
    affectedattributes = models.CharField(db_column='AffectedAttributes', max_length=50)  # Field name made lowercase.
    executiondate = models.DateTimeField(db_column='ExecutionDate')  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=50, blank=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ControlLog'


class Idbook(models.Model):
    idnumber = models.IntegerField(db_column='IDNumber', primary_key=True)  # Field name made lowercase.
    action = models.CharField(db_column='Action', max_length=10)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'IDBook'


class Interventionconstraintbook(models.Model):
    constraintid = models.CharField(db_column='ConstraintID', primary_key=True, max_length=10)  # Field name made lowercase.
    contractnumber = models.IntegerField(db_column='ContractNumber')  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=20)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=20)  # Field name made lowercase.
    value = models.FloatField(db_column='Value')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'InterventionConstraintBook'


class Interventionconstraintlog(models.Model):
    constraintid = models.CharField(db_column='ConstraintID', primary_key=True, max_length=10)  # Field name made lowercase.
    contractnumber = models.IntegerField(db_column='ContractNumber')  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=20)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=20)  # Field name made lowercase.
    value = models.FloatField(db_column='Value')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'InterventionConstraintLog'


class Loanbook(models.Model):
    contractnumber = models.ForeignKey('Idbook', db_column='ContractNumber', related_name='Loan_IDNumber', primary_key=True)  # Field name made lowercase.
    username = models.ForeignKey('Userbook', db_column='Username', to_field='username', related_name='Loan_Username')  # Field name made lowercase.
    medium = models.CharField(db_column='Medium', max_length=20)  # Field name made lowercase.
    volume = models.FloatField(db_column='Volume')  # Field name made lowercase.
    action = models.CharField(db_column='Action', max_length=10)  # Field name made lowercase.
    interestcompoundrate = models.CharField(db_column='InterestCompoundRate', max_length=50, blank=True)  # Field name made lowercase.
    interestrate = models.FloatField(db_column='InterestRate', blank=True, null=True)  # Field name made lowercase.
    duration = models.CharField(db_column='Duration', max_length=50)  # Field name made lowercase.
    endpoint = models.DateTimeField(db_column='EndPoint')  # Field name made lowercase.
    dividendtype = models.CharField(db_column='DividendType', max_length=10)  # Field name made lowercase.
    minimumborrowerconstraints = models.IntegerField(db_column='MinimumBorrowerConstraints', blank=True, null=True)  # Field name made lowercase.
    userinterventionconstraints = models.IntegerField(db_column='UserInterventionConstraints', blank=True, null=True)  # Field name made lowercase.
    userrequests = models.IntegerField(db_column='UserRequests', blank=True, null=True)  # Field name made lowercase.
    dateentered = models.DateTimeField(db_column='DateEntered')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LoanBook'


class Loanlog(models.Model):
    recordid = models.CharField(db_column='RecordID', primary_key=True, max_length=20)  # Field name made lowercase.
    contractnumber = models.IntegerField(db_column='ContractNumber')  # Field name made lowercase.
    versionnumber = models.IntegerField(db_column='VersionNumber')  # Field name made lowercase.
    lastmodified = models.CharField(db_column='LastModified', max_length=30, blank=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=20)  # Field name made lowercase.
    medium = models.CharField(db_column='Medium', max_length=20)  # Field name made lowercase.
    volume = models.FloatField(db_column='Volume')  # Field name made lowercase.
    action = models.CharField(db_column='Action', max_length=10)  # Field name made lowercase.
    interestcompoundrate = models.CharField(db_column='InterestCompoundRate', max_length=50, blank=True)  # Field name made lowercase.
    interestrate = models.FloatField(db_column='InterestRate', blank=True, null=True)  # Field name made lowercase.
    duration = models.CharField(db_column='Duration', max_length=50)  # Field name made lowercase.
    endpoint = models.DateTimeField(db_column='EndPoint')  # Field name made lowercase.
    dividendtype = models.CharField(db_column='DividendType', max_length=10)  # Field name made lowercase.
    minimumborrowerconstraints = models.IntegerField(db_column='MinimumBorrowerConstraints', blank=True, null=True)  # Field name made lowercase.
    userinterventionconstraints = models.IntegerField(db_column='UserInterventionConstraints', blank=True, null=True)  # Field name made lowercase.
    dateentered = models.DateTimeField(db_column='DateEntered')  # Field name made lowercase.
    agreementnumber = models.ForeignKey('Agreementlog', db_column='AgreementNumber', related_name='Loan_AgreementNumber', blank=True, null=True)  # Field name made lowercase.
    initiationdate = models.DateTimeField(db_column='InitiationDate', blank=True, null=True)  # Field name made lowercase.
    terminationreason = models.CharField(db_column='TerminationReason', max_length=50, blank=True)  # Field name made lowercase.
    terminationdate = models.DateTimeField(db_column='TerminationDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LoanLog'


class Mtcbook(models.Model):
    mtcnumber = models.ForeignKey('Idbook', db_column='MTCNumber', related_name='MTC_IDNumber', primary_key=True)  # Field name made lowercase.
    username = models.ForeignKey('Userbook', db_column='Username', to_field='username', related_name='MTC_Username')  # Field name made lowercase.
    price = models.FloatField(db_column='Price')  # Field name made lowercase.
    volume = models.FloatField(db_column='Volume')  # Field name made lowercase.
    action = models.CharField(db_column='Action', max_length=10)  # Field name made lowercase.
    interestcompoundrate = models.CharField(db_column='InterestCompoundRate', max_length=50, blank=True)  # Field name made lowercase.
    interestrate = models.FloatField(db_column='InterestRate', blank=True, null=True)  # Field name made lowercase.
    stoplossprice = models.FloatField(db_column='StopLossPrice', blank=True, null=True)  # Field name made lowercase.
    fulfillmentprice = models.FloatField(db_column='FulfillmentPrice', blank=True, null=True)  # Field name made lowercase.
    duration = models.CharField(db_column='Duration', max_length=50)  # Field name made lowercase.
    endpoint = models.DateTimeField(db_column='EndPoint')  # Field name made lowercase.
    dividendtype = models.CharField(db_column='DividendType', max_length=10)  # Field name made lowercase.
    minimumborrowerconstraints = models.IntegerField(db_column='MinimumBorrowerConstraints', blank=True, null=True)  # Field name made lowercase.
    userinterventionconstraints = models.IntegerField(db_column='UserInterventionConstraints', blank=True, null=True)  # Field name made lowercase.
    userrequests = models.IntegerField(db_column='UserRequests', blank=True, null=True)  # Field name made lowercase.
    dateentered = models.DateTimeField(db_column='DateEntered')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MTCBook'


class Mtclog(models.Model):
    recordid = models.CharField(db_column='RecordID', primary_key=True, max_length=20)  # Field name made lowercase.
    mtcnumber = models.IntegerField(db_column='MTCNumber')  # Field name made lowercase.
    versionnumber = models.IntegerField(db_column='VersionNumber')  # Field name made lowercase.
    lastmodified = models.CharField(db_column='LastModified', max_length=30, blank=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=20)  # Field name made lowercase.
    price = models.FloatField(db_column='Price')  # Field name made lowercase.
    volume = models.FloatField(db_column='Volume')  # Field name made lowercase.
    action = models.CharField(db_column='Action', max_length=10)  # Field name made lowercase.
    interestcompoundrate = models.CharField(db_column='InterestCompoundRate', max_length=50, blank=True)  # Field name made lowercase.
    interestrate = models.FloatField(db_column='InterestRate', blank=True, null=True)  # Field name made lowercase.
    stoplossprice = models.FloatField(db_column='StopLossPrice', blank=True, null=True)  # Field name made lowercase.
    fulfillmentprice = models.FloatField(db_column='FulfillmentPrice', blank=True, null=True)  # Field name made lowercase.
    duration = models.CharField(db_column='Duration', max_length=50)  # Field name made lowercase.
    endpoint = models.DateTimeField(db_column='EndPoint')  # Field name made lowercase.
    dividendtype = models.CharField(db_column='DividendType', max_length=10)  # Field name made lowercase.
    minimumborrowerconstraints = models.FloatField(db_column='MinimumBorrowerConstraints', blank=True, null=True)  # Field name made lowercase.
    userinterventionconstraints = models.FloatField(db_column='UserInterventionConstraints', blank=True, null=True)  # Field name made lowercase.
    dateentered = models.DateTimeField(db_column='DateEntered')  # Field name made lowercase.
    agreementnumber = models.ForeignKey('Agreementlog', db_column='AgreementNumber', related_name='MTC_AgreementNumber', blank=True, null=True)  # Field name made lowercase.
    initiationdate = models.DateTimeField(db_column='InitiationDate', blank=True, null=True)  # Field name made lowercase.
    terminationreason = models.CharField(db_column='TerminationReason', max_length=50, blank=True)  # Field name made lowercase.
    terminationdate = models.DateTimeField(db_column='TerminationDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MTCLog'


class Privatetradebook(models.Model):
    tradenumber = models.ForeignKey('Idbook', db_column='TradeNumber', related_name='PrivateTrade_IDNumber', primary_key=True)  # Field name made lowercase.
    username = models.ForeignKey('Userbook', db_column='Username', to_field='username', related_name='PrivateTrade_Username')  # Field name made lowercase.
    price = models.FloatField(db_column='Price')  # Field name made lowercase.
    volume = models.FloatField(db_column='Volume')  # Field name made lowercase.
    action = models.CharField(db_column='Action', max_length=10)  # Field name made lowercase.
    userrequests = models.IntegerField(db_column='UserRequests')  # Field name made lowercase.
    dateentered = models.DateTimeField(db_column='DateEntered')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PrivateTradeBook'


class Privatetradelog(models.Model):
    recordid = models.CharField(db_column='RecordID', primary_key=True, max_length=20)  # Field name made lowercase.
    tradenumber = models.IntegerField(db_column='TradeNumber')  # Field name made lowercase.
    versionnumber = models.IntegerField(db_column='VersionNumber')  # Field name made lowercase.
    lastmodified = models.CharField(db_column='LastModified', max_length=30, blank=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=20)  # Field name made lowercase.
    price = models.IntegerField(db_column='Price')  # Field name made lowercase.
    volume = models.IntegerField(db_column='Volume')  # Field name made lowercase.
    action = models.CharField(db_column='Action', max_length=10)  # Field name made lowercase.
    dateentered = models.DateTimeField(db_column='DateEntered')  # Field name made lowercase.
    transactionnumber = models.ForeignKey('Transactionlog', db_column='TransactionNumber', related_name='PrivateTrade_TransactionNumber', blank=True, null=True)  # Field name made lowercase.
    transactiondate = models.DateTimeField(db_column='TransactionDate', blank=True, null=True)  # Field name made lowercase.
    terminationreason = models.CharField(db_column='TerminationReason', max_length=50, blank=True)  # Field name made lowercase.
    terminationdate = models.DateTimeField(db_column='TerminationDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PrivateTradeLog'


class Transactionlog(models.Model):
    transactionnumber = models.IntegerField(db_column='TransactionNumber', primary_key=True)  # Field name made lowercase.
    transactiondate = models.DateTimeField(db_column='TransactionDate')  # Field name made lowercase.
    transactionprice = models.FloatField(db_column='TransactionPrice')  # Field name made lowercase.
    transactionvolume = models.FloatField(db_column='TransactionVolume')  # Field name made lowercase.
    transactiontotal = models.FloatField(db_column='TransactionTotal')  # Field name made lowercase.
    tradingfeeprofit = models.FloatField(db_column='TradingFeeProfit')  # Field name made lowercase.
    spreadprofit = models.FloatField(db_column='SpreadProfit')  # Field name made lowercase.
    totalprofit = models.FloatField(db_column='TotalProfit')  # Field name made lowercase.
    buyordernumber = models.IntegerField(db_column='BuyOrderNumber')  # Field name made lowercase.
    buyorderaccount = models.CharField(db_column='BuyOrderAccount', max_length=20)  # Field name made lowercase.
    buyorderprice = models.FloatField(db_column='BuyOrderPrice')  # Field name made lowercase.
    buyordervolume = models.FloatField(db_column='BuyOrderVolume')  # Field name made lowercase.
    buyordertype = models.CharField(db_column='BuyOrderType', max_length=20)  # Field name made lowercase.
    buyordercompletion = models.CharField(db_column='BuyOrderCompletion', max_length=10)  # Field name made lowercase.
    sellordernumber = models.IntegerField(db_column='SellOrderNumber')  # Field name made lowercase.
    sellorderaccount = models.CharField(db_column='SellOrderAccount', max_length=20)  # Field name made lowercase.
    sellorderprice = models.FloatField(db_column='SellOrderPrice')  # Field name made lowercase.
    sellordervolume = models.FloatField(db_column='SellOrderVolume')  # Field name made lowercase.
    sellordertype = models.CharField(db_column='SellOrderType', max_length=20)  # Field name made lowercase.
    sellordercompletion = models.CharField(db_column='SellOrderCompletion', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TransactionLog'


class Userbook(models.Model):
    username = models.CharField(db_column='Username', primary_key=True, max_length=20)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=50)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=50)  # Field name made lowercase.
    usdcredit = models.FloatField(db_column='USDCredit', default=0)  # Field name made lowercase.
    btccredit = models.FloatField(db_column='BTCCredit', default=0)  # Field name made lowercase.
    joindate = models.DateTimeField(db_column='JoinDate', blank=True, default=datetime.now)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=20)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=20)  # Field name made lowercase.
    bankname = models.CharField(db_column='BankName', max_length=50, blank=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=50, blank=True)  # Field name made lowercase.
    verified = models.IntegerField(db_column='Verified', default=0)  # Field name made lowercase.
    tradingfee = models.FloatField(db_column='TradingFee', default=.005)  # Field name made lowercase.
    volume = models.FloatField(db_column='Volume', default=0)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserBook'


class Userlog(models.Model):
    recordid = models.CharField(db_column='RecordID', primary_key=True, max_length=20)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=20)  # Field name made lowercase.
    versionnumber = models.IntegerField(db_column='VersionNumber')  # Field name made lowercase.
    lastmodified = models.CharField(db_column='LastModified', max_length=30, blank=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=50)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
    usdcredit = models.FloatField(db_column='USDCredit')  # Field name made lowercase.
    btccredit = models.FloatField(db_column='BTCCredit')  # Field name made lowercase.
    joindate = models.DateTimeField(db_column='JoinDate')  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=20)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=20)  # Field name made lowercase.
    bankname = models.CharField(db_column='BankName', max_length=50, blank=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=50, blank=True)  # Field name made lowercase.
    verified = models.IntegerField(db_column='Verified')  # Field name made lowercase.
    tradingfee = models.FloatField(db_column='TradingFee')  # Field name made lowercase.
    volume = models.FloatField(db_column='Volume')  # Field name made lowercase.
    deletioncomment = models.CharField(db_column='DeletionComment', max_length=50, blank=True)  # Field name made lowercase.
    deletiondate = models.DateTimeField(db_column='DeletionDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserLog'


class Userrequestbook(models.Model):
    requestid = models.CharField(db_column='RequestID', primary_key=True, max_length=10)  # Field name made lowercase.
    contractnumber = models.IntegerField(db_column='ContractNumber')  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=20)  # Field name made lowercase.
    daterequested = models.DateTimeField(db_column='DateRequested')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserRequestBook'


class Userrequestlog(models.Model):
    requestid = models.CharField(db_column='RequestID', primary_key=True, max_length=10)  # Field name made lowercase.
    contractnumber = models.IntegerField(db_column='ContractNumber')  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=20)  # Field name made lowercase.
    daterequested = models.DateTimeField(db_column='DateRequested')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserRequestLog'
