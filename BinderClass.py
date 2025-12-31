import os
import requests
import discord
from PIL import Image
from config import c_collection, m_collection, oc_collection, imgauth

class BinderClass():
    def newdir(self, ctx):
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

    def addtodb(self, ctx, cards):
        uids = []
        member = m_collection.find_one({'memberID': ctx.author.id})
        allcards = member.get('binder')
        totalcards = len(allcards)

        for newcard in cards:
            card = newcard.upper()
            if totalcards >= 6:
                print("too many cards")
                return False
            else:
                has_card = m_collection.find_one({'memberID': ctx.author.id, 'cards_collected': card})

                if has_card:
                    binder_card = m_collection.find_one({'memberID': ctx.author.id, 'binder': card})
                    if not binder_card:
                        m_collection.update_one({'memberID': ctx.author.id}, {'$push': {'binder': card}})
                        uids.append(card)
                        totalcards += 1
                    else:
                        pass
                else:
                    print(f"Card {card} not in collection. Skipping.")
        print(uids)

        for card in allcards:
            print(card)
            uids.append(card)
        print(uids)
        return uids
    
    def save(ctx, path, uid):
        card = c_collection.find_one({'uids': uid})
        if card:
            if os.path.isfile(f"{path}/{card['name']}{card['stars']}.png"):
                pass
            else:
                with open(f"{path}/{card['name']}{card['stars']}.png", 'wb') as f:
                    f.write(requests.get(card['url'], auth=imgauth).content)

    def merge(ctx, path):
        spacing = 20

        if os.path.isfile(f"{path}/currentfavs.png"):
            os.remove(f"{path}/currentfavs.png")
            
        files = [img for img in os.listdir(path)]

        open = [Image.open(os.path.join(path, img)) for img in files]

        count = 0
        i = 0
        while i < len(open):
            i += 1
            count += 1
            if count >= 3:
                count = 3

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
        
        merged.save(os.path.join(path, "currentfavs.png"))

        for file in os.listdir(path):
            if file == "currentfavs.png":
                pass
            else:
                os.remove(f"{path}/{file}")

    async def show(self, ctx):
        path = f"{self.newdir(ctx)}/currentfavs.png"
        embed = discord.Embed(color=discord.Color.from_rgb(190,130,201))
        if os.path.isfile(path):
            file = discord.File(f"{path}")
            embed.description = f"{ctx.author.display_name}'s Favorite Cards"
            embed.set_image(url="attachment://currentfavs.png")
            await ctx.reply(file=file, embed=embed)
        else:
            member = m_collection.find_one({'memberID': ctx.author.id})
            cards = member.get('binder')
            for card in cards:
                self.save(path, card)
            self.merge(path)
            file = discord.File(f"{path}/currentfavs.png")
            embed.description = f"{ctx.author.display_name}'s Favorite Cards"
            embed.set_image(url="attachment://currentfavs.png")
            await ctx.reply(file=file, embed=embed)

    async def add(self, ctx, cards):
        path = self.newdir(ctx)
        uids = self.addtodb(ctx, cards)
        if uids is False:
            await ctx.reply("Cannot add more than 6 cards to the binder")
        for card in uids:
            self.save(path, card)
        self.merge(path)
        await ctx.reply("Successfully added the cards to your binder")
    
    async def info(self, ctx):
        embed = discord.Embed(color=discord.Color.from_rgb(190,130,201))
        embed.description = f"{ctx.author.mention}'s Favorite Cards: "
        member = m_collection.find_one({'memberID': ctx.author.id})
        favcards = member.get('binder')
        if favcards == []:
            await ctx.reply("You don't have any favorite cards")
        else:
            for card in favcards:
                card = oc_collection.find_one({'uid': card})
                embed.add_field(name=f"\u2022 {card['name']} ({card['uid']})", value='', inline=False)
            await ctx.reply(embed=embed)

    async def remove(self, ctx, cards):
        path = self.newdir(ctx)
        member = m_collection.find_one({'memberID': ctx.author.id})
        bindercards = member.get('binder')
        if bindercards:
            for card in cards:
                if card.upper() in bindercards:
                    m_collection.update_one({'memberID': ctx.author.id}, {'$pull': {'binder': card.upper()}})
                else:
                    await ctx.reply("Something went wrong")
                    break
            newset = m_collection.find_one({'memberID': ctx.author.id})
            print(newset['binder'])
            for card in newset['binder']:
                self.save(path, card)
            self.merge(path)
            await ctx.reply("All mentioned card(s) removed")
        else:
            await ctx.reply("You don't have any favorite cards to remove")