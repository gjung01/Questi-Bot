from discord.ext import commands
from config import client

#typical, works fine
@commands.command(
        brief='- Checks the latency of the bot',
        description='''
            Checks the latency of the bot.

            For Example:
             - ?ping
        '''
)
async def ping(ctx):
    await ctx.reply('Pong! {0}'.format(round(client.latency * 1000, 1)))

async def setup(bot):
    bot.add_command(ping)