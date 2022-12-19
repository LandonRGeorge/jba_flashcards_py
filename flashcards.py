import logging
import random
import shutil
import sys
import typing

import sys

TEMP_FILEPATH = "myfile.log"


class LoggerOut:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.filename = filename

    def write(self, message):
        self.terminal.write(message)
        with open(self.filename, "a") as file:
            print(message, file=file, flush=True, end='')

    def flush(self):
        pass


class LoggerIn:
    def __init__(self, filename):
        self.terminal = sys.stdin
        self.filename = filename

    def readline(self):
        entry = self.terminal.readline()
        with open(self.filename, "a") as file:
            print(entry.rstrip(), file=file, flush=True)
        return entry


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

    def get_action(self):
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
        action = input(actions_prompt)
        actions[action]()

    def hardest_card(self):
        if not self.list:
            print("There are no cards with errors.")
            return
        cards = sorted(self.list, key=lambda x: x.wrong_count, reverse=True)
        max_wrong_count = cards[0].wrong_count
        if max_wrong_count == 0:
            print("There are no cards with errors.")
            return
        max_wrong_count_cards = []
        for card in cards:
            if card.wrong_count != max_wrong_count:
                break
            max_wrong_count_cards.append(card)
        if len(max_wrong_count_cards) == 1:
            print(
                f"The hardest card is \"{max_wrong_count_cards[0].front}\". You have {max_wrong_count} errors answering it.")
            return
        cards_text = " ".join([f'"{card.front}", ' for card in max_wrong_count_cards])
        print(f"The hardest cards are {cards_text}. You have {max_wrong_count} errors answering them.")

    def reset_stats(self):
        for card in self.list:
            card.wrong_count = 0
        print("Card statistics have been reset")
        pass

    def log(self):
        filepath = input("File name:\n")
        shutil.copy(TEMP_FILEPATH, filepath)

        print("The log has been saved.")

    def add(self):
        front = input("The card:\n")
        while True:
            if front in self.fronts:
                front = input(f'The term "{front}" already exists. Try again:\n')
                continue
            break
        back = input(f"The definition of the card:\n")
        while True:
            if back in self.backs:
                back = input(f'The definition "{back}" already exists. Try again:\n')
                continue
            break
        card = Card(front, back)
        self.fronts[front] = card
        self.backs[back] = card
        self.list.append(card)
        print(f'The pair ("{card.front}":"{card.back}") has been added.')

    def ask(self):
        n = int(input("How many times to ask?\n"))
        for _ in range(n):
            card = random.choice(self.list)
            back = input(f'Print the definition of "{card.front}":\n')
            if back == card.back:
                print("Correct!")
                continue
            existing_back = self.backs.get(back, None)
            card.wrong_count += 1

            if existing_back:
                print(
                    f'Wrong. The right answer is "{card.back}", but your definition is correct for "{existing_back.front}".')
                continue
            else:
                print(f'Wrong. The right answer is "{card.back}"')

    def remove(self):
        front = input("Which card?\n")
        card = self.fronts.get(front, None)
        if not card:
            print(f"Can't remove \"{front}\": there is no such card.")
            return
        self.list.remove(card)
        print("The card has been removed.")

    def _import(self):
        self.list = []
        filepath = input("File name:\n")
        try:
            with open(filepath) as f:
                for line in f:
                    front, back, wrong_count = line.split('|')
                    card = Card(front, back)
                    card.wrong_count = int(wrong_count)
                    self.list.append(card)
        except FileNotFoundError:
            print("File not found.")
        else:
            print(f"{len(self.list)} cards have been loaded.")

    def export(self):
        filepath = input("File name:\n")
        with open(filepath, "w") as f:
            for card in self.list:
                f.write(card.front + "|" + card.back + "|" + str(card.wrong_count) + "\n")
        print(f"{len(self.list)} cards have been saved.")

    def exit(self):
        print("Bye bye!")
        sys.exit()


if __name__ == "__main__":
    sys.stdout = LoggerOut(TEMP_FILEPATH)
    sys.stdin = LoggerIn(TEMP_FILEPATH)
    cards = Cards()
    while True:
        cards.get_action()
