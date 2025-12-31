import discord
import re
from datetime import datetime, timedelta
from config import m_collection, c_collection

class Member:
    def create_member(member):

        current_time = datetime.now()
        duration = current_time - timedelta(minutes=1)

        member_data = {
            "memberID": member.id,
            "name": member.name,
            "balance": 0,
            "items": [],
            "bio": "",
            "cards_collected": [],
            "favCard": "",
            "wants": [],
            "binder": [],
            "hasBinder": False,
            "next_drop": current_time,
            "next_work": current_time,
            "cooldown_duration": duration,
            "boost_duration": duration,
            "boost": False,
            "cooldown": False
        }
        m_collection.insert_one(member_data)

    def get_member(member_id):
        return m_collection.find_one({"memberID": member_id})
    
    def set_desc(ctx, desc):
        if desc is None or desc == '':
            pass
        else:
            m_collection.update_one(
                {'memberID': ctx.author.id},
                {'$set': {'bio': desc}}
            )
            return desc

    def get_bal(ctx):
        member = Member.get_member(ctx.author.id)
        balance = member.get('balance')
        return balance
    
    #change this to set a list of people to add and the theme
    def set_want(ctx, options, args):
        embed = discord.Embed(color=discord.Color.from_rgb(190,130,201))
        if options:
            if options and args:
                if options.lower() == "add":
                    adding = []
                    i = 0
                    while i < len(args):
                        print(args[i])
                        if args[i].lower() == "jy":
                            exists = c_collection.find_one({"name": "JY"})
                            adding.append(exists['name'])
                            i += 1
                        elif args[i].lower() == "warrior":
                            if i + 3 <= len(args) and args[i+1].lower() and args[i+2].lower() in ["of", "light"]:
                                exists = c_collection.find_one({"name": "Warrior of Light"})
                                adding.append(exists['name'])
                                i += 3
                            else:
                                exists = c_collection.find_one({"name": "Warrior of Light"})
                                adding.append(exists['name'])
                                i += 1
                        elif args[i].lower() in ["jiwoong's", "jiwoong"]:
                            if i + 2 <= len(args) and args[i+1].lower() in ["ren"]:
                                exists = c_collection.find_one({"name": "Jiwoong's Ren"})
                                adding.append(exists['name'])
                                i += 2
                                print("the first was used")
                            else:
                                exists = c_collection.find_one({"name": "Jiwoong's Ren"})
                                adding.append(exists['name'])
                                i += 1
                                print("the second was used")
                        else:
                            exists = c_collection.find_one({"name": f"{args[i].title()}"})
                            adding.append(exists['name'])
                            i += 1
                    
                    member = m_collection.find_one({'memberID': ctx.author.id})
                    currentwants = member.get('wants')
                    for name in adding:
                        if name in currentwants:
                            pass
                        else:
                            m_collection.update_one({'memberID': ctx.author.id}, {'$push': {'wants': name}})
                    embed.add_field(name="Successfully added. Please check your profile", value="", inline=False)
                    return embed

                elif options.lower() in ["remove", "rm"]:
                    adding = []
                    i = 0
                    while i < len(args):
                        print(args[i])
                        if args[i].lower() == "jy":
                            exists = c_collection.find_one({"name": "JY"})
                            adding.append(exists['name'])
                            i += 1
                        elif args[i].lower() == "warrior":
                            if i + 3 <= len(args) and args[i+1].lower() and args[i+2].lower() in ["of", "light"]:
                                exists = c_collection.find_one({"name": "Warrior of Light"})
                                adding.append(exists['name'])
                                i += 3
                            else:
                                exists = c_collection.find_one({"name": "Warrior of Light"})
                                adding.append(exists['name'])
                                i += 1
                        elif args[i].lower() in ["jiwoong's", "jiwoong"]:
                            if i + 2 <= len(args) and args[i+1].lower() in ["ren"]:
                                exists = c_collection.find_one({"name": "Jiwoong's Ren"})
                                adding.append(exists['name'])
                                i += 2
                            else:
                                exists = c_collection.find_one({"name": "Jiwoong's Ren"})
                                adding.append(exists['name'])
                                i += 1
                        else:
                            exists = c_collection.find_one({"name": f"{args[i].title()}"})
                            adding.append(exists['name'])
                            i += 1
                    
                    member = m_collection.find_one({'memberID': ctx.author.id})
                    currentwants = member.get('wants')
                    for name in adding:
                        if name in currentwants:
                            m_collection.update_one({'memberID': ctx.author.id}, {'$pull': {'wants': name}})
                    embed.add_field(name="Successfully removed. Please check your profile", value="", inline=False)
                    return embed
                else:
                    embed.add_field(name="Something went wrong", value="", inline=False)
                    return embed
            else:
                embed.add_field(name="Something went wrong", value="", inline=False)
                return embed
        else:
            embed.add_field(name="Something went wrong", value="", inline=False)
            return embed