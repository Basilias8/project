class CustomizationSystem:
    def __init__(self, career_system):
        self.career_system = career_system
        self.hair_styles = ["short", "long", "curly", "bald", "afro", "ponytail"]
        self.hair_colors = ["black", "brown", "blonde", "red", "gray", "blue"]
        self.skin_tones = ["light", "medium", "dark", "olive"]
        self.celebrations = ["arms_up", "kneeslide", "dance", "point_to_sky", "team_huddle"]
        self.warmup_outfits = ["track_suit", "hoodie", "jacket", "vest"]

    def change_hair_style(self, style):
        if style in self.hair_styles:
            self.career_system.data["player"]["customization"]["hair_style"] = style
            self.career_system.save_data()
            return f"Причёска изменена на: {style}"
        return "Недопустимый стиль причёски"

    def change_hair_color(self, color):
        if color in self.hair_colors:
            self.career_system.data["player"]["customization"]["hair_color"] = color
            self.career_system.save_data()
            return f"Цвет волос изменён на: {color}"
        return "Недопустимый цвет волос"

    def change_skin_tone(self, tone):
        if tone in self.skin_tones:
            self.career_system.data["player"]["customization"]["skin_tone"] = tone
            self.career_system.save_data()
            return f"Тон кожи изменён на: {tone}"
        return "Недопустимый тон кожи"

    def change_celebration(self, celebration):
        if celebration in self.celebrations:
            self.career_system.data["player"]["customization"]["celebration"] = celebration
            self.career_system.save_data()
            return f"Празднование изменено на: {celebration}"
        return "Недопустимое празднование"

    def change_warmup_outfit(self, outfit):
        if outfit in self.warmup_outfits:
            self.career_system.data["player"]["customization"]["warmup_outfit"] = outfit
            self.career_system.save_data()
            return f"Тренировочная одежда изменена на: {outfit}"
        return "Недопустимая одежда"