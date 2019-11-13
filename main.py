import time
import board
import neopixel
import requests
import threading

from char_mappings import get_mapping 
from datetime import datetime
from key import get_pubnub_obj, get_weather_key

from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener

pixel_pin = board.D18
num_pixels = 60 * 5
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.05, auto_write=False, pixel_order=ORDER)

pubnub = get_pubnub_obj()
my_listener = SubscribeListener()
pubnub.add_listener(my_listener)

pubnub.subscribe().channels('ledWall').execute()
my_listener.wait_for_connect()

color_index = 0

def get_clean_screen():
  return [
		'0000000000000000000000000000000000000000000000000000000000000',
		'0000000000000000000000000000000000000000000000000000000000000',
		'0000000000000000000000000000000000000000000000000000000000000',
		'0000000000000000000000000000000000000000000000000000000000000',
		'0000000000000000000000000000000000000000000000000000000000000'
	]

def shiftLeft(numTimes, screen):
	return [
		screen[0][numTimes:] + screen[0][:numTimes],
		screen[1][numTimes:] + screen[1][:numTimes],
		screen[2][numTimes:] + screen[2][:numTimes],
		screen[3][numTimes:] + screen[3][:numTimes],
		screen[4][numTimes:] + screen[4][:numTimes]
	]

def clear():
	pixels.fill((0,0,0))

def fillRow(rowIndex, screen):
	global color
	startingIndex = 60 * rowIndex

	rowString = screen[rowIndex][:60]

	if rowIndex % 2 == 0:
		rowString = rowString[::-1]

	for i in range(startingIndex, startingIndex+60):
		if rowString[i % 60] == '1':
			pixels[i] = color
		else:
			pixels[i] = ((0,0,0))
		
def fillScreen(screen):
	clear()
	fillRow(0, screen)
	fillRow(1, screen)
	fillRow(2, screen)
	fillRow(3, screen)
	fillRow(4, screen)
	pixels.show() 

def add_message(message, screen):
  message_mapping = get_mapping(message)
  return [
		screen[0] + message_mapping[0],
		screen[1] + message_mapping[1],
		screen[2] + message_mapping[2],
		screen[3] + message_mapping[3],
		screen[4] + message_mapping[4]
	]

def get_rainbow_color(index):
  index = index % 256
  if index < 85:
    r = int(index * 3)
    g = int(255 - index*3)
    b = 0
  elif index < 170:
    index -= 85
    r = int(255 - index*3)
    g = 0
    b = int(index*3)
  else:
    index -= 170
    r = 0
    g = int(index*3)
    b = int(255 - index*3)
  return (g, r, b)

def kelvin_to_far(float_val):
  celcius = float_val - 273.15
  return str(int(celcius * (9/5) + 32))
 
class get_time(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    while True:
      update_clock()
      time.sleep(60)

class get_scrolling_info(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    info_to_show = 0
    while True:
      screen = get_clean_screen()
      message = ""
      if info_to_show < 5:
        message = datetime.now().strftime('%A %B %d')
        message += "th" #will need to dynamically do this
      elif info_to_show == 5:
        try:
          response = requests.get("http://api.openweathermap.org/data/2.5/weather?zip=47905,us&appid=" + get_weather_key())
          response = response.json()

          message = "weather: " + kelvin_to_far(response['main']['temp']) + " degrees, "
          for forcast in response['weather']:
            message += forcast['description'] + ", "
          message += "wind " + str(response['wind']['speed']) + " mph"
          
        except Exception as err:
          print("404 weather")
      #else:
      # might throw in some stock tickers
      # idk

      screenLock.acquire()

      screen = add_message(message, screen)
      screen = shiftLeft(61, screen)
      fillScreen(screen)

      screenLock.release()
      time.sleep(2)

      for _ in range(len(screen[0]) - 60):
        screenLock.acquire()
        screen = shiftLeft(1, screen)
        fillScreen(screen)
        screenLock.release()
        time.sleep(0.05)

      info_to_show += 1
      if info_to_show == 6:
        info_to_show = 0

      update_clock()
      time.sleep(60)

class get_messages(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    global color
    while True:
      result = my_listener.wait_for_message_on('ledWall')
      screenLock.acquire()

      screen = get_clean_screen()
      clear()

      for i in range(255):
        for j in range(num_pixels):
          pixels[j] = get_rainbow_color((j * 256 // num_pixels) + i)
        pixels.show()
        time.sleep(0.01)

      screen = add_message(result.message['text'], screen)

      passed_color = result.message['color']
      color = (passed_color['r'], passed_color['g'], passed_color['b'])
      loops = result.message['loops']

      for _ in range(loops):
        for _ in range(len(screen[0])):
          screen = shiftLeft(1, screen)
          fillScreen(screen)
          time.sleep(0.01)

      screenLock.release()

      update_clock()

def update_clock():
  global color_index, color
  screenLock.acquire()

  time_str = datetime.now().strftime('%I:%M %p')
  color_index += 1
  color = get_rainbow_color(color_index)
  screen = get_clean_screen()

  screen = add_message(time_str, screen)
  screen = shiftLeft(44, screen)
  fillScreen(screen)

  screenLock.release()


clear()
pixels.show()

color = get_rainbow_color(color_index)
screenLock = threading.Lock()

message_thread = get_messages()
scrolling_thread = get_scrolling_info()
time_thread = get_time()

message_thread.start()
scrolling_thread.start()
time_thread.start()

