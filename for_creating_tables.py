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