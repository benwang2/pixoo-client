import conf, time

from classes.pixoo import Pixoo
from classes.platforms import Discord

ditoo = Pixoo(conf.__DEVICE_ADDRESS)
selfbot = Discord(conf.__DISCORD_TOKEN, ditoo)

ditoo.connect()

time.sleep(1)
selfbot.run()