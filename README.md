# RPi-SHT40-temphum
A Python script to send temperature and humidity sensor data from an SHT40 sensor on a Raspberry Pi to InfluxDB

The Adafruit adafruit_sht4x library should be installed.

$ pip install adafruit_sht4x

It is also suggested to run this as part of a cronjob on the Raspberry PiOS.  I use every 10 minutes.

$ crontab -e

*/10 * * * * /home/pi/Python/temphum/.env/bin/python /home/pi/Python/temphum/temphum.py
