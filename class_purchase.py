from database import execute
from datetime import datetime


class Purchase:
    def __init__(self) -> None:
        self.shopping_cart = []
        self.total_cost_of_shopping_cart = 0
        self.ordered_pizzas = []
        self.date_and_time = None

    def direct_pizza_to_shopping_cart_by_id_or_name(self, id_or_name_of_target_pizza: str) -> None:
        if id_or_name_of_target_pizza.isdigit():
            id_of_target_pizza = int(id_or_name_of_target_pizza)
            stmt_to_find_pizza = """
            SELECT cost_in_tenge, name FROM pizza WHERE pizza_id = ?
            """
        else:
            stmt_to_find_pizza = """
            SELECT cost_in_tenge, name FROM pizza WHERE name = ?
            """
        result = execute(stmt_to_find_pizza, (id_or_name_of_target_pizza,), is_fetchable=True, fetch_strategy="one")
        if result:
            cost_of_target_pizza, name_of_target_pizza = result
            self.shopping_cart.append(cost_of_target_pizza)
            self.ordered_pizzas.append(name_of_target_pizza)
            print(self.shopping_cart, self.ordered_pizzas)
            return True
        else:
            return "Пицца не найдена("

    def buy_pizza(self) -> str:
        now = datetime.now()
        self.date_and_time = now.strftime("%d/%m/%Y %H:%M:%S")
        self.total_cost_of_shopping_cart = sum(self.shopping_cart)
        counter = len(self.shopping_cart)
        return f"Поздравляю! Вы успешно заказали {counter} пицц на сумму {self.total_cost_of_shopping_cart} тенге"

    def to_empty_order(self) -> bool:
        self.shopping_cart.clear() 
        self.ordered_pizzas.clear() 
        return True 
