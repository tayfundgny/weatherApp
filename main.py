from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

configFile = 'config.ini'
config = ConfigParser()
config.read(configFile)
api_key = config['api_key']['key']

def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        # (City,Country,temp_celsius, temp_fahrenheit, icon, weather)
        city = json['name']
        country = json['sys']['country']
        tempKelvin = json['main']['temp']
        tempCelsius = tempKelvin - 273.15
        tempFahrenheit = (tempKelvin - 273.15) * 9 / 5 + 32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        final = (city, country, tempCelsius, tempFahrenheit, icon, weather)
        return final
    else:
        return  None



def search():
    city = cityText.get()
    weather = get_weather(city)
    if weather:
        locationLabel['text'] = '{},{}'.format(weather[0], weather[1])
        image['bitmap'] = 'weather_icons/{}.png'.format(weather[4])
        tempLabel['text'] = '{:.2f°C},{:.2f°F}'.format(weather[2], weather[3])
        weatherLabel['text'] = weather[5]
    else:
        messagebox.showerror('Error', 'Cannot Find City').format(city)




root = Tk()
root.title("Weather App")
root.geometry("700x350")



cityText = StringVar()
cityEntry = Entry(root, textvariable = cityText)
cityEntry.pack()

searchButton = Button(root, text="Search Weather", width=12, command=search)
searchButton.pack()

locationLabel = Label(root, text='', font=('bold', 20))
locationLabel.pack()

image = Label(root, bitmap='')
image.pack()

tempLabel = Label(root, text='')
tempLabel.pack()

weatherLabel = Label(root, text='')
weatherLabel.pack()

root.mainloop()