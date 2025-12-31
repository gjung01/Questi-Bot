import os
import discord
from discord.ext import commands
from Shop import Shop
from CardPack import CardPack

#works fine
@commands.command(
        brief='- Uses an item',
        description='''
            Uses an item that you specify.

            For Example:
             - ?use [Full item name]

            *Note: The item name is not case sensitive
            *Note: Don't use brackets
        '''
)
async def use(ctx, *item: str):
    if len(item) == 2:
        userctx = f"{item[0]} {item[1]}"
    else:
        userctx = f"{item[0]}"
    if userctx.title() == "Card Pack":
        exists = Shop.use(ctx, item)
        if exists is True:
            file, embed = CardPack.open(ctx)
            await ctx.reply(file=file, embed=embed)

            path = f"./Images/{ctx.author.id}"
            for file in os.listdir(path):
                if file == "currentfavs.png":
                    pass
                else:
                    os.remove(f"{path}/{file}")
        else:
            await ctx.reply("You don't have this item")
    else:
        itemuse = Shop.use(ctx, item)
        print(itemuse)
        if itemuse is None:
            await ctx.reply(f"You have no items to use")
        elif itemuse is False:
            await ctx.reply(f"You don't have this item")
        else:
            ctxitem = itemuse
            embed = discord.Embed(color=discord.Color.from_rgb(190,130,201))
            embed.description = f"Successfully used {ctxitem}. {ctxitem}'s effects will run out in one hour from now."
            await ctx.reply(embed=embed)

async def setup(bot):
    bot.add_command(use)