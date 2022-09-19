import logging
from unicodedata import name
from discord.commands import SlashCommandGroup
from discord.ext import commands

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from aadiscordbot import __branch__, __version__
from aadiscordbot.cogs.utils.decorators import sender_is_admin
from aadiscordbot.models import Channels, Servers

logger = logging.getLogger(__name__)


class Models(commands.Cog):
    """
    Django Model Population and Maintenance
    """

    def __init__(self, bot):
        self.bot = bot

    admin_commands = SlashCommandGroup("models", "Django Model Population", guild_ids=[
                                       int(settings.DISCORD_GUILD_ID)])


    @admin_commands.command(name="populate", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    @sender_is_admin()
    async def populate_models(self, ctx):
        """
        Populates Django Models for every Channel in the Guild
        """
        await ctx.respond(f"Populating Models, this might take a while on large servers", ephemeral = True)
        try:
            Servers.objects.update_or_create(
                server = ctx.guild.id,
                name = ctx.guild.name,
            )
            server = Servers.objects.get(id=ctx.guild.id)
        except Exception as e:
            logger.error(e)

        for channel in ctx.guild.channels:
            try:
                Channels.objects.update_or_create(
                    channel = channel.id,
                    name = channel.name,
                    server = server
                    )
            except Exception as e:
                logger.error(e)

        return await ctx.respond(f"Django Models Populated for {ctx.guild.name}", ephemeral = True)

    @commands.Cog.listener("on_guild_channel_delete")
    async def on_guild_channel_delete(self, channel):
        try: 
            Channels.objects.get(channel=channel.id).update(deleted = True)
        except ObjectDoesNotExist:
            #this is fine
            pass
        except Exception as e:
            logger.error(e)


    @commands.Cog.listener("on_guild_channel_create")
    async def on_guild_channel_create(self, channel):
        try: 
            Channels.objects.create(
                channel=channel.id,
                name=channel.name,
                server=Servers.objects.get(channel.guild.id)
                )
        except Exception as e:
            logger.error(e)

    @commands.Cog.listener("on_guild_channel_update")
    async def on_guild_channel_update(self, before_channel, after_channel):
        if before_channel.name == after_channel.name:
            pass
        else:
            try:
                Channels.objects.update_or_create(
                    channel = after_channel,
                    name = after_channel.name,
                    server=Servers.objects.get(after_channel.guild.id)
                    )
            except Exception as e:
                logger.error(e)

    @commands.Cog.listener("on_guild_update")
    async def on_guild_update(self, before_guild, after_guild):
        if before_guild.name == after_guild.name:
            pass
        else:
            try:
                Channels.objects.update_or_create(
                    server = after_guild.id,
                    name = after_guild.name
                    )
            except Exception as e:
                logger.error(e)


def setup(bot):
    bot.add_cog(Models(bot))