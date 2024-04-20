from class_pizza import Pizza
from database import execute


class DB:
    def __init__(self) -> None:
        pass

    def add_pizza_to_db(self, new_pizza: Pizza) -> None:
        new_pizza_description_words = new_pizza.description.split()
        new_pizza_formatted_description = ""
        line_len = 0
        
        for word in new_pizza_description_words:
            if line_len + len(word) <= 80:
                new_pizza_formatted_description += word + ' '
                line_len += len(word) + 1
            else:
                new_pizza_formatted_description += '\n' + word + ' '
                line_len = len(word) + 1 
        stmt = """
        INSERT INTO pizza(name, description, cost_in_tenge, is_available) VALUES (?, ?, ?, ?) 
        """
        return execute(
            stmt, (new_pizza.name, new_pizza_formatted_description, new_pizza.cost_in_tenge, new_pizza.is_available,), is_commitable=True,
            )
    
    def delete_pizza_from_db(self, target_pizza: Pizza) -> None:
        stmt = """
        DELETE FROM pizza WHERE name = ?
        """
        return execute(
            stmt, (target_pizza.name,), is_commitable=True,
            )
    
    def add_ingredient_to_db(self, targer_pizza: Pizza, new_ingredient: str) -> None:
        stmt_for_finding_id_pizza = """
        SELECT pizza_id FROM pizza WHERE name = ?
        """
        target_id_pizza = execute(stmt_for_finding_id_pizza, (targer_pizza.name,), is_fetchable=True, fetch_strategy="one")[0]
        stmt_for_adding_ingredient = """
        INSERT INTO ingredients(pizza_id, ingredient_name) VALUES (?, ?) 
        """
        return execute(stmt_for_adding_ingredient, (target_id_pizza, new_ingredient), is_commitable=True )
    
    def delete_ingredient_from_db(self, target_pizza: Pizza, target_ingredient: str) -> None:
        stmt_for_finding_id_pizza = """
        SELECT pizza_id FROM pizza WHERE name = ?
        """
        target_id_pizza = execute(stmt_for_finding_id_pizza, (target_pizza.name,), is_fetchable=True, fetch_strategy="one")[0]
        stmt = """
        DELETE FROM ingredients WHERE ingredient_name = ? AND pizza_id = ? 
        """
        return execute(
            stmt, (target_ingredient, target_id_pizza), is_commitable=True,
            )
    
    def to_find_pizza_by_id(self, id: int) -> Pizza:
        stmt_for_finding_id = """
        SELECT * FROM pizza WHERE pizza_id = ?
        """
        attributes = execute(stmt_for_finding_id, (id,), is_fetchable=True, fetch_strategy="all")
        new_pizza = Pizza(attributes[0][1], attributes[0][2], attributes[0][3], attributes[0][4])
        return new_pizza
# db_1 = DB()
# print(db_1.to_find_pizza_by_id(9))