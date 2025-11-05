import json
import random
import os
from datetime import datetime, timedelta

class CareerSystem:
    def __init__(self, save_slot=0):
        self.save_slot = save_slot
        self.data_file = f"saves/career_{save_slot}.json"
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = self.create_default_data()
            self.save_data()

    def save_data(self):
        os.makedirs("saves", exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def create_default_data(self):
        # Загружаем дефолтные данные
        try:
            with open("data/career_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Не удалось загрузить data/career_data.json: {e}")
            return {
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
                    "league": "League One",
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
                        "name": "League One",
                        "level": 3,
                        "country": "England",
                        "promotion_spots": 2,
                        "relegation_spots": 4,
                        "teams": ["Morecambe"],
                        "teams_data": {
                            "Morecambe": {
                                "players": [
                                    {"name": "Alex Hunter", "position": "ST", "rating": 60, "age": 17, "form": 0.7},
                                    {"name": "John Doe", "position": "CM", "rating": 58, "age": 24, "form": 0.65}
                                ],
                                "budget": 5000000,
                                "tactics": "4-4-2",
                                "coach": "Manager Smith",
                                "points": 0,
                                "goals_for": 0,
                                "goals_against": 0,
                                "position": 20,
                                "rating": 58
                            }
                        }
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

    def advance_date(self, days=1):
        if "season" not in self.data:
            self.data["season"] = {
                "current_year": 2025,
                "current_month": 1,
                "current_day": 1,
                "matches_played": 0,
                "league_table": {},
                "fixtures": []
            }
        
        season = self.data["season"]
        season["current_day"] += days
        
        if season["current_month"] in [1, 3, 5, 7, 8, 10, 12] and season["current_day"] > 31:
            season["current_day"] = 1
            season["current_month"] += 1
        elif season["current_month"] in [4, 6, 9, 11] and season["current_day"] > 30:
            season["current_day"] = 1
            season["current_month"] += 1
        elif season["current_month"] == 2 and season["current_day"] > 28:
            season["current_day"] = 1
            season["current_month"] += 1
            
        if season["current_month"] > 12:
            season["current_month"] = 1
            season["current_year"] += 1
            self.process_end_of_season()
            
        self.save_data()

    def process_end_of_season(self):
        for league in self.data["leagues"]:
            teams = league["teams"]
            for team_name in teams:
                if team_name in league["teams_data"]:
                    team = league["teams_data"][team_name]
                    team["points"] = random.randint(30, 90)
                    team["goals_for"] = random.randint(40, 80)
                    team["goals_against"] = random.randint(30, 70)
            
            sorted_teams = sorted(teams, key=lambda x: league["teams_data"][x]["points"], reverse=True)
            
            for i, team_name in enumerate(sorted_teams):
                league["teams_data"][team_name]["position"] = i + 1

    def train_player(self):
        player = self.data["player"]
        
        base_growth = 0
        if player["age"] < 21:
            base_growth = random.uniform(0.2, 0.8)
        elif player["age"] < 25:
            base_growth = random.uniform(0.1, 0.5)
        elif player["age"] < 28:
            base_growth = random.uniform(0.0, 0.3)
        elif player["age"] < 32:
            base_growth = random.uniform(-0.1, 0.2)
        else:
            base_growth = random.uniform(-0.3, -0.1)
        
        if player["rating"] >= player["potential"] - 5:
            base_growth *= 0.3
        elif player["rating"] >= player["potential"] - 10:
            base_growth *= 0.6
        
        form_multiplier = player["form"] * 0.8 + 0.2
        experience_multiplier = min(1.0, player["experience"] / 1000 + 0.5)
        final_growth = base_growth * form_multiplier * experience_multiplier
        
        new_rating = player["rating"] + final_growth
        player["rating"] = max(50, min(player["potential"], new_rating))
        
        player["experience"] += random.randint(15, 25)
        player["form"] = min(1.0, player["form"] + random.uniform(0.02, 0.08))
        player["age"] += 1/365
        
        if random.random() < 0.05:
            player["form"] = max(0.3, player["form"] - 0.3)
            result = f"⚠️ Травма! Форма упала. Рейтинг: {player['rating']:.1f}"
        else:
            result = f"🎯 Тренировка завершена! Рейтинг: {player['rating']:.1f}"
        
        self.advance_date(7)
        self.update_stats_history()
        self.save_data()
        return result

    def update_stats_history(self):
        player = self.data["player"]
        stats = player["stats_history"]
        
        stats["rating"].append(player["rating"])
        stats["goals"].append(player["goals"])
        stats["matches"].append(player["matches"])
        stats["dates"].append(datetime.now().strftime("%Y-%m-%d"))
        
        if len(stats["rating"]) > 20:
            stats["rating"] = stats["rating"][-20:]
            stats["goals"] = stats["goals"][-20:]
            stats["matches"] = stats["matches"][-20:]
            stats["dates"] = stats["dates"][-20:]

    def play_match(self, performance):
        player = self.data["player"]
        player["matches"] += 1
        
        base_form_change = random.uniform(-0.15, 0.15)
        if performance == "excellent":
            base_form_change += 0.2
        elif performance == "good":
            base_form_change += 0.1
        else:
            base_form_change -= 0.1
        
        player["form"] = max(0.3, min(1.0, player["form"] + base_form_change))
        
        goals = 0
        assists = 0
        rating_change = 0
        
        if performance == "excellent":
            goals = random.randint(1, 2)
            assists = random.randint(0, 1)
            rating_change = random.uniform(0.1, 0.3)
        elif performance == "good":
            if random.random() < 0.3:
                goals = 1
            assists = random.randint(0, 1)
            rating_change = random.uniform(0.05, 0.15)
        else:
            rating_change = random.uniform(-0.1, 0.05)
        
        player["goals"] += goals
        player["assists"] += assists
        
        if player["age"] < 28 and player["rating"] < player["potential"]:
            player["rating"] = min(player["potential"], player["rating"] + rating_change)
        
        # Безопасный доступ к данным команды
        team = None
        for league in self.data["leagues"]:
            if player["team"] in league["teams"]:
                if "teams_data" in league and player["team"] in league["teams_data"]:
                    team = league["teams_data"][player["team"]]
                    break
        
        if not team:
            print(f"⚠️ Нет данных для команды '{player['team']}' — создаём временные")
            team = {
                "players": [],
                "budget": 1000000,
                "tactics": "4-4-2",
                "coach": "Temp Coach",
                "points": 0,
                "goals_for": 0,
                "goals_against": 0,
                "position": 20,
                "rating": 60
            }
            # Добавляем данные в первый лист лиги
            if len(self.data["leagues"]) > 0:
                league = self.data["leagues"][0]
                if "teams_data" not in league:
                    league["teams_data"] = {}
                league["teams_data"][player["team"]] = team
        
        team["goals_for"] += goals
        match_result = "win"
        if random.random() < 0.7:
            team["points"] += 3
        elif random.random() < 0.3:
            team["points"] += 1
            match_result = "draw"
        else:
            match_result = "loss"
        
        if goals > 0:
            self.update_reputation(3)
        elif assists > 0:
            self.update_reputation(2)
        if match_result == "win":
            self.update_reputation(2)
        
        self.advance_date(3)
        self.update_stats_history()
        self.check_awards()
        self.check_secret_achievements()
        self.save_data()
        
        # ВСЕГДА возвращаем словарь
        return {
            "goals": goals,
            "assists": assists,
            "result": match_result,
            "rating_change": rating_change,
            "message": f"⚽ Матч сыгран! Голы: {goals}, Ассисты: {assists}"
        }

    def get_transfer_offers(self):
        player = self.data["player"]
        offers = []
        
        if player["rating"] > 65:
            for league in self.data["leagues"]:
                if league["level"] < 5:
                    for team in league["teams"][:2]:
                        offer = {
                            "team": team,
                            "league": league["name"],
                            "salary": int(player["salary"] * (1 + (player["rating"] - 60) / 20)),
                            "bonus": int(player["goals"] * 1000),
                            "years": random.randint(2, 5)
                        }
                        offers.append(offer)
        return offers

    def accept_transfer(self, offer):
        player = self.data["player"]
        old_team = player["team"]
        player["team"] = offer["team"]
        player["league"] = offer["league"]
        player["salary"] = offer["salary"]
        player["contract_years"] = offer["years"]
        
        self.update_reputation(10)
        
        top_clubs = ["Manchester City", "Real Madrid", "Bayern Munich", "Liverpool", "Barcelona"]
        if player["team"] in top_clubs:
            self.unlock_achievement("top_club")
        
        self.save_data()
        return f"✅ Переход в {offer['team']} ({offer['league']}) завершён!"

    def get_transfer_market(self):
        return self.data["transfer_market"]["players"]

    def buy_player(self, player_index):
        market = self.data["transfer_market"]
        if player_index < len(market["players"]):
            player = market["players"].pop(player_index)
            team = self.data["teams"][self.data["player"]["team"]]
            if team["budget"] >= player["asking_price"]:
                team["budget"] -= player["asking_price"]
                team["players"].append(player)
                self.save_data()
                return f"✅ Игрок {player['name']} куплен за ${player['asking_price']}"
            else:
                return "❌ Недостаточно бюджета!"
        return "❌ Игрок не найден"

    def unlock_achievement(self, achievement_id):
        for achievement in self.data["achievements"]:
            if achievement["id"] == achievement_id:
                achievement["unlocked"] = True
                print(f"🏆 Достижение разблокировано: {achievement['name']}")
                self.save_data()
                return True
        return False

    def participate_in_tournament(self, tournament_name):
        for tournament in self.data["tournaments"]:
            if tournament["name"] == tournament_name:
                player = self.data["player"]
                performance = random.choice(["excellent", "good", "average"])
                if performance == "excellent":
                    goals = random.randint(3, 5)
                    player["goals"] += goals
                    if tournament_name == "Чемпионат мира":
                        self.unlock_achievement("world_champion")
                        player["awards"].append("🏆 Чемпион мира")
                    self.save_data()
                    return f"🌟 {tournament_name}: {goals} голов! MVP турнира!"
                elif performance == "good":
                    goals = random.randint(1, 3)
                    player["goals"] += goals
                    self.save_data()
                    return f"⭐ {tournament_name}: {goals} голов"
                else:
                    self.save_data()
                    return f"😐 {tournament_name}: участие без голов"
        return "❌ Турнир не найден"

    def win_award(self, award_name):
        player = self.data["player"]
        player["awards"].append(award_name)
        self.save_data()
        return f"🏅 Награда получена: {award_name}"

    def check_awards(self):
        player = self.data["player"]
        if player["goals"] > 10 and "⚽ Топ-бомбардир" not in player["awards"]:
            self.win_award("⚽ Топ-бомбардир")
        if player["rating"] > 90 and "🌟 Золотой мяч" not in player["awards"]:
            self.win_award("🌟 Золотой мяч")
        if player["team"] in ["Manchester City", "Real Madrid", "Bayern Munich"] and not any(a["id"] == "top_club" and a["unlocked"] for a in self.data["achievements"]):
            self.unlock_achievement("top_club")

    def update_reputation(self, change):
        player = self.data["player"]
        player["reputation"] = max(0, min(100, player["reputation"] + change))
        self.save_data()
        return player["reputation"]

    def get_reputation_status(self):
        reputation = self.data["player"]["reputation"]
        if reputation >= 90:
            return "👑 Легенда: Все клубы мечтают о вас!"
        elif reputation >= 75:
            return "⭐ Звезда: Вас приглашают топ-клубы"
        elif reputation >= 60:
            return "👍 Уважаемый: Стабильный игрок"
        elif reputation >= 40:
            return "😐 Средний: Нужно улучшать игру"
        else:
            return "⚠️ Проблемный: Клубы сомневаются в вас"

    def check_secret_achievements(self):
        player = self.data["player"]
        now = datetime.now()
        
        if now.day == 17 and not any(a["id"] == "birthday_boy" and a["unlocked"] for a in self.data["achievements"]):
            for achievement in self.data["achievements"]:
                if achievement["id"] == "birthday_boy":
                    achievement["unlocked"] = True
                    print("🎉 Секретное достижение: День рождения!")
                    self.save_data()
                    break