from random import choice, randint
from typing import Any
from swords_bonus import SwordBonus

class Swords:
    who_has_buff = [] # Ця класова змінна відслідковує на які обєкти зараз накладено баф
    # Це мапа яка вказує коефіцієнт збільшення атрибутів відносно Рідкісності предмету
    rarity_map = {"Basic": 1, "White": 2, "Green": 3, "Blue": 5, "Yellow": 7, "Epic": 9, "Legend": 10} 
    
    def __init__(self, name:str, rarity:str, damag:int, vitality:int) -> None: # Це є свого роду конструктор
        """Конструктор для створення обєкту Меч.
        name: поля для імені;
        rarity: Рідкість предмету; 
        damag: Нанесення шкоди;
        vitality: Міцність предмету;
        bonus: необовязковий аргумент, буде містити опис бонуса який можна застосувати до обєкта;
        """
        self.name = name # це є атрибути обєкта, їх можна змінювати після створення обєкту
        self.rarity = rarity
        self.damag = damag
        self.vitality = vitality
        self.bonus = SwordBonus._nothing.__doc__ # тут ми просто будемо знати що за бонус був застосований до нашого обєкту
        
        self.buff_damage = 0
        self.buff_vitality = 0
        self.debuff = list()

    @classmethod
    def create_from_rarity(cls, name:str, rarity:str):
        """Це конструктор використовуємо коли ми отримуємо меч з крафту"""
        if rarity in cls.rarity_map.keys():
            return cls(name, rarity, damag=3*cls.rarity_map[rarity], vitality=5*cls.rarity_map[rarity])
        raise AttributeError(f"Неправильно задано рідкісність предмету, повинно бути один з {list(cls.rarity_map.keys())}")
    
    @classmethod
    def create_random_rarity(cls, name:str):
        """Тут ми випадково вибили меч з Боса"""
        rarity = choice(list(cls.rarity_map.keys()))
        return cls.create_from_rarity(name, rarity)
    
    def apply_bonus(self):
        """Застосовуємо накладання бонусу"""
        # Вибираємо бонуси з доступного списку
        bonus_list = SwordBonus.list_bonus_methods()
        bonus = SwordBonus._nothing
        if self.rarity in list(Swords.rarity_map.keys())[-3:]:
            # Якщо значення рідкісністі буде досить високим, то застосовуємо бонус
            bonus = getattr(SwordBonus, choice(bonus_list))
        bonus(self)
        self.bonus = bonus.__doc__
        return bonus.__doc__

    def get_buff_damag(self, damag:int) -> str:
        if self.__hash__ in Swords.who_has_buff:
            return f"На меч {self.name} вже накладено баф"
        self.buff_damage = damag
        Swords.who_has_buff.append(self.__hash__)
        return f"Накладено баф на {self.name} який додає атрибут нанесення шкоди +{damag}"
    
    def get_buff_vitality(self, vitality:int) -> str:
        if self.__hash__ in Swords.who_has_buff:
            return f"На меч {self.name} вже накладено баф"
        self.vitality += vitality
        self.buff_vitality = vitality
        Swords.who_has_buff.append(self.__hash__)
        return f"Накладено баф на {self.name} який додає атрибут здоровя +{vitality}, загальне здоровя: {self.vitality}"
    
    def expired_buff(self) -> str:
        Swords.who_has_buff.remove(self.__hash__)
        if self.buff_damage > 0:
            self.buff_damage = 0
            return "Дія бафу на нанасення шкоди завершилась!"
        if self.buff_vitality > 0:
            self.vitality -= self.buff_vitality
            self.buff_vitality = 0
            return "Дія бафу на здоровя завершилась!"
        return "На мечі не має ніякого бафу!"
    
    def aging(self):
        """Даний метод реалізує процес старіння меча"""
        if Swords.negative_effects("ржавіння"):
            self.debuff.append("ржавіння")
        if Swords.negative_effects("затуплення"):
            self.debuff.append("затуплення")
        if Swords.negative_effects("трішина"):
            self.debuff.append("трішина")
        self.vitality -= len(self.debuff)
    
    def repair(self):
        """Метод реалізує відновлення міцності предмету під час ремонту"""
        if randint(0, 1):
            self.vitality += Swords.rarity_map[self.rarity]
            self.debuff = [] # Знімаємо всі дебафи
            return f"{self.name} відремонтовано та знято всі дебафи."
        return f"Не вийшло відремонтувати {self.name}"

    def attack(self, item = None) -> str:
        """Метод для атаки
        """
        if isinstance(item, Swords):
            item.vitality -= self.hit
            return f"Нанесено шкоду {self.hit} мечу {item.name}"
        if item is None:
            return "Ми промахнулись!"
        return f"Ми попали по сторонньому предмету {type(item)}"
        
    def parry(self, damage) -> int:
        """Метод для парирування, тут в нас є бага, ми не можемо зменшувати проперті health
        """
        self.vitality -= damage
        return self.vitality
    
    @staticmethod
    def negative_effects(name:str) -> bool:
        """Визначаємо чи меч випадковим чином отримав якийсь негативний ефект"""
        if randint(0, 4) > 2:
            print(f"Меч отримав негативнй ефект {name}, повертаємо дебаф на 1")
            return True
        return False
    
    @property 
    def get_name(self) -> str:
        """Повертає значення імені. І тут проперті змінювати не можна! Це моле лише для читання."""
        return self.name
    
    @property
    def info(self) -> str:
        """Проперті для читання, виводить інформацію про обєкт."""
        return f"""<<<<< Стати для {self.name} >>>>>
Назва: {self.get_name}
Рідкість: {self.rarity}
Дамаг: {self.hit}
Витривалість: {self.health}
Унікальна характеристика: {self.bonus}
Накладені Бафи: Дамаг {self.buff_damage} та Витривалість {self.buff_vitality}
Накладені Дебафи: {self.debuff}
>>>>>\n"""

    @property
    def hit(self):
        """Проперті яка визначає загальне значення нанесення шкоди"""
        return self.damag + self.buff_damage
    
    @property
    def health(self):
        """Проперті яка визначає всю витривалість ХП який має обєкт"""
        return self.vitality
    
    def __repr__(self) -> str:
        return "Swords()"
