import nextcord
from nextcord.ext import commands
from nextcord.utils import get
from nextcord import Embed, Interaction


class Dashboard(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(nextcord.ui.Button(label="Website", url="https://vikingtactical.us"))
        self.add_item(nextcord.ui.Button(label="Apply", url="https://vikingtactical.us/apply"))
        self.add_item(nextcord.ui.Button(label="News", url="http://blog.vikingtactical.us"))
        self.add_item(nextcord.ui.Button(label="Forums", url="https://forum.vikingtactical.us"))


class SubCommandCP(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(nextcord.ui.Button(label="News", url="http://blog.vikingtactical.us"))
        self.add_item(nextcord.ui.Button(label="Forums", url="https://forum.vikingtactical.us"))

    @nextcord.ui.button(label="Sub-Command Handbook", style=nextcord.ButtonStyle.gray)
    async def schandbook(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_message("Sorry, this link is not yet available!", ephemeral=True)



class Buttons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            # Add Dashboard buttons
            if message.content == "$dashboard":
                em = nextcord.Embed(title="<:VTAC:282478642796298241> **VTAC Dashboard** <:VTAC:282478642796298241>")
                await message.channel.send(embed=em, view=Dashboard())
                await message.delete()
            # Add ControlPanel buttons
            elif message.content == "$sc-cp":
                em = nextcord.Embed(title='__**VTAC SubCommand Control Panel**__', description="", colour=0xFF0000)
                await message.channel.send(embed=em,view=SubCommandCP())
                await message.delete()
        except Exception as err:
                trace = traceback.format_exc()
                await errorMsg("Error in on_message for buttons", trace)


def setup(bot):
    bot.add_cog(Buttons(bot))
