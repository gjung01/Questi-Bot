import discord
from discord.ext import commands
from InventoryButton import CardInventoryView
from config import m_collection

#works fine
@commands.command(
        aliases= ['inv'],
        brief="- Shows your or someone else's inventory",
        description='''
            Shows your or someone else's card inventory.
            You can also make detailed searches.

            For Example:
             - ?inv
             - ?inv [name, type, theme] [your search]
             - ?inv @user
             - ?inv @user [name, type, theme] [your search]

            *Note: Be sure to double check you have @ them
        '''
)
async def inventory(ctx, *args):
    user = None
    type = None
    search = None

    if args:
        try:
            user = await commands.UserConverter().convert(ctx, args[0])
            args = args[1:]
        except commands.UserNotFound:
            pass

        if args:
            if args[0].lower() in ["name", "type", "theme"] and len(args) > 1:
                type = args[0].lower()
                search = ' '.join(args[1:])
            else:
                await ctx.reply("Invalid Arguments")
                return

    if not user:
        user = ctx.author

    view = CardInventoryView(user, ctx, type, search)
    await view.send(ctx)

async def setup(bot):
    bot.add_command(inventory)