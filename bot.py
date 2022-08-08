from typing import OrderedDict
import hikari
import lightbulb
import os

from table2ascii import table2ascii as t2a, PresetStyle

from config import *

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from datetime import datetime

cred = credentials.Certificate(firebase_config)
databaseApp = firebase_admin.initialize_app(cred, {
    'databaseURL' : databaseUrl
})

def filter_list_by_id(outputlist, id):
    if (id is not None):
        outputlist = list(filter(lambda element: int(element[0]) == int(id), outputlist))

    return outputlist

def filter_list_by_type(outputlist, type):
    if (type is not None):
        outputlist = list(filter(lambda element: element[5] == type, outputlist))

    return outputlist

bot = lightbulb.BotApp(
    token=os.environ.get("BOT_TOKEN"), 
    default_enabled_guilds=(1005819910724780092, 970723880857649213)
    )

@bot.listen(hikari.StartedEvent)
async def print_message(event):
    print("Bot is online!")

@bot.command
@lightbulb.command("ping", "Says pong!")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(context):
    await context.respond("Pong!")

@bot.command
@lightbulb.option('description', 'Description', type=str, required=False)
@lightbulb.option('type', 'Location type', type=str, required=False)
@lightbulb.option('z', 'z coordinate', type=int, required=True)
@lightbulb.option('y', 'y coordinate', type=int, required=True)
@lightbulb.option('x', 'x coordinate', type=int, required=True)
@lightbulb.option('name', 'Location name', type=str, required=True)
@lightbulb.command('add', "Adds a location")
@lightbulb.implements(lightbulb.SlashCommand)
async def write(context):
    guildId = context.guild_id
    refIndex = db.reference(f"/{guildId}/")
    if (refIndex.get() is None):
        index = 1
    else:
        index = int(refIndex.get()['count']) + 1
    
    refIndex.update({
        'count' : f"{index}"
    })
    ref = db.reference(f"/{guildId}/coordinates/")
    ref.push({
        'created_at' : f"{datetime.now()}",
        'updated_at' : f"{None}",
        'id' : f"{index - 1}",
        'name' : f"{context.options.name}",
        'x' : f"{context.options.x}",
        'y' : f"{context.options.y}",
        'z' : f"{context.options.z}",
        'type' : f"{context.options.type}",
        'description' : f"{context.options.description}",
    })
    await context.respond(f" '{context.options.name}' has been added!")

@bot.command
@lightbulb.option('type', 'location type', type=str, required=False)
@lightbulb.option('id', 'location id', type=int, required=False)
@lightbulb.option('description', 'shows description', type=bool, required=False)
@lightbulb.command("show", "Shows locations")
@lightbulb.implements(lightbulb.SlashCommand)
async def show(context):
    guildId = context.guild_id
    ref = db.reference(f"/{guildId}/coordinates")
    data = ref.order_by_key().get()
    if data is None:
        await context.respond(f"No locations added yet!")
        return
    outputlist = []
    headerlist = ['ID', 'Name', 'X', 'Y', 'Z']
    for key, val in data.items():
        outputlist.append([str(val['id']), str(val['name']), str(val['x']), str(val['y']), str(val['z']), str(val['type']), str(val['description'])])

    outputlist = filter_list_by_id(outputlist, context.options.id)
    outputlist = filter_list_by_type(outputlist, context.options.type)

    if context.options.description is True :
        outputlist = [[each_list[i] for i in [ x for x in range(0,7) if x != 5]] for each_list in outputlist]
    else:
        outputlist = [[each_list[i] for i in range(0,5)] for each_list in outputlist]
    if (len(outputlist) == 0):
        await context.respond(f"No results found!")
        return
    else:
        if context.options.description is True :
            headerlist.append('Description')
        output = t2a(
            header = headerlist,
            body = outputlist,
            first_col_heading=True
        )
        await context.respond(f"```\n{output}\n```")
        return

@bot.command
@lightbulb.option('description', 'Description', type=str, required=False)
@lightbulb.option('type', 'Location type', type=str, required=False)
@lightbulb.option('z', 'z coordinate', type=int, required=False)
@lightbulb.option('y', 'y coordinate', type=int, required=False)
@lightbulb.option('x', 'x coordinate', type=int, required=False)
@lightbulb.option('name', 'Location name', type=str, required=False)
@lightbulb.option('id', 'Location name', type=str, required=True)
@lightbulb.command('edit', "Edits a location")
@lightbulb.implements(lightbulb.SlashCommand)
async def edit(context):
    guildId = context.guild_id
    ref = db.reference(f"/{guildId}/coordinates/")
    data = ref.order_by_key().get()
    elementkey = ""
    for key, val in data.items():
        if (int(val['id']) == int(context.options.id)):
            elementkey = str(key)
    if elementkey == "":
        await context.respond(f"No location with id {context.options.id} found!")
        return
    ref.update({
        f"{elementkey}" : {
            'created_at' : f"{data[elementkey]['created_at']}",
            'updated_at' : f"{datetime.now()}",
            'id' : f"{data[elementkey]['id']}",
            'name' : f"{context.options.name if context.options.name is not None else data[elementkey]['name']}",
            'x' : f"{context.options.x if context.options.x is not None else data[elementkey]['x']}",
            'y' : f"{context.options.y if context.options.y is not None else data[elementkey]['y']}",
            'z' : f"{context.options.z if context.options.z is not None else data[elementkey]['z']}",
            'type' : f"{context.options.type if context.options.type is not None else data[elementkey]['type']}",
            'description' : f"{context.options.description if context.options.description is not None else data[elementkey]['description']}",
        }
    })
    await context.respond(f"'Location {context.options.id}' has been updated!")

@bot.command
@lightbulb.option('id', 'Location id', type=int, required=True)
@lightbulb.command('delete', "Deletes a location")
@lightbulb.implements(lightbulb.SlashCommand)
async def delete(context):
    guildId = context.guild_id
    ref = db.reference(f"/{guildId}/coordinates/")
    data = ref.order_by_key().get()
    if data is None:
        await context.respond(f"No location with id {context.options.id} found!")
        return
    elementkey = ""
    for key, val in data.items():
        if (int(val['id']) == int(context.options.id)):
            elementkey = str(key)
    if elementkey == "":
        await context.respond(f"No location with id {context.options.id} found!")
        return
    else:
        await context.respond(f"'Location {context.options.id}' deleted!")
    ref.child(elementkey).delete()
    data = ref.order_by_key().get()
    refcount = db.reference(f"/{guildId}/")
    count = int(refcount.child('count').get())
    refcount.child('count').set(str(count - 1))
    if data is not None:
        for key, val in data.items():
            if (int(val['id']) > int(context.options.id)):
                id = int(ref.child(key).child('id').get())
                ref.child(key).child('id').set(str(id - 1))
    print(f"{context.options.id} was removed")
    

bot.run()