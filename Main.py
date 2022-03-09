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
#Bot stuff
global VERSION
VERSION = '4.0'
global DEBUG
DEBUG = True
global iwanID
iwanID = 142076624072867840
global botID
botID = 217108205627637761
global vtacGuild
vtacGuild = [183107747217145856]
global mainChannel
mainChannel= 622144477233938482

intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

connection = sqlite3.connect('KatyushaData.db')
cur = connection.cursor()
#Lists
killResponses = ["%s 'accidentally' fell in a ditch... RIP >:)", "Oh, %s did that food taste strange? Maybe it was.....*poisoned* :wink:", "I didn't mean to shoot %s, I swear the gun was unloaded!", "Hey %s, do me a favor? Put this rope around your neck and tell me if it feels uncomfortable.", "*stabs %s* heh.... *stabs again*....hehe, stabby stabby >:D", "%s fell into the ocean whilst holding an anvil...well that was stupid."]
userCommands = ["hug", "pat", "roll", "flip", "remind", "kill", "addquote", "quote", "pfp", "info", "version", "changelog"]

welcome_message='''
Welcome to Viking Tactical!
If you'd like to apply for full-membership, you can submit an application at <https://vikingtactical.us/apply> (It usually takes 3-5 mins to complete).
Someone will read your application and either accept or decline it. Either way, you'd receive an e-mail with the decision
(might need to check your spam folder, sometimes our emails end up in there)
'''

##########
###RANKS###

rank_martialed = 492467059830161428


#Recruit Rank
rank_rec = 469376345672253451

#Enlisted Ranks
rank_enlisted = 281727465968369665
rank_spc = 632127911033569290
rank_pfc = 492801780002979850
rank_pvt = 574741329448534038

#Sub-Command Ranks
rank_subcommand = 594343305987489808
rank_sgm = 492802360616419338
rank_sgt = 492802074140999691
rank_cpl = 751656103741489263

#Command Ranks
rank_command = 569278265857015818
rank_cpt = 183109339991506945
rank_1lt = 751656315029422170
rank_2lt = 183110198188179456

#High-Command Ranks
rank_highcommand = 577169836476465153
rank_com = 183109993686499328
rank_gen = 751656615966670889
rank_col = 632122115096838144
rank_maj = 751656507946303539
#Rank Class Lists
rankClass_enlisted = [rank_pvt, rank_pfc, rank_spc]
rankClass_subcommand = [rank_cpl, rank_sgt, rank_sgm]
rankClass_command = [rank_2lt, rank_1lt, rank_cpt]
rankClass_highcommand = [rank_maj, rank_col, rank_gen, rank_com]


##########



#Remove default help command
bot.remove_command('help')

#Util funcs
def getTokens():
    config = configparser.ConfigParser()
    if not os.path.isfile("tokens.cfg"):
        print("tokens file missing. ")
        print("Creating one now.")
        config.add_section("Tokens")
        config.set("Tokens", "Bot", "null")
        with open ('tokens.cfg', 'w') as configfile:
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
    bot.get_guild(vtacGuild).get_role(rank)
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
    _curRank = bot.get_guild(vtacGuild).get_role(_curRank)
    _promoRank = bot.get_guild(vtacGuild).get_role(_promoRank)
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
    
def get_changelog(ver):
    with open ('changelogs/' + ver + '.txt', 'r') as changelog:
        changelog = changelog.read()
        changelog = changelog.splitlines()
    changelog = str(changelog)
    changelog = changelog.replace("',", "\n")
    changelog = changelog.split("['],")
    return changelog

    

#Bot Events
@bot.event
async def on_ready():
    print("nextcord.py version: " + nextcord.__version__)
    print("Logged in as: " + bot.user.name)
    print("ID: " + str(bot.user.id))
    print("------------------")
    _activity = nextcord.Game("Victory Through Comradery!")
    await bot.change_presence(activity=_activity)
    
@bot.event
async def on_member_join(member):
    print(member.name + " has joined the guild...assigning rank...")
    _role = bot.get_guild(vtacGuild).get_role(rank_rec)
    await member.add_roles(_role, reason="New member", atomic=True)
    print("Recruit rank added to " + member.display_name)
    print("Adding rank prefix...")
    _nick = "Rec. " + member.name
    await member.edit(nick=_nick, reason="New User")
    print("Added prefix to " + member.display_name)
    _chan = bot.get_guild(vtacGuild).get_channel(mainChannel)
    await _chan.send(":thumbsup: " + member.mention + " has joined Viking Tactical.")
    await member.send(welcome_message)

#OPERATOR ONLY COMMANDS:
@bot.command(pass_context = True)
async def say(ctx, *, msg: str):
    if getRankClass(ctx.author) == "highcommand":
        await ctx.message.delete()
        await ctx.channel.send(msg)
    else:
        await bot.say("ERROR: UNAUTHORIZED!")

@bot.command(pass_context = True)
async def purge(ctx):
    if getRankClass(ctx.author) == "highcommand":
        await ctx.send("UNDERSTOOD, COMMANDER. I WILL DESTROY THE EVIDENCE!")
        await asyncio.sleep(4)
        await ctx.channel.purge(limit=100, bulk=True)
        await ctx.send("CHANNEL HAS BEEN PURGED, SIR!")
    else:
        await ctx.send("ERROR: UNAUTHORIZED")
        
@bot.command(pass_context = True)
async def getBot(ctx):
    if getRankClass(ctx.author) == "highcommand":
        await ctx.message.delete()
        await ctx.author.send("Invite link:\nhttps://discordapp.com/api/oauth2/authorize?client_id=217108205627637761&scope=bot&permissions=1")
    else:
        await ctx.author("ERROR: UNAUTHORIZED!")
        
@bot.command(pass_context = True)
async def terminate(ctx):
    if getRankClass(ctx.author) == "highcommand":
        await ctx.author.send("Affirmative. Terminating now...")
        sys.exit()
    else:
        await ctx.author.send("ERROR: UNAUTHORIZED!")
        
#OFFICER COMMANDS


@bot.command(pass_context = True)
async def martial(ctx, member: nextcord.Member=None, *, reason: str=None):
    if getRankClass(ctx.author) == "command" or "highcommand":
        if member == None or reason == None:
            await ctx.channel.send("Please provide a member and reason.")
        else:
            await ctx.message.delete()
            _waitmsg = await ctx.channel.send("Creating paperwork for new Court-Martial, please wait...")
            await newCourtMartial(ctx.message.author, member, reason)
            await _waitmsg.delete()
    else:
        await ctx.channel.send("ERROR: UNAUTHORIZED!")


@bot.command(pass_context = True)
async def promote(ctx, *, member: nextcord.Member = None):
    if getRankClass(ctx.author) == "subcommand" or "command" or "highcommand":
        curRank, promoRank = getPromoRank(member)
        debug("\n" + "Member: " + member.display_name + "\n" + "Rank: " + curRank.name + "\n" + "Promo rank: " + promoRank.name)
        #Main Rank Work:
        debug("Adding Promo rank...")
        await member.add_roles(promoRank, reason="Promotion", atomic=True)
        debug("Removing old rank...")
        await member.remove_roles(curRank, reason="Promotion", atomic=True)
        if promoRank.id == rank_pvt:
            debug("New class - Enlisted")
            _rank = bot.get_guild(vtacGuild).get_role(rank_enlisted)
            await member.add_roles(_rank, reason="Promotion", atomic=True)
        elif promoRank.id == rank_cpl:
            debug("New Class - Subcommand")
            _rank = bot.get_guild(vtacGuild).get_role(rank_subcommand)
            await member.add_roles(_rank, reason="Promotion to SubCommand", atomic=True)
            _rank = bot.get_guild(vtacGuild).get_role(rank_enlisted)
            await member.remove_roles(_rank, reason="Promotion to SubCommand", atomic=True)
        elif promoRank.id == rank_2lt:
            debug("New Class - Command")
            _rank = bot.get_guild(vtacGuild).get_role(rank_command)
            await member.add_roles(_rank, reason="Promotion to Command", atomic=True)
            _rank = bot.get_guild(vtacGuild).get_role(rank_subcommand)
            await member.remove_roles(_rank, reason="Promotion to Command", atomic=True)
        elif promoRank.id == rank_maj:
            debug("New Class - High-Command")
            _rank = bot.get_guild(vtacGuild).get_role(rank_highcommand)
            await member.add_roles(_rank, reason="Promotion to High-Command", atomic=True)
            _rank = bot.get_guild(vtacGuild).get_role(rank_command)
            await member.remove_roles(_rank, reason="Promotion to High-Command", atomic=True)
        else:
            debug("No new class to process")
        #Set new name prefix
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

        #Post to log channel
        await bot.get_guild(vtacGuild).get_channel(logChannel).send("```" + "\n" + ctx.author.display_name + " has promoted " + member.name + " from " + curRank.name + " to " + promoRank.name + "\n" + "```")

    else:
        await ctx.channel.send("ERROR: UNAUTHORIZED!")
        
#USER COMMANDS
@bot.command(pass_context = True)
async def help(ctx):
    usrCmds = '\n'.join("!" + str(c) for c in userCommands)
    em = nextcord.Embed(title='', description=usrCmds, colour=0xFF0000)
    em.set_author(name='Commands:', icon_url=bot.user.avatar_url)
    await ctx.message.channel.send(embed=em)

@bot.command()
async def version(ctx):
    await ctx.channel.send("I am currently on version " + VERSION)
    
@bot.command(pass_context = True)
async def changelog(ctx, ver: str=VERSION):
    await ctx.channel.send("Changelog for version " + ver + ":")
    for x in get_changelog(ver):
        await ctx.channel.send("`" + str(x).strip("['],").replace("'", "") + "`")
    
@bot.command(pass_context = True)
async def hug(ctx):
    hug = random.choice([True, False])
    if hug == True:
        await ctx.channel.send(ctx.message.author.mention + ": :hugging:")
    else:
        await ctx.channel.send(ctx.message.author.mention + ": You don't deserve a hug, cyka.")
        
@bot.command()
async def roll(ctx, *, dice : str=None):
    if dice == None:
        await ctx.channel.send('Format has to be in NdN!')
        return
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.channel.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.channel.send(result)
      
@bot.command(pass_context = True)
async def flip(ctx):
    await ctx.channel.send("Okay, I'll flip it!")
    await asyncio.sleep(3)
    if random.choice([True, False]) == True:
        await ctx.channel.send(ctx.message.author.mention + ": the result is.......**HEADS**!")
    else:
        await ctx.channel.send(ctx.message.author.mention + ": the result is.......**TAILS**!")
      
@bot.group(pass_context = True)
async def remind(ctx, time: str = "0", *, reminder: str="null"):
    time = int(time)
    if time == 0 or reminder == "null":
        await ctx.channel.send("Correct Usage: !remind <time in minutes> <reminder>")
        await ctx.channel.send("Example: !remind 5 Tell me how reminders work")
        return
    else:
        await ctx.message.delete()
        await ctx.channel.send("Okay, " + ctx.message.author.mention + "! I'll remind you :smile:")
        await asyncio.sleep(time * 60)
        await ctx.message.author.send("You wanted me to remind you: " + reminder)
        
@bot.command(pass_context = True)
async def kill (ctx, *, member: nextcord.Member = None):
    if member is None:
        await ctx.channel.send(ctx.message.author.mention + ": I need a target!")
        return

    if member.id == botID and ctx.message.author.id == iwanID:
        await ctx.channel.send(ctx.message.author.mention + ": C-Commander, p-please...I'm useful! Please don't terminate me! :cry:")
    elif member.id == ctx.message.author.id:
        await ctx.channel.send(ctx.message.author.mention + ": Why do you want me to kill you? :open_mouth:")
    elif member.id == botID:
        await ctx.channel.send(ctx.message.author.mention + ": Hah! Don't get cocky kid, I could end you in less than a minute! :dagger:")
    elif member.id == iwanID:
        await ctx.channel.send(ctx.message.author.mention + ": Kill the Commander? I could never!")
    else:
        random.seed(time.time())
        choice = killResponses[random.randrange(len(killResponses))] % member.mention
        await ctx.channel.send(ctx.message.author.mention + ": " + choice)
      
@bot.command(pass_context = True)
async def pat(ctx, *, member: nextcord.Member = None):
    if member is None:
        await ctx.channel.send("Aww, does somebody need a headpat? I'll pat you, " + ctx.message.author.mention)
        await ctx.channel.send(file=nextcord.File("img/headpat.gif"))
    else:
        await ctx.channel.send(ctx.message.author.mention + " pats " + member.mention)
        await ctx.channel.send(file=nextcord.File("img/headpat.gif"))
       
@bot.command()
async def quote(ctx):
    await ctx.channel.send(get_quote())
    
@bot.command(pass_context = True)
async def poke(ctx, member: nextcord.Member=None):
    if member==None:
        await ctx.channel.send("I can't poke nobody! Try mentioning someone with `@`, like this\n`!poke @Iwan`")
        return
    else:
        await ctx.channel.send(ctx.message.author.mention + " just poked " + member.mention + "!")
        await ctx.channel.send(file=nextcord.File("img/poke.gif"))




    
# Slash Command testing
@bot.slash_command(name = "test", description= "This is a test slash command!", guild_ids=vtacGuild)
async def test(interaction: Interaction):
    await interaction.response.send_message("Hello World")

@bot.slash_command(name="pfp", description="Returns the profile picture of the user", guild_ids=vtacGuild)
async def pfp(interaction: Interaction,user:nextcord.User = nextcord.SlashOption(name="user",description="Returns the profile picture of the user",required=True)):
    await interaction.response.send_message(user.display_name + "'s profile picture:\n" + str(user.avatar.url))

@bot.slash_command(name="info", description="Returns info of a user", guild_ids=vtacGuild)
async def info(interaction: Interaction, user:nextcord.User = nextcord.SlashOption(name="user", description="Returns info of a user", required=True)):
    info = "Joined guild on: " + user.joined_at.strftime("%A %B %d, %Y at %I:%M%p") + "\n"
    info = info + "Account created on: " + user.created_at.strftime("%A %B %d, %Y at %I:%M%p")
    em = nextcord.Embed(title='', description=info, colour=0xFF0000)
    em.set_author(name=user.display_name, icon_url=user.avatar.url)
    await interaction.response.send_message(embed=em)

@bot.slash_command(name="addquote", description="Adds a quote to the database", guild_ids=vtacGuild)
async def addquote(interaction: Interaction, 
user: nextcord.User = nextcord.SlashOption(name="user", description="who said the funny?", required=True),
quote: str = nextcord.SlashOption(name="quote", description="the funny thing someone said", required=True)
):
    register_quote(user, quote)
    await interaction.response.send_message("Quote has been added :thumbsup:")
    load_quotes()

@bot.slash_command(name="quote", description="Receive a random quote", guild_ids=vtacGuild)
async def quote(interaction: Interaction):
    await interaction.response.send_message(get_quote())

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    debug("Passed cmd processing")
    if message.content.startswith("$embed "):
        #Custom embeds
        if getRankClass(message.author) == "highcommand":
            payload = message.content.strip("$embed ")
            embed = Embed.from_dict(json.loads(payload))
            embed.timestamp = datetime.now()
            await message.channel.send(embed=embed)
            await message.delete()


    
#Runtime, baby! Let's go!    
print ('Getting ready...')
print('Loading Katyusha v' + VERSION)
create_tables()
load_quotes()
getTokens()
bot.run(botToken)