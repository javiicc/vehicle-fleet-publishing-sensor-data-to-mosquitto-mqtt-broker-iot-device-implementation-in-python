from uuid import uuid4
import time
from sensors import GPS, Thermistor

import paho.mqtt.client as mqtt
from enum import Enum
import json


class VehicleType(Enum):
    VAN = 'van'
    TRUCK = 'truck'
 

class Engine():
    def __init__(self) -> None:
        self.thermistor = Thermistor("engine")


class Vehicle():
    def __init__(self, id: str, vehicle_type: VehicleType) -> None:
        self.id = id
        self.type = vehicle_type
        self.engine = Engine()
        self.gps = GPS("dublin-limerick")
        self.CentralDevice(self)


    class CentralDevice():
        def __init__(self, outer_vehicle) -> None:
            self.vehicle = outer_vehicle
            self.connected = False
            self.mqtt_broker = "localhost"
            self.port = 1883
            self.mqtt_topic_vehicle = f"fleet/{self.vehicle.id}"
            self.mqtt_topic_coordinates = "fleet/coordinates"
            self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
            self.start_publishing()


        def start_publishing(self):

            def on_connect(client, userdata, flags, reason_code, properties):
                # The callback for when the client receives a CONNACK response from the server
                print(f"Connected! Result code: {reason_code}")
                self.connected = True
            
            
            def on_publish(client, userdata, mid, reason_code, properties):
                # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
                # TODO access both publisehd messages to print
                print(f"Published: {coords}")

            self.mqttc.on_connect = on_connect
            self.mqttc.on_publish = on_publish
            self.mqttc.connect(self.mqtt_broker, self.port, 60)

            # Start the network loop in a separate thread
            self.mqttc.loop_start()
            
            # Wait for connection to be established
            while not self.connected:
                time.sleep(0.1)
                        
            while True:
                coords = self.vehicle.gps.read()

                vehicle_data = {
                    "id": self.vehicle.id,
                    "vehicle_type": self.vehicle.type.value,
                    "engine_data": self.vehicle.engine.thermistor.read(),
                    "coordinates": coords
                }
            
                self.mqttc.publish(self.mqtt_topic_vehicle, json.dumps(vehicle_data))
                self.mqttc.publish(self.mqtt_topic_coordinates, json.dumps(coords))
            
                time.sleep(1)


if __name__ == "__main__":
    van1 = Vehicle("van1", VehicleType.VAN)
    van2 = Vehicle("van2", VehicleType.VAN)
