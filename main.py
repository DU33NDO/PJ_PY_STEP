from database import execute


class Pizza:
    def __init__(self, name: str, description: str, cost_in_tenge: int, is_byable: bool, is_available: bool) -> None:
        self.name = name
        self.description = description
        self.cost_in_tenge = cost_in_tenge
        self.is_byable = is_byable
        self.is_available = is_available



    def __repr__(self) -> str:
        return f"Название - {self.name}, Описание - {self.description}, Цена - {self.cost_in_tenge}, Доступен ли - {self.is_available}, Купить - {self.is_byable}"


class Menu:
    pizzas: list[Pizza] = []

    def __init__(self) -> None:
        pass
    
        
    def __str__(self) -> str:
        return f"{self.pizzas}"


class DB:
    def __init__(self) -> None:
        pass

    def add_pizza_to_db(self, new_pizza: Pizza):
        stmt = """
        INSERT INTO pizza(name, description, cost_in_tenge, is_available) VALUES (?, ?, ?, ?) 
        """
        return execute(
            stmt, (new_pizza.name, new_pizza.description, new_pizza.cost_in_tenge, new_pizza.is_available,), is_commitable=True,
            )
    
    def delete_pizza_from_db(self, target_pizza: Pizza):
        stmt = """
        DELETE FROM pizza WHERE name = ?
        """
        return execute(
            stmt, (target_pizza.name,), is_commitable=True,
            )
    
    def add_ingredient_to_db(self, targer_pizza: Pizza, new_ingredient: str):
        stmt_for_finding_id_pizza = """
        SELECT pizza_id FROM pizza WHERE name = ?
        """
        target_id_pizza = execute(stmt_for_finding_id_pizza, (targer_pizza.name,), is_fetchable=True, fetch_strategy="one")[0]
        stmt_for_adding_ingredient = """
        INSERT INTO ingredients(pizza_id, ingredient_name) VALUES (?, ?) 
        """
        return execute(stmt_for_adding_ingredient, (target_id_pizza, new_ingredient), is_commitable=True )
    
    def delete_ingredient_from_db(self, target_pizza: Pizza, target_ingredient: Pizza):
        stmt_for_finding_id_pizza = """
        SELECT pizza_id FROM pizza WHERE name = ?
        """
        target_id_pizza = execute(stmt_for_finding_id_pizza, (target_pizza.name,), is_fetchable=True, fetch_strategy="one")[0]
        stmt = """
        DELETE FROM ingredients WHERE ingredient_name = ? AND pizza_id = ? 
        """
        return execute(
            stmt, (target_ingredient.name, target_id_pizza), is_commitable=True,
            )


    

pizza_1 = Pizza("Peperoni", "мясная пицца", 1200, True, True)
pizza_2 = Pizza("Dodo", "Не пицца, а вау", 11200, True, True)
menu_1 = Menu()
db_1 = DB()
# print(db_1.add_pizza_to_db(pizza_2))
#print(db_1.add_ingredient_to_db(pizza_2, "tomato"))
# print(db_1.delete_pizza_from_db(pizza_1))
print(db_1.delete_ingredient_from_db(pizza_1, "tomato"))






# create_table_menu_stmt = """
# CREATE TABLE menu(id INTEGER PRIMARY KEY, name varchar (20), description varchar (40), compound varchar (100), compcost_in_tenge float, is_available integer )
# """
# execute(create_table_menu_stmt, is_commitable=True)

create_table_pizza_stmt = """
CREATE TABLE pizza(pizza_id INTEGER PRIMARY KEY, name varchar (20), description varchar (40), compcost_in_tenge float, is_available integer )
"""
# execute(create_table_pizza_stmt, is_commitable=True)
create_table_ingr_stmt = """
CREATE TABLE ingredients(id_ingr INTEGER PRIMARY KEY, pizza_id integer, ingredient_name varchar(50), FOREIGN KEY (pizza_id) REFERENCES pizza(pizza_id) ON DELETE CASCADE)
"""
# execute(create_table_ingr_stmt, is_commitable=True)
