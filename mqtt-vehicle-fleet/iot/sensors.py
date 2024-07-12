from abc import ABC, abstractmethod
from uuid import uuid4
from random import uniform
import time
import pandas as pd
import os


class Sensor(ABC):
    def __init__(self, id: str) -> None:
        self.id = id

    @abstractmethod
    def read(self) -> dict:
        pass


class Thermistor(Sensor):
    def __init__(self, location) -> None:
        super().__init__(str(uuid4()))
        self.location = location
        self.unit = "Celsius"
        
    def read(self) -> dict:
        return {
            "id": self.id,
            "timestamp": time.time(),
            "temperature": uniform(105.0, 120.0),
            "unit": self.unit,
            "location": self.location
        }
    

class GPS(Sensor):
    def __init__(self, route: str) -> None:
        super().__init__(str(uuid4()))
        self.file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "coordinates", route + ".csv")
        self.coords = pd.read_csv(self.file_path)
        self.last_coords = None

    def read(self) -> dict:
        current_coords = self.coords.iloc[0].values
        self.last_coords = current_coords

        return {
            "id": self.id,
            "timestamp": time.time(),
            "lat": current_coords[0].item(),
            "lon": current_coords[1].item()
        }
    

if __name__ == "__main__":

    # thermistor = Thermistor("engine")
    # print(thermistor.read())

    gps = GPS("dublin-limerick")
    print(gps.read())
