import curses
from curses import wrapper
from commands import *
from snapshot import *


class EvalCalculator:
    def __init__(self):
        self.expression = Originator("")
        self.caretaker = Caretaker(self.expression)
        self.results = []

    def input_char(self, char: str):
        self.expression.add_char(char)

    def delete_char(self):
        self.expression.delete_char()

    def enter(self):
        try:
            self.caretaker.backup()
            result = float(eval(str(self.expression)))
            self.expression.restore(Memento(str(result)))
            result = f"{self.expression} = {result:.3f}"
            self.results.append(result)

        except:
            self.expression.restore(Memento("Invalid expression"))

    def undo(self):
        self.caretaker.undo()
        self.results = self.results[:-1]


def main(stdscr) -> None:
    calc = EvalCalculator()
    curses.echo()

    while True:
        stdscr.clear()
        stdscr.addstr(
            0,
            0,
            "Press 'q' to quit\nPress 'backspace' to delete\nPress 'enter' to calculate\nPress 'u' to undo\n",
        )

        height, width = stdscr.getmaxyx()
        for i, result in enumerate(calc.results):
            stdscr.addstr(i, width - len(result) - 1, result)

        stdscr.addstr(height - 1, 0, str(calc.expression))

        stdscr.refresh()
        c = stdscr.getkey()

        if c == "q":
            break
        elif c == "\x7f":
            DeleteCharCommand(calc).execute()
        elif c == "\n":
            EnterCommand(calc).execute()
        elif c == "u":
            UndoCommand(calc).execute()
        else:
            InputCharCommand(calc, c).execute()


wrapper(main)
