#!/usr/bin/python
from __future__ import division
from bottle import route, run, template
import RPi.GPIO as GPIO
import spidev
import time
import os


#web update
@route('/')
def index(name='usage'):
	f = open('current.txt', 'r')
	x = f.readlines()

	return template('<b> Current usage in pence/hour is: {{x}}</b>', x)
run(host='192.168.1.207', port=80)
	