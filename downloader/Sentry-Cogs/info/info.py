import discord
from discord.ext import commands
from random import choice, randint
import datetime
import time

# This is basicly the *info commands from general with more info.


class Info:
    """Shows Client, Channel and Server infos to the user."""

    def __init__(self, bot):
        self.bot = bot
        if self.bot.get_cog("Channelinfo") != None:
            raise Exception("This cog does not work with my Channelinfo cog")

        elif self.bot.get_cog("General") != None:
            raise Exception("This cog does not work with the General cog")

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

    @commands.command(pass_context=True, no_pm=True)
    async def userinfo(self, ctx, user: discord.Member=None):
        """Shows users's informations"""
        author = ctx.message.author
        server = ctx.message.server

        if not user:
            user = author

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        roles = [x.name for x in user.roles if x.name != "@everyone"]

        joined_at = user.joined_at
        since_created = (ctx.message.timestamp - user.created_at).days
        since_joined = (ctx.message.timestamp - joined_at).days
        user_joined = joined_at.strftime("%d %b %Y %H:%M")
        user_created = user.created_at.strftime("%d %b %Y %H:%M")

        created_on = "{}\n({} days ago)".format(user_created, since_created)
        joined_on = "{}\n({} days ago)".format(user_joined, since_joined)

        statususer = "{}".format(user.status)

        if user .avatar_url.find("gif") != -1:
            nitro = True
        else:
            nitro = False

        if roles:
            roles = sorted(roles, key=[x.name for x in server.role_hierarchy
                                       if x.name != "@everyone"].index)
            roles = ", ".join(roles)
        else:
            roles = "None"

        if user.bot == False:
            data = discord.Embed(description="User ID : " +
                                 user.id, colour=user.colour)
        elif author.is_afk == True:
            data = discord.Embed(description="AFK | User ID : " +
                                 user.id, colour=user.colour)
        else:
            data = discord.Embed(
                description="**Bot** | User ID : " + user.id, colour=user.colour)

        data.add_field(name="Joined Discord on", value=created_on)
        data.add_field(name="Joined this server on", value=joined_on)
        data.add_field(name="Status", value=statususer)
        data.add_field(name="Nitro", value=nitro)
        data.add_field(name="Serverwide Deafened", value=str(user.deaf))
        data.add_field(name="Serverwide Muted", value=str(user.mute))
        if user.voice_channel:
            data.add_field(name="In Voicechannel", value=user.voice_channel)
        if user.nick:
            data.add_field(name="Nickname", value=str(user.nick))
        if user.game:
            data.add_field(name="Playing", value=str(user.game))
        data.add_field(name="Roles", value=roles, inline=False)

        if user.avatar_url:
            data.set_author(name="{} {}".format(
                user.name, user.discriminator), url=user.avatar_url)
            data.set_thumbnail(url=user.avatar_url)
        else:
            data.set_author(name="{} {}".format(
                user.name, user.discriminator), url=user.default_avatar_url)
            data.set_thumbnail(url=user.default_avatar_url)

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(aliases=["getglobaluser"], pass_context=True)
    async def globaluserinfo(self, ctx, id: str):
        """Gives you the info of ANY user."""

        if not self.bot.user.bot:
            await self.bot.say("``This is not a bot account\n"
                               "It only works with bot accounts")
            return

        if not id.isdigit():
            await self.bot.say("You can only use IDs from a user\nExample: `137268543874924544` (ID of Sentry)")
            return

        try:
            user = await self.bot.get_user_info(id)
        except discord.errors.NotFound:
            await self.bot.say("No user with the id `{}` found.".format(id))
            return
        except:
            await self.bot.say("An error has occured.")
            return

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        user_created = user.created_at.strftime("%d %b %Y %H:%M")
        since_created = (ctx.message.timestamp - user.created_at).days

        created_on = "{}\n({} days ago)".format(user_created, since_created)

        if user .avatar_url.find("gif") != -1:
            nitro = True
        else:
            nitro = False

        if user.bot == False:
            data = discord.Embed(description="User ID : " +
                                 user.id, colour=colour)
        else:
            data = discord.Embed(
                description="**Bot** | User ID : " + user.id, colour=colour)

        data.add_field(name="Joined Discord on", value=created_on)
        data.add_field(name="Nitro", value=nitro)

        if user.avatar_url:
            data.set_author(name="{} {}".format(
                user.name, user.discriminator), url=user.avatar_url)
            data.set_thumbnail(url=user.avatar_url)
        else:
            data.set_author(name="{} {}".format(
                user.name, user.discriminator), url=user.default_avatar_url)
            data.set_thumbnail(url=user.default_avatar_url)

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True, no_pm=True)
    async def serverinfo(self, ctx, server=None):
        """Shows server's informations"""

        server = self.bot.get_server(server)
        if server is None:
            server = ctx.message.server

        if server.splash_url:
            splash = server.splash_url
            splashsmall = splash
            while not splashsmall.endswith("?"):
                if not splashsmall:
                    await self.bot.say("a error with splash screens happend.\nTell Sentry")
                splashsmall = splashsmall[:-1]
            splashsmall = splashsmall + "size=128"

        online = len([m.status for m in server.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle])
        total_users = len(server.members)
        normal_users = len([r for r in server.members if r.bot is False])
        bot_users = len([r for r in server.members if r.bot is True])
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len(server.channels) - text_channels
        passed = (ctx.message.timestamp - server.created_at).days
        created_at = ("Created on {} ({} days ago!)"
                      "".format(server.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        x = -1
        emojis = []
        while x < len([r for r in ctx.message.server.emojis]) - 1:
            x = x + 1
            emojis.append("<:{}:{}>".format([r.name for r in ctx.message.server.emojis][
                          x], [r.id for r in ctx.message.server.emojis][x]))

        emojis = ", ".join(emojis)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        vip = "vip" in "\n".join(server.features).lower()

        colour = [r.color for r in server.role_hierarchy][0]

        data = discord.Embed(
            description="Server ID: " + server.id,
            colour=colour)

        data.add_field(name="Region", value=str(server.region))
        data.add_field(name="Roles", value=len(server.roles))

        if bot_users != 0:
            data.add_field(name="Users", value="{}/{}\n"
                                               "*{} Humans\n"
                                               "{} Bots*".format(online, total_users, normal_users, bot_users))

        else:  # Incase of the cog being used by a selfbot on a server without bots
            data.add_field(
                name="Users", value="{}/{}".format(online, total_users))

        data.add_field(name="Channels", value="{}\n{} Text Channels\n{} Voice Channels".format(
            len(server.channels), text_channels, voice_channels))
        data.add_field(name="Emojis", value=len(server.emojis))
        if server.afk_channel:
            data.add_field(name="Afk Channel", value=str(server.afk_channel))
            data.add_field(name="Afk Timeout",
                           value="{} ms".format(server.afk_timeout))

        data.add_field(name="Verification Level",
                       value=str(server.verification_level))

        if server.owner:
            data.add_field(name="Owner", value="{}#{}".format(
                server.owner.display_name, server.owner.discriminator))

        else:
            # Incase of discordpy failing again
            data.add_field(
                name="Owner", value="Could not be found.\nPossible error in API")

        data.add_field(name="Vip", value=vip)

        if server.unavailable:
            data.add_field(name="Unavailable", value=str(server.unavailable))

        if server.splash_url:
            data.add_field(name="Splash screen",
                           value="[Full Image]({})".format(splash), inline=False)
            data.set_image(url=splashsmall)

        data.set_footer(text=created_at)

        if server.icon_url:
            data.set_author(name=server.name, url=server.icon_url)
            data.set_thumbnail(url=server.icon_url)
        else:
            data.set_author(name=server.name)

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True, no_pm=True)
    async def getserverinvite(self, ctx):
        """Get a invite to the current server"""

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        try:
            invite = await self.bot.create_invite(ctx.message.server)
        except:
            await self.bot.say("I do not have the `Create Instant Invite` Permission")
            return

        server = ctx.message.server

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        data = discord.Embed(
            colour=discord.Colour(value=colour))
        data.add_field(name=server.name, value=invite, inline=False)

        if server.icon_url:
            data.set_thumbnail(url=server.icon_url)

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True, no_pm=True, aliases=["getbotinvite"])
    async def getinvite(self, ctx):
        """Get a invite to the bot"""

        if not self.bot.user.bot:
            await self.bot.say("`This is not a bot account.\n"
                               "use the build in join command instead`")
            return

        invite = self.bot.oauth_url
        server = ctx.message.server

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        data = discord.Embed(colour=server.me.colour)
        data.add_field(name="{} #{}".format(
            server.me.name, server.me.discriminator), value=invite, inline=False)

        if server.me.avatar_url:
            data.set_thumbnail(url=server.me.avatar_url)
        else:
            data.set_thumbnail(url=server.me.default_avatar_url)

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")


def setup(bot):
    bot.add_cog(Info(bot))
