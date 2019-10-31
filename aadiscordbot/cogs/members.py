import logging
import pendulum
import traceback

import discord

from discord.ext import commands
from discord.embeds import Embed
from discord.colour import Color

#log = logging.getLogger(__name__)

from allianceauth.eveonline.models import EveCharacter

class Members(commands.Cog):
    """
    All about me!
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def info(self, ctx):
        input_name = ctx.message.content[6:]
        char = EveCharacter.objects.get(character_name=input_name)
        main = char.character_ownership.user.profile.main_character
        corp = main.corporation_ticker
        alts = char.character_ownership.user.character_ownerships.all().select_related('character').values_list('character__character_name', flat=True)

        await ctx.send(
            "**{0}** is linked to **{1} [{3}]**\n\n**All Linked Characters:** {2}".format(
                char, 
                main,
                ", ".join(alts),
                corp
            )
        )



def setup(bot):
    bot.add_cog(Members(bot))
