import discord
from discord.ext import commands
from Member import Member
from Startup import StartupCommands
from SearchButtons import SearchView
from config import c_collection

#implement this
@commands.command(
        aliases= ['wants'],
        brief='- Lists, adds, or removes any Idol you want',
        description='''
            Lists, adds, or removes any Idol you want.

            For Example:
             - ?want [list] (will show a list of names that are available)
             - ?want [add] [names with spaces after each one]
             - ?want [remove or rm] [names with spaces after each one]

            *Note: Names are not case sensitive nor is there any order that you have to list them
        '''
)
async def want(ctx, options:str, *args):
    if options.lower() in ["list", "show"]:
        pass
    elif options.lower() in ['add', 'remove', 'rm']:
        embed = Member.set_want(ctx, options, args)
        await ctx.reply(embed=embed)
    else:
        await ctx.reply("Please enter valid options")
    

async def setup(bot):
    bot.add_command(want)
