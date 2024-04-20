from database import execute
from class_purchase import Purchase
from class_users import User


class History:
    def __init__(self) -> None:
        pass

    def add_order_to_history(self, purchase: Purchase, target_user: User):
        ordered_pizzas_in_str = " "
        for i in purchase.ordered_pizzas:
            ordered_pizzas_in_str += i + ', '
        stmt_for_history = """
        INSERT INTO history(user_id, ordered_pizzas, total_price, date_time) VALUES (?, ?, ?, ?)
        """
        return execute(stmt_for_history, (target_user.current_user_id, ordered_pizzas_in_str, purchase.total_cost_of_shopping_cart, purchase.date_and_time), is_commitable=True)

