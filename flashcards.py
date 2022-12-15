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
        front = input("Card: ")
        self._front = front

    def set_back(self):
        back = input("Definition: ")
        self._back = back

    def get_answer(self):
        answer = input("Answer: ")
        if self.back == answer:
            print("right")
        else:
            print("wrong")


c = Card()
c.set_front()
c.set_back()
c.get_answer()
