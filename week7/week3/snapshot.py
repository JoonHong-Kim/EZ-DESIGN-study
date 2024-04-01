class Memento:
    def __init__(self, state: str):
        self._state = state

    def get_state(self):
        return self._state


class Originator:
    def __init__(self, state: str):
        self._state = state

    def __str__(self) -> str:
        return self._state

    def __len__(self) -> int:
        return len(self._state)

    def save(self):
        return Memento(self._state)

    def restore(self, memento: Memento):
        self._state = memento.get_state()

    def add_char(self, char: str):
        self._state += char

    def delete_char(self):
        self._state = self._state[:-1]


class Caretaker:
    def __init__(self, originator: Originator):
        self._mementos = []
        self._originator = originator

    def backup(self):
        self._mementos.append(self._originator.save())

    def undo(self):
        if not self._mementos:
            return
        memento = self._mementos.pop()
        self._originator.restore(memento)
