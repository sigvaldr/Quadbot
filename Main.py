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

##Variables & objects##
# Bot stuff
global VERSION
VERSION = '4.0-alpha.3'
global DEBUG
DEBUG = True
global iwanID
iwanID = 142076624072867840
global botID
botID = 217108205627637761
global VTAC
VTAC = 183107747217145856
global mainChannel
mainChannel = 622144477233938482
global logChannel
logChannel = 951018686867701790

intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

connection = sqlite3.connect('KatyushaData.db')
cur = connection.cursor()

welcome_message = '''
Welcome to Viking Tactical!
If you'd like to apply for full-membership, you can submit an application at <https://vikingtactical.us/apply> (It usually takes 3-5 mins to complete).
Someone will read your application and either accept or decline it. Either way, you'd receive an e-mail with the decision
(might need to check your spam folder, sometimes our emails end up in there)
'''

##########
###RANKS###

rank_martialed = 492467059830161428


# Recruit Rank
rank_rec = 469376345672253451

# Enlisted Ranks
rank_enlisted = 281727465968369665
rank_spc = 632127911033569290
rank_pfc = 492801780002979850
rank_pvt = 574741329448534038

# Sub-Command Ranks
rank_subcommand = 594343305987489808
rank_sgm = 492802360616419338
rank_sgt = 492802074140999691
rank_cpl = 751656103741489263

# Command Ranks
rank_command = 569278265857015818
rank_cpt = 183109339991506945
rank_1lt = 751656315029422170
rank_2lt = 183110198188179456

# High-Command Ranks
rank_highcommand = 577169836476465153
rank_com = 183109993686499328
rank_gen = 751656615966670889
rank_col = 632122115096838144
rank_maj = 751656507946303539
# Rank Class Lists
rankClass_enlisted = [rank_pvt, rank_pfc, rank_spc]
rankClass_subcommand = [rank_cpl, rank_sgt, rank_sgm]
rankClass_command = [rank_2lt, rank_1lt, rank_cpt]
rankClass_highcommand = [rank_maj, rank_col, rank_gen, rank_com]
##########


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


def getRankClass(member):
    _rankClass = "null"
    for r in member.roles:
        if r.id in rankClass_enlisted:
            _rankClass = "enlisted"
        if r.id in rankClass_subcommand:
            _rankClass = "subcommand"
        if r.id in rankClass_command:
            _rankClass = "command"
        if r.id in rankClass_highcommand:
            _rankClass = "highcommand"
    debug("Rank Class check: " + _rankClass)
    return _rankClass


def getRankObj(rank):
    bot.get_guild(VTAC).get_role(rank)
    return rank


def getEmoji(id):
    emoji = bot.get_emoji(id)
    return emoji


def getPromoRank(member):
    for r in member.roles:
        #_promoRank = None
        if r.id == rank_gen:
            _curRank = rank_gen
            _promoRank = None
        elif r.id == rank_col:
            _curRank = rank_col
            _promoRank = rank_gen
        elif r.id == rank_maj:
            _curRank = rank_maj
            _promoRank = rank_col
        elif r.id == rank_cpt:
            _curRank = rank_cpt
            _promoRank = rank_maj
        elif r.id == rank_1lt:
            _curRank = rank_1lt
            _promoRank = rank_cpt
        elif r.id == rank_2lt:
            _curRank = rank_2lt
            _promoRank = rank_1lt
        elif r.id == rank_sgm:
            _curRank = rank_sgm
            _promoRank = rank_2lt
        elif r.id == rank_sgt:
            _curRank = rank_sgt
            _promoRank = rank_sgm
        elif r.id == rank_cpl:
            _curRank = rank_cpl
            _promoRank = rank_sgt
        elif r.id == rank_spc:
            _curRank = rank_spc
            _promoRank = rank_cpl
        elif r.id == rank_pfc:
            _curRank = rank_pfc
            _promoRank = rank_spc
        elif r.id == rank_pvt:
            _curRank = rank_pvt
            _promoRank = rank_pfc
        elif r.id == rank_rec:
            _curRank = rank_rec
            _promoRank = rank_pvt
    _curRank = bot.get_guild(VTAC).get_role(_curRank)
    _promoRank = bot.get_guild(VTAC).get_role(_promoRank)
    return _curRank, _promoRank


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


# Bot Events
@bot.event
async def on_ready():
    print("nextcord version: " + nextcord.__version__)
    print("Logged in as: " + bot.user.name)
    print("ID: " + str(bot.user.id))
    print("------------------")
    _activity = nextcord.Game("Victory Through Comradery!")
    await bot.change_presence(activity=_activity)


@bot.event
async def on_member_join(member):
    print(member.name + " has joined the guild...assigning rank...")
    _role = bot.get_guild(VTAC).get_role(rank_rec)
    await member.add_roles(_role, reason="New member", atomic=True)
    print("Recruit rank added to " + member.display_name)
    print("Adding rank prefix...")
    _nick = "Rec. " + member.name
    await member.edit(nick=_nick, reason="New User")
    print("Added prefix to " + member.display_name)
    _chan = bot.get_guild(VTAC).get_channel(mainChannel)
    await member.send(welcome_message)

### Officer Commands ###


@bot.slash_command(name="promote", description="promote a user", guild_ids=[VTAC])
async def promote(interaction: Interaction, member: nextcord.User = nextcord.SlashOption(name="user", description="User to promote", required=True)):
    sender = interaction.user
    if getRankClass(sender) == "subcommand" or "command" or "highcommand":
        curRank, promoRank = getPromoRank(member)
        debug("\n" + "Member: " + member.display_name + "\n" + "Rank: " +
              curRank.name + "\n" + "Promo rank: " + promoRank.name)
        # Main Rank Work:
        debug("Adding Promo rank...")
        await member.add_roles(promoRank, reason="Promotion", atomic=True)
        debug("Removing old rank...")
        await member.remove_roles(curRank, reason="Promotion", atomic=True)
        if promoRank.id == rank_pvt:
            debug("New class - Enlisted")
            _rank = bot.get_guild(VTAC).get_role(rank_enlisted)
            await member.add_roles(_rank, reason="Promotion", atomic=True)
        elif promoRank.id == rank_cpl:
            debug("New Class - Subcommand")
            _rank = bot.get_guild(VTAC).get_role(rank_subcommand)
            await member.add_roles(_rank, reason="Promotion to SubCommand", atomic=True)
            _rank = bot.get_guild(VTAC).get_role(rank_enlisted)
            await member.remove_roles(_rank, reason="Promotion to SubCommand", atomic=True)
        elif promoRank.id == rank_2lt:
            debug("New Class - Command")
            _rank = bot.get_guild(VTAC).get_role(rank_command)
            await member.add_roles(_rank, reason="Promotion to Command", atomic=True)
            _rank = bot.get_guild(VTAC).get_role(rank_subcommand)
            await member.remove_roles(_rank, reason="Promotion to Command", atomic=True)
        elif promoRank.id == rank_maj:
            debug("New Class - High-Command")
            _rank = bot.get_guild(VTAC).get_role(rank_highcommand)
            await member.add_roles(_rank, reason="Promotion to High-Command", atomic=True)
            _rank = bot.get_guild(VTAC).get_role(rank_command)
            await member.remove_roles(_rank, reason="Promotion to High-Command", atomic=True)
        else:
            debug("No new class to process")
        # Set new name prefix
        if promoRank.id == rank_pvt:
            _nick = "Pvt. " + member.name
        elif promoRank.id == rank_pfc:
            _nick = "Pfc. " + member.name
        elif promoRank.id == rank_spc:
            _nick = "Spc. " + member.name
        elif promoRank.id == rank_cpl:
            _nick = "Cpl. " + member.name
        elif promoRank.id == rank_sgt:
            _nick = "Sgt. " + member.name
        elif promoRank.id == rank_sgm:
            _nick = "Sgm. " + member.name
        elif promoRank.id == rank_2lt:
            _nick = "2lt. " + member.name
        elif promoRank.id == rank_1lt:
            _nick = "LT. " + member.name
        elif promoRank.id == rank_cpt:
            _nick = "Cpt. " + member.name
        elif promoRank.id == rank_maj:
            _nick = "Maj. " + member.name
        elif promoRank.id == rank_col:
            _nick = "Col. " + member.name
        elif promoRank.id == rank_gen:
            _nick = "Gen. " + member.name
        await member.edit(nick=_nick, reason="Promotion")

        # Post to log channel
        await interaction.response.send_message("```" + member.name + " has been promoted to " + promoRank.name + "```")
        await bot.get_guild(VTAC).get_channel(logChannel).send("```" + "\n" + sender.display_name + " has promoted " + member.name + " from " + curRank.name + " to " + promoRank.name + "\n" + "```")

    else:
        await interaction.response.send_message("ERROR: UNAUTHORIZED!")


### User Commands ###
@bot.slash_command(name="addquote", description="Adds a quote to the database", guild_ids=[VTAC])
async def addquote(interaction: Interaction,
                   member: nextcord.User = nextcord.SlashOption(
                       name="user", description="who said the funny?", required=True),
                   quote: str = nextcord.SlashOption(
                       name="quote", description="the funny thing someone said", required=True)
                   ):
    register_quote(member, quote)
    await interaction.response.send_message("Quote has been added :thumbsup:")
    load_quotes()


@bot.slash_command(name="quote", description="Receive a random quote", guild_ids=[VTAC])
async def quote(interaction: Interaction):
    await interaction.response.send_message(get_quote())


# Message listner
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    debug("Passed cmd processing")
    if message.content.startswith("$embed "):
        # Custom embeds
        if getRankClass(message.author) == "highcommand":
            payload = message.content.strip("$embed ")
            embed = Embed.from_dict(json.loads(payload))
            embed.timestamp = datetime.now()
            await message.channel.send(embed=embed)
            await message.delete()


# Runtime, baby! Let's go!
print('Getting ready...')
print('Loading Katyusha v' + VERSION)
print('Loading cogs...')

modules = ["modules.commands.General", "modules.Buttons"]

if __name__ == "__main__":
    for extension in modules:
        bot.load_extension(extension)
print("Cogs loaded")
create_tables()
load_quotes()
getTokens()
bot.run(botToken)
