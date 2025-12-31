import discord
from datetime import datetime, timedelta
from Member import Member
from CardPack import CardPack
from config import m_collection, s_collection

class Shop:
    def use(ctx, item):
        if len(item) == 2:
            userctx = f"{item[0]} {item[1]}"
        else:
            userctx = f"{item[0]}"
        current_time = datetime.now()
        one_hour = current_time + timedelta(hours=1)
        member = m_collection.find_one({'memberID': ctx.author.id})
        items = member['items']
        
        if items:
            for useritem in items:
                if userctx.title() == useritem:
                    if useritem.title() in ["Cooldown Reducer", "Cooldown"]:
                        cooldown = member.get('cooldown_duration')
                        if current_time < cooldown:
                            return None
                        else:
                            print(one_hour)
                            m_collection.update_one(
                                {'memberID': ctx.author.id},
                                {'$set': {
                                    'cooldown_duration': one_hour,
                                    'cooldown': True
                                }}
                            )
                    elif useritem.title() == "Boost":
                        boost = member.get('boost_duration')
                        if current_time < boost:
                            return None
                        else:
                            m_collection.update_one(
                                {'memberID': ctx.author.id},
                                {'$set': {
                                    'boost_duration': one_hour,
                                    'boost': True
                                }}
                            )
                    elif useritem.title() == "Card Pack":
                        changes = [
                            {
                                "$set": {"items": {"$reduce": {"input": "$items", "initialValue": 
                                            {"stillLooking": True, "i": []}, "in": {"$cond": {"if": {
                                                "$and": [{"$eq": ["$$this", useritem]},"$$value.stillLooking",]},
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
                            {"$set": {"items": "$items.i"}}
                        ]
                        m_collection.update_one({'memberID': ctx.author.id}, changes)
                        return True
                    
                    changes = [
                            {
                                "$set": {"items": {"$reduce": {"input": "$items", "initialValue": 
                                            {"stillLooking": True, "i": []}, "in": {"$cond": {"if": {
                                                "$and": [{"$eq": ["$$this", useritem]},"$$value.stillLooking",]},
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
                            {"$set": {"items": "$items.i"}}
                        ]
                    m_collection.update_one({'memberID': ctx.author.id}, changes)
                    return useritem
            return False
        return False

    #seems to work fine and dandy
    def buy(ctx, buying):
        balance = Member.get_bal(ctx)
        buying = buying.title()
        print(buying)
        if buying == 'Cooldown':
            buying = 'Cooldown Reducer'
        elif buying == 'Card':
            buying = 'Card Pack'
        item = s_collection.find_one({'name': buying})
        if item is None or not item:
            return None
        elif buying.title() == "Binder":
            member = Member.get_member(ctx.author.id)
            print(member['hasBinder'])
            if member['hasBinder'] is not True:
                if balance >= item['cost']:
                    newbalance = balance - item['cost']
                    m_collection.update_one(
                        {'memberID': ctx.author.id},
                        {
                            '$set': {'balance': newbalance, 'hasBinder': True},
                        }
                    )
                else:
                    return False
                return True
            return "You already have a binder"
        else:
            if balance >= item['cost']:
                newbalance = balance - item['cost']
                m_collection.update_one(
                    {'memberID': ctx.author.id},
                    {
                        '$push': {'items': item['name']},
                        '$set': {'balance': newbalance}
                    }
                )
                return True
            else:
                return False
        
    #seems to be fine, make sure to ask to change the title later
    def listshop(ctx):
        shop = s_collection.find()
        embed = discord.Embed(title= "Questi's Wares", color=discord.Color.from_rgb(190,130,201))
        embed.description = f"Welcome to the shop!"
        star = "<a:teststar:1194398810722541598>"

        for items in shop:
            embed.add_field(name=f"__{items['name']}__", value="", inline=False)
            embed.add_field(name=f"Price: {items['cost']} {star}", value="", inline=False)
            embed.add_field(name="Description: ", value=f"{items['description']}\n\u200B", inline = False)
        return embed