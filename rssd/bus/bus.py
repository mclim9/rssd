"""abstract Rohde & Schwarz Communication Bus Class"""
from abc import ABC, abstractmethod

class bus(ABC):
    """abstract Rohde & Schwarz Communication Bus Class"""

    @abstractmethod
    def close(self): pass

    @abstractmethod
    def open(self, resourceID, param=None): pass

    @abstractmethod
    def query(self, SCPIstr): pass

    @abstractmethod
    def read_raw(self): pass

    @abstractmethod
    def timeout(self, seconds): pass

    @abstractmethod
    def write(self, SCPIstr): pass

    @abstractmethod
    def write_raw(self, SCPIstr): pass
