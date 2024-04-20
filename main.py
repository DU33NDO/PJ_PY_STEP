from database import execute
from tabulate import tabulate
from datetime import datetime
import hashlib
from class_pizza import Pizza
from class_users import User
from class_menu import Menu
from class_DB import DB
from class_purchase import Purchase
from class_history import History
import time


pizza_1 = Pizza("Сырная пицца", "Готовьтесь к взрыву сырного вкуса с нашей Сырной пиццей от Dodo Pizza! Насладитесь щедрой порцией разнообразных сыров, растопленных до идеальной нежности на нашем хрустящем корже. Каждый укус — это погружение в мир сырной гастрономии, где каждый вид сыра раскрывает свой неповторимый вкусовой шарм.", 3000, True)
pizza_2 = Pizza("Двойной цыпленок", "Приготовьтесь к вкусовому празднику с нашей Двойной Цыпленок пиццей от Dodo Pizza! Насладитесь двойной порцией нежного куриного мяса, обжаренного до золотистой хрустящей корочки, с изысканным сочетанием ароматных специй и натуральных ингредиентов, создающих настоящий вкусовой фейерверк. Ощутите множество оттенков вкуса в каждом укусе", 3200, True)
pizza_3 = Pizza("Ветчина и сыр", "Погрузитесь в атмосферу настоящего вкуса с нашей Ветчина и Сыр от Dodo Pizza! Нежная ветчина, сочный микс сыров, расплавленных до идеальной кремовой консистенции, на тонком хрустящем корже — это встреча с совершенством в каждом укусе. Раскройте новые грани наслаждения!", 3100, True)
pizza_4 = Pizza("Песто", "Откройте для себя волшебство вкуса с нашей пиццей Песто от Dodo Pizza! Нежное сочетание свежего базилика, ароматного чеснока и изысканного сыра, распределенное равномерно на тонком хрустящем корже — это настоящее воплощение итальянской кухни в каждом кусочке. Погрузитесь в мир неповторимого вкуса уже сегодня!", 3900, True)
pizza_5 = Pizza("Цыпленок барбекю", "Откройте новый мир вкусов с нашим главным хитом — Цыпленок барбекю от Dodo Pizza! Сочное куриное мясо, пропитанное ароматным барбекю-соусом, украшенное свежими помидорами и луком — это праздник для вашего вкуса! Закажите прямо сейчас и окунитесь в безграничный вкусовой рай!", 3900, True)
pizza_6 = Pizza("Пепперони", "Погрузитесь в классический вкус с нашей Пепперони-пиццей! Насладитесь идеальным сочетанием острого томатного соуса, тягучего моцарелла и ароматных ломтиков острой пепперони, все это на нашем неповторимом тонком корже. Каждый кусочек - это симфония вкусов, которая заставит ваши рецепторы желать еще.", 3900, True)

while True:
    print("Привет! Добро пожаловать в приложению для пиццерии!")
    user_answer = input("Выберите опицю: 1) Регистрация, 2) Вход: ")
    if user_answer == "1":
        user_current = User()
        current_username = input("Введите свой никнейм: ")
        current_password = input("Введите свой пароль: ")
        print(user_current.to_register(current_username, current_password))
    elif user_answer == "2":
        user_current = User()
        current_username = input("Введите свой никнейм: ")
        current_password = input("Введите свой пароль: ")
        print(user_current.to_login(current_username, current_password))
        if user_current.to_login(current_username, current_password) == True and user_current.current_status == 'user':
            while True:
                menu_current = Menu() 
                print(menu_current.create_menu())
                purchase_1 = Purchase()
                while True:
                    print("Если вы хотите выйти, то напишите 'выход'")
                    user_answer_after_menu = input("Для покупки пиццы можете написать название или id желанной пиццы: ")
                    if user_answer_after_menu.lower() == "выход":
                        break
                    if purchase_1.direct_pizza_to_shopping_cart_by_id_or_name(user_answer_after_menu):
                        user_answer_after_purchase = input("вы хотите продолжить покупку? /да, нет: ")
                        if user_answer_after_purchase.lower() == 'нет':
                            history_1 = History()
                            print(purchase_1.buy_pizza())
                            history_1.add_order_to_history(purchase_1, user_current)
                            purchase_1.to_empty_order()
                            break
                        elif user_answer_after_purchase.lower() != 'да':
                            print("Нет такого ответа(")
                time.sleep(7)
                user_answer_for_exit = int(input("Если вы хотите выйти из аккаунта напишите '3': "))
                if user_answer_for_exit == 3:
                    user_current.to_log_out()
                    break
        elif user_current.to_login(current_username, current_password) == True and user_current.current_status == 'admin':
            while True:
                user_answer_for_exit = int(input("Если вы хотите выйти из аккаунта напишите '3': "))
                if user_answer_for_exit == 3:
                    user_current.to_log_out()
                    break
                db_1 = DB()
                menu_current = Menu() 
                print(menu_current.create_menu())
                print()
                admin_answer_after_login = int(input("Выберите опицию: 1) изменить пиццы, 2) изменить ингредиенты пицц: "))
                if admin_answer_after_login == 1:
                    admin_answer_for_pizza = int(input("Выберите опцию: 1) Добавить пиццу; 2) Удалить пиццу: "))
                    if admin_answer_for_pizza == 1:
                        admin_answer_for_alter_pizza_name = input("Введите название новой пиццы: ")
                        admin_answer_for_alter_pizza_desc = input("Введите описание новой пиццы: ")
                        admin_answer_for_alter_pizza_cost_in_tenge = float(input("Введите стоимость новой пиццы: "))
                        admin_answer_for_alter_pizza_available = bool(input("Введите доступна ли новая пицца (True; False): "))
                        new_pizza = Pizza(admin_answer_for_alter_pizza_name, admin_answer_for_alter_pizza_desc, admin_answer_for_alter_pizza_cost_in_tenge,admin_answer_for_alter_pizza_available)
                        db_1.add_pizza_to_db(new_pizza)
                    elif admin_answer_for_pizza == 2:
                        admin_answer_for_target_delete_pizza_id = int(input("Введите id пиццы: "))
                        target_pizza = db_1.to_find_pizza_by_id(admin_answer_for_target_delete_pizza_id)
                        db_1.delete_pizza_from_db(target_pizza)
                    else: 
                        print("нет такого выбора(")
                elif admin_answer_after_login == 2:
                    admin_answer_for_ingred = int(input("Выберите опцию: 1) Добавить ингредиенты; 2) Удалить ингредиенты: "))
                    if admin_answer_for_ingred == 1:
                        while True:
                            admin_answer_for_target_delete_pizza_id = int(input("Введите id пиццы: "))
                            target_pizza = db_1.to_find_pizza_by_id(admin_answer_for_target_delete_pizza_id)
                            while True:
                                admin_answer_new_ingredient = input("Введите новый ингредиент: ")
                                db_1.add_ingredient_to_db(target_pizza, admin_answer_new_ingredient)
                                admin_choice_in_ingred_for_exit = int(input("Выберите опцию: 1) Добавить еще ингредиент; 2) Сменить пиццу; 3) Выйти отсюда: "))
                                if admin_choice_in_ingred_for_exit == 2:
                                    break
                                elif admin_choice_in_ingred_for_exit == 3:
                                    break
                            if admin_choice_in_ingred_for_exit == 3:
                                break
                    elif admin_answer_for_ingred == 2:
                        admin_answer_for_target_delete_pizza_id = int(input("Введите id пиццы: "))
                        target_pizza = db_1.to_find_pizza_by_id(admin_answer_for_target_delete_pizza_id)
                        admin_answer_delete_ingred = input("Введите название ингредиента для удаления: ")
                        db_1.delete_ingredient_from_db(target_pizza, admin_answer_delete_ingred)
                    else: 
                        print("нет такого выбора(")
    else:
        print("нет такого выбора(")