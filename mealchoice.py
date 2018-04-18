from orderitem import OrderItem


class MealChoice(OrderItem):

    def __init__(self, product_code:int, quantity:int=1):
        super().__init__(product_code, quantity)
        self.solution = None 


    def add_choice_solution(self, solution:OrderItem):
        self.solution = solution


    def output(self):
        '''
        Gives you the JSON for the order item output
        '''

        return {
            "ChoiceSolution": {**self.solution.output()},
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
