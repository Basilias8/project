import pygame
import os
import random

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music_playing = False
        self.volume = 0.7
        self.load_sounds()

    def load_sounds(self):
        # Создаём папку, если её нет
        os.makedirs("assets/audio", exist_ok=True)
        
        sound_files = {
            "click": "click.wav",
            "goal": "goal.mp3",
            "training": "training.mp3",
            "award": "award.mp3",
            "menu_music": "menu.mp3",
            "match_music": "match.mp3"
        }

        for name, filename in sound_files.items():
            path = os.path.join("assets", "audio", filename)
            if os.path.exists(path):
                try:
                    if name.endswith("music"):
                        continue
                    self.sounds[name] = pygame.mixer.Sound(path)
                    self.sounds[name].set_volume(self.volume)
                except Exception as e:
                    print(f"Не удалось загрузить звук {name}: {e}")
            else:
                print(f"Создаём заглушку: {path}")
                # Создаём пустой файл-заглушку
                open(path, 'a').close()

    def play_sound(self, name):
        if name in self.sounds:
            try:
                self.sounds[name].play()
            except Exception as e:
                print(f"Ошибка воспроизведения {name}: {e}")

    def play_music(self, track="menu_music"):
        try:
            pygame.mixer.music.stop()
            path = os.path.join("assets", "audio", f"{track}.mp3")
            if os.path.exists(path):
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(self.volume * 0.5)
                pygame.mixer.music.play(-1)
                self.music_playing = True
        except Exception as e:
            print(f"Ошибка воспроизведения музыки: {e}")

    def stop_music(self):
        try:
            pygame.mixer.music.stop()
            self.music_playing = False
        except:
            pass

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            try:
                sound.set_volume(self.volume)
            except:
                pass
        if self.music_playing:
            try:
                pygame.mixer.music.set_volume(self.volume * 0.5)
            except:
                pass