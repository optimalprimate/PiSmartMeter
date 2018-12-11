#!/usr/bin/python
from __future__ import division
from bottle import route, run, template
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



#take baseline for 20 loops (10s)
light_level_bs=0
for  i in range(0,40):
	light_level_bs = light_level_bs + ReadChannel(light_channel)
	time.sleep(delay)

mean_bs = light_level_bs / 40
bs_thresh = mean_bs - 12 # threshold for baseline with reduction

print "baseline= %d" %mean_bs

ms_event = int(round(time.time() * 1000)) # current time in ms
kwuse = 2.342355 #defines as float
costhour = 5.0043
cost = 345.345
flashperhour = 23.2355645


while True:
   # Read the light sensor data
  light_level = ReadChannel(light_channel)
  if light_level < bs_thresh:
	ms_now = int(round(time.time() * 1000)) # takes time of event
	ms_delay = ms_now - ms_event #dif between last even and this one
	ms_event = ms_now	# resets last event
	flashperhour = 3600000/ms_delay #number of flashes per hour
	kwuse = flashperhour/800 # there are 800 flashes / KwH
	GPIO.output(GPIO_LED,True) ## turn on green LED
	
	dt = list(time.localtime()) # take current time
	hour = dt[3] # take just the hour
	
	if hour > 1 and hour <8: # if night_cost
		cost = night_cost
	elif hour < 1 or hour >8:
		cost = day_cost
		
	costhour = kwuse * cost
	s_delay = ms_delay / 1000
	print "--------------------------"
	print "Current Pence per Hour = " 
	print("%.2f p" %costhour)
	
	
	time.sleep(0.5)
	GPIO.output(GPIO_LED,False) ## turn off LED
 

  # Wait before repeating loop
  time.sleep(delay)
  
#web update
@route('/')
def index(name='usage'):
	return template('<b> Current usage in pence/hour is: {{costhour}}</b>', costhour)
run(host='192.168.1.207', port=80)
	
	
