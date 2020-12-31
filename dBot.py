import discord   
import requests
import time as t
from datetime import datetime, time
import collections
from bs4 import BeautifulSoup
import smtplib
import asyncio
from datetime import datetime


client = discord.Client()

DOTA_LAST_VERSION = ""

async def check_dota_patch():
    global DOTA_LAST_VERSION
    while True:
        try:
            url = "https://www.dota2.com/patches/"
            # set the headers like we are a browser,
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            # download the homepage
            response = requests.get(url, headers=headers)
            # parse the downloaded homepage and grab all text, then,
            soup = BeautifulSoup(response.text, "lxml")
            
            # if the number of times the word "Google" occurs on the page is less than 1,
            if str(soup).find('PatchSelector') > -1:
                version_dropdown = soup.find("select", id="PatchSelector")
                version_list = version_dropdown.find_next_siblings("option")       
                for tag in soup.find_all(True):
                    if tag.name == "option" and "value" in tag.attrs:
                        if DOTA_LAST_VERSION == "":
                            DOTA_LAST_VERSION = tag["value"]
                            print(DOTA_LAST_VERSION)
                            print("version asetettu")
                            
                        elif tag["value"] != DOTA_LAST_VERSION:
                            channel = discord.utils.get(client.get_all_channels(), name='yleinen')
                            await channel.send("DOTES PÄTSI: https://www.dota2.com/patches/")

                            DOTA_LAST_VERSION = tag["value"]
                            print(DOTA_LAST_VERSION)

                        break

                # continue with the script,
            else:
                print("ei löydy")
                
            await asyncio.sleep(30) # task runs every 60 seconds
        except:
            print("virhe dota latauksessa")
    
@client.event #event decorator/wrapper
async def on_ready():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    print(f"Logged in as {client.user}")
    print(f"Dotes versio {DOTA_LAST_VERSION}")
    if not DOTA_LAST_VERSION:
        client.loop.create_task(check_dota_patch())
    print("looppi käynnissä")

@client.event 
async def on_message(message): #Viestin tullessa kanavalle
    try:
        print(f"{message.channel} {message.author.name} {message.content}")

        if message.author.name == "rapulaa": #hannulle responso yöllä
            now = datetime.now()
            now_time = now.time()
            if now_time <= time(7,00): 
                await message.channel.send("Hannu mee nukkumaan :sleeping: !")

        if "!sää" in message.content.lower(): # Säähaku

            msg = message.content.lower().split()

            api_address='http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q=' + msg[1]
            json_data = requests.get(api_address).json() #haetaan json rajapinnasta
            temp = json_data['main']['temp'] # parsitaan lämpötila
            weather_string = json_data['weather'][0]['main'] # parsitaan sää (Clouds, Rain, Clear)

            celc = round((temp - 273), 1) # asteet tulee kelvineinä joten muutetaan celciuksiksi
            if weather_string == "Clear":
                await message.channel.send(str(celc) + "°C :sun_with_face: ")
            elif weather_string == "Clouds":
                await message.channel.send(str(celc) + "°C :white_sun_cloud: ")
            elif weather_string == "Rain":
                await message.channel.send(str(celc) + "°C :white_sun_rain_cloud: ")
            else:
                await message.channel.send(str(celc) + "°C")
        
        if "!twitch" in message.content.lower():
            headers = {
                'Client-ID': 'asdasd',
            }

            params = (
                ('first', '10'),
            )


            game_headers = {
                'Accept': 'application/vnd.twitchtv.v5+json',
                'Client-ID': 'asdasd',
            }

            game_params = (
                ('limit', '50'),
            )

            game_response = requests.get('https://api.twitch.tv/kraken/games/top', headers=game_headers, params=game_params)
            game_data = game_response.json()
            game_name_dict = {}
            for game in game_data['top']:
                game_name_dict[str(game['game']['_id'])] = game['game']['name']
                   
            response = requests.get('https://api.twitch.tv/helix/streams', headers=headers, params=params)
            json_data = response.json()
            twitch_message = ""
            for streamer in json_data['data']:
                twitch_message += "**" + str(streamer['user_name']) + "**" + " - " + game_name_dict[streamer['game_id']] + " - " + str(streamer['viewer_count']) + "\n"

            await message.channel.send(twitch_message)
        
        if "!mee" in message.content.lower():
            await message.channel.send("!joinaa")
            t.sleep(1)
            await message.channel.send("!n meetoihin")
            t.sleep(2)
            await message.channel.send("!quittaa")
        
        if "!stats" in message.content.lower():
            messages = await message.channel.history(limit=None).flatten()
            message_dict = {}
            print(len(messages))
            for mes in messages:
                if mes.author.name in message_dict:
                    message_dict[mes.author.name] = message_dict[mes.author.name] + 1
                else:
                    message_dict[mes.author.name] = 1

            stats_message = ""
            
            message_dict = dict(collections.OrderedDict(sorted(message_dict.items(), key = lambda t: t[1], reverse=True)))
            
            for user in message_dict:
                if message_dict[user] > 9:
                    stats_message = stats_message + user + ":" + str(message_dict[user]) + "\n"
                    
            await message.channel.send(stats_message)

        if "botquit" in message.content.lower(): #botin poisto serveriltä
            await message.channel.send("Iam out!")
    except:
        print("Virhe tiedoston luvussa")
        
client.run("xxxxxxxxxxxxxxx", reconnect=True)



