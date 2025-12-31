from config import client, bot_token, m_collection, oc_collection
from Startup import StartupCommands
from Member import Member
from discord.ext import commands
import logging
import random
import discord

logging.basicConfig(filename='bot_errors.log', level=logging.ERROR)

@client.event
async def on_ready():
    await StartupCommands.load_commands()
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name='the Questi Stans addicted'))
    print("I'm Redy!")
    print("___________________")

@client.event
async def on_command(ctx):
    member_id = ctx.author.id
    member = Member.get_member(member_id)

    if member == None:
        await ctx.reply(f"Hi {ctx.author.mention}, be sure to use ?start first!")
    elif ctx.message.content == "?start":
        pass
    else:
        embed = discord.Embed(color=discord.Color.from_rgb(190,130,201))
        star = "<a:teststar:1194398810722541598>"
        options = ['yes', 'no']
        probability = [0.10, 0.90]
        choices = random.choices(options, weights=probability)[0]
        if choices == 'yes' and ctx.message.content.lower() != "?work":
            value = random.randint(1, 50)
            m_collection.update_one(
                {'memberID': member_id},
                {'$inc': {'balance': value}}
            )

            carduid = member.get('favCard')
            if carduid:
                card = oc_collection.find_one({'uid': carduid})
                if card['level'] != 50:
                    exp = random.randint(1, 20)
                    exp_limit = card.get('explimit')
                    checklevelup = card.get('exp') + exp
                    print(checklevelup >= exp_limit)
                    if checklevelup >= exp_limit:
                        newexp = (card.get('exp') + exp) - exp_limit
                        print(exp_limit)
                        print(newexp)
                        carduid = card.get('uid')
                        oc_collection.update_one({'uid': carduid}, {'$set': {'exp': newexp}})
                        oc_collection.update_one({'uid': carduid}, {'$inc': {'level': 1}})

                        newlimit = 50 * (card.get('level') + 1)
                        newlevel = card.get('level') + 1
                        if newlevel == 50:
                                oc_collection.update_one({'uid': carduid}, {'$set': {'exp': newlimit}})
                        oc_collection.update_one({'uid': carduid}, {'$set': {'explimit': newlimit}})
                        embed.add_field(name=f"Congrats! {card['name']} is now Level {newlevel}!", value="", inline=False)
                    else:
                        carduid = card.get('uid')
                        oc_collection.update_one({'uid': carduid}, {'$inc': {'exp': exp}})
                    embed.add_field(name=f"You got {value}{star} and {card['name']} got {exp}XP", value="", inline=False)
                    await ctx.reply(embed=embed)
                else:
                    pass
            else:
                pass
        else:
            pass

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply("That doesn't seem to be a command?")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("It seems you need to add some more details")
    elif isinstance(error, commands.CommandInvokeError):
        logging.error(f"Command execution error in {ctx.command}: {error}")
    else:
        logging.error(f"Unknown error in {ctx.command}: {error}")

client.run(bot_token)
