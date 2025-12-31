from discord.ext import commands
from Startup import StartupCommands

#works fine
@commands.command(
        name='reload',
        help='Only for development use',
        hidden=True
)
@commands.check(StartupCommands.is_it_meh)
async def reload(ctx): 
    await StartupCommands.reload_commands()
    print('reload complete')

async def setup(bot):
    bot.add_command(reload)