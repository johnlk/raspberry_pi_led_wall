import time
from char_mappings import get_mapping
from datetime import datetime
import requests
import threading

screenLock = threading.Lock()

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

class get_time(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    while 1:
      screenLock.acquire()
      print(datetime.now().strftime('%a %d   %I:%M %p'))
      screenLock.release()
      time.sleep(5)

def kelvin_to_far(float_val):
  celcius = float_val - 273.15
  return str(int(celcius * (9/5) + 32))

class get_weather(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    while True:
      try:
        response = requests.get("http://api.openweathermap.org/data/2.5/weather?zip=47905,us" +
          "&appid=5c48857cbe6c1763f27742ae12bd805f")

        response = response.json()

        weather = kelvin_to_far(response['main']['temp']) + " degrees, " + response['weather'][0]['description']
        screenLock.acquire()
        print(weather)
        screenLock.release()
      except Exception as err:
        screenLock.acquire()
        print("404 weather")
        screenLock.release()

      time.sleep(10)

thread1 = get_weather()
thread2 = get_time()

thread1.start()
thread2.start()

"""
while True:
	color = (0, 0, 255)
	shiftLeft(1)
	fillScreen()
	time.sleep(0.08)
"""