import discord
from discord.ext import commands
from Card import Card
from config import client


#works fine
@commands.command(
        aliases = ['fav', 'favourite'],
        brief= "- Sets your favorite card",
        description='''
            Sets your favorite card.

            For Example:
             - ?favorite or ?fav [card ID]

            *Note: Be sure to not include the brackets
            *Note: Card ID is not case sensitive
        '''
)
async def favorite(ctx, uid):
    favcard = Card.setFavCard(ctx, uid)
    embed = discord.Embed(color=discord.Color.from_rgb(190,130,201))

    if favcard is False:
        embed.description = f"The command was given no id or there are no cards with such id"
        await ctx.reply(embed=embed)
    else:
        card, uid = favcard
        embed.description = f"You set {card['name']} ({uid}) as your favorite card!"
        await ctx.reply(embed=embed)

async def setup(bot):
    bot.add_command(favorite)
