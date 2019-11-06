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
'011111110011111000001100011000110001100000000000000000000000',
'000011000011000110001100011000111001100000000000000000000000',
'000011000011000110001111111000111101100000000000000000000000',
'000011000011000110001100011000110111100000000000000000000000',
'011111000001111100001100011000110001100000000000000000000000'
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

#while True:
color = (0, 0, 255)
fillScreen()
	#time.sleep(1)
 
