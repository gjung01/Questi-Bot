from discord.ext import commands
from SearchButtons import SearchView
from Startup import StartupCommands

@commands.command(
        brief="- Searches through Questi's Collection",
        description='''
            Searches for all the cards specified by the user or just in general in Questi's Collection.

            For Example:
             - ?search (this provides all the cards that you can get)
             - ?search [name] [name of idol]
             - ?search [type] [Basic, Special, or Legendary]
             - ?serach [theme] [use ?want list for the current list of themes]

            *Note: Be sure not to include the brackets
            *Note: Name, type, and theme are not case sensitive nor does it matter if you add their entire name (i.e. Jiwoong's Ren or Warrior of Light)
        '''
)
async def search(ctx, *args):
    print(args)
    if len(args) >= 1:
        option = args[0]
        input = ' '.join(args[1:])
        print(input)
        view = SearchView()
        await view.send(ctx, option, input)
    else:
        option = None
        input = None
        view = SearchView()
        await view.send(ctx, option, input)

async def setup(bot):
    bot.add_command(search)