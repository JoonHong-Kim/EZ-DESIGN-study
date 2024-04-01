from abc import ABC, abstractmethod


class Cpu(ABC):
    @abstractmethod
    def process(self, tasks: list[int]) -> list[list[int]]:
        pass


class SingleCoreCPU(Cpu):
    def process(self, tasks: list[int]) -> list[list[int]]:
        return [tasks]


class DoubleCoreCPU(Cpu):
    def process(self, tasks: list[int]) -> list[list[int]]:
        return [tasks[::2], tasks[1::2]]


class CPUFactory:
    @staticmethod
    def make_cpu(type) -> Cpu:
        if type == "single":
            return SingleCoreCPU()
        elif type == "dual":
            return DoubleCoreCPU()
        else:
            raise ValueError(f"CPU type {type} not supported")
