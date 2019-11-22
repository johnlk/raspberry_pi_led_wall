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

def get_date_suffix(day_of_month):
  if day_of_month == 1 or day_of_month == 21 or day_of_month == 31:
    return "st"
  elif day_of_month == 2 or day_of_month == 22:
    return "nd"
  elif day_of_month == 3 or day_of_month == 23:
    return "rd"
  return "th"
