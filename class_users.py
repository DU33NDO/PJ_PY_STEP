from database import execute
import hashlib


class User:
    def __init__(self) -> None:
        self.current_user_id = 0
        self.current_status = ""

    def to_register(self, username: str, password: str) -> None: 
        print("РЕГИСТРАЦИЯ")
        str_hash_password = hashlib.sha512(password.encode()).hexdigest()
        stmt = """
        INSERT INTO users(username, password, status, is_in_account) VALUES (?, ?, ?, ?)
        """
        return execute(
            stmt, (username, str_hash_password, 'user', False), is_commitable=True
        )
    
    def to_login(self, username: str, password: str) -> bool:
        print("ЛОГИН")
        str_hash_password = hashlib.sha512(password.encode()).hexdigest()

        stmt_for_verify = """
        SELECT username, password FROM users WHERE username == ? AND password == ?
        """
        list_for_login = execute(
            stmt_for_verify, (username, str_hash_password), is_fetchable=True, fetch_strategy="one"
            )
        
        stmt_for_status = """
        SELECT status FROM users WHERE username == ? AND password == ?
        """
        self.current_status = execute(
            stmt_for_status, (username, str_hash_password), is_fetchable=True, fetch_strategy="one"
            )[0]
        
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
        
    def to_log_out(self) -> str:
        stmt_for_is_in_account = """
        UPDATE users SET is_in_account = ? WHERE user_id = ?
        """
        execute(stmt_for_is_in_account, (False, self.current_user_id), is_commitable=True)
        self.current_user_id = 0
        return "Вы вышли из аккаунт"
