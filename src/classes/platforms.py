import conf

import discord
from discord.ext import commands, tasks

import time, requests, math, threading
from PIL import Image
from io import BytesIO

class Discord:
    client = None

    def __init__(self, __TOKEN, BT_DEVICE):
        self.__TOKEN = __TOKEN
        self.BT_DEVICE = BT_DEVICE
        self.client = discord.Client()

        self.last_message_received = math.inf
        self.showing_discord_splash = False
        
        @self.client.event
        async def on_message(message):
            if message.author == self.client.user: return    # Ignore messages from self
            if message.guild != None: return                 # Ignore messages in guild
            avatar_url = str(message.author.avatar_url_as(format='png',size=1024))
            response = requests.get(avatar_url)
            
            pfp = Image.open(BytesIO(response.content))
            self.BT_DEVICE.draw_pil_img(pfp.convert(mode="RGB"))

            self.showing_discord_splash = False
            self.last_message_received = time.time()

        @self.client.event
        async def on_ready():
            self.BT_DEVICE.draw_pic("discord.png")
            self.showing_discord_splash = True

        self.timer.start()

    @tasks.loop(seconds=1)
    async def timer(self):
        if not self.showing_discord_splash and time.time() > self.last_message_received + 3:
            self.BT_DEVICE.draw_pic("discord.png")
            self.showing_discord_splash = True

    def run(self):
        self.client.run(self.__TOKEN, bot=False)

class Socket:

    def __init__(self):
        self.last_updated = 0
        self.timer = threading.Timer(1, self.loop)

    def get_recent(self):
        try:
            resp = requests.get("http://149.28.39.36/divoom_payload")

            resp.raise_for_status()

            data = resp.json()

            if self.last_updated != 0:
                if data["type"] == "image":
                    pass

            self.last_updated =  data["last_updated"]


        except Exception as e:
            requests.post(conf.__DISCORD_WEBHOOK, json={"content":repr(e)})

    def loop(self):
        pass

    def start(self):
        self.timer.start()