import curses
from curses import wrapper

from calculator import EvalCalculator
from commands import (DeleteCharCommand, EnterCommand, InputCharCommand,
                      UndoCommand)
from dependency_injector import containers, providers
from snapshot import Caretaker, Originator


class CalculatorContainer(containers.DeclarativeContainer):
    expression = providers.Factory(Originator, state="")
    caretaker = providers.Factory(Caretaker, originator=expression)
    calculator = providers.Factory(
        EvalCalculator, expression=expression, caretaker=caretaker
    )


def main(stdscr) -> None:
    container = CalculatorContainer()
    calc = container.calculator()

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
