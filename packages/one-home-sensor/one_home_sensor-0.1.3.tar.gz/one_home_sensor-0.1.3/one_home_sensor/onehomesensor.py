import time
from datetime import datetime
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from .libs.bme280 import BME280
from pymongo import MongoClient


class OneHomeSensor:
    def __init__(self, running_args,mongodb_con):
        self.print_only = running_args.print_only
        self.mongodb_con = mongodb_con
        self.sensor_instance_name = running_args.sensor_name

    def push_to_mongodb(self,temperature,pressure,humidity):
        client = MongoClient(self.mongodb_con)
        db = client.onehomesensor
        readings = db['readings_'+self.sensor_instance_name]
        time = int(datetime.now().timestamp())
        readings.insert_one({
            'ti' : str(time),
            'te': "{:05.2f}".format(temperature),
            'pr': "{:05.2f}".format(pressure),
            'hu': "{:05.2f}".format(humidity),
        })


    def run(self):        
        # Initialise the BME280
        bus = SMBus(1)
        bme280 = BME280(i2c_dev=bus)
        # Read sensors 
        temperature = bme280.get_temperature()
        time.sleep(0.5)
        pressure = bme280.get_pressure()
        humidity = bme280.get_humidity()

        # Output sensors Data 
        if self.print_only:
            print('{:05.2f}*C {:05.2f}hPa {:05.2f}%'.format(temperature, pressure, humidity))
        else: 
            self.push_to_mongodb(temperature,pressure,humidity)
