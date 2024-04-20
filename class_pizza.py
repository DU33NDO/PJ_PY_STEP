class Pizza:
    def __init__(self, name: str, description: str, cost_in_tenge: int, is_available: bool) -> None:
        self.name = name
        self.description = description
        self.cost_in_tenge = cost_in_tenge
        self.is_available = is_available

    def __repr__(self) -> str:
        return f"Название - {self.name}, Описание - {self.description}, Цена - {self.cost_in_tenge}, Доступен ли - {self.is_available}"
