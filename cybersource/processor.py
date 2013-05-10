from random import randrange

import suds
from suds.client import Client
from suds.sax.attribute import Attribute
from suds.sax.element import Element

import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)


class CyberSourceBaseException(Exception):
    def __init__(self, error_code, value):
        self.error_code = error_code
        self.value = value

    def __unicode__(self):
        return "{0} (Error code: {1})".format(repr(self.value), self.error_code)

    def __str__(self):
        return self.__unicode__()


class CyberScourceError(CyberSourceBaseException):
    pass


class CyberScourceFailure(CyberSourceBaseException):
    pass

CYBERSOURCE_RESPONSES = {
    '100': 'Successful transaction.',
    '101': 'The request is missing one or more required fields.',
    '102': 'One or more fields in the request contains invalid data.',
    '104': 'The merchantReferenceCode sent with this authorization request matches the merchantReferenceCode of another authorization request that you sent in the last 15 minutes.',
    '150': 'Error: General system failure. ',
    '151': 'Error: The request was received but there was a server timeout. This error does not include timeouts between the client and the server.',
    '152': 'Error: The request was received, but a service did not finish running in time.',
    '201': 'The issuing bank has questions about the request. You do not receive an authorization code in the reply message, but you might receive one verbally by calling the processor.',
    '202': 'Expired card. You might also receive this if the expiration date you provided does not match the date the issuing bank has on file.',
    '203': 'General decline of the card. No other information provided by the issuing bank.',
    '204': 'Insufficient funds in the account.',
    '205': 'Stolen or lost card.',
    '207': 'Issuing bank unavailable.',
    '208': 'Inactive card or card not authorized for card-not-present transactions.',
    '210': 'The card has reached the credit limit. ',
    '211': 'Invalid card verification number.',
    '221': 'The customer matched an entry on the processor\'s negative file.',
    '231': 'Invalid account number.',
    '232': 'The card type is not accepted by the payment processor.',
    '233': 'General decline by the processor.',
    '234': 'There is a problem with your CyberSource merchant configuration.',
    '235': 'The requested amount exceeds the originally authorized amount. Occurs, for example, if you try to capture an amount larger than the original authorization amount. This reason code only applies if you are processing a capture through the API.',
    '236': 'Processor Failure',
    '238': 'The authorization has already been captured. This reason code only applies if you are processing a capture through the API.',
    '239': 'The requested transaction amount must match the previous transaction amount. This reason code only applies if you are processing a capture or credit through the API.',
    '240': 'The card type sent is invalid or does not correlate with the credit card number.',
    '241': 'The request ID is invalid. This reason code only applies when you are processing a capture or credit through the API.',
    '242': 'You requested a capture through the API, but there is no corresponding, unused authorization record. Occurs if there was not a previously successful authorization request or if the previously successful authorization has already been used by another capture request. This reason code only applies when you are processing a capture through the API.',
    '243': 'The transaction has already been settled or reversed.',
    '246': 'The capture or credit is not voidable because the capture or credit information has already been submitted to your processor. Or, you requested a void for a type of transaction that cannot be voided. This reason code applies only if you are processing a void through the API.',
    '247': 'You requested a credit for a capture that was previously voided. This reason code applies only if you are processing a void through the API.',
    '250': 'Error: The request was received, but there was a timeout at the payment processor.',
    '520': 'The authorization request was approved by the issuing bank but declined by CyberSource based on your Smart Authorization settings.',
}


class Processor(object):

    def __init__(self, *args, **kwargs):
        # Test server
        self.client = Client('https://ics2wstest.ic3.com/commerce/1.x/transactionProcessor/CyberSourceTransaction_1.26.wsdl')

        self.password = '6CrXkQJxiZ0tKn2GCwpG4nSQ/fyQ9Z0tajLq01FsTGv4eV1cTivxsR1jdMD4ddOM/NBHdOKGQ7Y03LRMS3lwgavgAQBNCuLSOrQh0nc3bQ8YMgCs6W/SKw+r8MVC0Thbc4kVW6250Xl+mWoJcVNxkumxSJTkUoVUtRMdISwfcFynkPmUo8gJtcgmeYYLCkbidJD9/JD1nS1qMurTUWxMa/h5XVxOK/GxHWN0wPh104z80Ed04oZDtjTctExLeXCBq+ABAE0K4tI6tCHSdzdtDxgyAKzpb9IrD6vwxULROFtziRVbrbnReX6ZaglxU3GS6bFIlORShVS1Ex0hLB9wXA=='
        self.merchantid = 'cybersource_proame'

        # Maybe Live Who knows
        # self.password = '3c+R2H8XYm2y/Pkh3pcBHwpqwxYboIW51wSjQLoOQeRBmw8TFjwFAMGmWcS9s04fUsAW24g8LN9D/p+eok/AJ8n8WRbUsmRvqjKzzuo+33sn5QhdsfBmyilBN/40Navx2y0Bc36i2w3inElm5FJnfgYPeGwlrVPPjBGWl6ro0MqH9ThANN19U7joXB3elwEfCmrDFhughbnXBKNAug5B5EGbDxMWPAUAwaZZxL2zTh9SwBbbiDws30P+n56iT8AnyfxZFtSyZG+qMrPO6j7feyflCF2x8GbKKUE3/jQ1q/HbLQFzfqLbDeKcSWbkUmd+Bg94bCWtU8+MEZaXqujQyg=='
        # self.merchantid = 'v2922736'

    def create_headers(self):
        wssens = ('wsse', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd')
        mustAttribute = Attribute('SOAP-ENV:mustUnderstand', '1')

        security = Element('Security', ns=wssens)
        security.append(mustAttribute)
        security.append(Attribute('xmlns:wsse', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd'))

        usernametoken = Element('UsernameToken', ns=wssens)

        username = Element('Username', ns=wssens).setText(self.merchantid)

        passwordType = Attribute('Type', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wssusername-token-profile-1.0#PasswordText')
        password = Element('Password', ns=wssens).setText(self.password)
        password.append(passwordType)

        usernametoken.append(username)
        usernametoken.append(password)

        security.append(usernametoken)

        self.client.set_options(soapheaders=security)

    def run_transaction(self):
        ccAuthService = self.client.factory.create('ns0:ccAuthService')
        ccAuthService._run = 'true'

        self.result = self.client.service.runTransaction(
            merchantID=self.merchantid,
            merchantReferenceCode=randrange(0, 100),
            ics_applications='ics_auth',
            card=self.card,
            billTo=self.bill_to,
            purchaseTotals=self.payment,
            ccAuthService=ccAuthService
        )

    def create_request(self):
        self.request = self.client.factory.create('ns0:RequestMessage')
        self.request.card = self.card
        self.request.billTo = self.bill_to

    def payment_amount(self, **kwargs):
        '''
            currency = None
            discountAmount = None
            taxAmount = None
            dutyAmount = None
            grandTotalAmount = None
            freightAmount = None
            foreignAmount = None
            foreignCurrency = None
            exchangeRate = None
            exchangeRateTimeStamp = None
            additionalAmountType0 = None
            additionalAmount0 = None
            additionalAmountType1 = None
            additionalAmount1 = None
            additionalAmountType2 = None
            additionalAmount2 = None
            additionalAmountType3 = None
            additionalAmount3 = None
            additionalAmountType4 = None
            additionalAmount4 = None
            serviceFeeAmount = None
        '''

        kwargs['currency'] = 'USD'
        kwargs['total'] = 12.50

        currency = kwargs.get('currency')
        grandTotalAmount = kwargs.get('total')

        self.payment = self.client.factory.create('ns0:PurchaseTotals')
        self.payment.currency = currency
        self.payment.grandTotalAmount = grandTotalAmount

    def set_card_info(self, **kwargs):
        '''
            fullName = None
            accountNumber = None
            expirationMonth = None
            expirationYear = None
            cvIndicator = None
            cvNumber = None
            cardType = None
            issueNumber = None
            startMonth = None
            startYear = None
            pin = None
            accountEncoderID = None
            bin = None
        '''

        # Test stuff
        kwargs['account_number'] = '4111111111111111'
        kwargs['exp_month'] = '05'
        kwargs['exp_year'] = '2015'
        kwargs['cvv'] = '123'

        accountNumber = kwargs.get('account_number')
        expirationMonth = kwargs.get('exp_month')
        expirationYear = kwargs.get('exp_year')
        cvNumber = kwargs.get('cvv')

        # if not all([fullName, accountNumber, expirationMonth, expirationYear, cvNumber]):
        #     raise CyberScourceError('', 'Not all credit card info was gathered')

        self.card = self.client.factory.create('ns0:Card')

        self.card.accountNumber = accountNumber
        self.card.expirationMonth = expirationMonth
        self.card.expirationYear = expirationYear
        self.card.cvIndicator = 1
        self.card.cvNumber = cvNumber

    def bill_to(self, **kwargs):
        '''
            title = None
            firstName = None
            middleName = None
            lastName = None
            suffix = None
            buildingNumber = None
            street1 = None
            street2 = None
            street3 = None
            street4 = None
            city = None
            county = None
            state = None
            postalCode = None
            country = None
            company = None
            companyTaxID = None
            phoneNumber = None
            email = None
            ipAddress = None
            customerPassword = None
            ipNetworkAddress = None
            hostname = None
            domainName = None
            dateOfBirth = None
            driversLicenseNumber = None
            driversLicenseState = None
            ssn = None
            customerID = None
            httpBrowserType = None
            httpBrowserEmail = None
            httpBrowserCookiesAccepted = None
            nif = None
            personalID = None
            language = None
            name = None
        '''

        # Test Stuff
        kwargs['title'] = 'Mr.'
        kwargs['first_name'] = 'Colin'
        kwargs['last_name'] = 'Fletcher'
        kwargs['address1'] = '3800 Quick Hill Rd'
        kwargs['address2'] = 'Bldg 1-100'
        kwargs['city'] = 'Austin'
        kwargs['state'] = 'TX'
        kwargs['zipcode'] = '78728'
        kwargs['country'] = 'US'
        kwargs['cid'] = '0123456789'
        kwargs['email'] = 'colin@protectamerica.com'

        title = kwargs.get('title')
        firstName = kwargs.get('first_name')
        lastName = kwargs.get('last_name')
        street1 = kwargs.get('address1')
        street2 = kwargs.get('address2')
        city = kwargs.get('city')
        state = kwargs.get('state')
        postalCode = kwargs.get('zipcode')
        country = kwargs.get('country', 'US')
        customerID = kwargs.get('cid')
        email = kwargs.get('email')

        self.bill_to = self.client.factory.create('ns0:BillTo')

        self.bill_to.title = title
        self.bill_to.firstName = firstName
        self.bill_to.lastName = lastName
        self.bill_to.street1 = street1
        self.bill_to.street2 = street2
        self.bill_to.city = city
        self.bill_to.state = state
        self.bill_to.postalCode = postalCode
        self.bill_to.country = country
        self.bill_to.customerID = customerID
        self.bill_to.email = email

    def check_response_for_cybersource_error(self):
        if self.response.reasonCode == 100:
            raise CyberScourceError(self.response.reasonCode,
                CYBERSOURCE_RESPONSES.get(self.response.reasonCode))
