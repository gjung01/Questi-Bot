import os
import re
import discord
from datetime import datetime
from discord.ext import commands
from Startup import StartupCommands
from config import oc_collection, m_collection, c_collection

#irrelevant atm
@commands.command(
        aliases= ['ic'],
        help= 'Only for development use',
        hidden=True
)
@commands.check(StartupCommands.is_it_meh)
async def imagecheck(ctx, *args):
    m_collection.update_many({}, {'$inc': {"balance": 300}})
    '''cards = c_collection.find({"theme": "EP4"})
    embed = discord.Embed()
    for card in cards:
        embed.description = f"{card['name']}"     
        embed.set_image(url=card['url'])
        await ctx.send(embed=embed)'''



async def setup(bot):
    bot.add_command(imagecheck)

