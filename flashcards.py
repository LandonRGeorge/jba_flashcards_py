import typing


class Card:
    def __init__(self):
        self.front = None
        self.back = None

    def __repr__(self):
        return self.front


class Cards:
    def __init__(self):
        self.fronts: typing.Dict[str, Card] = {}
        self.backs: typing.Dict[str, Card] = {}
        self._gather()

    def _gather(self):
        nbr = int(input("Input the number of cards:\n"))
        self.list = [Card() for _ in range(nbr)]
        for _i, card in enumerate(self.list):
            i = _i + 1
            front = input(f"The term for card #{i}:\n")
            while True:
                if front in self.fronts:
                    front = input(f'The term "{front}" already exists. Try again:\n')
                    continue
                break
            card.front = front
            self.fronts[front] = card
            back = input(f"The definition for card #{i}:\n")
            while True:
                if back in self.backs:
                    back = input(f'The definition "{back}" already exists. Try again:\n')
                    continue
                break
            card.back = back
            self.backs[back] = card

    def ask(self):
        for card in self.list:
            back = input(f'Print the definition of "{card.front}":\n')
            if back == card.back:
                print("Correct!")
                continue
            existing_back = self.backs.get(back, None)
            if existing_back:
                print(
                    f'Wrong. The right answer is "{card.back}", but your definition is correct for "{existing_back.front}".')
                continue
            else:
                print(f'Wrong. The right answer is "{card.back}"')


if __name__ == "__main__":
    cards = Cards()
    cards.ask()
