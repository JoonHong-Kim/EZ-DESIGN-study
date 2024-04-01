from snapshot import Caretaker, Memento, Originator


class EvalCalculator:
    def __init__(self, expression: Originator, caretaker: Caretaker):
        self.expression = expression
        self.caretaker = caretaker
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
