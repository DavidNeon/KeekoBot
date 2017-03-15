import os
import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO

JSON = 'data/away/away.json'


class Away:
    """Le away cog"""
    def __init__(self, bot):
        self.bot = bot
        self.data = dataIO.load_json(JSON)

    async def listener(self, message):
        tmp = {}
        for mention in message.mentions:
            tmp[mention] = True
        if message.author.id != self.bot.user.id:
            for author in tmp:
                if author.id in self.data:
                    avatar = author.avatar_url if author.avatar else author.default_avatar_url
                    if self.data[author.id]['MESSAGE']:
                        em = discord.Embed(description=self.data[author.id]['MESSAGE'], color=discord.Color.red())
                        em.set_author(name='{} is currently away for'.format(author.display_name), icon_url=avatar)
                    else:
                        em = discord.Embed(color=discord.Color.blue())
                        em.set_author(name='{} is currently away'.format(author.display_name), icon_url=avatar)
                    await self.bot.send_message(message.channel, embed=em)

    @commands.command(pass_context=True, name="away")
    async def _away(self, context, *message: str):
        """Tell the bot you're away or back."""
        author = context.message.author
        if author.id in self.data:
            del self.data[author.id]
            msg = 'You\'re now back.'
        else:
            self.data[context.message.author.id] = {}
            if len(str(message)) < 256:
                self.data[context.message.author.id]['MESSAGE'] = ' '.join(context.message.clean_content.split()[1:])
            else:
                self.data[context.message.author.id]['MESSAGE'] = True
            msg = 'You\'re now set as away.'
        dataIO.save_json(JSON, self.data)
        await self.bot.say(msg)


def check_folder():
    if not os.path.exists('data/away'):
        print('Creating data/away folder...')
        os.makedirs('data/away')


def check_file():
    f = 'data/away/away.json'
    if not dataIO.is_valid_json(f):
        dataIO.save_json(f, {})
        print('Creating default away.json...')


def setup(bot):
    check_folder()
    check_file()
    n = Away(bot)
    bot.add_listener(n.listener, 'on_message')
    bot.add_cog(n)
