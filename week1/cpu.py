from abc import ABC, abstractmethod


class CPU(ABC):
    @abstractmethod
    def process(self, tasks: list[int]):
        pass


class SingleCoreCPU(CPU):
    def process(self, tasks: list[int]):
        return [tasks]


class DoubleCoreCPU(CPU):
    def process(self, tasks: list[int]):
        return [tasks[::2], tasks[1::2]]


class CPUFactory:
    @staticmethod
    def make_cpu(type) -> CPU:
        if type == "singe":
            return SingleCoreCPU()
        elif type == "dual":
            return DoubleCoreCPU()
        else:
            raise NotImplementedError(f"CPU type {type} not supported")
