import random
from datetime import datetime, timedelta

class StadiumSystem:
    def __init__(self, career_system):
        self.career_system = career_system

    def get_stadium(self, stadium_name):
        if stadium_name in self.career_system.data["stadiums"]:
            return self.career_system.data["stadiums"][stadium_name]
        return None

    def rename_stadium(self, old_name, new_name):
        if old_name in self.career_system.data["stadiums"]:
            stadium = self.career_system.data["stadiums"][old_name]
            stadium["name"] = new_name
            self.career_system.data["stadiums"].pop(old_name)
            self.career_system.data["stadiums"][new_name] = stadium
            self.career_system.save_data()
            return f"Стадион переименован: {new_name}"
        return "Стадион не найден"

    def upgrade_stadium(self, stadium_name, upgrade_type):
        stadium = self.get_stadium(stadium_name)
        if not stadium:
            return "Стадион не найден"
        
        team = self.career_system.data["teams"][self.career_system.data["player"]["team"]]
        if team["budget"] < 100000:
            return "Недостаточно бюджета для улучшения"
        
        if upgrade_type == "capacity":
            increase = random.randint(1000, 5000)
            stadium["capacity"] += increase
            team["budget"] -= 50000
            return f"Вместимость увеличена на {increase} мест"
        elif upgrade_type == "facilities":
            stadium["facilities"] = min(100, stadium["facilities"] + 10)
            team["budget"] -= 30000
            return "Улучшены раздевалки и тренажёры"
        elif upgrade_type == "atmosphere":
            stadium["atmosphere"] = min(100, stadium["atmosphere"] + 15)
            team["budget"] -= 20000
            return "Улучшена атмосфера стадиона"
        
        self.career_system.save_data()
        return "Улучшение завершено"

    def get_stadium_info(self, stadium_name):
        stadium = self.get_stadium(stadium_name)
        if stadium:
            return f"""
{stadium['name']}
Вместимость: {stadium['capacity']}
Посещаемость: {stadium['attendance']}
Состояние: {stadium['condition']}%
Удобства: {stadium['facilities']}%
Атмосфера: {stadium['atmosphere']}%
Стоимость ремонта: ${stadium['renovation_cost']}
Последний ремонт: {stadium['last_renovation']}
"""
        return "Стадион не найден"