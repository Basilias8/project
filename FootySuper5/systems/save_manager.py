import json
import os
from datetime import datetime

class SaveManager:
    def __init__(self):
        self.save_slots = 5
        self.save_dir = "saves"
        os.makedirs(self.save_dir, exist_ok=True)

    def get_save_path(self, slot):
        return os.path.join(self.save_dir, f"career_{slot}.json")

    def save_game(self, data, slot):
        path = self.get_save_path(slot)
        save_data = {
            "data": data,
            "saved_at": datetime.now().isoformat(),
            "slot": slot
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)

    def load_game(self, slot):
        path = self.get_save_path(slot)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
                if "data" in save_data:
                    return save_data["data"]
        return None

    def get_save_info(self, slot):
        path = self.get_save_path(slot)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
                if "data" in save_data:
                    player = save_data["data"]["player"]
                    return {
                        "exists": True,
                        "player_name": player["name"],
                        "team": player["team"],
                        "rating": player["rating"],
                        "league": player["league"],
                        "saved_at": save_data["saved_at"]
                    }
                else:
                    print(f"Файл сохранения {slot} повреждён — нет ключа 'data'")
        return {"exists": False}

    def create_new_game(self, slot, player_name="New Career"):
        # Загружаем дефолтные данные
        try:
            with open("data/career_data.json", "r", encoding="utf-8") as f:
                default_data = json.load(f)
        except Exception as e:
            print(f"Не удалось загрузить data/career_data.json: {e}")
            default_data = {
                "player": {
                    "name": "Alex Hunter",
                    "age": 17,
                    "rating": 60,
                    "potential": 85,
                    "position": "ST",
                    "form": 0.7,
                    "experience": 0,
                    "injury_risk": 0.1,
                    "team": "Morecambe",
                    "league": "League Two",
                    "contract_years": 2,
                    "salary": 5000,
                    "goals": 0,
                    "assists": 0,
                    "matches": 0,
                    "awards": [],
                    "achievements": [],
                    "reputation": 50,
                    "customization": {
                        "hair_style": "short",
                        "hair_color": "black",
                        "skin_tone": "light",
                        "celebration": "arms_up",
                        "warmup_outfit": "track_suit"
                    },
                    "stats_history": {
                        "rating": [60],
                        "goals": [0],
                        "matches": [0],
                        "dates": ["2025-01-01"]
                    }
                },
                "season": {
                    "current_year": 2025,
                    "current_month": 1,
                    "current_day": 1,
                    "matches_played": 0,
                    "league_table": {},
                    "fixtures": []
                },
                "leagues": [
                    {
                        "name": "Premier League",
                        "level": 1,
                        "country": "England",
                        "promotion_spots": 0,
                        "relegation_spots": 3,
                        "teams": ["Manchester City", "Arsenal", "Liverpool", "Aston Villa", "Tottenham"]
                    }
                ],
                "tournaments": [
                    {
                        "name": "Champions League",
                        "type": "club",
                        "level": 1,
                        "teams": [],
                        "matches": [],
                        "prize_money": 100000000
                    }
                ],
                "stadiums": {
                    "Etihad Stadium": {
                        "name": "Etihad Stadium",
                        "capacity": 55000,
                        "attendance": 54000,
                        "condition": 95,
                        "facilities": 98,
                        "atmosphere": 92,
                        "renovation_cost": 10000000,
                        "last_renovation": "2024-06-15"
                    }
                },
                "transfer_market": {
                    "players": [
                        {
                            "name": "Young Talent",
                            "age": 18,
                            "rating": 65,
                            "position": "RW",
                            "asking_price": 50000,
                            "team": "Academy FC"
                        }
                    ]
                },
                "achievements": [
                    {"id": "first_goal", "name": "First Goal", "description": "Score your first goal", "unlocked": False},
                    {"id": "top_club", "name": "Top Club", "description": "Join a top-5 league club", "unlocked": False}
                ]
            }

        default_data["player"]["name"] = player_name
        default_data["player"]["team"] = "Morecambe"
        default_data["player"]["league"] = "League Two"
        
        self.save_game(default_data, slot)
        return default_data