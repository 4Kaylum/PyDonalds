import requests
from errorchecker import ErrorChecker, McDonaldsException
from order import Order
from itemfactory import ItemFactory


class Spoofer(object):

    BASE = 'https://eu-mcd.eu.cloudhub.io'
    ORDER = BASE + '/v3/order/total'
    SIGNIN = BASE + '/v3/customer/session/sign-in-and-authenticate'
    PAYMENT = BASE + '/v3/order/payment'
    PICKUP = BASE + '/v3/order/finalization/pickup'

    def __init__(self, api_key:str, *, hashstr:str="McD_API_Spoofer", market_id:str='UK', application:str='MOT', language_name:str='en-GB', platform:str='android', version_id:str='0.0.1.I', nonce:str='happybaby'):
        # Auth stuff
        self.token = None
        self.api_key = api_key
        self.nonce = nonce
        self.username = None

        # Login
        self.hash = hashstr

        # Used in order
        self.platform = platform
        self.market_id = market_id
        self.application = application
        self.language_name = language_name
        self.version_id = version_id

        # Payment info
        self.order_payment_id = None

    @property
    def headers(self):
        '''
        Gets the headers for the class
        '''

        v = {
            'marketId': self.market_id,
            'mcd_apikey': self.api_key
        }
        if self.token:
            v.update({'Token': self.token})
        return v


    def _check_signed_in(f):
        def wrapper(self, *args, **kwargs):
            if not self.username:
                raise McDonaldsException('Not signed in.')
            return f(self, *args, **kwargs)
        return wrapper


    def sign_in(self, username:str, password:str):
        '''
        Signs in and gets the token for you
        '''

        # Get the url and params
        url = self.SIGNIN
        json = {
            "marketId": self.market_id,
            "application": self.application,
            "languageName": self.language_name,
            "platform": self.platform,
            "versionId": self.version_id,
            "nonce": self.nonce,
            "hash": self.hash,
            "userName": username,
            "password": password,
            "newPassword": None
        }

        # Send request to McD
        site = requests.post(url, json=json, headers=self.headers)

        # Make sure there's no status error
        ErrorChecker.check(site)

        # Store relevant information in class
        self.username = username
        self.token = site.json()['Data']['AccessData']['Token']
        return 


    @_check_signed_in
    def new_order(self, store_id:str):
        '''
        Gets a new order object for you
        '''

        # Requires you to be signed in

        return Order(
            store_id=store_id,
            market_id=self.market_id, 
            application=self.application, 
            language_name=self.language_name, 
            platform=self.platform, 
            username=self.username
        )


    @_check_signed_in
    def get_total(self, order:Order):
        '''
        Gets you the total for an order
        '''

        # Generate params
        json = order.output()

        # Send request
        site = requests.post(self.ORDER, json=order.output(), headers=self.headers)

        # Make sure it's valid
        if not site.status_code == 200:
            return site

        # Return the relevant info
        json = site.json()
        try:
            return json['Data']['OrderView']['TotalValue']
        except KeyError:
            raise McDonaldsException('Login timed out.')


    @_check_signed_in
    def payment(self, order:Order, *, price_type:int=2, payment_data_id:int=-1, payment_method_id:int=5, pod:int=0, customer_payment_method_id:int):
        '''
        Sends a payment to the store location
        '''

        # Generate params
        json = order.output()
        json['orderView']['Payment'] = {
            "POD": pod,
            "CustomerPaymentMethodId": customer_payment_method_id,
            "PaymentDataId": payment_data_id,
            "PaymentMethodId": payment_method_id
        }
        json['orderView']['PriceType'] = price_type
        url = self.PAYMENT

        # Send request
        site = requests.post(url, json=json, headers=self.headers)

        # Check it's valid
        ErrorChecker.check(site)

        # Store the useful data
        data = site.json()
        # self.order_payment_id = data['Data']['OrderView']['OrderPaymentId']
        self.order_payment_id = -1


    @_check_signed_in
    def pickup(self, order:Order, *, check_in_data:str='0', price_type:int=2, payment_data_id:int=-1, payment_method_id:int=5, pod:int=0, customer_payment_method_id:int):
        '''
        Lets you pick up your order - THIS WILL CHARGE YOUR PAYMENT METHOD
        '''

        # Generate the params
        json = order.output()
        json['orderView']['Payment'] = {
            "POD": pod,
            "CustomerPaymentMethodId": customer_payment_method_id,
            "PaymentDataId": payment_data_id,
            "PaymentMethodId": payment_method_id,
            "OrderPaymentId": self.order_payment_id
        }
        json['orderView']['PriceType'] = price_type
        json['checkInData'] = check_in_data
        url = self.PICKUP 

        # Send request
        site = requests.post(url, json=json, headers=self.headers)

        # Check it's valid
        ErrorChecker.check(site)

        # Return relevant info
        data = site.json()
        try:
            return data['Data']['OrderNumber']
        except:
            return data
