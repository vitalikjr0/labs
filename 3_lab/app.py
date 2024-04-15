# спочатку йдуть імпорти бібліотек
from sword import Swords
from random import randint, choice
# опис функціоналу програми у вигляді функцій

SWORD_NAMES = [
        "Меч Смертівника",
        "Драконобійчий Клинок",
        "Стрілецька Сага",
        "Кований Піднебінник",
        "Тіньовий Катана",
        "Ластівчиний Клинок",
        "Зоряний Рапір",
        "Проклятий Кинджал",
        "Молот Богів",
        "Легендарний Лезо",
        "Гнів Берсерка",
        "Вогняний Розрив",
        "Лісовий Сокирян",
        "Чорний Рубіж",
        "Лютівний Гак",
        "Кам'яний Розтрощувач",
        "Драконячий Топір",
        "Палаючий Клин",
        "Буревій Сокира",
        "Королівський Відламник"]


def create_players() -> Swords:
    """Функція призначена для ініціалізації гравців та їх Мечів"""
    # Створюємо меч для гравця та надаємо йому випадкову назву
    s = Swords.create_random_rarity(choice(SWORD_NAMES))
    print(s.apply_bonus())  # Тут у явному вигляді будемо застосовувати накладення бонусу
    # Робими динамічний атрибут який буде вказувати кому належить даний меч
    s.player = input("Введіть імя першого гравця: ")
    print(f"Гравець {s.player} отримує Меч:", s.info)
    return s


def select_buff(player_name: str) -> str:
    """Функція для здійснення ходу гравцем, вибір Бафа."""
    buff = input(f"{player_name}, введіть 1 для бафу на атаку, 2 для бафу на міцність, будь-яка кнопка щоб пропустити: ")
    if buff in ["1", "2"]:
        return buff
    print("Помилка: Потрібно було ввести 1 або 2. Гравець пропускає хід.")
    return None


# виконання всієї програми
if __name__ == "__main__":
    print("Старт гри:")
    # за допомогою функцій ми уніфікували створення гравця
    c = create_players()
    d = create_players()

    # Дозволимо гравцю впливати на те як ми будемо змагатись на отриманих мечах
    c.player_buff = select_buff(c.player)
    d.player_buff = select_buff(d.player)

    for pb in [c, d]:
        if pb.player_buff == "1":   # Ця перевірка нам потрібна щоб визначити чи гравці ввели правильні значення
            print(f"{pb.player} застосував баф на нанесення шкоди:")
            pb.get_buff_damag(randint(2, 5))
        elif pb.player_buff == "2":
            print(f"{pb.player} застосував баф на міцність:")
            pb.get_buff_vitality(randint(6, 12))
        else:
            print("Введено не коректне значення, тому ніяких бафів не застосовано!")
        # меч старіє/зношується від використання, тому накладаємо випадковий негативний ефект
        print(pb.aging(), pb.info)

    # емулюємо як ми користуємось нашим мечем та проводимо бої де його міцність зменшується через атаки
    # Перший хід за першим гравцем
    while c.vitality > 0 and d.vitality > 0:
        print("Новий раунд:")
        c.attack(d)
        print(f"{c.player} з {c.name} атакував {d.player} з {d.name}")
        d.attack(c)
        print(f"Зворотньо {d.player} з {d.name} атакував {c.player} з {c.name}")
        print(f"Закінчилась дія бафу: {c.expired_buff()} ||||| {d.expired_buff()}")
        print(f"<<<<< {c.name} {c.vitality} ||||| {d.name} {d.vitality} >>>>>>")
        print(f"Починаємо ремонтувати мечі: {c.repair()} ||||| {d.repair()}")
        print(f"<<<<< {c.name} {c.vitality} ||||| {d.name} {d.vitality} >>>>>>")

    if c.vitality > 0 and c.vitality >= d.vitality:
        print(f"Гравець {c.player} переміг над {d.player}")
    else:
        print(f"Гравець {d.player} переміг над {c.player}")

    print("Завершення гри")
