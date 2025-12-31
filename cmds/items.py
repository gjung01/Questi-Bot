import discord
from discord.ext import commands
from Member import Member

#works fine
@commands.command(
        aliases= ['item'],
        brief='- Shows items that you have',
        description='''
            Shows items that you have.

            For Example:
             - ?items or ?item
        '''
)
async def items(ctx):
    member = Member.get_member(ctx.author.id)
    items = member.get('items')
    embed = discord.Embed(title=f"{ctx.author.display_name}'s Items:", color=discord.Color.from_rgb(190,130,201))

    if items is None or not items:
        embed.description = f'You have no items'
    else:
        for item in items:
            embed.add_field(name= f"\u2022 {item}", value='', inline=False)
    await ctx.reply(embed=embed)

async def setup(bot):
    bot.add_command(items)