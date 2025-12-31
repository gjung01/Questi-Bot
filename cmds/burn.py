import discord
from discord.ext import commands
from Card import Card

#works fine
@commands.command(
        brief= f'- Burns/Sacrifices any card for stars',
        description='''
                Burns/Sacrifices any card for stars.
                You can burn multiple cards.

                For Example:
                 - ?burn [card ID] [Card ID]

                *Note: Be sure to not include the brackets
                *Note: the ID is not case sensitive
            '''
)
async def burn(ctx, *cardID):
    embed = discord.Embed(color=discord.Color.from_rgb(190,130,201))
    star = "<a:teststar:1194398810722541598>"
    cards = list(cardID)
    print(cards)

    option, burn = Card.burnCard(ctx.author.id, cards)
    if option is True:
        embed.description = f"You gained {burn} {star} from sacrificing a card"
        await ctx.reply(embed=embed)
    elif option is False:
        embed.description = "You do not have that card or one of the cards you tried to burn does not exist"
        await ctx.reply(embed=embed)
    else:
        pass

async def setup(bot):
    bot.add_command(burn)