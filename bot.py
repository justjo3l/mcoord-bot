import hikari
import os

f = open('ev.txt', 'r')
token = f.readline()

bot = hikari.GatewayBot(token=os.environ.get("BOT_TOKEN"))
bot.run()