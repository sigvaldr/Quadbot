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
VERSION = '1.0-alpha.1'
global botID
botID = 1032489361033396244
global logChannel
logChannel = 1032107411466637332
global errorLogChan
errorLogChan = 1032107411466637332

intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

connection = sqlite3.connect('QuadBotData.db')
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
        config.add_section("Options")
        config.set("Options", "GuildID", "null")
        config.set("Options", "Debug", "off")
        with open('tokens.cfg', 'w') as configfile:
            config.write(configfile)
        print("File created.")
        print("Please edit tokens.cfg and then restart.")
        _ = input()
    else:
        config.read('tokens.cfg')
        global botToken
        botToken = config.get('Tokens', 'Bot')
        global GUILD_ID
        GUILD_ID = config.get("Options", "GuildID")
        global DEBUG
        if config.get("Options", "Debug") is "on":
            DEBUG = True
        else:
            DEBUG = False


def getRankObj(rank):
    bot.get_guild(GUILD_ID).get_role(rank)
    return rank


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
    err = msg + "\n" + "```python" + "\n" + trace + "\n" + "```" + bot.get_guild(GUILD_ID)
    await bot.get_guild(GUILD_ID).get_channel(errorLogChan).send(str(err))



# Bot Events
@bot.event
async def on_ready():
    print("nextcord version: " + nextcord.__version__)
    print("Logged in as: " + bot.user.name)
    print("ID: " + str(bot.user.id))
    print("------------------")
    _activity = nextcord.Game("Quadopoly!")
    await bot.change_presence(activity=_activity)


### User Commands ###
@bot.slash_command(name="addquote", description="Adds a quote to the database", guild_ids=[GUILD_ID])
async def addquote(interaction: Interaction,
                   member: nextcord.User = nextcord.SlashOption(
                       name="user", description="who said the funny?", required=True),
                   quote: str = nextcord.SlashOption(
                       name="quote", description="the funny thing someone said", required=True)
                   ):
    try:
        register_quote(member, quote)
        await interaction.response.send_message("Quote has been added :thumbsup:")
        load_quotes()
    except Exception as err:
                trace = traceback.format_exc()
                await errorMsg("Error in addquote command", trace)


@bot.slash_command(name="quote", description="Receive a random quote", guild_ids=[GUILD_ID])
async def quote(interaction: Interaction):
    try:
        await interaction.response.send_message(get_quote())
    except Exception as err:
                trace = traceback.format_exc()
                await errorMsg("Error in quote command", trace)


# Runtime, baby! Let's go!
print('Getting ready...')
print('Loading QuadBot v' + VERSION)
print('Loading cogs...')

modules = ["modules.commands.General"]

if __name__ == "__main__":
    for extension in modules:
        bot.load_extension(extension)
print("Cogs loaded")
create_tables()
load_quotes()
getTokens()
bot.run(botToken)
