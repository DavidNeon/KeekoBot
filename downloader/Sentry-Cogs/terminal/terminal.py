from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
from cogs.utils.chat_formatting import pagify, box
from subprocess import Popen, CalledProcessError, PIPE, STDOUT
from platform import system, release
from os import name, path, makedirs


class Terminal:
    """Terminal inside Discord"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_owner()
    async def os(self):
        """Displays your current Operating System"""

        await self.bot.say(box(system() + "\n" + release(), 'Bash'))

    @commands.command(pass_context=True, aliases=["cmd", "terminal"])
    @checks.is_owner()
    async def shell(self, ctx, *, command: str):
        """Terminal inside Discord"""

        try:
            blacklist = dataIO.load_json('data/terminal/blacklist.json')
        except:
            await self.bot.say('Blacklist corrupt.\nReplacing it...\n')
            blacklist = []
            check_folder()
            check_file()

        try:
            whitelist = dataIO.load_json('data/terminal/whitelist.json')
        except:
            await self.bot.say('Whitelist corrupt.\nReplacing it...\n')
            whitelist = []
            check_folder()
            check_file()

        if command.find("&") != -1:
            command = command.split("&")[0]

        if whitelist:
            for x in whitelist:
                if command.lower().find(x.lower()) == -1:
                    await self.bot.say(box("'{}' isnt on the command whitelist".format(command), 'Prolog'))
                    return

        for x in blacklist:
            if command.lower().find(x.lower()) != -1:
                await self.bot.say(box("'{}' is on the command blacklist".format(command), 'Prolog'))
                return

        if command.lower().find("apt-get install") != -1 and command.lower().find("-y") == -1:
            command = "{} -y".format(command)

        if command.lower().find("apt-get install") != -1 or command.lower().find("pip") != -1 and command.lower().find('install') != -1:
            # Storing text in variables for easier editing
            msg = 'WARNING\nUsing apt-get or pip with this cog\nmay result in multiple problems\nranging from Red freezing up to bigger stuff\nDo you really want to continue ? (yes/no)'
            cancel = "Canceling"
            contin = "Please Wait...\nThis process can take some time based on which package is getting installed"

            await self.bot.say(box(msg, 'Prolog'))
            answer = await self.bot.wait_for_message(timeout=10, author=ctx.message.author)

            if answer.content.lower().strip() != 'yes':
                await self.bot.say(box(cancel, 'Prolog'))
                return

            await self.bot.say(box(contin, 'Prolog'))

        try:
            # getting user directory
            userdir = path.expanduser("~")

            # main command routine
            output = Popen(command, cwd=userdir, shell=True,
                           stdout=PIPE, stderr=STDOUT).communicate()[0]
            error = False
        except CalledProcessError as e:
            # error routine in the worst cases
            try:
                output = e.output
            except:
                output = b'a error has occured'
            error = True

        # Fallback incase unicode doesnt like to function, which is very unlikely
        try:
            shell = output.decode('utf_8')
        except:
            shell = output.decode('ascii')

        if shell == "" and not error:
            # in the case no output is given but no error has happened
            return

        for page in pagify(shell, shorten_by=20):
            await self.bot.say(box(page, 'Prolog'))

def check_folder():
    if not path.exists("data/terminal"):
        print("[Terminal]Creating data/terminal folder...")
        makedirs("data/terminal")

def check_file():
    whitelist = []
    f = "data/terminal/whitelist.json"
    if not dataIO.is_valid_json(f):
        print("[Terminal]Creating default whitelist.json...")
        dataIO.save_json(f, whitelist)

    blacklist = []
    k = "data/terminal/blacklist.json"
    if not dataIO.is_valid_json(k):
        print("[Terminal]Creating default blacklist.json...")
        dataIO.save_json(k, blacklist)

def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Terminal(bot))
