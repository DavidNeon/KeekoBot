from discord import Embed, Colour
from discord.ext import commands
from __main__ import send_cmd_help
import valve.source.a2s
from socket import gethostbyname_ex

class GameServer:

    def __init__(self, bot):
        self.bot = bot

    def validate_ip(self, s):
        a = s.split('.')
        if len(a) != 4:
            return False
        for x in a:
            if not x.isdigit():
                return False
            i = int(x)
            if i < 0 or i > 255:
                return False
        return True

    @commands.command(pass_context=True,aliases=['gameserver'])
    async def getserver(self, ctx, serverip: str):
        """Get infos about a gameserver"""

        while serverip.find(":") == -1:
            print("No port specified using 27015\n")
            serverip += ":27015"

        serverc = serverip.split(":")
        if not serverc[0][0].isdigit():
            try:
                ip = gethostbyname_ex(serverc[0])[2][0]
            except:
                await self.bot.say("The specified domain is not valid")
                return
            servercheck = ip
            serverc = [str(ip), int(serverc[1])]
        else:
            servercheck = serverc[0]
            serverc = [str(serverc[0]), int(serverc[1])]
        serverc = tuple(serverc)

        if not self.validate_ip(str(servercheck)):
            await send_cmd_help(ctx)
            return

        try:
            server = valve.source.a2s.ServerQuerier(serverc)
            try:
                info = server.get_info()  # workaround for old version ADD GIT SUPPORT 26
            except:
                info = server.info()

        except valve.source.a2s.NoResponseError:
            await self.bot.say("Could not fetch Server or the Server is not on the Steam masterlist")
            return
        except:
            await self.bot.say("Unkown Error has occured")
            return

        map = info.values['map']

        if map.lower().startswith("workshop"):
            link = "https://steamcommunity.com/sharedfiles/filedetails/?id={}".format(
                map.split("/")[1])
            map = "{} [(Workshop map)]({})".format(map.split("/")[2], link)

        game = info.values['folder']
        gamemode = info.values['game']

        servername = info.values['server_name'].strip()

        playernumber = str(
            info.values['player_count'] - info.values['bot_count'])
        botnumber = str(info.values['bot_count'])
        maxplayers = str(info.values['max_players'])

        if int(info.values['vac_enabled']):
            vac = "enabled"
        else:
            vac = "disabled"
        os = str(info.values['platform'])

        em = Embed(colour=Colour.green())
        em.add_field(name="Game", value=game)
        em.add_field(name="Gamemode", value=gamemode)
        em.add_field(name="servername", value=servername, inline=False)
        em.add_field(name="IP", value=serverc[0])
        em.add_field(name="Operating System", value=os)
        em.add_field(name="VAC", value=vac)
        if botnumber != '0':
            if botnumber == "1":
                em.add_field(
                    name="Playernumber", value="{}/{}\n{} Bot".format(playernumber, maxplayers, botnumber))
            else:
                em.add_field(
                    name="Playernumber", value="{}/{}\n{} Bots".format(playernumber, maxplayers, botnumber))
        else:
            em.add_field(name="Playernumber",
                         value="{}/{}\n".format(playernumber, maxplayers))
        em.add_field(name="Map", value=map, inline=False)
        em.add_field(
            name=u"\u2063", value="[Connect](steam://connect/{})\n(starting the game over this link may result in lag)".format(serverip), inline=False)

        await self.bot.say(embed=em)


def setup(bot):
    bot.add_cog(GameServer(bot))
