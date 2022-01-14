import time
import board
import adafruit_sht4x
import argparse
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Main code
parser = argparse.ArgumentParser(prog='GetTempHum.py',
    description='Get Temperature & Humidity data from Raspberry Pi and push into InfluxDB')
parser.add_argument('-d', '--debug', action='store_true', help='Run in debug mode with output to STDOUT')
args = parser.parse_args()


# InfluxDB API token and database vars
token = "INSERT_YOUR_TOKEN"
org = "INSERT_YOUR_ORG"
bucket = "INSERT_YOUR_BUCKET"
influxserver = "INSERT_YOUR_INFLUX_SERVER"
location = "INSERT_LOCATION_TAG"


i2c = board.I2C()   # uses board.SCL and board.SDA
sht = adafruit_sht4x.SHT4x(i2c)
sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
# Can also set the mode to enable heater
# sht.mode = adafruit_sht4x.Mode.LOWHEAT_100MS

tempc, relative_humidity = sht.measurements
tempf = tempc * 9/5 + 32

if (args.debug):
    print("Using debug mode...\n\n")
    print("Current mode is: ", adafruit_sht4x.Mode.string[sht.mode])
    print(f"Temperature: {tempf:.1f} " + u"\N{DEGREE SIGN}" + "F")
    print(f"Humidity   : {relative_humidity:.1f} %")

with InfluxDBClient(url=influxserver + ":8086", token=token, org=org) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS)
    sequence = [f"environmentals,location={location} temp={tempf:.1f}",
                f"environmentals,location={location} humidity={relative_humidity:.1f}"]
    if (args.debug): print(sequence)
    write_api.write(bucket, org, sequence)
    client.close()
