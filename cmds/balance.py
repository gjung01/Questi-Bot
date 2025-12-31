import discord
from discord.ext import commands
from Member import Member

#this is completely fine
@commands.command(
        aliases = ['bal'],
        brief= '- Shows your balance',
        description = '''
            Shows your balance.

            For Example:
             - "?bal" or "?balance"
        '''
)
async def balance(ctx):
    balance = Member.get_bal(ctx)
    star = "<a:teststar:1194398810722541598>"
    embed = discord.Embed(description=f"**{ctx.author.display_name}'s Balance:** {balance} {star}", color=discord.Color.from_rgb(190,130,201))
    await ctx.reply(embed=embed)

async def setup(bot):
    bot.add_command(balance)