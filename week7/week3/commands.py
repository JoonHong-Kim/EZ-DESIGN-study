from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


class InputCharCommand(Command):
    def __init__(self, receiver, char: str) -> None:
        self._receiver = receiver
        self._char = char

    def execute(self) -> None:
        self._receiver.input_char(self._char)


class DeleteCharCommand(Command):
    def __init__(self, receiver) -> None:
        self._receiver = receiver

    def execute(self) -> None:
        self._receiver.delete_char()


class EnterCommand(Command):
    def __init__(self, receiver) -> None:
        self._receiver = receiver

    def execute(self) -> None:
        self._receiver.enter()


class UndoCommand(Command):
    def __init__(self, receiver) -> None:
        self._receiver = receiver

    def execute(self) -> None:
        self._receiver.undo()


class QuitCommand(Command):
    def __init__(self, receiver) -> None:
        self._receiver = receiver

    def execute(self) -> None:
        self._receiver.quit()
