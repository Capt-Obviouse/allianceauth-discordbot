import logging
import pendulum
import traceback
import re

import discord

from discord.ext import commands
from discord.embeds import Embed
from discord.colour import Color
from django.conf import settings

from datetime import datetime
import pytz

from aadiscordbot.app_settings import get_site_url, timezones_active


logger = logging.getLogger(__name__)

class Time(commands.Cog):
    """
    A series of Time tools
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def time(self, ctx):
        """
        Returns EVE Time
        """
        await ctx.trigger_typing()

        if timezones_active():
            url = get_site_url() + "timezones/"
        else:
            url = get_site_url()

        message = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        return await ctx.send(message)

def setup(bot):
    bot.add_cog(Time(bot))