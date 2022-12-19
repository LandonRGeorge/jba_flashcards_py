import random
import typing
import io
import sys

buffer = io.StringIO()


def print_and_log(text):
    print(text)
    buffer.write(text + "\n")


def input_and_log(text):
    response = input(text)
    buffer.write(text)
    return response


class Card:
    def __init__(self, front, back):
        self.front = front
        self.back = back
        self.wrong_count = 0

    def __repr__(self):
        return self.front

    def __eq__(self, other):
        return self.front == other.front and self.back == other.back

    def __hash__(self):
        return hash(self.front + " " + self.back)


class Cards:
    def __init__(self):
        self.fronts: typing.Dict[str, Card] = {}
        self.backs: typing.Dict[str, Card] = {}
        self.list: typing.List[Card] = []

    def run(self):
        actions = {
            "add": self.add,
            "remove": self.remove,
            "import": self._import,
            "export": self.export,
            "ask": self.ask,
            "exit": self.exit,
            "log": self.log,
            "hardest card": self.hardest_card,
            "reset stats": self.reset_stats,
        }
        actions_prompt = "Input the action (" + ", ".join(actions.keys()) + "):\n"
        action = input_and_log(actions_prompt)
        actions[action]()

    def hardest_card(self):
        if not self.list:
            print_and_log("There are no cards with errors.")
            return
        cards = sorted(self.list, key=lambda x: x.wrong_count, reverse=True)
        max_wrong_count = cards[0].wrong_count
        if max_wrong_count == 0:
            print_and_log("There are no cards with errors.")
            return
        max_wrong_count_cards = []
        for card in cards:
            if card.wrong_count != max_wrong_count:
                break
            max_wrong_count_cards.append(card)
        if len(max_wrong_count_cards) == 1:
            print_and_log(
                f"The hardest card is \"{max_wrong_count_cards[0].front}\". You have {max_wrong_count} errors answering it.")
            return
        cards_text = " ".join([f'"{card.front}", ' for card in max_wrong_count_cards])
        print_and_log(f"The hardest cards are {cards_text}. You have {max_wrong_count} errors answering them.")

    def reset_stats(self):
        for card in self.list:
            card.wrong_count = 0
        print_and_log("Card statistics have been reset")
        pass

    def log(self):
        filepath = input_and_log("File name:\n")
        with open(filepath, "w") as f:
            log = buffer.getvalue()
            f.write(log)

        print_and_log("The log has been saved.")

    def add(self):
        front = input_and_log("The card:\n")
        while True:
            if front in self.fronts:
                front = input_and_log(f'The term "{front}" already exists. Try again:\n')
                continue
            break
        back = input_and_log(f"The definition of the card:\n")
        while True:
            if back in self.backs:
                back = input_and_log(f'The definition "{back}" already exists. Try again:\n')
                continue
            break
        card = Card(front, back)
        self.fronts[front] = card
        self.backs[back] = card
        self.list.append(card)
        print_and_log(f'The pair ("{card.front}":"{card.back}") has been added.')

    def ask(self):
        n = int(input_and_log("How many times to ask?\n"))
        for _ in range(n):
            card = random.choice(self.list)
            back = input_and_log(f'Print the definition of "{card.front}":\n')
            if back == card.back:
                print_and_log("Correct!")
                continue
            existing_back = self.backs.get(back, None)
            card.wrong_count += 1

            if existing_back:
                print_and_log(
                    f'Wrong. The right answer is "{card.back}", but your definition is correct for "{existing_back.front}".')
                continue
            else:
                print_and_log(f'Wrong. The right answer is "{card.back}"')

    def remove(self):
        front = input_and_log("Which card?\n")
        card = self.fronts.get(front, None)
        if not card:
            print_and_log(f"Can't remove \"{front}\": there is no such card.")
            return
        self.list.remove(card)
        print_and_log("The card has been removed.")

    def _import(self):
        self.list = []
        filepath = input_and_log("File name:\n")
        try:
            with open(filepath) as f:
                for line in f:
                    front, back, wrong_count = line.split('|')
                    card = Card(front, back)
                    card.wrong_count = int(wrong_count)
                    self.list.append(card)
        except FileNotFoundError:
            print_and_log("File not found.")
        else:
            print_and_log(f"{len(self.list)} cards have been loaded.")

    def export(self):
        filepath = input_and_log("File name:\n")
        with open(filepath, "w") as f:
            for card in self.list:
                f.write(card.front + "|" + card.back + "|" + str(card.wrong_count) + "\n")
        print_and_log(f"{len(self.list)} cards have been saved.")

    def exit(self):
        print_and_log("Bye bye!")
        sys.exit()


if __name__ == "__main__":
    cards = Cards()
    while True:
        cards.run()
