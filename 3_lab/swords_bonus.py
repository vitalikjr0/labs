from typing import Any

class SwordBonus:
    """Описує функціонал бонусів"""
    count = 0

    def __init__(self) -> None:
        SwordBonus.count += 1

    @staticmethod
    def bonus_poison(item) -> str:
        """Накладення отрути, шкода +1"""
        if SwordBonus.__check_obj(item):
            item.damag += 1
            return f"Застосовано бонус отрути {item.name}"
    
    @staticmethod
    def bonus_confusion(item) -> str:
        """Накладення конфузії, шкода +2"""
        if SwordBonus.__check_obj(item):
            item.damag += 2
            return f"Застосовано бонус спантеличеність {item.name}"
    
    @staticmethod
    def bonus_berserk(item) -> str:
        """Ефект Берсерка, нанесення шкоди збільшується вдвічі"""
        if SwordBonus.__check_obj(item):
            item.damag *= 2
            return f"Застосовано бонус Берсерка {item.name}"
    
    @staticmethod
    def bonus_strength(item) -> str:
        """Накладення міцності, міцність +5"""
        if SwordBonus.__check_obj(item):
            item.vitality += 5
            return f"Застосовано бонус сили до {item.name}"
        
    @staticmethod
    def bonus_invincible(item) -> str:
        """Накладення ефект Незламності, міцність +15"""
        if SwordBonus.__check_obj(item):
            item.vitality += 15
            return f"Застосовано бонус сили до {item.name}"
    
    # Якщо тут добавлять новий бонус то нам прийдеться дописувати для нього тести

    @staticmethod
    def _nothing(item) -> str:
        """Пустий бонус для мечів з низькою якістю"""
        if SwordBonus.__check_obj(item):
            return f"Меч {item.name} має занизьку рідкісність!"
    
    @staticmethod
    def list_bonus_methods() -> list:
        """Знаходимо методи що надають бонуси, вони будуть починатись з bonus_, та повертаємо їх список"""
        return [method for method in dir(SwordBonus) if callable(getattr(SwordBonus, method)) and method.startswith("bonus_")]

    @staticmethod
    def __check_obj(obj: Any) -> bool:
        """Реалізували приватний метод який перевіряє чи ми працюємо з правильним обєктом
        - модифікуємо даний метод і використаємо твердження assert;
        - щоб не імпортувати клас Swords, ми просто перевіримо чи обєкт має таке саме представлення як і власне клас Меча; 
        - зробили 2 перевірки, на представлення обєкту та на його тип, чи він відноситься до класу Меч;
        - якщо б у нас були інші класи зброї і ми хотіли накладати бафи на будь-яку зброю, 
        то нам варто було просто перевірити в даних твердженнях чи існують потрібні нам атрибути, такі як
        нанесення шкоди або витривалість;
        """
        assert hasattr(obj, "damag"), f"В обєкта {obj} немає атрибуту нанесення шкоди!"
        assert hasattr(obj, "vitality"), f"В обєкта {obj} немає атрибуту витривалості!"
        #assert obj.__repr__() == "Swords()", f"Даний обєкт {obj.__class__} не відноситься до класу Swords()"
        #t = ["<class '__main__.Swords'>", "<class '__main__.SwordMock'>", "<class '__main__.Axe'>"]
        #assert str(type(obj)) in t, f"Невідповідність типів переданого обєкту {type(obj)} до потрібного {t}"
        
        # Спрощуємо перевірку, Якщо виконались твердження повертаємо True
        return True
    
    def __str__(self) -> str:
        """Представлення об'єкта у вигляді рядка, Це буде викликатись коли застосовуємо функцію прінт"""
        return f"Клас SwordBonus: реалізує функціонал бонусів, поточний обєкт має хеш {self.__hash__()}"

    def __repr__(self) -> str:
        """Канонічне представлення об'єкту"""
        return f"SwordBonus()"
    
    def __len__(self) -> int:
        """Застосування методу довжини поверне кількість бонусів які реалізовані в даному класі"""
        return len(SwordBonus.bonus_list())