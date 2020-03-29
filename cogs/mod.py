import discord
from discord.ext import commands
from discord.utils import get
import random
import datetime
import asyncio


class modCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Simply bans a User
    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *reason):
        await ctx.message.delete()
        member = ctx.author if not member else member
        if member is not None:
            if reason:
                reason = ' '.join(reason)
            else:
                reason = None
            await member.ban(reason=reason)

            ban = discord.Embed(colour=discord.Colour.dark_red(), timestamp=ctx.message.created_at)

            ban.set_author(name="Created Ban Successfull", icon_url=ctx.author.avatar_url)
            ban.add_field(name="Banned User: ", value=member)
            ban.add_field(name="Banned by: ", value=reason)

            await ctx.send(embed=ban, delete_after=15)
        else:
            await ctx.send('**:no_entry:** No User tagged!', delete_after=15)

    # Removes the Ban from the User
    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def removeban(self, ctx, *, member):
        ban_list = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in ban_list:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)

                unban = discord.Embed(colour=discord.Colour.green(), timestamp=ctx.message.created_at)

                unban.set_author(name="Ban Removed", icon_url=ctx.author.avatar_url)
                unban.add_field(name="Ban removed from User: ", value=user)
                unban.add_field(name="Ban was removed by: ", value=ctx.message.author)

                await ctx.send(embed=unban, delete_after=15)

    # List all Bans in the Guild
    @commands.command()
    @commands.has_permissions(kick_members=True)
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

    # Kicks a User from the Guild
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member):
        await ctx.message.delete()
        await member.kick()
        kick = discord.Embed(colour=discord.Colour.blue(), timestamp=ctx.message.created_at)

        kick.add_field(name="Kicked User:", value=member)

        await ctx.send(embed=kick)

    # Adds a Role called "Muted" to the tagged User. Still requires you to setup the Role for the Channels.
    # I will make a Set-Up command later that creates this Role automatically for you when first time running this Bot
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member,):
        await ctx.message.delete()
        message = []
        for role in ctx.guild.roles:
            if role.name == "Muted":
                message.append(role.name)
        try:
            therole = discord.Object(id=message[0])
        except IndexError:
            return await ctx.send("Error! Are you sure that there exists a Role named **Mute**? Remember that they are Case-Sensitive")

        try:
            await member.add_roles(therole, reason="Bad behavior"(ctx.author))
            await ctx.send("muted")
        except Exception as e:
            await ctx.send(e)

    # Removes the "Muted" ROle
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        message = []
        for role in ctx.guild.roles:
            if role.name == "Mute":
                message.append(role.id)
        try:
            therole = discord.Object(id=message[0])
        except IndexError:
            return await ctx.send("Error! Are you sure that there exists a Role named **Mute**? Remember that they are Case-Sensitive")

        try:
            await member.remove_roles(therole, reason="Bad behavior"(ctx.author))
            await ctx.send("unmuted")
        except Exception as e:
            await ctx.send(e)

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