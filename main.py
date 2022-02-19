from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from configparser import ConfigParser
from pip._vendor import requests
import json

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
        tempCelsius = (tempKelvin - 273.15 )
        tempFahrenheit = (tempKelvin - 273.15) * 9 / 5 + 32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        wind = json['wind']
        final = (city, country, tempCelsius, tempFahrenheit, icon, weather, wind)
        return final
    else:
        return  None



def search():
    city = cityText.get()
    weather = get_weather(city)
    if weather:
        locationLabel['text'] = '{},{}'.format(weather[0], weather[1])
        image['file'] = 'weather_icons/{}.png'.format(weather[4])
        tempLabelC['text'] = '{:.2f}°C'.format(weather[2])
        tempLabelF['text'] = '{:.2f}°F'.format(weather[3])
        weatherLabel['text'] = weather[5]
        windLabel['text'] = weather[6]
    else:
        messagebox.showerror('Error', 'Cannot Find City').format(city)




root = Tk()
root.title("Weather App")
root.geometry("350x350")



cityText = StringVar()
cityEntry = Entry(root, textvariable=cityText)
cityEntry.pack(pady=10)

searchButton = Button(root, text="Search Weather", width=12, command=search)
searchButton.pack()

locationLabel = Label(root, text='', font=('bold', 20))
locationLabel.pack()

image = PhotoImage(file='')

imageLabel = Label(root, image=image, background="gray")
imageLabel.pack()

tempLabelC = Label(root, text='', font=20)
tempLabelC.pack()

tempLabelF = Label(root, text='', font=20)
tempLabelF.pack()

weatherLabel = Label(root, text='')
weatherLabel.pack()

windLabel = Label(root, text='')
windLabel.pack()

root.mainloop()
