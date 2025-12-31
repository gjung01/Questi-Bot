import os
import random
import discord
import requests
from Card import Card
from PIL import Image
from config import c_collection, m_collection, oc_collection, imgauth

class CardPack():
    def dropcards(ctx):
        uid = Card.randomUID()
        card = CardPack.getCard()

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
        
        c_collection.update_one({'_id': card['_id']},{'$push': {'uids': uid, 'memberIDs': ctx.author.id}})
        m_collection.update_one({'memberID': ctx.author.id},{'$push': {'cards_collected': uid}})
        oc_collection.insert_one(owned_card)

        newcard = oc_collection.find_one({'uid': uid})
        print(newcard)
        return newcard

    
    def getCard():
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
    
    def newdir(ctx):
        path = f"./Images/{ctx.author.id}"
        if os.path.exists(path):
            print("path exists")
            print(path)
            return path
        else:
            print("path doesn't exist")
            path = os.mkdir(f"./Images/{ctx.author.id}")
            print(path)
            return path
    
    def save(ctx, path, uid):
        card = c_collection.find_one({'uids': uid})
        if card:
            if os.path.isfile(f"{path}/{card['name']}.png"):
                pass
            else:
                with open(f"{path}/{card['name']}{card['stars']}.png", 'wb') as f:
                    f.write(requests.get(card['url'], auth=imgauth).content)
    
    def merge(path):
        spacing = 20

        files = [img for img in os.listdir(path) if img != "currentfavs.png"]

        open = [Image.open(os.path.join(path, img)) for img in files if img != "current.png"]

        count = 0
        i = 0
        while i < len(open):
            i += 1
            count += 1
            if count >= 3:
                count = 3

        print(count)

        total_width = max(img.width * count for img in open) + spacing * (len(open) - 1)
        
        if len(open) > 3:
            max_height = max(img.height*2 for img in open)
        else:
            max_height = max(img.height  for img in open)

        merged = Image.new('RGBA', (total_width, max_height), (0, 0, 0, 0))

        count = 0
        x_offset = 10
        y_offset = 0

        for img in open:
            count += 1
            merged.paste(img, (x_offset, y_offset))
            x_offset += img.width + spacing
            if count == 3:
                x_offset = 0
                y_offset = img.height
        
        merged.save(os.path.join(path, "cardpack.png"))


    def open(ctx):
        embed = discord.Embed(color=discord.Color.from_rgb(190,130,201))
        path = CardPack.newdir(ctx)
        newcards = []

        count = random.randint(3, 5)
        i = 0
        while i != count:
            card = CardPack.dropcards(ctx)
            if card:
                newcards.append(card)
                i += 1
        print(newcards)
        for card in newcards:
            print(card['uid'])
            CardPack.save(ctx, path, card['uid'])
        CardPack.merge(path)

        file = discord.File(f"{path}/cardpack.png")
        embed.add_field(name=f"You opened your card pack. Here's what you got:", value="", inline=False)
        embed.set_image(url="attachment://cardpack.png")
        return file, embed

        