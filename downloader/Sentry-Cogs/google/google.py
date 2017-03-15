from google import search
from random import randint
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
from os import path, makedirs
from cogs.utils.chat_formatting import box
from __main__ import send_cmd_help

# attempt at remaking the google cog out of the now dead community repo


class GoodGoogle:
    """Get any info quickly"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json('data/google/settings.json')
        self.maxresults = self.settings['MAXRESULTS']

    @commands.command()
    async def google(self, *, searchterm: str):
        """Search things on the Internet"""

        maxsearch = self.maxresults
        # TODO make maxsearch changable

        results = []
        results.append("**Here are your search results:**\n")
        # Message you get before the result post.
        # TODO Make result message changeable

        # Generates the list of google results
        for url in search(searchterm, pause=randint(1.0, 2.0)):
            results.append("<{}>".format(url))
            maxsearch = maxsearch - 1
            if maxsearch < 1:
                break

        await self.bot.say("\n".join(results))  # Post all results

    @commands.group(pass_context=True)
    @checks.admin()
    async def googlesettings(self, ctx):
        """Settings for the google command"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @googlesettings.command(name="maxresults", pass_context=True)
    async def _googlesettings(self, ctx, maxresults: int=0):
        """Set the amount of results appearing"""

        if not self.maxresults:  # If statement incase someone removes it or sets it to 0
            self.maxresults = 3

        if maxresults == 0:
            message = box(
                "Current max search result is {}".format(self.maxresults))
            await send_cmd_help(ctx)
        elif maxresults > 10:
            await self.bot.say('`Cannot set max search results higher then 10`')
            return
        elif maxresults < 1:
            await self.bot.say('`Cannot set max search results lower then 0`')
            return
        else:
            self.maxresults = maxresults
            self.settings['MAXRESULTS'] = self.maxresults
            dataIO.save_json('data/google/settings.json', self.settings)
            message = '`Changed max search results to {} `'.format(
                self.maxresults)
        await self.bot.say(message)


def check_folder():  # Paddo is great
    if not path.exists("data/google"):
        print("[Google]Creating data/google folder...")
        makedirs("data/google")


def check_file():
    data = {}
    data['MAXRESULTS'] = 3
    f = "data/google/settings.json"
    if not dataIO.is_valid_json(f):
        print("[Google]Creating default settings.json...")
        dataIO.save_json(f, data)

def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(GoodGoogle(bot))
