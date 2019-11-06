import time
import board
import neopixel
 
pixel_pin = board.D18
 
num_pixels = 60 * 5
 
ORDER = neopixel.GRB
 
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.05, auto_write=False,
                           pixel_order=ORDER)

color = (255, 0, 0)
words = [
'0000000000000000000000001111111001111100000110001100011000110',
'0000000000000000000000000001100001100011000110001100011100110',
'0000000000000000000000000001100001100011000111111100011110110',
'0000000000000000000000000001100001100011000110001100011011110',
'0000000000000000000000001111100000111110000110001100011000110'
]

def shiftLeft(numTimes):
	global words
	words = [
		words[0][numTimes:] + words[0][:numTimes],
		words[1][numTimes:] + words[1][:numTimes],
		words[2][numTimes:] + words[2][:numTimes],
		words[3][numTimes:] + words[3][:numTimes],
		words[4][numTimes:] + words[4][:numTimes]
	]

def clear():
	pixels.fill((0,0,0))

def fillRow(rowIndex):
	startingIndex = 60 * rowIndex

	rowString = words[rowIndex]

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

while True:
	color = (0, 0, 255)
	shiftLeft(1)
	fillScreen()
	time.sleep(0.1)
 
