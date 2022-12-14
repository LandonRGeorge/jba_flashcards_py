class Card:
    def __init__(self):
        self._front = None
        self._back = None

    @property
    def front(self):
        return self._front

    @property
    def back(self):
        return self._back

    def set_front(self):
        # front = input("Card:\n")
        print("Card:")
        front = "2 + 2"
        print(front)
        self._front = front

    def set_back(self):
        # back = input("Definition:\n")
        print("Definition:")
        back = "4"
        print(back)
        self._back = back


c = Card()
c.set_front()
c.set_back()
