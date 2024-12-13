from display import display

class Data:
    def __init__(self, display):
        self.display = display
        self._health = 10 # private attribute
        self._keys = 0 # private attribute
        self._damage = 1

        self.update_display()

        self.current_level = 0

    @property # getter
    def health(self):
        return self._health

    @health.setter # setter
    def health(self, value):
        self._health = value
        self.update_display()

    @property # getter
    def keys(self):
        return self._keys

    @keys.setter # setter
    def keys(self, value):
        self._keys = value

    @property # getter
    def damage(self):
        return self._damage

    @damage.setter # setter
    def damage(self, value):
        self._damage = value
        self.update_display()

    def update_display(self):
        self.display.create_heart(self._health)
        self.display.create_sword(self._damage)


