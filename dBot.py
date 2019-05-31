# id 576075997556768768
# token XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# permission 67648
#https://discordapp.com/api/oauth2/authorize?client_id=576075997556768768&scope=bot&permissions=67648

import discord   
import requests
from datetime import datetime, time

client = discord.Client()

@client.event #event decorator/wrapper
async def on_ready():
    print(f"Logged in as {client.user}")    

@client.event 
async def on_message(message): #Viestin tullessa kanavalle
    print(f"{message.channel} {message.author.name} {message.content}")

    if message.author.name == "rapulaa": #hannulle responso yöllä
        now = datetime.now()
        now_time = now.time()
        if now_time <= time(7,00): 
            print(now_time)
            await message.channel.send("Hannu mee nukkumaan :sleeping:")

    if "sää" in message.content.lower(): # Säähaku

        msg = message.content.lower().split()

        api_address='http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q=' + msg[1]
        json_data = requests.get(api_address).json() #haetaan json rajapinnasta
        temp = json_data['main']['temp'] # parsitaan lämpötila
        weather_string = json_data['weather'][0]['main'] # parsitaan sää (Clouds, Rain, Clear)

        celc = round((temp - 273), 1) # asteet tulee kelvineinä joten muutetaan celciuksiksi
        if weather_string == "Clear":
            await message.channel.send(str(celc) + "°C :sun_with_face:")
        elif weather_string == "Clouds":
            await message.channel.send(str(celc) + "°C :white_sun_cloud: ")
        elif weather_string == "Rain":
            await message.channel.send(str(celc) + "°C :white_sun_rain_cloud: ")
        else:
            await message.channel.send(str(celc) + "°C")

    if "botquit" in message.content.lower(): #botin poisto serveriltä
        await message.channel.send("Iam out!")

client.run("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

