import discord
from discord.ext import commands
from Card import Card

#works fine
@commands.command(
        brief='- Shows card details',
        description='''
            Shows the details of a card that you specify

            For Example:
             - ?show [card ID]

            *Note: Card ID is not case sensitive
        '''
)
async def show(ctx, cardID):
    card = Card.showCard(ctx, cardID)
    embed = discord.Embed(color=discord.Color.from_rgb(190,130,201))
    
    if card is False:
        await ctx.reply(f"You don't own that card")
    else:
        membercard, url = card
        embed.set_image(url=url)
        embed.add_field(name="Name: ", value=f"{membercard['name']}", inline=True)
        embed.add_field(name="Type: ", value=f"{membercard['type']}", inline=True)
        embed.add_field(name="Theme: ", value=f"{membercard['theme']}", inline=True)
        embed.add_field(name="Level: ", value=f"{membercard['level']}", inline=True)
        embed.add_field(name="Exp: ", value=f"{membercard['exp']} / {membercard['explimit']}", inline=True)
        await ctx.reply(embed=embed)

async def setup(bot):
    bot.add_command(show)

