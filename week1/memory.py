from abc import ABC, abstractmethod
from pydantic import BaseModel


class Memory(BaseModel, ABC):
    data: list[int]

    @property
    def size(self) -> int:
        return len(self.data)

    @abstractmethod
    def read(self, idx: int) -> int:
        pass

    @abstractmethod
    def write(self, idx: int, value: int):
        pass


class Ram(Memory):
    def read(self, idx: int) -> int:
        return self.data[idx]

    def write(self, idx: int, value: int):
        self.data[idx] = value


class Rom(Memory):
    def read(self, idx: int) -> int:
        return self.data[idx]

    def write(self, idx: int, value: int):
        raise ValueError("ROM is read-only")


class MemoryFactory(ABC):
    @staticmethod
    @abstractmethod
    def make_memory(size: int = 0, data: list[int] = []) -> Memory:
        pass


class RamFactory(MemoryFactory):
    @staticmethod
    def make_memory(size: int = 0, data: list[int] = []) -> Ram:
        if data:
            raise ValueError("RAM cannot be initialized with data")
        return Ram(data=[0] * size)


class RomFactory(MemoryFactory):
    @staticmethod
    def make_memory(size: int = 0, data: list[int] = []) -> Rom:
        if size > 0:
            raise ValueError("ROM cannot be initialized with size")
        return Rom(data=data)
