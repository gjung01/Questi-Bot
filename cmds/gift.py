import discord
import asyncio
from discord.ext import commands
from Startup import StartupCommands
from Card import Card
from config import m_collection, oc_collection, c_collection

class DenyException(Exception):
    pass

#works fine but i think we'll need to change it so it calls a function instead
@commands.command(
        brief='- Gifts a card to another user',
        description='''
            Gifts a card to a user that has done ?start.
            The Giftee must either type in 'accept' or do nothing to deny the gift.

            For Example:
             - ?gift @friend [card ID]

            *Note: Be sure to double check you have @ them
            *Note: Card ID is not case sensitive
        '''
)
@commands.check(StartupCommands.user_in_database)
async def gift(ctx, user: discord.User, cardID: str):  # defaults user to None if nothing is passed

    if cardID is None:
        return await ctx.send("You didn't give a card ID")
    else:
        cardId = cardID.upper()
        card_exists = Card.getCard(cardId)
        if m_collection.find_one({'memberID': user.id}):
            if card_exists:
                if ctx.message.content.startswith('?gift'):
                    channel = ctx.channel
                    await channel.send(f"{user.mention}, {ctx.author.mention} has sent you {card_exists['name']} ({cardId})! Please respond with 'accept' to receive it or 'deny' to deny the gift.")

                    def check(m):
                        if m.content.lower() == 'accept' and m.author.id == user.id:
                            return True
                        elif m.content.lower() == 'deny' and m.author.id == user.id:
                            raise DenyException()

                    try:
                        msg = await ctx.bot.wait_for('message', check=check, timeout=60)
                        m_collection.update_one(
                            {'memberID': ctx.author.id},
                            {'$pull': {'cards_collected': cardId}}              
                        )
                        m_collection.update_one(
                            {'memberID': user.id},
                            {'$push': {'cards_collected': cardId}}
                        )
                        changes = [
                            {
                                "$set": {"memberIDs": {"$reduce": {"input": "$memberIDs", "initialValue": 
                                            {"stillLooking": True, "i": []}, "in": {"$cond": {"if": {
                                                "$and": [{"$eq": ["$$this", ctx.author.id]},"$$value.stillLooking",]},
                                                    "then": {"stillLooking": False, "i": "$$value.i"},
                                                    "else": {
                                                        "stillLooking": "$$value.stillLooking",
                                                        "i": {"$concatArrays": ["$$value.i", ["$$this"]]},
                                                    },
                                                }
                                            },
                                        }
                                    }
                                }
                            },
                            {"$set": {"memberIDs": "$memberIDs.i"}}
                        ]
                        c_collection.update_one({'_id': card_exists['_id']}, changes)
                        c_collection.update_one(
                            {'uids': cardId},
                            {
                                '$push': {'memberIDs': user.id}
                            }
                        )
                        oc_collection.update_one(
                            {'uid': cardId},
                            {'$set': {'owner': user.id}}
                        )
                        return await channel.send(f'Gift accepted by {msg.author.mention}!')
                    except asyncio.TimeoutError:
                        return await channel.send(f'Sorry {ctx.author.mention}, {user.mention} did not accept the gift.')
                    except DenyException:
                        return await channel.send(f'Sorry {ctx.author.mention}, {user.mention} denied the gift.')
            else:
                return await ctx.reply(f"Sorry {ctx.author.mention}, the card seems to not exist")
        else:
            return await ctx.reply(f"Sorry {ctx.author.mention}, the user hasn't done ?start yet")

async def setup(bot):
    bot.add_command(gift)