import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.chat_formatting import box,  pagify, escape_mass_mentions
from random import choice, randint
import datetime

# embeds messages so you can use them without being a coder


class EmbedSay:
    """Makes the bot say things for in embeds"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def embedsay(self, ctx, *, text: str):
        """Says Something as the bot in a embed"""

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        data = discord.Embed(description=str(
            text), colour=discord.Colour(value=colour))

        if ctx.message.author.avatar_url:
            data.set_author(name=ctx.message.author.name,
                            url=ctx.message.author.avatar_url, icon_url=ctx.message.author.avatar_url)
        else:
            data.set_author(name=ctx.message.author.name)

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission to send this")

    @commands.command(pass_context=True, no_pm=True)
    async def embedsayto(self, ctx, channel: discord.Channel, *, text: str):
        """Says Something as the bot in a embed"""

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        data = discord.Embed(description=str(
            text), colour=discord.Colour(value=colour))

        if ctx.message.author.avatar_url:
            data.set_author(name=ctx.message.author.name,
                            url=ctx.message.author.avatar_url, icon_url=ctx.message.author.avatar_url)
        else:
            data.set_author(name=ctx.message.author.name)

        try:
            await self.bot.send_message(channel, emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission to send this")

    @commands.command(pass_context=True, no_pm=True, aliases=["embedsayop"])
    @checks.admin_or_permissions(administrator=True)
    async def embedsayadmin(self, ctx, *, text: str):
        """Says Something as the bot without any trace of the message author in a embed"""

        if ctx.message.server.me.bot:
            try:
                await self.bot.delete_message(ctx.message)
            except:
                await self.bot.send_message(ctx.message.author, 'Could not delete your message on ' + ctx.message.server.name)

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        data = discord.Embed(description=str(
            text), colour=discord.Colour(value=colour))

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True, no_pm=True)
    async def embedcolorto(self, ctx, channel: discord.Channel, color: str, *, text: str):
        """Says Something as the bot in a colored embed"""

        created_at = ("Created on {}".format(
            ctx.message.timestamp.strftime("%d %b %Y %H:%M")))

        color = color.replace("#", "")
        color = color.replace("0x", "")
        color = int(color, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        data = discord.Embed(description=str(
            text), colour=discord.Colour(value=color))

        if ctx.message.author.avatar_url:
            data.set_author(name=ctx.message.author.name,
                            url=ctx.message.author.avatar_url, icon_url=ctx.message.author.avatar_url)
        else:
            data.set_author(name=ctx.message.author.name)

        try:
            await self.bot.send_message(channel, emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission to send this")

    @commands.command(pass_context=True, no_pm=True)
    async def embedcolor(self, ctx, color: str, *, text: str):
        """Says Something as the bot in a colored embed"""

        created_at = ("Created on {}".format(
            ctx.message.timestamp.strftime("%d %b %Y %H:%M")))

        color = color.replace("#", "")
        color = color.replace("0x", "")
        color = int(color, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        data = discord.Embed(description=str(
            text), colour=discord.Colour(value=color))

        if ctx.message.author.avatar_url:
            data.set_author(name=ctx.message.author.name,
                            url=ctx.message.author.avatar_url, icon_url=ctx.message.author.avatar_url)
        else:
            data.set_author(name=ctx.message.author.name)

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission to send this")

    @commands.command(pass_context=True, no_pm=True, aliases=["embedcolorop"])
    @checks.admin_or_permissions(administrator=True)
    async def embedcoloradmin(self, ctx, color: str, *, text: str):
        """Says Something as the bot without any trace of the message author in a colored embed"""

        if ctx.message.server.me.bot:
            try:
                await self.bot.delete_message(ctx.message)
            except:
                await self.bot.send_message(ctx.message.author, 'Could not delete your message on ' + ctx.message.server.name)

        color = color.replace("#", "")
        color = color.replace("0x", "")
        color = int(color, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        data = discord.Embed(description=str(
            text), colour=discord.Colour(value=color))

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission to send this")

    @commands.command(pass_context=True, no_pm=True)
    async def embedurl(self, ctx, text: str, url: str=None):
        """Embed links into a embed"""

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        if not url:
            data = discord.Embed(description=str(
                text), colour=discord.Colour(value=colour))
        else:
            if text.find("]") != -1:
                textnumber = text.find("]") + 1
                url = "({})".format(url)
                text = text[:textnumber] + url + text[textnumber:]

                data = discord.Embed(description=str(
                    text), colour=discord.Colour(value=colour))

            else:
                data = discord.Embed(description=str(
                    text), colour=discord.Colour(value=colour))

        if ctx.message.author.avatar_url:
            data.set_author(name=ctx.message.author.name,
                            url=ctx.message.author.avatar_url, icon_url=ctx.message.author.avatar_url)
        else:
            data.set_author(name=ctx.message.author.name)

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission to send this")

    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(administrator=True)
    async def embedurladmin(self, ctx, text: str, url: str=None):
        """Embed links into a embed without knowing who wrote it"""

        if ctx.message.server.me.bot:
            try:
                await self.bot.delete_message(ctx.message)
            except:
                await self.bot.send_message(ctx.message.author, 'Could not delete your message on ' + ctx.message.server.name)

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        if not url:
            data = discord.Embed(description=str(
                text), colour=discord.Colour(value=colour))
        else:
            if text.find("]") != -1:
                textnumber = text.find("]") + 1
                url = "({})".format(url)
                text = text[:textnumber] + url + text[textnumber:]

                data = discord.Embed(description=str(
                    text), colour=discord.Colour(value=colour))

            else:
                data = discord.Embed(description=str(
                    text), colour=discord.Colour(value=colour))

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission to send this")

    @commands.command(pass_context=True, no_pm=True)
    async def embedimage(self, ctx, *, image: str):
        """Embed a image as the bot"""

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        if image.lower().endswith(".gifv") or image.lower().endswith(".gif") or image.lower().endswith(".png") or image.lower().endswith(".jpeg") or image.lower().endswith(".jpg"):
            data = discord.Embed(colour=discord.Colour(value=colour))
            data.set_image(url=image)
        else:
            await self.bot.say("Not a Valid Link")
            return

        if ctx.message.author.avatar_url:
            data.set_author(name=ctx.message.author.name,
                            url=ctx.message.author.avatar_url, icon_url=ctx.message.author.avatar_url)
        else:
            data.set_author(name=ctx.message.author.name)

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission to send this")

    @commands.command(pass_context=True, no_pm=True, aliases=["embedimageop"])
    @checks.admin_or_permissions(administrator=True)
    async def embedimageadmin(self, ctx, *, image: str):
        """Embed a image as the bot without anyone knowing from who"""

        if ctx.message.server.me.bot:
            try:
                await self.bot.delete_message(ctx.message)
            except:
                await self.bot.send_message(ctx.message.author, 'Could not delete your message on ' + ctx.message.server.name)

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        if image.lower().endswith(".gifv") or image.lower().endswith(".gif") or image.lower().endswith(".png") or image.lower().endswith(".jpeg") or image.lower().endswith(".jpg"):
            data = discord.Embed(colour=discord.Colour(value=colour))
            data.set_image(url=image)
        else:
            await self.bot.say("Not a Valid Link")
            return

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")


def setup(bot):
    bot.add_cog(EmbedSay(bot))
