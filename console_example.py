import time
from char_mappings import get_mapping
from datetime import datetime
import requests

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

def fillScreen():
  print(screen[0][:60])
  print(screen[1][:60])
  print(screen[2][:60])
  print(screen[3][:60])
  print(screen[4][:60])
  print("\n")

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

add_message(get_weather())

while True:
	color = (0, 0, 255)
	shiftLeft(1)
	fillScreen()
	time.sleep(0.08)
