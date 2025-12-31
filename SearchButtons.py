import discord
import asyncio
import re
from config import m_collection, c_collection

class SearchView(discord.ui.View):
    current_page: int = 1
    names_per_page: int = 5
    timeout: int = 180

    def __init__(self):
        super().__init__()
        self.option = ""
        self.args = ""

    async def send(self, ctx, option, args):
        self.option = option
        self.args = args
        data = self.fetch_all_cards()
        self.message = await ctx.reply(mention_author=True, embed=self.create_embed(data, ctx.author.id), view=self)
        self.timeout_task = ctx.bot.loop.create_task(self.timeout_task())

    async def timeout_task(self):
        await asyncio.sleep(self.timeout)
        await self.stop()

    async def stop(self):
        self.clear_items()

    def create_embed(self, data, ctx):
        embed = discord.Embed(title="Questi's Card Collection", color=discord.Color.from_rgb(190,130,201))
        embed.set_footer(text="*Note: If the page doesn't change, it means it has reached the end")
        for card in data:
            resultcard = self.hasCard(ctx, card)
            embed.add_field(name=f"{resultcard}", value=f"", inline=False)
        return embed
        
    async def update_message(self, data, ctx):
        await self.message.edit(embed=self.create_embed(data, ctx), view=self)

    @discord.ui.button(label="|<", style=discord.ButtonStyle.gray)
    async def first_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message.reference.message_id
        messagecontent = await interaction.channel.fetch_message(message)
        if interaction.user.id == messagecontent.author.id:
            await interaction.response.defer()
            self.current_page = 1
            data = self.fetch_all_cards()
            await self.update_message(data, interaction.user.id)
        else:
            pass

    @discord.ui.button(label="<", style=discord.ButtonStyle.gray)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message.reference.message_id
        messagecontent = await interaction.channel.fetch_message(message)
        if interaction.user.id == messagecontent.author.id:
            await interaction.response.defer()
            if self.current_page == 1:
                self.current_page = 1
            else:
                self.current_page -= 1
            data = self.fetch_all_cards()
            await self.update_message(data, interaction.user.id)
        else:
            pass

    @discord.ui.button(label=">", style=discord.ButtonStyle.gray)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message.reference.message_id
        messagecontent = await interaction.channel.fetch_message(message)
        if interaction.user.id == messagecontent.author.id:
            await interaction.response.defer()
            total_pages = self.calculate_total_pages()
            if self.current_page == total_pages:
                self.current_page = total_pages
            else:
                self.current_page += 1
            data = self.fetch_all_cards()
            await self.update_message(data, interaction.user.id)
        else:
            pass

    @discord.ui.button(label=">|", style=discord.ButtonStyle.gray)
    async def last_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message.reference.message_id
        messagecontent = await interaction.channel.fetch_message(message)
        if interaction.user.id == messagecontent.author.id:
            await interaction.response.defer()
            total_pages = self.calculate_total_pages()
            self.current_page = total_pages
            data = self.fetch_all_cards()
            await self.update_message(data, interaction.user.id)
        else:
            pass

    def fetch_all_cards(self):
        dict = {}
        if self.option and self.args:
            if self.option.lower() == "name":
                if self.args.lower() == "jy":
                    cards = list(c_collection.find({"name": "JY"}))
                elif self.args.lower() in ["warrior of light", "warrior"]:
                    cards = list(c_collection.find({"name": "Warrior of Light"}))
                elif self.args.lower() in ["jiwoong's", "jiwoong's ren", "jiwoong"]:
                    cards = list(c_collection.find({"name": "Jiwoong's Ren"}))
                else:
                    cards = list(c_collection.find({"name": f"{self.args.title()}"}))
            elif self.option.lower() == "type":
                dict['type'] = self.args.capitalize()
                cards = list(c_collection.find(dict).sort([('name', 1), ('theme', 1)]))
            elif self.option.lower() == "theme":
                regex_pattern = re.compile(f'{re.escape(self.args)}', re.IGNORECASE)
                dict['theme'] = {'$regex': regex_pattern}
                cards = list(c_collection.find(dict).sort([('name', 1), ('theme', 1)]))
        else:
            cards = list(c_collection.find().sort([('name', 1), ('theme', 1)]))
        if not cards:
            cards = list(c_collection.find().sort([('name', 1), ('theme', 1)]))

        listcards = cards[((self.current_page - 1) * self.names_per_page):(self.current_page * self.names_per_page)]
        if listcards == []:
            cards = list(c_collection.find().sort([('name', 1), ('theme', 1)]))
            listcards = cards[((self.current_page - 1) * self.names_per_page):(self.current_page * self.names_per_page)]
        return listcards

    def calculate_total_pages(self):
        dict = {}
        if self.option and self.args:
            if self.option.lower() == "name":
                if self.args.lower() == "jy":
                    cards = list(c_collection.find({"name": "JY"}))
                elif self.args.lower() == ["warrior of light", "warrior"]:
                    cards = list(c_collection.find({"name": "Warrior of Light"}))
                elif self.args.lower() in ["jiwoong's", "jiwoong's ren", "jiwoong"]:
                    cards = list(c_collection.find({"name": "Jiwoong's Ren"}))
                else:
                    cards = list(c_collection.find({"name": f"{self.args.title()}"}))
            elif self.option.lower() == "type":
                dict['type'] = self.args.capitalize()
                cards = list(c_collection.find(dict).sort([('name', 1), ('theme', 1)]))
            elif self.option.lower() == "theme":
                regex_pattern = re.compile(f'{re.escape(self.args)}', re.IGNORECASE)
                dict['theme'] = {'$regex': regex_pattern}
                cards = list(c_collection.find(dict).sort([('name', 1), ('theme', 1)]))
        else:
            cards = list(c_collection.find().sort([('name', 1), ('theme', 1)]))

        if not cards:
            cards = list(c_collection.find().sort([('name', 1), ('theme', 1)]))

        total_pages = (len(cards) + self.names_per_page - 1) // self.names_per_page
        return total_pages
    
    def get_member_cards(self, ctx):
        member = m_collection.find_one({'memberID': ctx})
        return member['cards_collected']
    
    def hasCard(self, ctx, card):
        member = m_collection.find_one({'memberID': ctx})
        memberCards = member['cards_collected']
        for uid in memberCards:
            if uid in card['uids']:
                return f"\u2713 ~~{card['name']} [{card['theme']}]~~"
        return f"\u26ac {card['name']} [{card['theme']}]"
