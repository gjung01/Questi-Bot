from discord.ext import commands
from BinderClass import BinderClass
from config import m_collection

#options for binder

@commands.command(
        aliases = ['bind'],
        brief= '- Show, add, remove, or info cards from your binder',
        description= 
            '''
                Show, add or remove cards from your binder if you have one.

                For Example:
                 - ?binder show - will show current binder image
                 - ?binder add [card ID] [card ID] [card ID] or just one card
                 - ?binder remove or ?binder rm [card ID] [card ID] [card ID] or just one card
                 - ?binder info - shows what cards are on the binder

                *Note: Be sure not to include the brackets
                *Note: The card IDs are not case sensitive
            '''
)
async def binder(ctx, options: str, *cards):
    member = m_collection.find_one({'memberID': ctx.author.id})
    if member and member.get('hasBinder', False):  # Check if member has a binder
        if options.lower() == "show":
            embed = BinderClass()
            if embed:
                await embed.show(ctx)
            else:
                await ctx.reply("You don't have any cards set")
        elif options.lower() == "add":
            if len(cards) <= 6:
                message = BinderClass()
                await message.add(ctx, cards)
            else:
                await ctx.reply("Too many cards")
        elif options.lower() == "info":
            embed = BinderClass()
            await embed.info(ctx)
        elif options.lower() in ["remove", "rm"]:
            embed = BinderClass()
            await embed.remove(ctx, cards)
        else:
            await ctx.reply("Something went wrong")
    else:
        await ctx.reply("You don't have a binder")

async def setup(bot):
    bot.add_command(binder)