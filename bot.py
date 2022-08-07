import hikari
import os

bot = hikari.GatewayBot(token=os.environ.get("BOT_TOKEN"))
bot.run()