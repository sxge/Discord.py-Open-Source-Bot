from discord.ext import commands
import discord
import psutil
import os
import time

class cmdCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Just some simple help commands.
    # I decided to use Command Groups until i get my ass up to make a proper paginator 


    @commands.group(name="help", case_insensitive=True)
    async def help(self, ctx):
        await ctx.message.delete()

        if ctx.invoked_subcommand is None:
            embed = discord.Embed(description="**Main Page**", colour=discord.Colour.green())
            embed.add_field(name="levelsystem", value="See all level-related Commands", inline=False)
            embed.add_field(name="members", value="See all member-related Commands", inline=False)
            embed.add_field(name="mod", value="See all moderation-related Commands", inline=False)
            embed.add_field(name="misc", value="See all misc-related Commands", inline=False)

            await ctx.send(embed=embed)
        

    @help.command(name="levelsystem", case_insensitive=True)
    async def levelsystem(self, ctx):

        levelsystem = discord.Embed(description="**Levelsystem**", colour=discord.Colour.orange())
        levelsystem.add_field(name="level [user]", value="To see other Users level, simply Tag them after 'level'", inline=False)
        levelsystem.add_field(name="slots", value="Play Slots with your XP. WARNING: You need atleast 50 XP", inline=False)
        levelsystem.add_field(name="daily", value="Get your daily amount of XP", inline=False)

        await ctx.send(embed=levelsystem)

    @help.command(name="members", case_insensitive=True)
    async def members(self, ctx):

        members = discord.Embed(description="**Members**", colour=discord.Colour.orange())
        members.add_field(name="userinfo [user]", value="Shows all Info about the Tagged User", inline=False)
        members.add_field(name="serverinfo", value="Shows all Info about the Server the Command was triggered in", inline=False)
        members.add_field(name="botinfo", value="Shows all Info about the Bot itself", inline=False)

        await ctx.send(embed=members)

    @help.command(name="mod", case_insensitive=True)
    async def mod(self, ctx):

        mod = discord.Embed(description="**Moderation**", colour=discord.Colour.orange())
        mod.add_field(name="ban [user]", value="Bans a User from the Server", inline=False)
        mod.add_field(name="removeban [user]", value="Remove the Ban of a banned User", inline=False)
        mod.add_field(name="listbans", value="Lists all Bans", inline=False)
        mod.add_field(name="kick [user]", value="Kicks a User from the Server", inline=False)
        mod.add_field(name="mute [user]", value="Mutes a User [You still need to setup the Role for it]", inline=False)
        mod.add_field(name="unmute [user]", value="Unmutes a User", inline=False)
        mod.add_field(name="purge [x]", value="Clears x amount of Messages (Dont overload it!)", inline=False)
        mod.add_field(name="say [xyz]", value="Let the Bot say something", inline=False)

        await ctx.send(embed=mod)

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
    bot.add_cog(cmdCog(bot))

