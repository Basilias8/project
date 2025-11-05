import random

class AICoach:
    def __init__(self, career_system):
        self.career_system = career_system

    def get_advice(self):
        player = self.career_system.data["player"]
        
        # Анализ текущей ситуации
        if player["rating"] < 70:
            return "Тренер: Сфокусируйся на тренировках! Твой рейтинг ещё низкий."
        elif player["goals"] < 5:
            return "Тренер: Тебе нужно чаще бить по воротам! Попробуй мини-игру 'Попади по цели'."
        elif player["team"] in ["Rookie FC", "Village United"] and player["rating"] > 75:
            return "Тренер: Пора искать трансфер в более сильный клуб!"
        elif player["rating"] > 85:
            return "Тренер: Ты готов к топ-турнирам! Попробуй Лигу чемпионов."
        elif player["form"] < 0.6:
            return "Тренер: Твоя форма упала! Отдохни пару дней."
        elif player["contract_years"] <= 1:
            return "Тренер: Контракт скоро закончится! Готовься к переговорам."
        else:
            tips = [
                "Тренер: Отдыхай между матчами — это улучшает форму.",
                "Тренер: Играй в мини-игры — они дают бонусы к рейтингу.",
                "Тренер: Следи за контрактом — не упусти выгодное предложение!",
                "Тренер: Участвуй в турнирах — это путь к наградам!",
                "Тренер: Работай над ассистами — командная игра важна!",
                "Тренер: Анализируй соперников перед матчами!"
            ]
            return random.choice(tips)

    def get_training_recommendation(self):
        player = self.career_system.data["player"]
        if player["age"] < 25:
            return "Рекомендация: Тренируйся чаще — твой возраст идеален для роста!"
        elif player["age"] < 30:
            return "Рекомендация: Балансируй тренировки и отдых — сохраняй форму."
        else:
            return "Рекомендация: Фокусируйся на поддержании формы — возраст не помеха!"

    def get_transfer_recommendation(self):
        player = self.career_system.data["player"]
        top_clubs = ["Manchester City", "Real Madrid", "Bayern Munich", "Liverpool", "Barcelona"]
        
        if player["rating"] > 80 and player["team"] in ["Rookie FC", "Village United"]:
            return "Рекомендация: Запроси трансфер в топ-клуб — ты готов!"
        elif player["rating"] > 85 and player["team"] not in top_clubs:
            return "Рекомендация: Ты звезда! Требуй перехода в элитный клуб!"
        elif player["contract_years"] <= 1:
            return "Рекомендация: Подумай о новом контракте — срок истекает!"
        elif player["team"] in top_clubs:
            return "Рекомендация: Ты в элите! Докажи, что достоин основного состава!"
        else:
            return "Рекомендация: Останься в клубе — тебе доверяют!"