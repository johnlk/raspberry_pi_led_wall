import requests
from key import get_pubnub_obj, get_weather_key
from helpers import kelvin_to_far

def get_weather():
  weather = ""
  try:
    response = requests.get("http://api.openweathermap.org/data/2.5/weather?zip=47905,us&appid=" + get_weather_key())
    response = response.json()

    weather = "weather: " + kelvin_to_far(response['main']['temp']) + " degrees, "
    for forcast in response['weather']:
      weather += forcast['description'] + ", "
    weather += "wind " + str(response['wind']['speed']) + " mph"
          
  except Exception as err:
    print(err)
    print("404 weather")
    weather = "404 weather"
  return weather

def get_chuck_norris_joke():
  joke = ""
  try:
    response = requests.get("https://api.chucknorris.io/jokes/random")
    response = response.json()

    joke = "Chuck norris joke: " + response['value']
  except Exception as err:
    print(err)
    print("bad chuck norris")
    joke = "404 chuck"
  return joke

def get_useless_fact():
  fact = ""
  try:
    response = requests.get("https://uselessfacts.jsph.pl//random.json?language=en")
    response = response.json()

    fact = "useless fact: " + response['text']
  except Exception as err:
    print(err)
    print("404 useless fact")
    fact = "404 useless fact"
  return fact

def get_trivia():
  question = ""
  try:
    response = requests.get("https://opentdb.com/api.php?amount=1&difficulty=easy&type=multiple")
    response = response.json()
    response = response['results'][0]

    question = "trivia question: " + response['question']
    question += "                              "
    question += response['correct_answer']
  except Exception as err:
    print(err)
    print("404 trivia api")
    question = "404 trivia"
  return question