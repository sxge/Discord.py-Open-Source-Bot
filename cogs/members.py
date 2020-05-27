import discord
from discord.ext import commands
import psutil
import os
import time

class MembersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    # Simple Command to get Infos about yourself or another user
    @commands.command()
    @commands.guild_only()
    async def userinfo(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        member = ctx.author if not member else member

        user = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at)

        user.set_thumbnail(url=member.avatar_url)

        user.add_field(name="ID:", value=member.id, inline=False)
        user.add_field(name="Server Nickname:", value=member.display_name, inline=False)

        user.add_field(name="Status: ", value=member.status, inline=False)
        user.add_field(name="Playing: ", value=member.activity, inline=False)

        user.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                       inline=False)
        user.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                       inline=False)

        await ctx.send(embed=user)


    # Lets get some Info about the Server
    @commands.command()
    @commands.guild_only()
    async def serverinfo(self, ctx):
        await ctx.message.delete()
        server = ctx.message.author.guild

        memberCount = 0
        memberOnline = 0
        for member in server.members:
            memberCount += 1
            if not member.status == discord.Status.offline:
                memberOnline += 1

        iServer = discord.Embed(colour=discord.Colour.blue(), timestamp=ctx.message.created_at)

        iServer.set_author(name=server.name, icon_url=server.icon_url)
        iServer.set_thumbnail(url=server.icon_url)
        iServer.add_field(name="Server ID: ", value=server.id, inline=False)
        iServer.add_field(name="Members: ", value=server.member_count, inline=False)
        iServer.add_field(name="Roles: ", value=len(server.roles) - 1, inline=False)
        iServer.add_field(name="Owner: ", value=server.owner.name, inline=False)
        iServer.add_field(name="Users online: ", value=" {:,} / {:,} Users are online".format(memberOnline, memberCount), inline=False)

        await ctx.send(embed=iServer)

    # And who doesn't want to know more about this mysterius Bot huh?
    @commands.command()
    @commands.guild_only()
    async def botinfo(self, ctx):
        await ctx.message.delete()
        ramUsage = self.process.memory_full_info().rss / 1024**2
        avgmembers = round(len(self.bot.users) / len(self.bot.guilds))

        binfo = discord.Embed(colour=discord.Colour.dark_teal(), timestamp=ctx.message.created_at)

        binfo.set_footer(text="Bot-Info", icon_url=ctx.author.avatar_url)
        binfo.add_field(name="Bot-Name: ", value=f"{self.bot.user.name}", inline=False)
        binfo.add_field(name="Discord.py Version: ", value=f"{discord.__version__}", inline=False)
        binfo.add_field(name="Bot-ID: ", value=f"{self.bot.user.id}", inline=False)
        binfo.add_field(name="RAM Usage: ", value=f"{ramUsage:.2f} MB", inline=True)
        binfo.add_field(name="Joined Servers: ", value=f"{len(ctx.bot.guilds)} ( avg: {avgmembers} users/server )", inline=False)

        await ctx.send(embed=binfo)


def setup(bot):
    bot.add_cog(MembersCog(bot))
