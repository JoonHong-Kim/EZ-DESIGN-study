from abc import ABC, abstractmethod
from pydantic import BaseModel
from memory import Ram, Rom, RamFactory, RomFactory
from cpu import Cpu, SingleCoreCPU, DoubleCoreCPU, CPUFactory


class Computer(BaseModel, ABC):
    cpu: Cpu
    ram: Ram
    rom: Rom

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def bootstrap(self) -> dict[str, list[int] | list[list[int]]]:
        pass


class Laptop(Computer):
    def bootstrap(self) -> dict[str, list[int] | list[list[int]]]:
        state = {}
        state["cpu_processed"] = self.cpu.process(tasks=[1, 2, 3, 4])
        state["ram_data"] = self.ram.data
        state["rom_data"] = self.rom.data

        return state


class Desktop(Computer):

    def bootstrap(self) -> dict[str, list[int] | list[list[int]]]:
        state = {}
        state["cpu_processed"] = self.cpu.process(tasks=[1, 2, 3, 4, 5, 6, 7, 8])
        state["ram_data"] = self.ram.data
        state["rom_data"] = self.rom.data

        return state


class ComputerBuilder:
    @staticmethod
    def build_computer(type: str) -> Computer:
        if type == "laptop":
            cpu = CPUFactory.make_cpu(type="single")
            ram = RamFactory.make_memory(size=8)
            rom = RomFactory.make_memory(data=[1, 2, 3, 4])
            return Laptop(cpu=cpu, ram=ram, rom=rom)
        elif type == "desktop":
            cpu = CPUFactory.make_cpu(type="dual")
            ram = RamFactory.make_memory(size=16)
            rom = RomFactory.make_memory(data=[1, 2, 3, 4, 5, 6, 7, 8])
            return Desktop(cpu=cpu, ram=ram, rom=rom)
        else:
            raise ValueError(f"Computer type {type} not supported")
