import unittest
from unittest.mock import patch
import pytest
from random import randint, choice
from axe import Axe
from swords_bonus import SwordBonus
from sword import Swords
from app import SWORD_NAMES, create_players, select_buff

# клас для тестування повинен починатись з слова Test
class TestSwordBonus(unittest.TestCase):
    """Починаємо тестування Бонусів для меча"""
    # В даному класі реалізуються всі юніттести у вигляді методів
    # кожен юніттест (назва функції) повинен починатись з префікса імені "test_"
    # оскільки ми працюємо в класі, ми працюємо з методами, і маємо вказівник на обєкт self який містить 
    # весь функціонал батьківського класу TestCase, з якого ми будемо використовувати перевірки assert

    def setUp(self) -> None:
        print("Проводимо початкову ініціалізацію для тестів....")
        self.sw = Axe() # створений макет на який можемо накласти баф отрути
        self.sword = Swords(choice(SWORD_NAMES), "Legend", 1, 1) # ми підмінили наш макет на реальний меч
        self.sb = SwordBonus() # імплементація бонусів
        self.d, self.v = self.sw.damag, self.sw.vitality  # Початкове значення характеристик витягуємо через подвійне присвоєння
        return super().setUp()
    
    def tearDown(self) -> None:
        print("Видаляємо обєкти після завершення тестування.")
        del self.sw
        del self.sb
        self.d, self.v = None, None
        return super().tearDown()

    def test_bonus_poison(self):
        """Тестуємо правильність накладення бафу отрути"""
        result = self.sb.bonus_poison(self.sw) # після накладення бонусі наша метод має повернути якись результат
        # нам відомий результат що повертається, тому ми просто перевіряємо результат на рівність
        self.assertEqual(result, f"Застосовано бонус отрути {self.sw.name}", f"Повернене значення {result} не відповідає очікуваному")
        # після накладення бафу отрути наш демедж має збільшитись, 
        # тому перевіряємо що поточно значення шкоди має бути більшим за початкове
        self.assertGreater(self.sw.damag, self.d, "Накладений бонус отрути не збільшив значення шкоди.")

    def test_bonus_strength(self):
        """Тестуємо накладання бафу міцності"""
        result = self.sb.bonus_strength(self.sw)
        self.assertEqual(result, f"Застосовано бонус сили до {self.sw.name}")
        self.assertGreater(self.sw.vitality, self.v, "Накладений бонус міцності не збільшив значення міцності.")
        # Якщо ми передали неправильний обєкт, до якого не можна накласти баф, то винике помилка
        with self.assertRaises(AssertionError, msg="До цього обєкта не можна застосовувати накладення бафів, неправильний обєкт"):
            self.sb.bonus_strength(1)
    
    def test_bonus_confusion(self):
        """Тестуємо накладання бафу конфузії"""
        ##### Цей підрозділ робить початкову ініціалізацію
        # Весь цей підрозділ ми можемо винести у спеціальний метод який називається setUp
        #sw = Axe() # створений макет на який можемо накласти баф отрути
        #sb = SwordBonus() # імплементація бонусів
        #d, v = sw.damag, sw.vitality  # Початкове значення характеристик витягуємо через подвійне присвоєння
        
        ##### Це новий підрозділ, де ми власне викликаємо методи який хочемо протестувати
        # передаємо в нього потрібно нам аргументи та записуємо результа
        result = self.sb.bonus_confusion(self.sw)
        
        ##### Це є останній розділів тесту, який власне тустує що ми отримали
        # тут тестуємо що повинна повертати наш метод накладення бафу
        self.assertTrue(isinstance(result, str), "Повернене значення не відповіє стрічковому типу даних")
        self.assertIn(self.sw.name, result, f"Отримана відповідь не вказує не містить {self.sw.name}")
        self.assertIn("бонус", result, "Повернене значення не містить слова бонус")
        
        # тут тестуємо зміни які були здійснені накладанням бафу
        self.assertGreaterEqual(self.sw.damag, self.d, "Баф мав залишити рівним або збільшити значення Нанесення шкоди.")
        self.assertGreaterEqual(self.sw.vitality, self.v, "Баф мав залишити рівним або збільшити значення Міцності.")
        # Якщо ми передали неправильний обєкт, до якого не можна накласти баф, то нам просто виникне помилка
        with self.assertRaises(AssertionError, msg="До цього обєкне не можна застосовувати накладення бафів, неправильний обєкт"):
            self.sb.bonus_confusion(1)
    
    def test_bonus_berserk(self):
        """Тестуємо бонус Берсерка"""
        # Невелика перевірка чи ми дійсько працюємо з Мечем
        self.assertTrue(self.sw.__repr__() is Axe.__repr__(self.sw), f"{self.sw.__repr__()} Не відноситься до класу Меча {Swords.__repr__(self.sw)}")
        # початкова ініціалізація шкоди = 0, тому ставимо якесь значення яке ми хочемо протестувати
        min_damage = 5
        self.sw.damag = randint(min_damage, 10)
        # ініціалізуємо накладання бонусу на Меч
        result = self.sb.bonus_berserk(self.sw)

        # Ефект бурсерка подвоюює атаку, протестуємо це
        self.assertGreater(self.sw.damag, min_damage * 2 - 1) # шкода має бути збільшена
        # і збільшена у 2 рази
        self.assertTrue(self.sw.damag / min_damage >= 2, "Шкода від бафу берсеркера має бути більшою хочаб у 2 рази")
        # значення міцності не посинне бути зміненим і залишитись 0 як було ініціалізовано у класі Axe
        self.assertTrue(self.sw.vitality == 0)
        self.assertIsInstance(result, str, "Повернений результат повинен бути стрічкою.")

    def test_bonus_invincible(self):
        """Тестуємо бонус Незламності"""
        v = self.sw.vitality # початкове значення витривалості
        result = self.sb.bonus_invincible(self.sw)
        self.assertGreater(self.sw.vitality, v, f"Після накладення бонусу значення {self.sw.vitality} має бути більшим за {v}")

    def test_bonus_apply_on_legendary_rarity(self):
        """Тестуємо що для меча з Легендарною ріднісністю буде додано випадковий бонус"""
        # викиристаємо альтернативний конструктор та створимо Легендарний меч
        s = Swords.create_from_rarity(choice(SWORD_NAMES), "Legend")
        # Перевіряємо ми ще не наклали бонус
        self.assertTrue(s.bonus == SwordBonus._nothing.__doc__, "Опис бонусу має відповідати пустому значення якщо ми ще не наклали Бонус")
        bonus_description = s.apply_bonus() # Застосували бонус до Меча
        self.assertTrue(s.bonus == bonus_description, f"Легендарна рідкісність повинна мати бонус відмінний від {SwordBonus._nothing.__doc__}")
        # перевіряємо що накладений бонус збільшив атрибути Меча
        self.assertTrue(s.damag > (3 * Swords.rarity_map["Legend"]) or s.vitality > (5 * Swords.rarity_map["Legend"]), f"Накладений бонус {s.bonus} не збільшив атрибути шкоди {s.damag} або витривалості {s.vitality}")

    def test_no_bonus_for_low_rarity(self):
        """Тестуємо що на Меч з низькою якістю не буде накладено бонусів"""
        s = Swords.create_from_rarity(choice(SWORD_NAMES), "Basic")
        d = s.apply_bonus()
        self.assertEqual(s.bonus, d, f"На меч з якістю Basic має бути накладено бонус: {SwordBonus._nothing.__doc__}")


class TestApplyBuffs(unittest.TestCase):
    """Клас призначений для тестування накладання бафів на меч"""
    def setUp(self) -> None:
        self.s = Swords.create_random_rarity("Тренувальний Меч")
        return super().setUp()
    
    def tearDown(self) -> None:
        del self.s
        return super().tearDown()
    
    def test_get_correct_damage_buff(self):
        """Тестуємо правильність накладання бафу нанесення шкоди"""
        self.assertEqual(self.s.hit, self.s.damag, f"Значення damage {self.s.damag} не рівне значенню hit {self.s.hit}")
        result = self.s.get_buff_damag(4)
        self.assertIsInstance(result, str, "Відповідь після накладення бафу має бути стрічкою.")
        self.assertGreater(self.s.hit, self.s.damag, "Накладений баф нанесення шкоди НЕ підвищив атрибут нанесення шкоди.")
        self.assertIn(self.s.__hash__, Swords.who_has_buff, f"Неправильно відстежуються накладені бафи в глобальній змінній who_has_buff {Swords.who_has_buff}")

        result_fail = self.s.get_buff_damag(5)
        self.assertNotEqual(result, result_fail, f"Не можна накласти баф вдруге, відповідь неправильна -> {result_fail}.")

    def test_get_correct_buff_vitality(self):
        """Тестеємо застосування бафу витривалості"""
        v = 5 # значення на яке ми збільшуємо витривалість через баф
        result = self.s.get_buff_vitality(v)
        self.assertIsNotNone(result, "Ми отримали None при виклику накладення бафу витривалості.")
        self.assertIsInstance(result, str, "Відповідь після накладення бафу має бути стрічкою.")
        self.assertTrue(hasattr(self.s, "buff_vitality"), "В обєкта Меча відсутній атрибут 'buff_vitality'.")
        self.assertEqual(self.s.buff_vitality, v, f"Застосоване значення бафу витривалості не відповідає значенню {v}.")

        self.assertTrue(len(Swords.who_has_buff) > 0, f"Не було додано запис про накладення бафу на Меч, {Swords.who_has_buff}")

        result_fail = self.s.get_buff_vitality(v)
        self.assertNotEqual(result, result_fail, f"Не можна накласти баф вдруге, відповідь неправильна -> {result_fail}.")


class TestSwordsCreation(unittest.TestCase):
    """В цьому класі ми тестуємо Клас Меча"""
    # давайте не будемо робити в цьому класі початкової ініціалізації для Меча
    # а натомість, в кожному тесті ми просто будемо тестувати інший спосіб створення Меча
    
    def test_create_sword_from_constructor(self):
        """Тестуємо створення меча через основний конструктор класу Swords"""
        d = {'name': 'Тренувальний Меч', 
             'rarity': 'Epic', 
             'damag': 5, 
             'vitality': 10, 
             'bonus': SwordBonus._nothing.__doc__, 
             'buff_damage': 0, 
             'buff_vitality': 0, 
             'debuff': []}
        s = Swords(d["name"], d["rarity"], d["damag"], d["vitality"])
        self.assertIsInstance(s, Swords, f"Щось пішло не так і меч не є класу {Swords.__repr__}")
        self.assertDictEqual(d, s.__dict__, f"У стореному Мечі немає базових атрибутів доступних через __dict__ {s.__dict__}")
    
    def test_create_sword_with_correct_rarity(self):
        """Тестуємо правильність сторення меча із задоною характеристикою рідкісності"""
        s = Swords.create_from_rarity("Тренувальний Меч", "Epic")
        s.apply_bonus()
        self.assertGreaterEqual(s.damag, 3*Swords.rarity_map["Epic"], "Неправильно вирахувано величину нанесення шкоди.")
        # наступна перевірка. викличе помилку в ініціалізації Меча, але ми так і хочемо, тому ми виловлюємо цю помилку
        with self.assertRaises(AttributeError):
            Swords.create_from_rarity("Тренувальний Меч", "NonExist")
        # навіть після виникнення помилки, ми продовжуємо тестування
        # тут тестуємо, відповідність присвоєного бонусу відповідно до заданої рідкісності
        self.assertFalse(s.bonus == SwordBonus._nothing.__doc__, "Меч з рідкісністю Epic повинен мати бонус")
        s = Swords.create_from_rarity("Тренувальний Меч", "Green")
        self.assertTrue(s.bonus == SwordBonus._nothing.__doc__, "Меч з рідкісністю Green НЕ повинен мати бонус")

    def test_create_sword_from_random_rarity(self):
        """Тестуємо створення меча з випідковою характеристикою рідкісності"""
        name = 'Тренувальний Меч'
        s = Swords.create_random_rarity(name)
        self.assertIn(s.rarity, Swords.rarity_map.keys(), f"Рідкісність меча не відповідає заданим в {Swords.rarity_map.keys()}.")
        self.assertTrue(s.name == name, "Меч з випадковою рідкіснісю має неправильне Імя.")

# дану фікстуру нам підказав ChatGPT
@pytest.fixture
def sword():
    """Фікстура для створення меча."""
    return Swords.create_random_rarity(choice(SWORD_NAMES))
    #return Axe()

def test_sword_with_random_rarity(sword):
    """Тестуємо меч з використання фікстур"""
    assert hasattr(sword, 'rarity'), f"В обєкта неправильно встановлено атрибут рідкісності!"
    assert isinstance(sword.rarity, str), "Назва типу рідкісності має бути словом/стрічкою."
    assert sword.rarity in Swords.rarity_map.keys(), f"Рідкісність меча {sword.rarity} не відповідає заданим {Swords.rarity_map.keys()}"
    assert isinstance(sword, Swords), f"Обєкт що тестується класу {type(sword)} має бути мечем класу {type(Swords)}"


@pytest.fixture
def player_select_attack():
    return lambda _: "1"

@pytest.fixture
def player_select_defense():
    return lambda _: "2"

@pytest.fixture
def player_select_nothing():
    return lambda _: None

def test_player_select_buffs(monkeypatch, player_select_attack, player_select_defense, player_select_nothing):
    """Тестуємо правильність вводу гравцем значень для вибону накладання Бафу."""
    monkeypatch.setattr('builtins.input', player_select_attack)
    assert select_buff("Player1") == '1', "Неправильно введено вибір для атаки!"

    monkeypatch.setattr('builtins.input', player_select_defense)
    assert select_buff("Player1") == '2', "Неправильно введено вибір для захисту!"

    monkeypatch.setattr('builtins.input', player_select_nothing)
    assert select_buff("Player1") == None, "Гравець ввів не коректні дані!"


def test_player_creation(monkeypatch):
    """Тестуємо правильність ініціалізаціцї гравців та їх Мечів"""
    # даний тест буде розпізнаватись лише бібліотекою PyTest, unittest його не побачить

    # створюємо гравця
    monkeypatch.setattr('builtins.input', lambda _: "Богдан")
    p = create_players()
    #assert False # Даний тест впаде, ми просто хочемо протестувати чи це буде працювати
    assert isinstance(p, Swords)
    assert p.player == "Богдан"
    assert p.name in SWORD_NAMES


def test_reply_from_negative_effects(sword):
    """Тестуємо виклик функції випадкової геренації накладання негативних ефектів"""
    response = sword.negative_effects("Тестувальний ефект")
    assert isinstance(response, bool), "Повинно повернутись значення True або False"
    # Перевірка, що функція працює коректно для всіх можливих значень випадкового числа
    
    with patch('builtins.print') as mock_print:
        response = sword.negative_effects("Тестувальний ефект")
        if response:
            assert mock_print.called, "Виклик print не відбувся при застосування негативних ефектів"

# Ця конструкція if не дозволить запустити цей код якщо ми його імпортнемо в інший файл
if __name__ == '__main__':
    unittest.main(verbosity=2)