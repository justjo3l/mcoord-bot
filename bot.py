import hikari

f = open('ev.txt', 'r')
token = f.readline()

bot = hikari.GatewayBot(token=token)
bot.run()