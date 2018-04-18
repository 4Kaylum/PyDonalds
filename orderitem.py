class OrderItem(object):

    def __init__(self, product_code:int, quantity:int=1):
        self.product_code = product_code
        self.quantity = quantity
        self.customizations = []
        self.choices = []
        self.components = []


    def __repr__(self):
        return '<{0.__class__.__name__} object; Item={0!s}, Customizations={1}>'.format(
            self, len(self.customizations)
        )


    def __str__(self):
        return {
            3010: 'Large Coke',
            90080440: 'Ice'
        }.get(self.product_code, 'UNKNOWN_ITEM')


    def add_customization(self, custom):
        '''
        Adds a customization to the order
        '''

        self.customizations.append(custom)


    def add_component(self, component):
        '''
        Adds a component to the order
        '''

        self.components.append(component)


    def add_choice(self, choice):
        '''
        Adds a choice to the order
        '''

        self.choices.append(choice)


    def output(self):
        '''
        Gives you the JSON for the order item output
        '''

        return {
            "Choices": [i.output() for i in self.choices],
            "Components": [i.output() for i in self.components],
            "Customizations": [i.output() for i in self.customizations],
            "ChangeStatus": 0,
            "IsLight": False,
            "IsPromotional": False,
            "ProductCode": self.product_code,
            "PromoQuantity": 0,
            "Quantity": self.quantity,
            "TotalEnergy": 0.0,
            "TotalValue": 0.0,
            "UnitPrice": 0.0,
            "ValidationErrorCode": 0
        }
