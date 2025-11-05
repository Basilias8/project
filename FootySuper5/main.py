import pygame
import sys
import os
import random
from datetime import datetime

def resource_path(relative_path):
    """Получает абсолютный путь к ресурсу, работает для dev и для PyInstaller"""
    try:
        # PyInstaller создаёт временную папку и хранит путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class FootballManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("🧊⚽ FOOTYSUPER⁵: LEGENDARY EDITION")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"
        
        # Импорт всех систем
        from systems.career_system import CareerSystem
        from systems.save_manager import SaveManager
        from systems.minigames import Minigame
        from systems.audio_manager import AudioManager
        from systems.ai_coach import AICoach
        from systems.analytics_system import AnalyticsSystem
        from systems.customization_system import CustomizationSystem
        from systems.stadium_system import StadiumSystem
        from ui.career_ui import CareerUI
        
        # Инициализация систем
        self.save_manager = SaveManager()
        self.career_system = CareerSystem(0)  # Начинаем с первого слота
        self.minigame = Minigame(self.screen, self.career_system)
        self.audio_manager = AudioManager()
        self.ai_coach = AICoach(self.career_system)
        self.analytics_system = AnalyticsSystem(self.career_system)
        self.customization_system = CustomizationSystem(self.career_system)
        self.stadium_system = StadiumSystem(self.career_system)
        self.career_ui = CareerUI(
            self.screen, 
            self.career_system, 
            self.audio_manager, 
            self.ai_coach,
            self.analytics_system,
            self.customization_system,
            self.stadium_system
        )
        
        # Переменная для хранения результата матча
        self.match_result_data = None
        
        # Запускаем музыку
        self.audio_manager.play_music("menu_music")

    def run(self):
        while self.running:
            if self.state == "menu":
                self.show_main_menu()
            elif self.state == "career":
                self.run_career()
            elif self.state == "minigames":
                self.run_minigames()
            elif self.state == "tournaments":
                self.run_tournaments()
            elif self.state == "match_result":
                self.run_match_result()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def show_main_menu(self):
        self.screen.fill((10, 10, 30))
        
        # Фон с обработкой ошибок
        try:
            background_path = resource_path("assets/images/menu_background.jpg")
            background = pygame.image.load(background_path).convert()
            background = pygame.transform.scale(background, (1920, 1080))
            self.screen.blit(background, (0, 0))
        except Exception as e:
            # Если файла нет, используем цветной фон
            self.screen.fill((30, 60, 90))
            print(f"⚠️ Фон не найден: {e}")
        
        # Логотип
        title = pygame.font.SysFont("Arial", 80, bold=True).render("FOOTYSUPER⁵", True, (255, 215, 0))
        subtitle = pygame.font.SysFont("Arial", 40).render("LEGENDARY CAREER MODE", True, (200, 230, 255))
        self.screen.blit(title, (self.screen.get_width()//2 - title.get_width()//2, 100))
        self.screen.blit(subtitle, (self.screen.get_width()//2 - subtitle.get_width()//2, 180))
        
        # Кнопки сохранений
        y = 300
        for slot in range(self.save_manager.save_slots):
            save_info = self.save_manager.get_save_info(slot)
            if save_info["exists"]:
                btn_text = f"📁 Карьера {slot + 1}: {save_info['player_name']} ({save_info['team']}) - ⭐{save_info['rating']:.0f}"
                btn_color = (70, 130, 180)
            else:
                btn_text = f"🆕 Новая карьера {slot + 1}"
                btn_color = (46, 139, 87)
            
            text = pygame.font.SysFont("Arial", 32).render(btn_text, True, (255, 255, 255))
            rect = pygame.Rect(400, y, 1100, 80)
            pygame.draw.rect(self.screen, btn_color, rect, border_radius=15)
            self.screen.blit(text, (rect.x + 20, rect.y + 20))
            
            mouse_pos = pygame.mouse.get_pos()
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (100, 180, 220) if save_info["exists"] else (70, 200, 120), rect, border_radius=15, width=5)
                if pygame.mouse.get_pressed()[0]:
                    if save_info["exists"]:
                        self.career_system.data = self.save_manager.load_game(slot)
                        self.career_system.save_slot = slot
                    else:
                        player_name = f"Career {slot + 1}"
                        self.career_system.data = self.save_manager.create_new_game(slot, player_name)
                        self.career_system.save_slot = slot
                    self.state = "career"
                    return
            
            y += 100
        
        # Кнопка выхода
        exit_btn = pygame.font.SysFont("Arial", 32).render("🚪 Выйти", True, (255, 255, 255))
        exit_rect = pygame.Rect(800, y, 300, 80)
        pygame.draw.rect(self.screen, (139, 0, 0), exit_rect, border_radius=15)
        self.screen.blit(exit_btn, (exit_rect.x + 20, exit_rect.y + 20))
        
        if exit_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, (180, 0, 0), exit_rect, border_radius=15, width=5)
            if pygame.mouse.get_pressed()[0]:
                self.running = False
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run_career(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            result = self.career_ui.handle_input(event)
            if result == "menu":
                self.state = "menu"
                return
            
            if self.career_ui.state == "main":
                menu_result = self.career_ui.update(event)
                if menu_result == "menu":
                    self.state = "menu"
                    return
                elif isinstance(menu_result, dict) and "message" in menu_result:
                    # Это результат матча
                    self.match_result_data = menu_result
                    self.state = "match_result"
                    return
        
        if self.career_ui.state == "main":
            self.career_ui.draw_main_menu()
        elif self.career_ui.state == "training":
            self.career_ui.draw_training()
        elif self.career_ui.state == "transfers":
            self.career_ui.draw_transfers()
        elif self.career_ui.state == "awards":
            self.career_ui.draw_awards()
        elif self.career_ui.state == "achievements":
            self.career_ui.draw_achievements()
        elif self.career_ui.state == "analytics":
            self.career_ui.draw_analytics()
        elif self.career_ui.state == "customization":
            self.career_ui.draw_customization()
        elif self.career_ui.state == "stadium":
            self.career_ui.draw_stadium()
        elif self.career_ui.state == "reputation":
            self.career_ui.draw_reputation()
        elif self.career_ui.state == "secret_achievements":
            self.career_ui.draw_secret_achievements()
        elif self.career_ui.state == "minigames":
            self.career_ui.draw_minigames()
        elif self.career_ui.state == "tournaments":
            self.career_ui.draw_tournaments()
        elif self.career_ui.state == "match_result":
            self.career_ui.draw_match_result(self.match_result_data)

    def run_match_result(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.career_ui.state = "main"
                self.state = "career"
                return
        self.career_ui.draw_match_result(self.match_result_data)

    def run_minigames(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.career_ui.state = "main"
                self.state = "career"
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.career_ui.selected == 0:
                    result = self.minigame.run_target_practice()
                    if result["score"] > 10:
                        self.career_system.data["player"]["rating"] += 0.5
                        self.career_system.save_data()
                        print(f"🎯 Улучшение: +0.5 к рейтингу!")
                elif self.career_ui.selected == 1:
                    result = self.minigame.run_dribbling_challenge()
                    if result["score"] > 50:
                        self.career_system.data["player"]["rating"] += 0.5
                        self.career_system.save_data()
                        print(f"⚽ Улучшение: +0.5 к рейтингу!")
        
        self.career_ui.draw_minigames()

    def run_tournaments(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.career_ui.state = "main"
                self.state = "career"
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                tournaments = ["Лига чемпионов", "Чемпионат мира", "Чемпионат Европы"]
                if self.career_ui.selected < len(tournaments):
                    result = self.career_system.participate_in_tournament(tournaments[self.career_ui.selected])
                    print(result)
                    if "MVP" in result or "Чемпион мира" in result:
                        if self.audio_manager:
                            self.audio_manager.play_sound("award")
                    self.career_system.check_awards()
                    self.career_system.check_secret_achievements()
        
        self.career_ui.draw_tournaments()

if __name__ == "__main__":
    game = FootballManager()
    game.run()