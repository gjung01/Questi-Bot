from discord.ext import commands
from Member import Member

@commands.command(
        brief="- Starts the user's journey",
        description='''
            Starts a user's journey in collecting their 
            favorite cards from Questi's Collection.

            For Example:
             - ?start
        '''
)
async def start(ctx):
    member_id = ctx.author.id
    member = Member.get_member(member_id)

    if member == None:
        Member.create_member(ctx.author)
        await ctx.reply("Have fun collecting!")
    else:
        await ctx.reply(f"You have already started your journey!")

async def setup(bot):
    bot.add_command(start)