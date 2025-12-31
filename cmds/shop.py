from discord.ext import commands
from Shop import Shop
from Startup import StartupCommands

#works fine
@commands.command(
        brief='- Shows a list of items in the shop',
        description='''
            Shows a list of items in the shop.

            For Example:
             - ?shop
        '''
)
@commands.check(StartupCommands.user_in_database)
async def shop(ctx):
    embed = Shop.listshop(ctx)
    await ctx.reply(embed=embed)

async def setup(bot):
    bot.add_command(shop)