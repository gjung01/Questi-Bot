import discord
from datetime import datetime
from discord.ext import commands
from config import m_collection

@commands.command(
        aliases= ['cd'],
        brief= "- Gives you a rundown of your cooldowns",
        description= '''
            Tells you which cooldowns are available and 
            how much time you have left from your items

            For Example:
             - ?cooldown or ?cd
        '''
)
async def cooldown(ctx):
    embed = discord.Embed(title="Current Cooldowns", color=discord.Color.from_rgb(190,130,201))
    member = m_collection.find_one({'memberID': ctx.author.id})
    drop = member.get("next_drop")
    work = member.get("next_work")
    current_time = datetime.now()

    drop_cooldown = (drop - current_time).total_seconds()
    dropminutes = int(drop_cooldown // 60)
    dropseconds = int(drop_cooldown % 60)
    if drop <= current_time:
        embed.add_field(name="Drop: Available", value="", inline=False)
    else:
        embed.add_field(name=f"Drop: {dropminutes}m {dropseconds}s", value="", inline=False)

    work_cooldown = (work - current_time).total_seconds()
    workminutes = int(work_cooldown // 60)
    workseconds = int(work_cooldown % 60)
    if work <= current_time:
        embed.add_field(name="Work: Available", value="", inline=False)
    else:
        embed.add_field(name=f"Work: {workminutes}m {workseconds}s", value="", inline=False)

    if member.get("cooldown") is True:
        cd = member.get("cooldown_duration")
        cd_cooldown = (cd - current_time).total_seconds()
        cdminutes = int(cd_cooldown // 60)
        cdseconds = int(cd_cooldown % 60)
        if cd <= current_time:
            embed.add_field(name="Cooldown: Deactivated", value="", inline=False)
        else:
            embed.add_field(name=f"Cooldown: {cdminutes}m {cdseconds}s", value="", inline=False)

    if member.get("boost") is True:
        boost = member.get("boost_duration")
        boost_cooldown = (boost - current_time).total_seconds()
        boostminutes = int(boost_cooldown // 60)
        boostseconds = int(boost_cooldown % 60)
        if boost <= current_time:
            embed.add_field(name="Boost: Deactivated", value="", inline=False)
        else:
            embed.add_field(name=f"Boost: {boostminutes}m {boostseconds}s", value="", inline=False)
    
    await ctx.reply(embed=embed)



async def setup(bot):
    bot.add_command(cooldown)