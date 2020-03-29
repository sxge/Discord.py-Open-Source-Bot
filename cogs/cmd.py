from discord.ext import commands
import discord


class cmdCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Just some simple help commands.
    # Im probably gonna make a Paginator System at a later point.
    # Nothing Special here

    @commands.command()
    async def help(self, ctx):
        await ctx.message.delete()

        embed = discord.Embed(description="Main Page")
        embed.add_field(name="levelsystem", value="See all level-related Commands", inline=False)
        embed.add_field(name="members", value="See all member-related Commands", inline=False)
        embed.add_field(name="moderation", value="See all moderation-related Commands", inline=False)
        embed.add_field(name="misc", value="See all misc-related Commands", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def levelsystem(self, ctx):
        await ctx.message.delete()

        embed = discord.Embed(description="levelsystem")
        embed.add_field(name="level [user]", value="To see other Users level, simply Tag them after 'level'", inline=False)
        embed.add_field(name="slots", value="Play Slots with your XP. WARNING: You need atleast 50 XP", inline=False)
        embed.add_field(name="daily", value="Get your daily amount of XP", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def members(self, ctx):
        await ctx.message.delete()

        embed = discord.Embed(description="members")
        embed.add_field(name="userinfo [user]", value="Shows all Info about the Tagged User", inline=False)
        embed.add_field(name="serverinfo", value="Shows all Info about the Server the Command was triggered in", inline=False)
        embed.add_field(name="botinfo", value="Shows all Info about the Bot itself", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def moderation(self, ctx):
        await ctx.message.delete()

        embed = discord.Embed(description="Moderation")
        embed.add_field(name="ban [user]", value="Bans a User from the Server", inline=False)
        embed.add_field(name="removeban [user]", value="Remove the Ban of a banned User", inline=False)
        embed.add_field(name="listbans", value="Lists all Bans", inline=False)
        embed.add_field(name="kick [user]", value="Kicks a User from the Server", inline=False)
        embed.add_field(name="mute [user]", value="Mutes a User [You still need to setup the Role for it]", inline=False)
        embed.add_field(name="unmute [user]", value="Unmutes a User", inline=False)
        embed.add_field(name="purge [x]", value="Clears x amount of Messages (Dont overload it!)", inline=False)
        embed.add_field(name="say [xyz]", value="Let the Bot say something", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def misc(self, ctx):
        await ctx.message.delete()

        embed = discord.Embed(description="Misc")
        embed.add_field(name="password", value="Generate and send you a Password in your PM's", inline=False)
        embed.add_field(name="poll [xyz]", value="Starts a Poll", inline=False)
        embed.add_field(name="random [flip], [choice], [user]", value="", inline=False)
        embed.add_field(name="coinflip", value="Throws a Coin", inline=False)
        embed.add_field(name="avatar", value="Gets the Avatar of a User", inline=False)
        
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(cmdCog(bot))

