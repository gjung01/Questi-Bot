import discord
import asyncio
import re
from config import m_collection, oc_collection, client

class CardInventoryView(discord.ui.View):
    def __init__(self, user, ctx, type, search, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author = ctx.author
        self.user = user
        self.type = type
        self.search = search
        self.current_page = 1
        self.cards_per_page = 5
        self.timeout = 180

    async def send(self, ctx):
        data = self.get_cards(self.user.id)
        self.message = await ctx.reply(mention_author=True, embed=self.create_embed(data), view=self)
        self.timeout_task = ctx.bot.loop.create_task(self.timeout_task())

    async def timeout_task(self):
        await asyncio.sleep(self.timeout)
        await self.stop()

    def stop(self):
        self.clear_items()

    def create_embed(self, data):
        embed = discord.Embed(color=discord.Color.from_rgb(190,130,201))
        embed.set_footer(text="*Note: If the page doesn't change, it means it has reached the end")
        embed.description = f"{self.user.display_name}'s Inventory"
        for card in data:
            embed.add_field(name=f"\u2022 **{card['name']} - [{card['theme']}] - ({card['uid']})**", value=f"", inline=False)
        return embed
        
    async def update_message(self, data):
        await self.message.edit(embed=self.create_embed(data), view=self)


    @discord.ui.button(label="|<", style=discord.ButtonStyle.gray)
    async def first_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.author.id:
            await interaction.response.defer()
            self.current_page = 1
            data = self.get_cards(self.user.id)
            await self.update_message(data)
        else:
            pass

    @discord.ui.button(label="<", style=discord.ButtonStyle.gray)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.author.id:
            await interaction.response.defer()
            if self.current_page == 1:
                self.current_page = 1
            else:
                self.current_page -= 1
            data = self.get_cards(self.user.id)
            await self.update_message(data)
        else:
            pass

    @discord.ui.button(label=">", style=discord.ButtonStyle.gray)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.author.id:
            await interaction.response.defer()
            total_pages = self.total_pages(self.user.id)
            if self.current_page == total_pages:
                self.current_page = total_pages
            else:
                self.current_page += 1
            data = self.get_cards(self.user.id)
            await self.update_message(data)
        else:
            pass

    @discord.ui.button(label=">|", style=discord.ButtonStyle.gray)
    async def last_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.author.id:
            await interaction.response.defer()
            total_pages = self.total_pages(self.user.id)
            self.current_page = total_pages
            data = self.get_cards(self.user.id)
            await self.update_message(data)
        else:
            pass

    def total_pages(self, memberID):
        if self.type is not None:
            if self.search is None:
                return 0
            else:
                if self.type.lower() == "name":
                    search_query = self.search.lower()
                    if search_query == "jy":
                        search_query = "JY"
                    elif search_query in ["warrior of light", "warrior"]:
                        search_query = "Warrior of Light"
                    elif search_query in ["jiwoong's", "jiwoong's ren", "jiwoong"]:
                        search_query = "Jiwoong's Ren"
                    else:
                        search_query = self.search.title()

                    totalcards = oc_collection.count_documents({"owner": memberID, "name": f"{search_query}"})
                    print(totalcards)
                    return (totalcards + self.cards_per_page - 1) // self.cards_per_page

                elif self.type.lower() == "theme":
                    regex_pattern = re.compile(re.escape(self.search), re.IGNORECASE)
                    query = {"owner": memberID, "theme": {'$regex': regex_pattern}}
                    totalcards = oc_collection.count_documents(query)
                    return (totalcards + self.cards_per_page - 1) // self.cards_per_page
                elif self.type.lower() == "type":
                    totalcards = oc_collection.count_documents({"owner": memberID, "type": f"{self.search.title()}"})
                    return (totalcards + self.cards_per_page - 1) // self.cards_per_page

        else:
            member = m_collection.find_one({'memberID': memberID})
            uids = member['cards_collected']
            return (len(uids) + self.cards_per_page - 1) // self.cards_per_page

    def get_cards(self, memberID):
        if self.type is not None:
            if self.search is None:
                return False
            else:
                if self.type.lower() == "name":
                    if self.search.lower() == "jy":
                        self.search = "JY"
                    elif self.search.lower() in ["warrior of light", "warrior"]:
                        self.search = "Warrior of Light"
                    elif self.search.lower() in ["jiwoong's", "jiwoong's ren", "jiwoong"]:
                        self.search = "Jiwoong's Ren"
                    else:
                        self.search = self.search.title()

                    totalcards = oc_collection.find({"owner": memberID, "name": f"{self.search}"}).sort([('name', 1), ('theme', 1)])
                    return totalcards[((self.current_page - 1) * self.cards_per_page):(self.current_page * self.cards_per_page)]
                elif self.type.lower() == "theme":
                    regex_pattern = re.compile(re.escape(self.search), re.IGNORECASE)
                    query = {"owner": memberID, "theme": {'$regex': regex_pattern}}
                    totalcards = oc_collection.find(query).sort([('name', 1), ('theme', 1)])
                    return totalcards[((self.current_page - 1) * self.cards_per_page):(self.current_page * self.cards_per_page)]
                elif self.type.lower() == "type":
                    totalcards = oc_collection.find({"owner": memberID, "type": f"{self.search.title()}"}).sort([('name', 1), ('theme', 1)])
                    return totalcards[((self.current_page - 1) * self.cards_per_page):(self.current_page * self.cards_per_page)]
        else:
            member = m_collection.find_one({'memberID': memberID})
            uids = member['cards_collected']
            cards = list(oc_collection.find({'uid': {'$in': uids}}).sort('name', 1))
            return cards[((self.current_page - 1) * self.cards_per_page):(self.current_page * self.cards_per_page)]