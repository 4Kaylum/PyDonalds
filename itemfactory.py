from orderitem import OrderItem


class ItemFactory(object):

    @staticmethod
    def large_coke(quantity:int=1):
        return OrderItem(3010, quantity)


    @staticmethod
    def ketchup(quantity:int=1):
        return OrderItem(7616, quantity)


    @staticmethod
    def onion(quantity:int=1):
        return OrderItem(7611, quantity)


    @staticmethod
    def cheese(quantity:int=1):
        return OrderItem(7971, quantity)


    @staticmethod
    def pickles(quantity:int=1):
        return OrderItem(7617, quantity)


    @staticmethod
    def mustard(quantity:int=1):
        return OrderItem(7888, quantity)


    @staticmethod
    def mayo(quantity:int=1):
        return OrderItem(7619, quantity)


    @staticmethod
    def lettuce(quantity:int=1):
        return OrderItem(7979, quantity)


    @staticmethod
    def ice(quantity:int=1):
        return OrderItem(90080440, quantity)


    @staticmethod
    def quarter_pounder(quantity:int=1):
        return OrderItem(1060, quantity)


    @staticmethod
    def mcchicken_sandwich(quantity:int=1):
        return OrderItem(1472, quantity)


    @staticmethod
    def three_chicken_selects(quantity:int=1):
        return OrderItem(1427, quantity)


    @staticmethod
    def meal_constructor(main:OrderItem, side:OrderItem, drink:OrderItem, large:bool=True):
        '''
        Compiles your three items into a meal
        '''

        # Get the meal code
        meal_codes = {
            1427: (0, 6214),  # 3 Selects
            1472: (0, 6111),  # McChicken Sandwich, large
            1060: (6020, 0),  # Quarter Pounder, regular
        }.get(main.product_code)

        # Get the meal code
        meal_code = meal_codes[{True: 1, False: 0}[large]]

        # Construct the meal
        meal = OrderItem(meal_code)
        meal.add_component(main)

        # Make the side
        side_choice = MealChoice(10000011)
        new_side_code = {
            'LARGE_FRIES': 4834,  # Large fries
            'REGULAR_FRIES': 4833,  # Regular fries
        }.get(side.product_code)
        side = OrderItem(new_side_code, side.quantity)
        side_choice.add_choice_solution(side)
        meal.add_choice(side_choice)

        # Add the drink
        drink_choice = MealChoice(10000008)  # Drink menu
        sub_menu_hack = OrderItem(0)
        soft_drink_menu = MealChoice(9021)  # Soft drink sub-menu
        new_drink_code = {
            3010: 3030,  # Large Coke
            'LARGE_DIET': 3080,  # Large Diet Coke
            'REGULAR_ZERO': 3175,  # Regular Coke Zero
        }.get(drink.product_code)
        drink = OrderItem(new_drink_code, drink.quantity)
        soft_drink_menu.add_choice_solution(drink)
        sub_menu_hack.add_choice(soft_drink_menu)
        drink_choice.add_choice_solution(sub_menu_hack)
        meal.add_choice(drink_choice)

        return meal


