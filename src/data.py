# from UI import UI
class Data:
    def __init__(self, ui):
        # self.ui = ui
        self._coins = 0
        self._health = 5 # private attribute

        # self.ui.create_heart(self._health)

        self.unlocked_level = 0
        self.current_level = 0

    @property # getter
    def health(self):
        return self._health

    @health.setter # setter
    def health(self, value):
        self._health = value
        # self.ui.create_heart(value)

    @property # getter
    def coins(self):
        return self._coins

    @coins.setter # setter
    def coins(self, value):
        self._coins = value
        if self.coins >= 100:
            self.coins -= 100
            self.health += 1
        # self.ui.show_coins(self.coins)

    print("hello")
