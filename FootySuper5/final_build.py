import PyInstaller.__main__
import os
import shutil

def build_final():
    print("🔨 Финальная сборка Football Manager...")
    
    # Очистка предыдущих сборок
    for folder in ['dist', 'build']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    
    # Удаляем старый spec файл если есть
    if os.path.exists("FootballManager.spec"):
        os.remove("FootballManager.spec")
    
    # Команда сборки
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
        '--hidden-import=PIL',
        '--collect-all=matplotlib',
        '--clean'
    ]
    
    try:
        PyInstaller.__main__.run(cmd)
        
        # Проверяем результат
        if os.path.exists("dist/FootballManager.exe"):
            file_size = os.path.getsize("dist/FootballManager.exe") / (1024*1024)
            print(f"✅ Сборка завершена успешно!")
            print(f"📏 Размер EXE: {file_size:.1f} MB")
            print(f"📍 Файл: dist/FootballManager.exe")
            
            # Создаём папку релиза
            if not os.path.exists("FootballManager_Release"):
                os.makedirs("FootballManager_Release")
            
            # Копируем EXE
            shutil.copy2("dist/FootballManager.exe", "FootballManager_Release/")
            
            # Создаём README
            with open("FootballManager_Release/README.txt", "w", encoding="utf-8") as f:
                f.write("FOOTYSUPER⁵: LEGENDARY EDITION\n\n")
                f.write("Управление:\n")
                f.write("- Стрелки ВВЕРХ/ВНИЗ - навигация\n")
                f.write("- ENTER - выбор\n") 
                f.write("- ESC - назад/выход\n\n")
                f.write("Для запуска откройте FootballManager.exe\n")
            
            print(f"📦 Дистрибутив создан в папке: FootballManager_Release")
        else:
            print("❌ Сборка не удалась - EXE файл не создан")
            
    except Exception as e:
        print(f"❌ Ошибка сборки: {e}")

if __name__ == "__main__":
    build_final()