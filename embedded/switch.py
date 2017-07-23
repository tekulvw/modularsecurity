import RPi.GPIO as io
import requests
import json
import time

io.setmode(io.BCM)
door_pin = 6

io.setup(door_pin, io.IN, io.PUD_UP)
 
url='https://modular-security-system.appspot.com/api/device/data'
flag=True

while True:
	if io.input(door_pin) != flag:
		response = requests.post(url,
					data=json.dumps({'serial_number': '1',
							'data': {'open': bool(io.input(door_pin))},
							'type': 'door',
							'ext': 'json'}),
					headers={'content-type': 'application/json'})
		flag = bool(io.input(door_pin))

		#print(response.status_code)
		#print(response.content)
		#print(io.input(door_pin))

	time.sleep(1)
