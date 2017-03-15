import discord
from discord.ext import commands
from .utils.chat_formatting import pagify, box
from random import choice, randint
import datetime
import time

# Custom Channelinfo command out of my info cog


class Channelinfo:
    """Shows Channel infos."""

    def __init__(self, bot):
        self.bot = bot
        if self.bot.get_cog("Info") != None:
            raise Exception("This cog does not work with my Info cog")

    @commands.command(pass_context=True, no_pm=True)
    async def channelinfo(self, ctx, *, channel: discord.Channel=None):
        """Shows channel informations"""
        author = ctx.message.channel
        server = ctx.message.server

        if not channel:
            channel = author

        userlist = [r.display_name for r in channel.voice_members]
        if not userlist:
            userlist = None
        else:
            userlist = "\n".join(userlist)

        passed = (ctx.message.timestamp - channel.created_at).days
        created_at = ("Created on {} ({} days ago!)"
                      "".format(channel.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        data = discord.Embed(description="Channel ID: " +
                             channel.id, colour=discord.Colour(value=colour))
        if "{}".format(channel.is_default) == "True":
            data.add_field(name="Default Channel", value="Yes")
        else:
            data.add_field(name="Default Channel", value="No")
        data.add_field(name="Type", value=channel.type)
        data.add_field(name="Position", value=channel.position)
        if "{}".format(channel.type) == "voice":
            if channel.user_limit != 0:
                data.add_field(
                    name="User Number", value="{}/{}".format(len(channel.voice_members), channel.user_limit))
            else:
                data.add_field(name="User Number", value="{}".format(
                    len(channel.voice_members)))
            data.add_field(name="Users", value=userlist)
            data.add_field(name="Bitrate", value=channel.bitrate)
        elif "{}".format(channel.type) == "text":
            if channel.topic != "":
                data.add_field(name="Topic", value=channel.topic, inline=False)

        data.set_footer(text=created_at)
        data.set_author(name=channel.name)

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")


def setup(bot):
    bot.add_cog(Channelinfo(bot))
