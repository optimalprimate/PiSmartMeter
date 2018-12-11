#!/usr/bin/python
 
import RPi.GPIO as GPIO
import spidev
import time
import os
 
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
GPIO.setmode(GPIO.BCM)

# Define green LED PIN
GPIO_LED = 17
GPIO.setup(GPIO_LED,GPIO.OUT)
 
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
 
# Define sensor channels
light_channel = 0
 
# Define delay between readings
delay = 0.1
 
# Power costs (p / KwH)
day_cost = 18.3
night_cost = 6.75




ms_event = int(round(time.time() * 1000)) # current time in ms
while True:
   # Read the light sensor data
  light_level = ReadChannel(light_channel)
  print light_level

  # Wait before repeating loop
  time.sleep(delay)
