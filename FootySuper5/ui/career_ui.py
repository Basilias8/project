import pygame
import random
import os
import sys
from datetime import datetime

def resource_path(relative_path):
    """Получает абсолютный путь к ресурсу"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class CareerUI:
    def __init__(self, screen, career_system, audio_manager=None, ai_coach=None, analytics_system=None, customization_system=None, stadium_system=None):
        self.screen = screen
        self.career_system = career_system
        self.audio_manager = audio_manager
        self.ai_coach = ai_coach
        self.analytics_system = analytics_system
        self.customization_system = customization_system
        self.stadium_system = stadium_system
        self.font = pygame.font.SysFont("Arial", 32)
        self.small_font = pygame.font.SysFont("Arial", 24)
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.selected = 0
        self.state = "main"
        self.offers = []
        self.match_result_data = None

    def draw_background(self, background_name):
        """Отрисовывает фон с обработкой ошибок"""
        try:
            background_path = resource_path(f"assets/images/{background_name}")
            background = pygame.image.load(background_path).convert()
            background = pygame.transform.scale(background, (1920, 1080))
            self.screen.blit(background, (0, 0))
        except Exception as e:
            # Запасной цветной фон
            if "menu" in background_name:
                self.screen.fill((20, 20, 40))
            elif "training" in background_name:
                self.screen.fill((30, 50, 30))
            elif "transfers" in background_name:
                self.screen.fill((50, 30, 30))
            elif "minigames" in background_name:
                self.screen.fill((60, 30, 60))
            elif "tournaments" in background_name:
                self.screen.fill((30, 60, 90))
            elif "awards" in background_name:
                self.screen.fill((80, 80, 40))
            elif "achievements" in background_name:
                self.screen.fill((40, 80, 40))
            elif "analytics" in background_name:
                self.screen.fill((30, 30, 60))
            elif "customization" in background_name:
                self.screen.fill((80, 40, 80))
            elif "stadium" in background_name:
                self.screen.fill((60, 80, 60))
            elif "reputation" in background_name:
                self.screen.fill((80, 60, 40))
            elif "secret" in background_name:
                self.screen.fill((40, 40, 80))
            elif "match" in background_name:
                self.screen.fill((20, 40, 60))
            else:
                self.screen.fill((20, 20, 40))

    def draw_main_menu(self):
        self.draw_background("menu_background.jpg")
        
        # Инфо игрока
        player = self.career_system.data["player"]
        info_lines = [
            f"⭐ Рейтинг: {player['rating']:.1f} (Потенциал: {player['potential']})",
            f"🎂 Возраст: {int(player['age'])} лет",
            f"⚽ Позиция: {player['position']}",
            f"📊 Форма: {player['form']:.2f}",
            f"🏆 Команда: {player['team']}",
            f"🌍 Лига: {player['league']}",
            f"💰 Зарплата: ${player['salary']}/год",
            f"📅 Контракт: {player['contract_years']} лет",
            f"⚽ Голы: {player['goals']}, 🅰️ Ассисты: {player['assists']}, 🎮 Матчи: {player['matches']}",
            f"⭐ Репутация: {player['reputation']}/100"
        ]
        
        y = 50
        for line in info_lines:
            text = self.font.render(line, True, (200, 255, 255))
            self.screen.blit(text, (50, y))
            y += 40
        
        # Советы тренера
        if self.ai_coach:
            advice = self.ai_coach.get_advice()
            advice_text = self.font.render(advice, True, (255, 255, 0))
            self.screen.blit(advice_text, (50, y))
            y += 50
        
        # Меню
        menu_items = [
            "📊 Аналитика", 
            "🎨 Кастомизация", 
            "🏟️ Стадион", 
            "📈 Репутация", 
            "🏆 Секретные достижения",
            "🏋️ Тренировки", 
            "🎯 Мини-игры", 
            "⚽ Матчи", 
            "🌍 Турниры", 
            "💼 Трансферы", 
            "🛒 Трансферный рынок", 
            "🏅 Награды", 
            "🏆 Достижения", 
            "🏠 Главное меню"
        ]
        y = max(y, 300)
        for i, item in enumerate(menu_items):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(item, True, color)
            self.screen.blit(text, (50, y))
            y += 60
        
        pygame.display.flip()

    def draw_match_result(self, result_data):
        """Отображает результат матча на экране"""
        self.draw_background("match_background.jpg")
        
        # Заголовок
        title = self.title_font.render("⚽ РЕЗУЛЬТАТ МАТЧА", True, (255, 255, 0))
        self.screen.blit(title, (self.screen.get_width()//2 - title.get_width()//2, 50))
        
        # Проверяем, есть ли данные
        if result_data is None:
            error_text = self.title_font.render("❌ Ошибка: Нет данных матча", True, (255, 0, 0))
            self.screen.blit(error_text, (self.screen.get_width()//2 - error_text.get_width()//2, 150))
            
            back_btn = self.font.render("Нажмите ENTER для возврата", True, (255, 255, 255))
            self.screen.blit(back_btn, (self.screen.get_width()//2 - back_btn.get_width()//2, 300))
            pygame.display.flip()
            return
        
        # Результат
        result_color = (0, 255, 0) if result_data["result"] == "win" else (255, 255, 0) if result_data["result"] == "draw" else (255, 0, 0)
        result_text = "ПОБЕДА!" if result_data["result"] == "win" else "НИЧЬЯ" if result_data["result"] == "draw" else "ПОРАЖЕНИЕ"
        result_surface = self.title_font.render(result_text, True, result_color)
        self.screen.blit(result_surface, (self.screen.get_width()//2 - result_surface.get_width()//2, 120))
        
        # Статистика
        stats = [
            f"⚽ Голы: {result_data['goals']}",
            f"🅰️ Ассисты: {result_data['assists']}",
            f"⭐ Изменение рейтинга: {result_data['rating_change']:+.1f}"
        ]
        
        y = 220
        for stat in stats:
            text = self.font.render(stat, True, (200, 255, 255))
            self.screen.blit(text, (self.screen.get_width()//2 - text.get_width()//2, y))
            y += 50
        
        # Кнопка продолжения
        continue_btn = self.font.render("Нажмите ENTER для продолжения", True, (255, 255, 255))
        self.screen.blit(continue_btn, (self.screen.get_width()//2 - continue_btn.get_width()//2, 500))
        
        pygame.display.flip()

    # Остальные методы отрисовки с использованием draw_background
    def draw_training(self):
        self.draw_background("training_background.jpg")
        
        title = self.title_font.render("🏋️ ТРЕНИРОВКИ", True, (255, 255, 0))
        self.screen.blit(title, (50, 50))
        
        instructions = [
            "Нажмите ENTER для начала тренировки",
            "Тренировки улучшают рейтинг и форму",
            "Эффект зависит от возраста и потенциала",
            "",
            "Совет тренера:",
            f"«{self.ai_coach.get_training_recommendation()}»" if self.ai_coach else "Тренер недоступен"
        ]
        
        y = 150
        for line in instructions:
            color = (255, 255, 0) if "Совет тренера" in line else (200, 255, 200)
            text = self.font.render(line, True, color)
            self.screen.blit(text, (50, y))
            y += 40
        
        back_btn = self.small_font.render("ESC — назад", True, (200, 200, 200))
        self.screen.blit(back_btn, (50, 650))
        pygame.display.flip()

    def draw_transfers(self):
        self.draw_background("transfers_background.jpg")
        
        title = self.title_font.render("💼 ТРАНСФЕРЫ", True, (255, 255, 0))
        self.screen.blit(title, (50, 50))
        
        if not self.offers:
            self.offers = self.career_system.get_transfer_offers()
            if not self.offers:
                text = self.font.render("Нет предложений. Улучшите рейтинг!", True, (255, 100, 100))
                self.screen.blit(text, (50, 100))
            else:
                text = self.font.render(f"Получено {len(self.offers)} предложений!", True, (100, 255, 100))
                self.screen.blit(text, (50, 100))
        
        y = 150
        for i, offer in enumerate(self.offers):
            color = (255, 255, 0) if i == self.selected else (200, 255, 255)
            lines = [
                f"➡️ {offer['team']} ({offer['league']})",
                f"💰 Зарплата: ${offer['salary']}/год + ${offer['bonus']} бонус",
                f"📅 Контракт: {offer['years']} лет"
            ]
            for line in lines:
                text = self.font.render(line, True, color)
                self.screen.blit(text, (50, y))
                y += 30
            y += 20
        
        if self.offers:
            hint = self.small_font.render("ENTER — принять предложение | ESC — назад", True, (200, 200, 200))
            self.screen.blit(hint, (50, 650))
        pygame.display.flip()

    def draw_minigames(self):
        self.draw_background("minigames_background.jpg")
        
        title = self.title_font.render("🎮 МИНИ-ИГРЫ", True, (255, 255, 0))
        self.screen.blit(title, (50, 50))
        
        games = ["🎯 Попади по цели", "⚽ Дриблинг через конусы"]
        y = 150
        for i, game in enumerate(games):
            color = (255, 255, 0) if i == self.selected else (200, 255, 255)
            text = self.font.render(game, True, color)
            self.screen.blit(text, (50, y))
            y += 60
        
        hint = self.small_font.render("ENTER — выбрать | ESC — назад", True, (200, 200, 200))
        self.screen.blit(hint, (50, 650))
        pygame.display.flip()

    def draw_tournaments(self):
        self.draw_background("tournaments_background.jpg")
        
        title = self.title_font.render("🌍 МЕЖДУНАРОДНЫЕ ТУРНИРЫ", True, (255, 255, 0))
        self.screen.blit(title, (50, 50))
        
        tournaments = ["🏆 Лига чемпионов", "🌎 Чемпионат мира", "🇪🇺 Чемпионат Европы"]
        y = 150
        for i, tour in enumerate(tournaments):
            color = (255, 255, 0) if i == self.selected else (200, 255, 255)
            text = self.font.render(tour, True, color)
            self.screen.blit(text, (50, y))
            y += 60
        
        hint = self.small_font.render("ENTER — участвовать | ESC — назад", True, (200, 200, 200))
        self.screen.blit(hint, (50, 650))
        pygame.display.flip()

    def draw_awards(self):
        self.draw_background("awards_background.jpg")
        
        title = self.title_font.render("🏅 НАГРАДЫ ИГРОКА", True, (255, 255, 0))
        self.screen.blit(title, (50, 50))
        
        player = self.career_system.data["player"]
        y = 100
        if player["awards"]:
            for award in player["awards"]:
                text = self.font.render(f"• {award}", True, (255, 255, 255))
                self.screen.blit(text, (50, y))
                y += 40
        else:
            text = self.font.render("Нет наград. Играй лучше!", True, (255, 100, 100))
            self.screen.blit(text, (50, 100))
        
        back_btn = self.small_font.render("ESC — назад", True, (200, 200, 200))
        self.screen.blit(back_btn, (50, 650))
        pygame.display.flip()

    def draw_achievements(self):
        self.draw_background("achievements_background.jpg")
        
        title = self.title_font.render("🏆 ДОСТИЖЕНИЯ", True, (255, 255, 0))
        self.screen.blit(title, (50, 50))
        
        achievements = self.career_system.data["achievements"]
        y = 100
        for achievement in achievements:
            color = (255, 255, 0) if achievement["unlocked"] else (100, 100, 100)
            status = "✅" if achievement["unlocked"] else "🔒"
            text = self.font.render(f"{status} {achievement['name']}", True, color)
            self.screen.blit(text, (50, y))
            desc = self.small_font.render(achievement["description"], True, (200, 200, 200))
            self.screen.blit(desc, (80, y + 30))
            y += 70
        
        back_btn = self.small_font.render("ESC — назад", True, (200, 200, 200))
        self.screen.blit(back_btn, (50, 650))
        pygame.display.flip()

    def draw_analytics(self):
        self.draw_background("analytics_background.jpg")
        
        title = self.title_font.render("📊 АНАЛИТИКА ИГРОКА", True, (255, 255, 0))
        self.screen.blit(title, (50, 50))
        
        try:
            if self.analytics_system:
                # Создаём график рейтинга
                rating_graph = self.analytics_system.create_rating_graph()
                self.screen.blit(rating_graph, (50, 100))
                
                # Создаём график голов
                goals_graph = self.analytics_system.create_goals_graph()
                self.screen.blit(goals_graph, (50, 400))
            else:
                text = self.font.render("Аналитика недоступна", True, (255, 100, 100))
                self.screen.blit(text, (50, 100))
                
        except Exception as e:
            error_text = self.font.render(f"Ошибка: {str(e)}", True, (255, 100, 100))
            self.screen.blit(error_text, (50, 100))
        
        back_btn = self.small_font.render("ESC — назад", True, (200, 200, 200))
        self.screen.blit(back_btn, (50, 650))
        pygame.display.flip()

    def draw_customization(self):
        self.draw_background("customization_background.jpg")
        
        title = self.title_font.render("🎨 КАСТОМИЗАЦИЯ", True, (255, 255, 0))
        self.screen.blit(title, (50, 50))
        
        player = self.career_system.data["player"]
        customization = player["customization"]
        
        options = [
            f"💇 Причёска: {customization['hair_style']}",
            f"🎨 Цвет волос: {customization['hair_color']}",
            f"👤 Тон кожи: {customization['skin_tone']}",
            f"🎉 Празднование: {customization['celebration']}",
            f"🧥 Тренировочная одежда: {customization['warmup_outfit']}"
        ]
        
        y = 150
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == self.selected else (200, 255, 255)
            text = self.font.render(option, True, color)
            self.screen.blit(text, (50, y))
            y += 60
        
        hint = self.small_font.render("ENTER — изменить | ESC — назад", True, (200, 200, 200))
        self.screen.blit(hint, (50, 650))
        pygame.display.flip()

    def draw_stadium(self):
        self.draw_background("stadium_background.jpg")
        
        title = self.title_font.render("🏟️ УПРАВЛЕНИЕ СТАДИОНОМ", True, (255, 255, 0))
        self.screen.blit(title, (50, 50))
        
        try:
            if self.stadium_system:
                stadium_name = f"{self.career_system.data['player']['team']} Stadium"
                info = self.stadium_system.get_stadium_info(stadium_name)
                
                y = 100
                for line in info.strip().split('\n'):
                    text = self.font.render(line, True, (200, 255, 200))
                    self.screen.blit(text, (50, y))
                    y += 40
                
                upgrades = ["📈 Увеличить вместимость", "🔧 Улучшить удобства", "🎉 Улучшить атмосферу"]
                y = 400
                for i, upgrade in enumerate(upgrades):
                    color = (255, 255, 0) if i == self.selected else (200, 255, 255)
                    text = self.font.render(upgrade, True, color)
                    self.screen.blit(text, (50, y))
                    y += 50
            else:
                text = self.font.render("Система стадионов недоступна", True, (255, 100, 100))
                self.screen.blit(text, (50, 100))
                
        except Exception as e:
            error_text = self.font.render(f"Ошибка: {str(e)}", True, (255, 100, 100))
            self.screen.blit(error_text, (50, 100))
        
        hint = self.small_font.render("ENTER — улучшить | ESC — назад", True, (200, 200, 200))
        self.screen.blit(hint, (50, 650))
        pygame.display.flip()

    def draw_reputation(self):
        self.draw_background("reputation_background.jpg")
        
        title = self.title_font.render("📈 РЕПУТАЦИЯ ИГРОКА", True, (255, 255, 0))
        self.screen.blit(title, (50, 50))
        
        player = self.career_system.data["player"]
        reputation = player["reputation"]
        status = self.career_system.get_reputation_status()
        
        # Репутация в виде прогресс-бара
        pygame.draw.rect(self.screen, (100, 100, 100), (50, 150, 500, 40), border_radius=10)
        pygame.draw.rect(self.screen, (0, 255, 0), (50, 150, 5 * reputation, 40), border_radius=10)
        
        rep_text = self.font.render(f"Репутация: {reputation}/100", True, (255, 255, 255))
        self.screen.blit(rep_text, (50, 200))
        
        status_text = self.font.render(status, True, (255, 255, 0))
        self.screen.blit(status_text, (50, 250))
        
        back_btn = self.small_font.render("ESC — назад", True, (200, 200, 200))
        self.screen.blit(back_btn, (50, 650))
        pygame.display.flip()

    def draw_secret_achievements(self):
        self.draw_background("secret_achievements_background.jpg")
        
        title = self.title_font.render("🏆 СЕКРЕТНЫЕ ДОСТИЖЕНИЯ", True, (255, 255, 0))
        self.screen.blit(title, (50, 50))
        
        achievements = self.career_system.data["achievements"]
        y = 100
        for achievement in achievements:
            color = (255, 255, 0) if achievement["unlocked"] else (100, 100, 100)
            status = "✅" if achievement["unlocked"] else "🔒"
            text = self.font.render(f"{status} {achievement['name']}", True, color)
            self.screen.blit(text, (50, y))
            desc = self.small_font.render(achievement["description"], True, (200, 200, 200))
            self.screen.blit(desc, (80, y + 30))
            y += 70
        
        back_btn = self.small_font.render("ESC — назад", True, (200, 200, 200))
        self.screen.blit(back_btn, (50, 650))
        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = "main"
                self.selected = 0
                return True
            elif event.key == pygame.K_UP:
                if self.state == "transfers" and self.offers:
                    self.selected = max(0, self.selected - 1)
                else:
                    self.selected = max(0, self.selected - 1)
            elif event.key == pygame.K_DOWN:
                if self.state == "transfers" and self.offers:
                    self.selected = min(len(self.offers) - 1, self.selected + 1)
                else:
                    self.selected = min(13, self.selected + 1)
            elif event.key == pygame.K_RETURN:
                if self.state == "training":
                    result = self.career_system.train_player()
                    print(result)
                elif self.state == "transfers" and self.offers:
                    if self.selected < len(self.offers):
                        result = self.career_system.accept_transfer(self.offers[self.selected])
                        print(result)
                        self.offers = []
                        self.selected = 0
                return True
        return False

    def update(self, event):
        if self.state == "main":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.selected == 0:  # Аналитика
                    self.state = "analytics"
                    return True
                elif self.selected == 1:  # Кастомизация
                    self.state = "customization"
                    return True
                elif self.selected == 2:  # Стадион
                    self.state = "stadium"
                    return True
                elif self.selected == 3:  # Репутация
                    self.state = "reputation"
                    return True
                elif self.selected == 4:  # Секретные достижения
                    self.state = "secret_achievements"
                    return True
                elif self.selected == 5:  # Тренировки
                    self.state = "training"
                elif self.selected == 6:  # Мини-игры
                    self.state = "minigames"
                    return True
                elif self.selected == 7:  # Матчи
                    performance = random.choice(["excellent", "good", "average"])
                    result = self.career_system.play_match(performance)
                    self.match_result_data = result
                    self.state = "match_result"
                    return True
                elif self.selected == 8:  # Турниры
                    self.state = "tournaments"
                    return True
                elif self.selected == 9:  # Трансферы
                    self.state = "transfers"
                    self.offers = []
                elif self.selected == 10:  # Трансферный рынок
                    self.state = "transfer_market"
                    return True
                elif self.selected == 11:  # Награды
                    self.state = "awards"
                    return True
                elif self.selected == 12:  # Достижения
                    self.state = "achievements"
                    return True
                elif self.selected == 13:  # Главное меню
                    return "menu"
        return None