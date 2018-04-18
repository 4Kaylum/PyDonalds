from orderitem import OrderItem


class Order(object):

    def __init__(self, store_id:str, *, market_id:str="UK", application:str="MOT", language_name:str="en-GB", platform:str="android", username:str=""):
        self.store_id = store_id
        self.market_id = market_id
        self.application = application
        self.language_name = language_name
        self.platform = platform 
        self.username = username

        # Items in the order
        self.items = []


    def add_item(self, item:OrderItem):
        '''
        Adds an item to your order
        '''

        self.items.append(item)


    def output(self):
        '''
        Gives you the JSON data for the raw order
        '''

        base = {
            "marketId": self.market_id,
            "application": self.application,
            "languageName": self.language_name,
            "platform": self.platform,
            "userName": self.username,
            "storeId": self.store_id,
            "orderView": {}
        }
        order_view = {
            'CouponValue': 0.0,
            'ConfirmationNeeded': False,
            'IsEDTCalculationEnabled': False,
            'IsLargeOrder': False,
            'IsNormalOrder': False,
            'Language': self.language_name,
            'Market': self.market_id,
            'NickName': '',
            'OrderValue': 0.0,
            'PriceType': 1,
            'Products': [],
            'PromotionListView': [],
            'StoreID': self.store_id,
            'TotalDiscount': 0.0,
            'TotalDue': 0.0,
            'TotalEnergy': 0.0,
            'TotalTax': 0.0,
            'TotalValue': 0.0,
            'UserName': self.username
        }
        products = [i.output() for i in self.items]

        # Compile together
        order_view['Products'] = products
        base['orderView'] = order_view
        return base

