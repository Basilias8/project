import matplotlib
matplotlib.use('Agg')  # Для работы без GUI
import matplotlib.pyplot as plt
import io
import pygame
from datetime import datetime

class AnalyticsSystem:
    def __init__(self, career_system):
        self.career_system = career_system

    def create_rating_graph(self):
        """Создаёт график роста рейтинга"""
        player = self.career_system.data["player"]
        stats = player["stats_history"]
        
        plt.figure(figsize=(10, 6))
        plt.plot(stats["dates"], stats["rating"], 'bo-', linewidth=2, markersize=8)
        plt.title('Рост рейтинга игрока', fontsize=16, fontweight='bold')
        plt.xlabel('Дата', fontsize=12)
        plt.ylabel('Рейтинг', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Конвертируем в изображение Pygame
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        plt.close()
        buf.seek(0)
        
        image = pygame.image.load(buf, 'rating_graph.png')
        return image

    def create_goals_graph(self):
        """Создаёт график голов"""
        player = self.career_system.data["player"]
        stats = player["stats_history"]
        
        plt.figure(figsize=(10, 6))
        plt.bar(stats["dates"], stats["goals"], color='red', alpha=0.7)
        plt.title('Голы по датам', fontsize=16, fontweight='bold')
        plt.xlabel('Дата', fontsize=12)
        plt.ylabel('Голы', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        plt.close()
        buf.seek(0)
        
        image = pygame.image.load(buf, 'goals_graph.png')
        return image