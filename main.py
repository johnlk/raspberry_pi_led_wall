import time
import board
import neopixel
import threading

from helpers import get_rainbow_color, get_date_suffix
from apis import get_weather, get_chuck_norris_joke, get_useless_fact, get_trivia
from char_mappings import get_mapping 
from datetime import datetime
from key import get_pubnub_obj

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
		screen[0][numTimes:],
		screen[1][numTimes:],
		screen[2][numTimes:],
		screen[3][numTimes:],
		screen[4][numTimes:]
	]

def clear():
	pixels.fill((0,0,0))

def fillRow(rowIndex, screen):
	global color
	startingIndex = 60 * rowIndex

	rowString = screen[rowIndex][:60]

	if len(rowString) < 60:
		rowString += '0000000000000000000000000000000000000000000000000000000000000'[:(60 - len(rowString))]

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

class get_scrolling_info(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    info_to_show = 1
    while True:
      screen = get_clean_screen()
      message = ""

      if info_to_show % 5 != 0:
        message = datetime.now().strftime('%A %B %d')
        message += get_date_suffix(int(message.split(' ')[2]))
      elif info_to_show == 5:
        message = get_weather()
      elif info_to_show == 10:
        message = get_chuck_norris_joke()
      elif info_to_show == 15:
        message = get_useless_fact()
      elif info_to_show == 20:
        message = get_trivia()

      screenLock.acquire()

      screen = add_message(message, screen)
      screen = shiftLeft(61, screen)
      fillScreen(screen)

      screenLock.release()
      time.sleep(5)

      while len(screen[0]) > 0:
        screenLock.acquire()
        screen = shiftLeft(1, screen)
        fillScreen(screen)
        screenLock.release()

      info_to_show += 1
      if info_to_show == 21:
        info_to_show = 1

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

      clear()

      for i in range(255):
        for j in range(num_pixels):
          pixels[j] = get_rainbow_color((j * 256 // num_pixels) + i)
        pixels.show()

      message = result.message['text']
      passed_color = result.message['color']
      color = (passed_color['r'], passed_color['g'], passed_color['b'])
      loops = result.message['loops']

      for _ in range(loops):
        screen = get_clean_screen()
        screen = add_message(message, screen)
        while len(screen[0]) > 0:
          screen = shiftLeft(1, screen)
          fillScreen(screen)

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

if __name__ == '__main__':
  clear()
  pixels.show()

  color = get_rainbow_color(color_index)

  screenLock = threading.Lock()

  message_thread = get_messages()
  scrolling_thread = get_scrolling_info()

  message_thread.start()
  scrolling_thread.start()
