from abc import ABC, abstractmethod
from uuid import uuid4
from random import uniform
import time


class Sensor(ABC):
    def __init__(self, id: str):
        self.id = id

    @abstractmethod
    def read(self) -> dict:
        pass


class Thermistor(Sensor):
    def __init__(self, location):
        super().__init__(str(uuid4()))
        self.location = location
        self.unit = "Celsius"
        
    def read(self):
        return {
            "id": self.id,
            "timestamp": time.time(),
            "temperature": uniform(105.0, 120.0),
            "unit": self.unit,
            "location": self.location
        }


if __name__ == "__main__":
    thermistor = Thermistor("engine")
    print(thermistor.read())
