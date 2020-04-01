import discord
from discord.ext import commands
from discord.utils import get
import random
import datetime
import asyncio


class modCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command(no_pm=True)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason ="No Reason set"):
        embed = discord.Embed(
            title="Ban",
            description=f"{member.name} was banned for **{reason}**.",
        )
        await ctx.guild.ban(member, reason=reason)
        await ctx.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("It seems like the User already left the Server.")
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("Cant ban User")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry but you don't have permissions to do that.")


    # List all Bans in the Guild
    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def listbans(self, ctx):
        users = await ctx.guild.bans()
        if len(users) > 0:
            msg = f'`{"ID, ":21}{"Name, ":25} Reason\n'
            for entry in users:
                userID = entry.user.id
                userName = str(entry.user)
                if entry.user.bot:
                    username = '🤖' + userName
                reason = str(entry.reason)
                msg += f'{userID:<21}{userName:25} {reason}\n'
            embed = discord.Embed(color=0xe74c3c)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text=f'Server: {ctx.guild.name}')
            embed.add_field(name='Bans:', value=msg + '`', inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send('**:negative_squared_cross_mark:** No banned Users found!')


    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    async def mute(ctx, member: discord.Member):
        role = discord.utils.get(member.server.roles, name='Muted')
        await member.add_roles(member, role)
        embed = discord.Embed(description=f"**{0}** was muted by **{1}**!".format(member, ctx.message.author))
        await member.send(embed=embed)
        if role not in member.server.roles:
            norole = discord.Embed(description="No Role named 'Muted' was found on the Server.")
            await ctx.send(embed=norole)

    @mute.error
    async def mute_error(self, ctx):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(description="You don't have permission to use this command.")
        await ctx.send(embed=embed)


    # Deletes x Amount of Messages in the Channel
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.message.delete()
        member = ctx.author
        await ctx.channel.purge(limit=amount)
        purge = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

        purge.set_footer(text="Chat purged", icon_url=member.avatar_url)
        purge.add_field(name="",
                        value="Waht have the Users done wrong again? ^^")

        await ctx.send(embed=purge)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.channel.send("How should i know how many Messages you want me to delete???")


    # Repeats everything you wrote after "say"
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def say(self, ctx, *, arg):
        await ctx.message.delete()
        time = 0.2 * len(arg.split(' '))
        async with ctx.channel.typing():
            await asyncio.sleep(time)
            await ctx.channel.send(arg)

    @say.error
    async def say_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.channel.send("Waht the heck you want me to say?", delete_after=3)



def setup(bot):
    bot.add_cog(modCog(bot))
