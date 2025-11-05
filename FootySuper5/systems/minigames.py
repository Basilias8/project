import pygame
import random
import time

class Minigame:
    def __init__(self, screen, career_system):
        self.screen = screen
        self.career_system = career_system
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.title_font = pygame.font.SysFont("Arial", 32, bold=True)

    def run_target_practice(self):
        """Мини-игра: Попади по цели"""
        score = 0
        targets = []
        start_time = time.time()
        game_time = 30  # 30 секунд

        while time.time() - start_time < game_time:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return {"score": 0, "message": "Игра прервана"}
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for target in targets[:]:
                        if (mouse_pos[0] - target[0])**2 + (mouse_pos[1] - target[1])**2 < 20**2:
                            targets.remove(target)
                            score += 1

            # Создаем новые цели
            if random.random() < 0.1:
                x = random.randint(50, 1230)
                y = random.randint(50, 670)
                targets.append((x, y))

            self.screen.fill((30, 30, 60))
            title = self.title_font.render("ТРЕНИРОВКА: ПОПАДИ ПО ЦЕЛИ", True, (255, 255, 0))
            self.screen.blit(title, (50, 20))

            time_left = int(game_time - (time.time() - start_time))
            time_text = self.font.render(f"Время: {time_left}", True, (255, 255, 255))
            self.screen.blit(time_text, (50, 70))

            score_text = self.font.render(f"Счёт: {score}", True, (255, 255, 255))
            self.screen.blit(score_text, (50, 110))

            for target in targets:
                pygame.draw.circle(self.screen, (255, 0, 0), target, 20)
                pygame.draw.circle(self.screen, (255, 255, 255), target, 20, 3)

            pygame.display.flip()
            pygame.time.delay(50)

        return {"score": score, "message": f"Счёт: {score}"}

    def run_dribbling_challenge(self):
        """Мини-игра: Дриблинг через конусы"""
        cones = [(100 + i*150, 360) for i in range(8)]
        player_x, player_y = 50, 360
        score = 0
        start_time = time.time()
        game_time = 45

        while time.time() - start_time < game_time:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return {"score": 0, "message": "Игра прервана"}

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]: player_y -= 3
            if keys[pygame.K_s]: player_y += 3
            if keys[pygame.K_a]: player_x -= 3
            if keys[pygame.K_d]: player_x += 3

            self.screen.fill((30, 60, 30))
            title = self.title_font.render("ТРЕНИРОВКА: ДРИБЛИНГ", True, (255, 255, 0))
            self.screen.blit(title, (50, 20))

            time_left = int(game_time - (time.time() - start_time))
            time_text = self.font.render(f"Время: {time_left}", True, (255, 255, 255))
            self.screen.blit(time_text, (50, 70))

            # Рисуем конусы
            for cone in cones:
                pygame.draw.circle(self.screen, (255, 165, 0), cone, 15)
                if (player_x - cone[0])**2 + (player_y - cone[1])**2 < 30**2:
                    cones.remove(cone)
                    score += 10

            # Рисуем игрока
            pygame.draw.circle(self.screen, (30, 144, 255), (player_x, player_y), 15)

            pygame.display.flip()
            pygame.time.delay(30)

        return {"score": score, "message": f"Счёт: {score}"}