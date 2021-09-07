import conf

import discord
from structs.pixoo import Pixoo

from PIL import Image
from io import BytesIO
import time, requests

client = discord.Client()
ditoo = Pixoo(conf.__DEVICE_ADDRESS)
ditoo.connect()

@client.event
async def on_message(message):
    if message.author == client.user: return    # Ignore messages from self
    if message.guild != None: return            # Ignore messages in guilds
    if message.author.is_blocked(): return      # Ignore blocked users
    avatar_url = str(message.author.avatar_url_as(format='png',size=1024))
    response = requests.get(avatar_url)
    
    pfp = Image.open(BytesIO(response.content))
    ditoo.draw_pil_img(pfp.convert(mode="RGB"))
    time.sleep(5)
    ditoo.draw_pic("discord.png")

@client.event
async def on_ready():
    time.sleep(1)
    ditoo.draw_pic("discord.png")


client.run(conf.__DISCORD_TOKEN, bot=False)