import discord
from discord.ext import commands
from random import choice
from cogs.utils.dataIO import dataIO
from os import path, makedirs

class Nep:
    "Nep Nep"

    def __init__(self, bot):
        self.bot = bot
        self.nep = dataIO.load_json('data/nep/images.json')
        self.nepsay = dataIO.load_json('data/nep/text.json')

    @commands.command(no_pm=True, aliases=["nep"])
    async def Nep(self):
        """Displays a random Nep."""

        nep = choice(self.nep)

        nepsay = choice(self.nepsay)

        if not nep or not nepsay:
            await self.bot.say('Something went wrong')
            return

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        data = discord.Embed(
            title=nepsay, colour=discord.Colour(value=colour))
        data.set_image(url=nep)

        try:
            await self.bot.say(embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

def check_folder():  # Paddo is great
    if not path.exists("data/nep"):
        print("[Nep]Creating data/nep folder...")
        makedirs("data/nep")


def check_file():
    images = ["http://i.imgur.com/13hoMVJ.jpg",
              "http://i.imgur.com/kIzXdwN.jpg",
              "http://i.imgur.com/DICh64t.jpg",
              "http://i.imgur.com/nMp3NMp.png",
              "http://i.imgur.com/MMf1YfR.png",
              "http://i.imgur.com/CGABJEs.jpg",
              "http://i.imgur.com/GRz1oCo.jpg"]

    i = "data/nep/images.json"
    if not dataIO.is_valid_json(i):
        print("[Nep]Creating default images.json...")
        dataIO.save_json(i, images)

    text = ["Nep!!11",
            "Neeeeeeepppppp",
            "Neeeeeeeeeeeeeeeeeeeeeeepppppppppp",
            "Nep Nep",
            "I ran out of Nep so here is some more",
            "Nep²",
            "Nep³"]

    l = "data/nep/text.json"
    if not dataIO.is_valid_json(l):
        print("[Nep]Creating default text.json...")
        dataIO.save_json(l, text)


def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Nep(bot))
