from discord.ext import commands
import discord
import json
import asyncio
import random

# Funfact: Most People who paste struggle with the levelsystem. I dont know why since its pretty easy to understand, even
# without much knownledge of Python and JSON

# NOTE: Doing further Stuff with JSON, i recommend learning more about JSON and how it works exactly. Pasting isnt a good idea here.

# This Levelsystem works with JSON.
# Doing this with JSON is good for a few small Servers, but if you want to make a Puplic Bot i recommend using 
# a DataBase such as SQlite or similar since they are much faster.

class levelsystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.save_users())

        # First off, we need to open and load the JSON file we want to store everything in
        with open(r"users.json", 'r') as f:
            self.users = json.load(f)

    # So we want to write and save into our JSON file.
    async def save_users(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open(r"users.json", 'w') as f:
                json.dump(self.users, f, indent=4)
            await asyncio.sleep(60)

    # Here we define how much XP a User needs to get 1 Level UP
    def lvl_up(self, author_id):
        cur_xp = self.users[author_id]['xp']
        cur_lvl = self.users[author_id]['level']

        if cur_xp >= round((4 * (cur_lvl ** 8)) / 10):
            self.users[author_id]['level'] += 1
            return True
        else:
            return False


    # Here is our on_message Event.
    # You should be already familiar with it at this Point.
    @commands.Cog.listener()
    async def on_message(self, message):
        # First, we dont want the Bot to level UP himself so we need to take him out... PENG!
        if message.author == self.bot.user:
            return
        # Users should not be able to recieve XP in Private Messages or Groups right?
        if not message.guild:
            return

        # Here we check if the User that just sended us a message is already in the JSOn file or not -> If he's cool or not!
        # When he is NOT in the File, we just add him and grand him +1 XP. How Generus!
        author_id = str(message.author.id)
        if not author_id in self.users:
            self.users[author_id] = {}
            self.users[author_id]['level'] = 0
            self.users[author_id]['xp'] = 0
        # Otherwise we just give a User 1 XP for each Message. I recommend putting a cooldown in here too since users could simply just 
        # spam themselves up.
        self.users[author_id]['xp'] += 1

        if self.lvl_up(author_id):
            await message.channel.send(f"{message.author.mention} just reached level {self.users[author_id]['level']}, Well done!")


    # Ok so it would be cool if a User can Check his / others level and XP right? Here we go!
    @commands.command()
    @commands.guild_only()
    # Guild only because you cant level up outside of groups and PM.
    async def level(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        member = ctx.author if not member else member
        member_id = str(member.id)

        if not member_id in self.users:
            await ctx.send("This User did not achieved level 1 yet.")
        # Sad bro, you didn't even got to level 1 yet. Waht a looser. He needs to get active, Staff? Where are you? Your Members aren't active enough!
        else:
            lvl = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

            lvl.set_author(name=f"Level - {member}", icon_url=self.bot.user.avatar_url)
            lvl.set_footer(text=f"Called by: {ctx.author}", icon_url=ctx.author.avatar_url)

            lvl.add_field(name="Level", value=self.users[member_id]['level'])
            lvl.add_field(name="XP", value=self.users[member_id]['xp'])

            await ctx.send(embed=lvl)



    # But wahts the Point of having XP When you cant to anything with it? Why not make a game with the XP to gain even MORE XP!
    # Lets make a Slot Machine Game, very simple and without edits.
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def slots(self, ctx, member: discord.Member = None):
        await ctx.message.delete()

        member = ctx.author if not member else member
        member_id = str(member.id)

        # Here you can put the Amount of XP one Round of Slots costs
        if self.users[member_id]['xp'] >= 50:
from discord.ext import commands
import discord
import random
import asyncio


class levelsystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        


    async def lvl_up(self, user):
        cur_xp = user['xp']
        cur_lvl = user['lvl']

        if cur_xp >= round((3 * (cur_lvl ** 7)) / 10):
            await self.bot.pg_con.execute("UPDATE users SET lvl = $1 WHERE user_id = $2 AND guild_id = $3", cur_lvl + 1, user['user_id'], user['guild_id'])
            return True
        else:
            return False


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if not message.guild:
            return


        author_id = str(message.author.id)
        guild_id = str(message.guild.id)

        user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
        
        if not user:
            await self.bot.pg_con.execute("INSERT INTO users (user_id, guild_id, lvl, xp) VALUES ($1, $2, 1, 0)", author_id, guild_id)
        
        
        user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)

        if user:
            await self.bot.pg_con.execute("UPDATE users SET xp = $1 WHERE user_id = $2 AND guild_id = $3", user['xp'] + 1, author_id, guild_id)

   
        if await self.lvl_up(user):
            await message.channel.send(f"{message.author.mention} just reached level {user['lvl'] + 1}, Well done!")


    @commands.command()
    @commands.guild_only()
    async def level(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        member = ctx.author if not member else member
        author_id = str(member.id)
        guild_id = str(member.guild.id)
        user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)

        if not user:
            await ctx.send("This User did not achieved any level yet.")
        else:
            lvl = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

            lvl.set_author(name=f"Level - {member}", icon_url=self.bot.user.avatar_url)
            lvl.set_footer(text=f"Called by: {ctx.author}", icon_url=ctx.author.avatar_url)

            lvl.add_field(name="Level", value=user[0]['lvl'])
            lvl.add_field(name="XP", value=user[0]['xp'])

            await ctx.send(embed=lvl)


    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx, member: discord.Member = None):
        await ctx.message.delete()

        member = ctx.author if not member else member
        author_id = str(member.id)
        guild_id = str(member.guild.id)
        
        user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
        await self.bot.pg_con.execute("UPDATE users SET xp = $1 WHERE user_id = $2 AND guild_id = $3", user['xp'] + 80, author_id, guild_id)

        await ctx.send("You recieved your daily 80XP")




def setup(bot):
    bot.add_cog(levelsystemCog(bot))
