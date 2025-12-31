import discord
from discord.ext import commands
from Member import Member
from Card import Card

#works fine
@commands.command(
        aliases= ['pf'],
        brief="- Shows your or someone else's profile",
        description='''
            Shows a profile which includes:
             - Discord nickname or name
             - Balance
             - Bio
             - Wants
             - Favorite card
            (If you have not set some of these they will say otherwise)

            For Example:
             - ?profile or ?pf
             - ?profile @user or ?pf @user

            *Note: Be sure to double check you have @ them
        '''
)
async def profile(ctx, user: discord.User = None):
    if user is not None:
        member_id = user.id
        member = Member.get_member(member_id)
        fav = Card.getCard(member['favCard'])
        star = "<a:teststar:1194398810722541598>"
        embed = discord.Embed(title=f"{user.display_name}'s Profile", color=discord.Color.from_rgb(190,130,201))
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name="Balance", value=f"{member['balance']} {star}", inline=False)
        embed.add_field(name="About Me:", value=member['bio'] or "Not set", inline=False)
        embed.add_field(name="I Want: ",  value='', inline=False)
        if member['wants']:
            joined = ", ".join(member['wants'])
            embed.add_field(name=f"\u2022 {joined}", value="", inline=False)
        else:
            embed.add_field(name="\u2022 Nothing Yet", value='', inline=False)

        if fav is None or fav == "":
            embed.description = f"({user.display_name} has yet to decide on their favorite card)"
        else:
            favimg = fav.get('url')
            embed.set_image(url=favimg)
        await ctx.reply(embed=embed)
    else:
        member_id = ctx.author.id
        member = Member.get_member(member_id)
        fav = Card.getCard(member['favCard'])
        star = "<a:teststar:1194398810722541598>"
        embed = discord.Embed(title=f"{ctx.author.display_name}'s Profile", color=discord.Color.from_rgb(190,130,201))
        embed.set_thumbnail(url=ctx.author.display_avatar)
        embed.add_field(name="Balance", value=f"{member['balance']} {star}", inline=False)
        embed.add_field(name="About Me:", value=member['bio'] or "Not set", inline=False)
        embed.add_field(name="I Want: ",  value='', inline=False)
        if member['wants']:
            joined = ", ".join(member['wants'])
            embed.add_field(name=f"\u2022 {joined}", value="", inline=False)
        else:
            embed.add_field(name="\u2022 Nothing Yet", value='', inline=False)

        if fav is None or fav == "":
            embed.description = f"({ctx.author.display_name} has yet to decide on their favorite card)"
        else:
            favimg = fav.get('url')
            embed.set_image(url=favimg)
        await ctx.reply(embed=embed)

async def setup(bot):
    bot.add_command(profile)