import discord
from discord.ext import commands
from Shop import Shop

#works fine
@commands.command(
        brief='- Buy an item from the shop',
        description='''
                Buy an item from the shop.
                
                For Example:
                 - ?buy [Full item name without the brackets]

                *Note: Be sure to not include the brackets
                *Note: The item name is not case sensitive
            '''
)
async def buy(ctx, *item: str):
    if len(item) == 2:
        item = f"{item[0]} {item[1]}"
    else:
        item = f"{item[0]}"
    item = Shop.buy(ctx, item)
    embed = discord.Embed(color=discord.Color.from_rgb(190,130,201))

    if item is None:
        embed.description = f"The item you're buying does not exist"
        await ctx.reply(embed=embed)
    elif item is False:
        embed.description = f"You cannot afford this item"
        await ctx.reply(embed=embed)
    elif item is True:
        embed.description = f"Successfully bought! If you bought a binder you will be able to check with ?binder info."
        await ctx.reply(embed=embed)
    else:
        embed.description = item
        await ctx.reply(embed=embed)

async def setup(bot):
    bot.add_command(buy)

