#####KatyushaV2#####
import nextcord
from nextcord.ext import commands
from nextcord.utils import get
from nextcord import Embed, Interaction
import json
from json import loads
import asyncio
import sys
import random
import time
import datetime
from datetime import datetime
import configparser
import os
import sqlite3
import traceback

##Variables & objects##
# Bot stuff
global VERSION
VERSION = '1.0-alpha'
global DEBUG
DEBUG = True
global botID
botID = 1032489361033396244
global GUILD
GUILD = 1032040015078895616
global admin_role
admin_role = 1032040844888391730
global logChannel
logChannel = 1032107411466637332
global errorLogChan
errorLogChan = 1032107411466637332

intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

connection = sqlite3.connect('ScruffyData.db')
cur = connection.cursor()

# Remove default help command
bot.remove_command('help')

# Util funcs
def getTokens():
    config = configparser.ConfigParser()
    if not os.path.isfile("tokens.cfg"):
        print("tokens file missing. ")
        print("Creating one now.")
        config.add_section("Tokens")
        config.set("Tokens", "Bot", "null")
        with open('tokens.cfg', 'w') as configfile:
            config.write(configfile)
        print("File created.")
        print("Please edit tokens.cfg and then restart.")
        _ = input()
    else:
        config.read('tokens.cfg')
        global botToken
        botToken = config.get('Tokens', 'Bot')

def getRankObj(rank):
    bot.get_guild(GUILD).get_role(rank)
    return rank

def isAdmin(member):
    _admin = False
    for r in member.roles:
        if r.id == admin_role:
            _admin = True
    if _admin:
        return True
    else:
        return False

def getEmoji(id):
    emoji = bot.get_emoji(id)
    return emoji

def debug(msg):
    if DEBUG == True:
        print("DEBUG: " + msg)


def create_tables():
    cur.execute('''CREATE TABLE IF NOT EXISTS quoteList
                     (QUOTES TEXT)''')


def register_quote(usr, quote):
    quote = usr.name + ': "' + quote + '"'
    cur.execute("INSERT INTO quoteList (quotes) VALUES (?)", (quote,))
    connection.commit()


def load_quotes():
    print("Loading Quotes...")
    cur.execute('''SELECT * FROM quoteList''')
    global quotes
    quotes = cur.fetchall()


def get_quote():
    quote = random.choice(quotes)
    quote = str(quote)
    quote = quote.strip("('',)")
    return quote

async def errorMsg(msg, trace):
    #err = msg + "\n" + "```python" + "\n" + trace + "\n" + "```" + bot.get_guild(GUILD).get_role(admin_role).mention
    err = msg + "\n" + "```python" + "\n" + trace + "\n" + "```"
    await bot.get_guild(GUILD).get_channel(errorLogChan).send(str(err))

# Bot Events
@bot.event
async def on_ready():
    print("nextcord version: " + nextcord.__version__)
    print("Logged in as: " + bot.user.name)
    print("ID: " + str(bot.user.id))
    print("------------------")
    _activity = nextcord.Game("Quadopoly")
    await bot.change_presence(activity=_activity)


# @bot.slash_command(name="say", description="Sends a message as the bot", guild_ids=[GUILD])
# async def say(interaction: Interaction,
#     chan: nextcord.TextChannel = nextcord.SlashOption(
#         name="channel", description="Channel to send message", required=True),
#     msg: str = nextcord.SlashOption(
#         name="message", description="message you'd like to send", required=True)
# ):
#     try:
#         await chan.send(msg)
#         await interaction.response.send_message("Message sent :thumbsup:")
#     except Exception as err:
#         trace = traceback.format_exc()
#         await errorMsg("Error in say command", trace)


#Embed command
# @bot.slash_command(name="embed", description="Use discohook for help", guild_ids=[GUILD])
# async def embed(interaction: Interaction,
#                 chan: nextcord.TextChannel = nextcord.SlashOption(
#                     name="channel", description='Channel to send embed message', required=True),
#                 data: str = nextcord.SlashOption(
#                     name='data', description='json data for embed', required=True)
#                 ):
#     try:
#         embed = Embed.from_dict(json.loads(data))
#         embed.timestamp = datetime.now()
#         await chan.send(embed=embed)
#         await interaction.response.send_message("Embed Sent :thumbsup:")
#     except Exception as err:
#         trace = traceback.format_exc()
#         await errorMsg("Error in $embed function", trace)



# Message listner
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    debug("Passed cmd processing")
    if message.content.startswith("$embed "):
        # Custom embeds
        if isAdmin(message.author):
            try:
                payload = message.content.strip("$embed ")
                embed = Embed.from_dict(json.loads(payload))
                embed.timestamp = datetime.now()
                await message.channel.send(embed=embed)
                await message.delete()
            except Exception as err:
                trace = traceback.format_exc()
                await errorMsg("Error in $embed function", trace)


# Runtime, baby! Let's go!
print()
print('Getting ready...')
print('Loading RoboScruff v' + VERSION)
print('Loading cogs...')

modules = ["modules.commands.General"]

if __name__ == "__main__":
    for extension in modules:
        bot.load_extension(extension)
print("Cogs loaded")
#create_tables()
#load_quotes()
getTokens()
bot.run(botToken)