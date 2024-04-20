from class_pizza import Pizza
from database import execute
from tabulate import tabulate


class Menu:
    pizzas: list[Pizza] = []

    def __init__(self) -> None:
        pass

    def create_menu(self, pizzas=pizzas) -> None:
        stmt_for_all_rows_pizza = """
        SELECT * FROM pizza
        """
        all_pizza_information = execute(stmt_for_all_rows_pizza, is_fetchable=True, fetch_strategy="all")
        
        stmt_for_all_rows_ingredients = """
        SELECT * FROM ingredients
        """
        all_ingredients_information = execute(stmt_for_all_rows_ingredients, is_fetchable=True, fetch_strategy="all")

        for pizza in all_pizza_information:
            new_pizza = list(pizza)
            new_list_for_ingredients = []
            for ingredient in all_ingredients_information:
                if ingredient[1] == pizza[0]:
                    new_list_for_ingredients.append(ingredient[2])
            new_pizza.insert(3, new_list_for_ingredients)
            self.pizzas.append(new_pizza)
        
        headers = ["Название", "Описание", "Ингредиенты", "Цена в тенге", "Доступность"]
        return tabulate(pizzas, headers=headers, tablefmt="grid", numalign="center")
