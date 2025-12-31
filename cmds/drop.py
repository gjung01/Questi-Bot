from datetime import datetime
from discord.ext import commands
from Card import Card
from Member import Member

#works fine
@commands.command(
        brief="- Drops a card with random rarity",
        description= '''
            Drops a card with random rarity.

            For Example:
             - ?drop

            *Note: Using the Boost item increases the chances of a rarer card
        '''
)
async def drop(ctx):
    card = Card.randomCard(ctx)
    member = Member.get_member(ctx.author.id)
    current_time = datetime.now()
    next_drop = member.get('next_drop')
    cooldown = next_drop - current_time

    total_seconds = cooldown.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)

    if card is False:
        await ctx.reply(f"You have {minutes}m{seconds}s left")
    else:
        await ctx.reply(embed=card)

async def setup(bot):
    bot.add_command(drop)