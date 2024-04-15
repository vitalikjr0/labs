class Axe:
    """Тимчавсовий клас, емулюючий наш головник клас Меча, використовується для тестів"""
    def __init__(self) -> None:
        self.name = "Сокира"
        self.damag = 0
        self.vitality = 0

    def __repr__(self) -> str:
        return "Swords()"
