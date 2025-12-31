import random
from discord.ext import commands
from config import m_collection
from Card import Card

@commands.command(
        brief='- Lets your favorite idol work',
        description='''
            Your favorite idol is forced to work to provide money for you while gaining experience.

            For Example:
             - ?work
        '''
)
async def work(ctx):
    worked, embed = Card.work(ctx.author.id)
    if worked is True:
        await ctx.reply(embed=embed)
    elif worked is False:
        await ctx.reply(embed=embed)
    else:
        await ctx.reply("Something went wrong")


async def setup(bot):
    bot.add_command(work)