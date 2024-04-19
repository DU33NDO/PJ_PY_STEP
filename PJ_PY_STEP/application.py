from database import execute
from tabulate import tabulate
from datetime import datetime
import hashlib


class Pizza:
    def __init__(self, name: str, description: str, cost_in_tenge: int, is_byable: bool, is_available: bool) -> None:
        self.name = name
        self.description = description
        self.cost_in_tenge = cost_in_tenge
        self.is_byable = is_byable
        self.is_available = is_available

    def __repr__(self) -> str:
        return f"Название - {self.name}, Описание - {self.description}, Цена - {self.cost_in_tenge}, Доступен ли - {self.is_available}, Купить - {self.is_byable}"


class DB:
    def __init__(self) -> None:
        pass

    def add_pizza_to_db(self, new_pizza: Pizza):
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
            stmt, (target_ingredient, target_id_pizza), is_commitable=True,
            )

        
class User:
    def __init__(self, current_user_id = 0) -> None:
        self.current_user_id = current_user_id

    def to_register(self, username: str, password: str): 
        print("РЕГИСТРАЦИЯ")
        str_hash_password = hashlib.sha512(password.encode()).hexdigest()
        stmt = """
        INSERT INTO users(username, password, status, is_in_account) VALUES (?, ?, ?, ?)
        """
        return execute(
            stmt, (username, str_hash_password, 'user', False), is_commitable=True
        )
    
    def to_login(self, username: str, password: str):
        print("ЛОГИН")
        str_hash_password = hashlib.sha512(password.encode()).hexdigest()

        stmt_for_verify = """
        SELECT username, password FROM users WHERE username == ? AND password == ?
        """
        list_for_login = execute(
            stmt_for_verify, (username, str_hash_password), is_fetchable=True, fetch_strategy="one"
            )
        
        if list_for_login is None: 
            print("Нет такого аккаунта(")
            return False 
        else: 
            print("Вы вошли в аккаунт!")
            stmt_for_user_id = """
            SELECT user_id FROM users WHERE username == ? AND password == ?
            """
            self.current_user_id = execute(stmt_for_user_id, (username, str_hash_password), is_fetchable=True, fetch_strategy="one")[0]
            stmt_for_is_in_account = """
            UPDATE users SET is_in_account = ? WHERE user_id = ?
            """
            execute(stmt_for_is_in_account, (True, self.current_user_id), is_commitable=True)
            return True
        
    def to_log_out(self):
        stmt_for_is_in_account = """
        UPDATE users SET is_in_account = ? WHERE user_id = ?
        """
        execute(stmt_for_is_in_account, (False, self.current_user_id), is_commitable=True)
        self.current_user_id = 0
        return "Вы вышли из аккаунт"
    
    class Purchase:
        shopping_cart: list[int] = []
        total_cost_of_shopping_cart: int = 0
        ordered_pizzas: list[str] = []
        date_and_time: datetime = ''

        def __init__(self) -> None:
            pass

        def direct_pizza_to_shopping_cart_by_id(self, id_of_target_pizza: int, shopping_cart=shopping_cart, ordered_pizzas=ordered_pizzas):
            stmt_to_find_pizza_by_id = """
            SELECT cost_in_tenge FROM pizza WHERE pizza_id = ?
            """
            cost_of_target_pizza = execute(stmt_to_find_pizza_by_id, (id_of_target_pizza,), is_fetchable=True, fetch_strategy="one")[0]
            self.shopping_cart.append(cost_of_target_pizza)

            stmt_to_find_pizza_name_by_id = """
            SELECT name FROM pizza WHERE pizza_id = ?
            """
            name_of_target_pizza = execute(stmt_to_find_pizza_name_by_id, (id_of_target_pizza,), is_fetchable=True, fetch_strategy="one")[0]
            self.ordered_pizzas.append(name_of_target_pizza)
            return (self.shopping_cart + self.ordered_pizzas)

        def direct_pizza_to_shopping_cart_by_name(self, name_of_target_pizza: str, shopping_cart=shopping_cart, ordered_pizzas=ordered_pizzas):
            stmt_to_find_pizza_by_id = """
            SELECT cost_in_tenge FROM pizza WHERE name = ?
            """
            cost_of_target_pizza = execute(stmt_to_find_pizza_by_id, (name_of_target_pizza.capitalize(),), is_fetchable=True, fetch_strategy="one")[0]
            self.shopping_cart.append(cost_of_target_pizza)

            stmt_to_find_pizza_name_by_id = """
            SELECT name FROM pizza WHERE name = ?
            """
            name_of_target_pizza = execute(stmt_to_find_pizza_name_by_id, (name_of_target_pizza.capitalize(),), is_fetchable=True, fetch_strategy="one")[0]
            self.ordered_pizzas.append(name_of_target_pizza)
            return (self.shopping_cart + self.ordered_pizzas)
        
        def buy_pizza(self, shopping_cart=shopping_cart):
            counter = 0
            now = datetime.now()
            self.date_and_time = now.strftime("%d/%m/%Y %H:%M:%S")
            for item in self.shopping_cart:
                counter += 1
                self.total_cost_of_shopping_cart += item
            return f"Поздравляю! Вы успешно заказали {counter} пицц на сумму {self.total_cost_of_shopping_cart}"
        
    class Menu:
        pizzas: list[Pizza] = []

        def __init__(self) -> None:
            pass
        
        def __str__(self) -> str:
            ...

        def create_menu(self, pizzas=pizzas):
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
    
    class History:
        def __init__(self) -> None:
            pass

        def add_order_to_history(self, purchase: , target_user: User):
            ordered_pizzas_in_str = " "
            for i in purchase.ordered_pizzas:
                ordered_pizzas_in_str += i + ', '
            stmt_for_history = """
            INSERT INTO history(user_id, ordered_pizzas, total_price, date_time) VALUES (?, ?, ?, ?)
            """
            return execute(stmt_for_history, (target_user.current_user_id, ordered_pizzas_in_str, purchase.total_cost_of_shopping_cart, purchase.date_and_time))
        



        


pizza_1 = Pizza("Сырная пицца", "Готовьтесь к взрыву сырного вкуса с нашей Сырной пиццей от Dodo Pizza! Насладитесь щедрой порцией разнообразных сыров, растопленных до идеальной нежности на нашем хрустящем корже. Каждый укус — это погружение в мир сырной гастрономии, где каждый вид сыра раскрывает свой неповторимый вкусовой шарм.", 3000, True, True)
pizza_2 = Pizza("Двойной цыпленок", "Приготовьтесь к вкусовому празднику с нашей Двойной Цыпленок пиццей от Dodo Pizza! Насладитесь двойной порцией нежного куриного мяса, обжаренного до золотистой хрустящей корочки, с изысканным сочетанием ароматных специй и натуральных ингредиентов, создающих настоящий вкусовой фейерверк. Ощутите множество оттенков вкуса в каждом укусе", 3200, True, True)
pizza_3 = Pizza("Ветчина и сыр", "Погрузитесь в атмосферу настоящего вкуса с нашей Ветчина и Сыр от Dodo Pizza! Нежная ветчина, сочный микс сыров, расплавленных до идеальной кремовой консистенции, на тонком хрустящем корже — это встреча с совершенством в каждом укусе. Раскройте новые грани наслаждения!", 3100, True, True)
pizza_4 = Pizza("Песто", "Откройте для себя волшебство вкуса с нашей пиццей Песто от Dodo Pizza! Нежное сочетание свежего базилика, ароматного чеснока и изысканного сыра, распределенное равномерно на тонком хрустящем корже — это настоящее воплощение итальянской кухни в каждом кусочке. Погрузитесь в мир неповторимого вкуса уже сегодня!", 3900, True, True)
pizza_5 = Pizza("Цыпленок барбекю", "Откройте новый мир вкусов с нашим главным хитом — Цыпленок барбекю от Dodo Pizza! Сочное куриное мясо, пропитанное ароматным барбекю-соусом, украшенное свежими помидорами и луком — это праздник для вашего вкуса! Закажите прямо сейчас и окунитесь в безграничный вкусовой рай!", 3900, True, True)
pizza_6 = Pizza("Пепперони", "Погрузитесь в классический вкус с нашей Пепперони-пиццей! Насладитесь идеальным сочетанием острого томатного соуса, тягучего моцарелла и ароматных ломтиков острой пепперони, все это на нашем неповторимом тонком корже. Каждый кусочек - это симфония вкусов, которая заставит ваши рецепторы желать еще.", 3900, True, True)
menu_1 = Menu()
db_1 = DB()
purchase_1 = Purchase()
user_1 = User()
user_2 = User()
user_3 = User()
history_1 = History()

# print(purchase_1.direct_pizza_to_shopping_cart_by_id(1))
# print(purchase_1.direct_pizza_to_shopping_cart_by_id(3))
# print(purchase_1.direct_pizza_to_shopping_cart_by_id(1))
# print(purchase_1.direct_pizza_to_shopping_cart_by_name("пепперони"))
# print(purchase_1.buy_pizza())
# print(history_1.add_order_to_history(purchase_1, user_2))

# print(user_3.to_register("admin", "123"))
# print(user_2.to_login("1111", "11"))
# print(user_2.to_log_out())


# print(db_1.add_pizza_to_db(pizza_6))
# print(db_1.add_ingredient_to_db(pizza_1, "Cucumber"))
# print(db_1.delete_pizza_from_db(pizza_6))
# print(db_1.delete_ingredient_from_db(pizza_1, "Cucumber"))
print(menu_1.create_menu())






# create_table_menu_stmt = """
# CREATE TABLE menu(id INTEGER PRIMARY KEY, name varchar (20), description varchar (40), compound varchar (100), compcost_in_tenge float, is_available integer )
# """
# execute(create_table_menu_stmt, is_commitable=True)

create_table_pizza_stmt = """
CREATE TABLE pizza1(pizza_id INTEGER PRIMARY KEY, name varchar (20), description varchar (40), compcost_in_tenge float, is_available BOOLEAN DEFAULT 1 )
"""
# execute(create_table_pizza_stmt, is_commitable=True)
create_table_ingr_stmt = """
CREATE TABLE ingredients(id_ingr INTEGER PRIMARY KEY, pizza_id integer, ingredient_name varchar(50), FOREIGN KEY (pizza_id) REFERENCES pizza(pizza_id) ON DELETE CASCADE)
"""
# execute(create_table_ingr_stmt, is_commitable=True)
create_table_users_stmt = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, username varchar(50), password varchar(50), status varchar(10), is_in_account integer)
"""
# execute(create_table_users_stmt, is_commitable=True)
create_table_history_stmt = """
CREATE TABLE history( history_id INTEGER PRIMARY KEY, user_id INTEGER, ordered_pizzas VARCHAR(250), total_price INTEGER, date_time VARCHAR(70), FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
"""
#execute(create_table_history_stmt, is_commitable=True)