from discord.ext import commands
from Member import Member

#this is completely fine
@commands.command(
        aliases = ['desc', 'me'],
        brief= '- Sets your bio',
        description= '''
            Sets your bio.

            For Example:
             - ?bio [any text or emojis you want to add]

            *Note: Be sure to not include the brackets
        '''
)
async def bio(ctx, *, description:str):
    desc = Member.set_desc(ctx, description)
    await ctx.reply(f'Bio set to **"{desc}"**')

async def setup(bot):
    bot.add_command(bio)