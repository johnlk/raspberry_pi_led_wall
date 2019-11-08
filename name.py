import time
import board
import neopixel
from char_mappings import get_mapping 

pixel_pin = board.D18
 
num_pixels = 60 * 5
 
ORDER = neopixel.GRB
 
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.05, auto_write=False,
                           pixel_order=ORDER)

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

clear()
pixels.show()
pixels.fill((234, 105, 5))
pixels.show()
time.sleep(2)

add_message('we can handle this like reasonable sexy teenagers')

while True:
	color = (195, 6, 49)
	shiftLeft(1)
	fillScreen()
	time.sleep(0.01)


