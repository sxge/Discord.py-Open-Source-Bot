from discord.ext import commands
import discord
import json
import asyncio
import random





class gamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def slots(self, ctx, member: discord.Member = None):
        await ctx.message.delete()

        member = ctx.author if not member else member
        author_id = str(member.id)
        guild_id = str(member.guild.id)


        user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
        await self.bot.pg_con.execute("UPDATE users SET xp = $1 WHERE guild_id = $2 AND user_id = $3", user['xp'] - 50, guild_id, author_id)
        

        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
            await self.bot.pg_con.execute("UPDATE users SET xp = $1 WHERE user_id = $2 AND guild_id = $3", user['xp'] + 800, author_id, guild_id)
            
            embed1 = discord.Embed(colour=discord.Colour.dark_gold(), timestamp=ctx.message.created_at)
            embed1.set_footer(text=f"Played by: {ctx.author}", icon_url=ctx.author.avatar_url)
            embed1.add_field(name=f"{slotmachine}", value="***WOW***, you just hit 3x the same Symbol! 🎉", inline=False)
            embed1.add_field(name="You won 800 XP", value="🎉 🎉 🎉", inline=False)

            await ctx.send(embed=embed1)


        elif (a == b) or (a == c) or (b == c):
            user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
            await self.bot.pg_con.execute("UPDATE users SET xp = $1 WHERE user_id = $2 AND guild_id = $3", user['xp'] + 200, author_id, guild_id)

            embed2 = discord.Embed(colour=discord.Colour.dark_gold(), timestamp=ctx.message.created_at)
            embed2.set_footer(text=f"Played by: {ctx.author}", icon_url=ctx.author.avatar_url)
            embed2.add_field(name=f"{slotmachine}", value="***WOW***, you achieved 200XP! 🎉", inline=False)
            await ctx.send(embed=embed2)


        else:
            user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
            await self.bot.pg_con.execute("UPDATE users SET xp = $1 WHERE user_id = $2 AND guild_id = $3", user['xp'] + 20, author_id, guild_id)

            embed3 = discord.Embed(colour=discord.Colour.dark_gold(), timestamp=ctx.message.created_at)
            embed3.set_footer(text=f"Played by: {ctx.author}", icon_url=ctx.author.avatar_url)
            embed3.add_field(name=f"{slotmachine}", value="Not this time! 😢 Maybe you get it with the next try", inline=False)
            await ctx.send(embed=embed3)

    @commands.command()
    async def dice(self, ctx, member: discord.Member = None):


        member = ctx.author if not member else member
        member_id = str(member.id)

        if self.users[member_id]['xp'] >= 30:
            self.users[member_id]['xp'] -= 30
        else:
            await ctx.send("You need to have atleast 30XP to play Slots!")


        points = ['1', '2', '3', '4', '5', '6']
        randompoint = random.choice(points)
        prediction = discord.Embed(title="Dice rolled:", description=randompoint)
        await ctx.send(embed=prediction)
        for points in randompoint:
            if randompoint == '6':
                self.users[member_id]['xp'] += 60
            if randompoint == '5':
                self.users[member_id]['xp'] += 50
            if randompoint == '4':
                self.users[member_id]['xp'] += 40
            if randompoint == '3':
                self.users[member_id]['xp'] += 30
            if randompoint == '2':
                self.users[member_id]['xp'] += 20
            if randompoint == '1':
                self.users[member_id]['xp'] += 10



def setup(bot):
    bot.add_cog(gamesCog(bot))