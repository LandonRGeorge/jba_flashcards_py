import typing


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

    @front.setter
    def front(self, value):
        self._front = value

    @back.setter
    def back(self, value):
        self._back = value


while True:
    nbr_cards = input("Input the number of cards:\n")
    try:
        nbr_cards = int(nbr_cards)
    except ValueError:
        continue
    break

cards: typing.List[Card] = []
for i in range(1, nbr_cards + 1):
    card = Card()
    card.front = input(f"The term for card #{i}:\n")
    card.back = input(f"The definition for card #{i}:\n")
    cards.append(card)

for card in cards:
    back = input(f'Print the definition of "{card.front}":\n')
    if back == card.back:
        print("Correct!")
    else:
        print(f'Wrong. The right answer is "{card.back}"')
