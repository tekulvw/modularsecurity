import RPi.GPIO as io
import requests
import json

io.setmode(io.BCM)
door_pin = 17

io.setup(door_pin, io.IN, io.PUD_UP)

response = requests.post('https://modular-security-system.appspot.com/api/device/data',
			data=json.dumps({'serial_number': '0', 'data': {'open': io.input(door_pin)}, 'type': 'door', 'ext': 'json'}),
			headers={'content-type': 'application/json'})

