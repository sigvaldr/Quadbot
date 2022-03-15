from nextcord.ext import commands
from nextcord.utils import get
from nextcord import Embed, Interaction

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    VTAC = 183107747217145856

    @commands.Cog.listener()
    async def on_reaction_add():
        debug("Listening for reactions")


def setup(bot):
    bot.add_cog(ReactionRoles(bot))