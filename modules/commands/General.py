import nextcord
from nextcord.ext import commands
from nextcord.utils import get
from nextcord import Embed, Interaction
import random

class General(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    VTAC = 183107747217145856


    @nextcord.slash_command(name="pfp", description="Returns the profile picture of the user", guild_ids=[VTAC])
    async def pfp(self, interaction:Interaction,member:nextcord.User = nextcord.SlashOption(name="user",description="Returns the profile picture of the user",required=True)):
        await interaction.response.send_message(member.display_name + "'s profile picture:\n" + str(member.avatar.url))

    @nextcord.slash_command(name="info", description="Returns info of a user", guild_ids=[VTAC])
    async def info(self, interaction:Interaction, member:nextcord.User = nextcord.SlashOption(name="user", description="Returns info of a user", required=True)):
        info = "Joined guild on: " + member.joined_at.strftime("%A %B %d, %Y at %I:%M%p") + "\n"
        info = info + "Account created on: " + member.created_at.strftime("%A %B %d, %Y at %I:%M%p")
        em = nextcord.Embed(title='', description=info, colour=0xFF0000)
        em.set_author(name=member.display_name, icon_url=member.avatar.url)
        await interaction.response.send_message(embed=em)

    @nextcord.slash_command(name="poke", description="Poke someone!", guild_ids=[VTAC])
    async def poke(self, interaction:Interaction,member:nextcord.User = nextcord.SlashOption(name="user",description="person to poke",required=True)):
        await interaction.response.send_message(interaction.user.mention + " just poked " + member.mention + "!", file=nextcord.File("img/poke.gif"))

    @nextcord.slash_command(name="flip", description="Flip a coin", guild_ids=[VTAC])
    async def flip(self, interaction:Interaction):
        if random.choice([True, False]) == True:
            await interaction.response.send_message("Heads!")
        else:
            await interaction.response.send_message("Tails!")

    @nextcord.slash_command(name="hug", description="A hug, perhaps?", guild_ids=[VTAC])
    async def hug(self, interaction:Interaction):
        if random.choice([True, False]) == True:
            await interaction.response.send_message(":hugging:")
        else:
            await interaction.response.send_message("No hug for you, cyka")

    @nextcord.slash_command(name="roll", description="Roll n amount of n-sided dice", guild_ids=[VTAC])
    async def roll(self, interaction:Interaction,
    dice: str = nextcord.SlashOption(name="ndn", description="NdN format only", required=True)
    ):
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await interaction.response.send_message('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await interaction.response.send_message(result)


def setup(bot):
    bot.add_cog(General(bot))