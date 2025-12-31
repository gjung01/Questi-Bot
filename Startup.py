import os
import discord
from config import client
from Member import Member

class StartupCommands:
    async def load_commands():
        for filename in os.listdir("./cmds"):
            if filename.endswith(".py"):
                # cut off the .py from the file name
                await client.load_extension(f"cmds.{filename[:-3]}")

    async def reload_commands():
        for filename in os.listdir("./cmds"):
            if filename.endswith(".py"):
                # cut off the .py from the file name
                print(filename)
                await client.reload_extension(f"cmds.{filename[:-3]}")

    def user_in_database(ctx):
        memberId = ctx.author.id
        member = Member.get_member(memberId)
        return member is not None
    
    async def is_it_meh(ctx):
        if ctx.author.id == 377267947829198859:
            return "meh is here"
        else:
            await ctx.send("Sorry you can't use this command")
