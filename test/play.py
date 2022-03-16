class Play:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def test(self):
        if hasattr(self, 'name'):
            print('name:', self.name)

playboy = Play('playboy', 18)
playboy.test()