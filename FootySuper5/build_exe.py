import PyInstaller.__main__
import os
import shutil

# Очистка предыдущих сборок
if os.path.exists("dist"):
    shutil.rmtree("dist")
if os.path.exists("build"):
    shutil.rmtree("build")

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--noconsole',
    '--name=FootballManager',
    # УБИРАЕМ строку с иконкой
    '--add-data=assets;assets',
    '--add-data=data;data',
    '--add-data=saves;saves',
    '--add-data=systems;systems',
    '--add-data=ui;ui',
    '--hidden-import=pygame',
    '--hidden-import=matplotlib',
    '--hidden-import=Pillow',
    '--hidden-import=numpy',
    '--collect-all=matplotlib.backends.backend_agg',
    # Убираем UPX если его нет
])