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
            self.users[member_id]['xp'] -= 50
        else:
            # Ofcourse playing a Game where you can WIN XP needs to cost you XP... Who did this again?
            await ctx.send("You need to have atleast 50XP to play Slots!")

        # I think we need some juice fruits for this to make it look good, so here we go: Strawberry, Melons, Citrons, Cherrys.... YUMMY
        # You can use wahtever Emojies you want to use for this.
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        # This is like THE JACKPOT. THE HIGHSCORE. THE BEST. Pretty Rare to hit this, but possible. 
        if (a == b == c):
            self.users[member_id]['xp'] += 800
            embed1 = discord.Embed(colour=discord.Colour.dark_gold(), timestamp=ctx.message.created_at)

            embed1.set_footer(text=f"Played by: {ctx.author}", icon_url=ctx.author.avatar_url)

            embed1.add_field(name=f"{slotmachine}", value="***WOW***, you just hit 3x the same Symbol! 🎉", inline=False)
            embed1.add_field(name="You won 800 XP", value="🎉 🎉 🎉", inline=False)

            await ctx.send(embed=embed1)

        # This is still good, but not as good as the one above.
        # You just need to hit 2 same Symbols and you got it.
        elif (a == b) or (a == c) or (b == c):
            self.users[member_id]['xp'] += 200

            embed2 = discord.Embed(colour=discord.Colour.dark_gold(), timestamp=ctx.message.created_at)

            embed2.set_footer(text=f"Played by: {ctx.author}", icon_url=ctx.author.avatar_url)

            embed2.add_field(name=f"{slotmachine}", value="***WOW***, you achieved 200XP! 🎉", inline=False)

            await ctx.send(embed=embed2)

        # This is the badest one. you actually lost it. But hey, we'll give you 20XP Still since we're crying with you :((((
        else:
            self.users[member_id]['xp'] += 20

            embed3 = discord.Embed(colour=discord.Colour.dark_gold(), timestamp=ctx.message.created_at)

            embed3.set_footer(text=f"Played by: {ctx.author}", icon_url=ctx.author.avatar_url)

            embed3.add_field(name=f"{slotmachine}", value="Not this time! 😢 Maybe you get it with the next try", inline=False)

            await ctx.send(embed=embed3)


    # This was an idea to keep Users Active. Daily free XP? Who says no to that? I don't.
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx, member: discord.Member = None):
        await ctx.message.delete()

        member = ctx.author if not member else member
        member_id = str(member.id)

        self.users[member_id]['xp'] += 80
        await ctx.send("You recieved your daily 80XP")

# Now this was much right? If you did NOT just copy + pasted this, i think you are on a good way to make a great Bot :=)



def setup(bot):
    bot.add_cog(levelsystemCog(bot))