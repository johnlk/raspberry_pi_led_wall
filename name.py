import time
import board
import neopixel
import requests
from char_mappings import get_mapping 
from datetime import datetime

from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener

pixel_pin = board.D18
num_pixels = 60 * 5
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.05, auto_write=False, pixel_order=ORDER)

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-41e1caba-e89a-11e6-81cc-0619f8945a4f'
pubnub = PubNub(pnconfig)

my_listener = SubscribeListener()
pubnub.add_listener(my_listener)

pubnub.subscribe().channels('ledWall').execute()
my_listener.wait_for_connect()

screen = [
'0000000000000000000000000000000000000000000000000000000000000',
'0000000000000000000000000000000000000000000000000000000000000',
'0000000000000000000000000000000000000000000000000000000000000',
'0000000000000000000000000000000000000000000000000000000000000',
'0000000000000000000000000000000000000000000000000000000000000'
]

def shiftLeft(numTimes):
	global screen
	screen = [
		screen[0][numTimes:] + screen[0][:numTimes],
		screen[1][numTimes:] + screen[1][:numTimes],
		screen[2][numTimes:] + screen[2][:numTimes],
		screen[3][numTimes:] + screen[3][:numTimes],
		screen[4][numTimes:] + screen[4][:numTimes]
	]


color = (255, 0, 0)

def clear():
	pixels.fill((0,0,0))

def fillRow(rowIndex):
	startingIndex = 60 * rowIndex

	rowString = screen[rowIndex][:60]

	if rowIndex % 2 == 0:
		rowString = rowString[::-1] #reverse it

	for i in range(startingIndex, startingIndex+60):
		if rowString[i % 60] == '1':
			pixels[i] = color
		else:
			pixels[i] = ((0,0,0))
		

def fillScreen():
	clear()
	fillRow(0)
	fillRow(1)
	fillRow(2)
	fillRow(3)
	fillRow(4)
	pixels.show() 

def add_message(message):
  global screen
  message_mapping = get_mapping(message)
  screen = [
		screen[0] + message_mapping[0],
		screen[1] + message_mapping[1],
		screen[2] + message_mapping[2],
		screen[3] + message_mapping[3],
		screen[4] + message_mapping[4]
	]

def get_time():
  return datetime.now().strftime('%a-%d   %I:%M %p')

def kelvin_to_far(float_val):
  celcius = float_val - 273.15
  return str(int(celcius * (9/5) + 32))

def get_weather():
  #response = requests.get("api.openweathermap.org/data/2.5/weather?zip=47905,us&" +
  #  "appid=5c48857cbe6c1763f27742ae12bd805f")
  response = requests.get("https://samples.openweathermap.org/data/2.5/weather?zip=94040,us&appid=b6907d289e10d714a6e88b30761fae22")
  if response.status_code != 200:
    return "404 weather"

  response = response.json()
  #print(response)

  weather = kelvin_to_far(response['main']['temp']) + " degrees, " + response['weather'][0]['description']
  return weather


clear()
pixels.show()

while True:
	result = my_listener.wait_for_message_on('ledWall')
	#print(result.message)

	clear()
	pixels.show()
	pixels.fill((234, 105, 5))
	pixels.show()
	time.sleep(2)

	add_message(result.message['text'])

	passed_color = result.message['color']
	color = (passed_color['r'], passed_color['g'], passed_color['b'])

	for _ in range(len(screen[0])):	
		shiftLeft(1)
		fillScreen()
		time.sleep(0.01)

	screen = [
		'0000000000000000000000000000000000000000000000000000000000000',
		'0000000000000000000000000000000000000000000000000000000000000',
		'0000000000000000000000000000000000000000000000000000000000000',
		'0000000000000000000000000000000000000000000000000000000000000',
		'0000000000000000000000000000000000000000000000000000000000000'
	]




