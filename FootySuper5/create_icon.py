from PIL import Image, ImageDraw
import os

def create_simple_icon():
    """Создаёт простую иконку для игры"""
    # Создаём папку если её нет
    os.makedirs("assets/images", exist_ok=True)
    
    # Создаём изображение 256x256
    img = Image.new('RGB', (256, 256), color=(30, 60, 90))
    draw = ImageDraw.Draw(img)
    
    # Рисуем футбольный мяч
    draw.ellipse([50, 50, 206, 206], fill=(255, 255, 255), outline=(0, 0, 0), width=3)
    draw.ellipse([78, 78, 178, 178], fill=(0, 0, 0))
    
    # Сохраняем как ICO
    img.save("assets/images/icon.ico", format="ICO")
    print("✅ Иконка создана: assets/images/icon.ico")

if __name__ == "__main__":
    create_simple_icon()