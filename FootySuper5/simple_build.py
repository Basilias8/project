import PyInstaller.__main__
import os
import sys

def build_game():
    print("🔨 Сборка Football Manager...")
    
    # Создаём базовую структуру если её нет
    folders = ['assets/images', 'assets/audio', 'data', 'saves', 'systems', 'ui']
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    
    # Базовые команды без иконки и UPX
    cmd = [
        'main.py',
        '--onefile',
        '--noconsole',
        '--name=FootballManager',
        '--add-data=assets;assets',
        '--add-data=data;data',
        '--add-data=saves;saves',
        '--add-data=systems;systems',
        '--add-data=ui;ui',
        '--hidden-import=pygame',
        '--hidden-import=matplotlib.backends.backend_agg',
        '--clean'  # Очистка предыдущих сборок
    ]
    
    try:
        PyInstaller.__main__.run(cmd)
        print("✅ Сборка завершена! EXE в папке 'dist/'")
        
        # Проверяем результат
        if os.path.exists("dist/FootballManager.exe"):
            print("🎉 Файл создан успешно!")
            file_size = os.path.getsize("dist/FootballManager.exe") / (1024*1024)
            print(f"📏 Размер файла: {file_size:.1f} MB")
        else:
            print("❌ Файл не создан")
            
    except Exception as e:
        print(f"❌ Ошибка сборки: {e}")

if __name__ == "__main__":
    build_game()