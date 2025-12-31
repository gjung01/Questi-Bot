import random
import discord
import string
from datetime import datetime, timedelta
from Member import Member
from config import c_collection, m_collection, oc_collection
from discord.ui import Button

class Card:
    def getCard(uid):
        card = c_collection.find_one({'uids': uid})
        if card:
            return card
        
    def showCard(ctx, uid):
        uid = uid.upper()

        card = oc_collection.find_one(
            {'uid': uid, 'owner': ctx.author.id}
        )
        url = c_collection.find_one(
            {'uids': uid}
        )

        if card:
            cardurl = url.get('url')
            return card, cardurl
        return False
    
    def dialogue(type):
        num = random.randint(10000, 1000000)
        if type == 'good':
            pick = [
                ' got scouted by Questi!',
                ' collabed with Questi!',
                f' did a tiktok challenge and got over {num} views!',
                " sang a perfect high note in today's performance!",
                " performed amazingly at SCountdown!"
            ]
        elif type == 'bad':
            pick = [
                "'s voice cracked at a live performance.",
                " couldn't perform well with their teammates.",
                " tripped and fell in the Idol Quest recording booth.",
                " performed horribly at SCountdown.",
                " was playing video games and forgot their concert was today."
            ]
        else:
            pick = [
                ' did some charity work.',
                ' went viral for a post.',
                ' livestreamed for their oomfs.',
                ' went viral for an outfit.',
                ' performed at a local show.',
                ' went viral for a cute pose.',
                ' went to the recording booth to practice.'
            ]
        saying = random.choice(pick)
        return saying
    
    def work(memberid):
        member = m_collection.find_one({'memberID': memberid})
        nextwork = member.get('next_work')
        current_time = datetime.now()
        embed = discord.Embed(color=discord.Color.from_rgb(190,130,201))

        if current_time >= nextwork:
            star = "<a:teststar:1194398810722541598>"
            money = random.randint(1, 300)
            new_next_work = current_time + timedelta(minutes=10)
            print(new_next_work)
            if money >= 200:
                exp = random.randint(30, 49)
                dialog = Card.dialogue("good")
            elif money <= 100:
                exp = random.randint(1, 20)
                dialog = Card.dialogue("bad")
            else:
                exp = random.randint(10, 40)
                dialog = Card.dialogue("neutral")

            favCard = oc_collection.find_one({'uid': f"{member['favCard']}"})
            
            if favCard:
                level = favCard.get('level')
                if level != 50:
                    m_collection.update_one({'memberID': memberid}, {'$set': {'next_work': new_next_work}})
                    exp_limit = favCard.get('explimit')
                    checklevelup = favCard.get('exp') + exp
                    if checklevelup >= exp_limit:
                        newexp = (favCard.get('exp') + exp) - exp_limit
                        carduid = favCard.get('uid')
                        oc_collection.update_one({'uid': carduid}, {'$set': {'exp': newexp}})
                        oc_collection.update_one({'uid': carduid}, {'$inc': {'level': 1}})

                        newlimit = 50 * (favCard.get('level') + 1)
                        newlevel = favCard.get('level') + 1
                        if newlevel == 50:
                            oc_collection.update_one({'uid': carduid}, {'$set': {'exp': newlimit}})
                        oc_collection.update_one({'uid': carduid}, {'$set': {'explimit': newlimit}})
                        embed.add_field(name=f"Congrats! {favCard['name']} is now Level {newlevel}!", value="", inline=False)
                    else:
                        carduid = favCard.get('uid')
                        oc_collection.update_one({'uid': carduid}, {'$inc': {'exp': exp}})
                    embed.add_field(name=f"{favCard['name']}{dialog} They got {money}{star} and {exp}xp", value="", inline=False)
                    m_collection.update_one({'memberID': memberid}, {'$inc': {'balance': money}})
                    return True, embed
                else:
                    embed.add_field(name="Your favorite card is max level", value="", inline=False)
                    return False, embed
            else:
                    embed.add_field(name="You don't have a favorite card set!", value="", inline=False)
                    return False, embed
        else:
            cooldown = nextwork - current_time
            total_seconds = cooldown.total_seconds()
            minutes = int(total_seconds // 60)
            seconds = int(total_seconds % 60)
            embed.add_field(name=f"You have {minutes}m{seconds}s left", value="", inline=False)
            return False, embed
        
    #only burns one so far
    def burnCard(memberID, uids):
        totalstars = 0
        member = m_collection.find_one({"memberID": memberID})
        
        for card in uids:
            print(card)
            cardid = card.upper()
            card = oc_collection.find_one({'owner': memberID, 'uid': cardid})
            og_card = Card.getCard(cardid)

            if card:
                stars = card.get('stars')
                level = card.get('level')

                if stars == 1:
                    value = (stars * level) * 10
                elif stars == 2:
                    value = (stars * level) * 10
                elif stars == 3:
                    value = (stars * level) * 10
                elif stars == 4:
                    value = (stars * level) * 10
                else:
                    value = (stars * level) * 10

                if member['hasBinder'] is True:
                    if cardid in member['binder']:
                        m_collection.update_one(
                            {'memberID': memberID},
                            {'$pull': {'binder': cardid}}
                        )
                
                oc_collection.delete_one({'owner': memberID, 'uid': cardid})
                m_collection.update_one(
                    {'memberID': memberID},
                    {'$pull': {'cards_collected': cardid}}
                )
                c_collection.update_one(
                    {'_id': og_card['_id']},
                    {'$pull': {'uids': cardid}}
                )
                changes = [
                    {
                        "$set": {
                            "memberIDs": {
                                "$reduce": {
                                    "input": "$memberIDs",
                                    "initialValue": {"stillLooking": True, "i": []},
                                    "in": {
                                        "$cond": {
                                            "if": {
                                                "$and": [
                                                    {"$eq": ["$$this", memberID]},
                                                    "$$value.stillLooking",
                                                ]
                                            },
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
                c_collection.update_one({'_id': og_card['_id']}, changes)
                m_collection.update_one(
                    {'memberID': memberID},
                    {'$inc': {'balance': value}}
                )
                totalstars += value
            else:
                return False, totalstars
        return True, totalstars

    def setFavCard(ctx, uid):
        member = Member.get_member(ctx.author.id)
        uids = member.get('cards_collected')

        if uids:
            userctx = uid.upper()
            for uid in uids:
                if uid == userctx:
                    card = Card.getCard(uid)
                    if card:
                        m_collection.update_one(
                            {'memberID':  ctx.author.id},
                            {'$set': {'favCard': uid}}
                        )
                        return card, uid
        return False
    
    def cardCooldown(ctx):
        member = Member.get_member(ctx.author.id)
        next_drop = member.get('next_drop')
        current_time = datetime.now()
        normal_drop_time = current_time + timedelta(minutes=10)
        cooldown = member.get('cooldown')
        time_left = member.get('cooldown_duration')
        if current_time >= next_drop:
            if cooldown is True:
                if current_time <= time_left:
                    print("cooldown is in use")
                    reduced_drop = current_time + timedelta(minutes=5)
                    m_collection.update_one(
                        {'memberID': ctx.author.id},
                        {'$set': {
                                'next_drop': reduced_drop,
                                'cooldown': True
                            }
                        }
                    )
                    return True
                else:
                    print("cooldown is no longer active and we need to set cooldown to false")
                    m_collection.update_one(
                        {'memberID': ctx.author.id},
                        {'$set': {
                                'next_drop': normal_drop_time,
                                'cooldown': False
                            }
                        }
                    )
                    return True
            else:
                print("no cooldown was used")
                m_collection.update_one(
                        {'memberID': ctx.author.id},
                        {'$set': {
                                'next_drop': normal_drop_time
                            }
                        }
                    )
                return True
        else:
            return False

    def randomStars(type):
        if type == 'Basic':
            return random.randint(1, 2)
        elif type == 'Special':
            return random.randint(3, 4)
        else:
            return 5

    def cardBoost(ctx):
        member = Member.get_member(ctx.author.id)
        current_time = datetime.now()
        boost = member.get('boost')
        boost_duration = member.get('boost_duration')

        if boost is True:
            if current_time <= boost_duration:
                print("boost is active")
                card_types = ['Basic', 'Special', 'Legendary']
                probabilities = [0.5, 0.3, 0.2]
            else:
                print("boost was active but time passed")
                m_collection.update_one(
                    {'memberID': ctx.author.id},
                    {'$set': {'boost': False}}
                )
                card_types = ['Basic', 'Special', 'Legendary']
                probabilities = [0.7, 0.2, 0.1]

            while True:
                chosen_card_type = random.choices(card_types, weights=probabilities)[0]
                chosen_star = Card.randomStars(chosen_card_type)
                print(chosen_card_type)
                cardpool = list(c_collection.find({'type': chosen_card_type, 'stars': chosen_star}))

                if cardpool:
                    break
            randomcard = random.choice(cardpool)
            return randomcard
        
        print("no boost used")
        card_types = ['Basic', 'Special', 'Legendary']
        probabilities = [0.7, 0.2, 0.1]
        while True:
            chosen_card_type = random.choices(card_types, weights=probabilities)[0]
            chosen_star = Card.randomStars(chosen_card_type)
            print(chosen_star)
            cardpool = list(c_collection.find({'type': chosen_card_type, 'stars': chosen_star}))

            if cardpool:
                break
        randomcard = random.choice(cardpool)
        return randomcard
    
    def randomUID(length=4):
        uid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

        existing_card = oc_collection.find_one({'uid': uid})

        if existing_card:
            return Card.randomUID()
        return uid

    def randomCard(ctx):
        checktime = Card.cardCooldown(ctx)

        if checktime is True:
            card = Card.cardBoost(ctx)
            uid = Card.randomUID()
            owned_card = {
                'uid': uid,
                'owner': ctx.author.id,
                'name': card.get('name'),
                'stars': card.get("stars"),
                'type': card.get('type'),
                'theme': card.get('theme'),
                'exp': 0,
                'explimit': 50,
                'level': 1
            }

            c_collection.update_one(
                {'_id': card['_id']},
                {
                    '$push': {
                        'uids': uid,
                        'memberIDs': ctx.author.id
                    }
                }
            )
            m_collection.update_one(
                {'memberID': ctx.author.id},
                {
                    '$push': {
                        'cards_collected': uid
                    }
                }
            )
            oc_collection.insert_one(owned_card)

            card_url = card['url']

            embed = discord.Embed(color=discord.Color.from_rgb(190,130,201))
            stars = "★" * card['stars'] + "☆" * (5 - card['stars'])
            embed.description = f"**Congrats! You got:** ***[{card['theme']}]*** \n***{card['name']} ({uid}) - {stars} ***"
            embed.set_image(url= card_url)
            return embed
        return False
        
        