import discord
from discord.ext import commands
import secrets


class miscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Creates a random Password with the lenght of 18
    @commands.command()
    @commands.guild_only()
    async def password(self, ctx, nbytes: int = 18):
        await ctx.message.delete()
        if nbytes not in range(3, 32):
            return await ctx.send("Error!")
        if hasattr(ctx, 'guild') and ctx.guild is not None:
            await ctx.send(f"**I'll send you your random Password in a Second dear {ctx.author.name}**")
        await ctx.author.send(f"🎁 **Here is your Password:** 🎁\n{secrets.token_urlsafe(nbytes)}")

    # Incase the user has private Messages set to only Friends
    @password.error
    async def password_error(self, ctx):
        await ctx.send("Oops something went wrong, Do you have PM's on private?")

    # Starts a simple poll
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def poll(self, ctx, *, arg):
        pollembed = discord.Embed(colour=discord.Colour.green(), timestamp=ctx.message.created_at)

        pollembed.set_footer(text=f"This Poll was started by {ctx.message.author.name} ", icon_url=ctx.author.avatar_url)
        pollembed.add_field(name="Question: ", value=arg, inline=False)

        msg = await ctx.send(embed=pollembed)
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')

    # Here i just played around with the "random" module
    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def random(self, ctx, *arg):
        await ctx.message.delete()
        if ctx.invoked_subcommand is None:
            if not arg:
                start = 1
                end = 100
            elif arg[0] == 'flip' or arg[0] == 'coin':
                coin = ['Head', 'Tails']
                await ctx.send(f':arrows_counterclockwise: {random.choice(coin)}')
                return
            elif arg[0] == 'choice':
                choices = list(arg)
                choices.pop(0)
                await ctx.send(f':congratulations: Winner: {random.choice(choices)}')
                return
            elif arg[0] == 'user':
                online = self.userOnline(ctx.guild.members)
                randomuser = random.choice(online)
                if ctx.channel.permissions_for(ctx.author).mention_everyone:
                    user = randomuser.mention
                else:
                    user = randomuser.display_name
                await ctx.send(f':congratulations: Winner: {user}')
                return
            elif len(arg) == 1:
                start = 1
                end = int(arg[0])
            elif len(arg) == 2:
                start = int(arg[0])
                end = int(arg[1])
            await ctx.send(
                f'**:arrows_counterclockwise:** Random Number: ({start} - {end}): {random.randint(start, end)}')

    # You could also use this in the levelsystem to have another Game to earn XP
    @commands.command()
    @commands.guild_only()
    async def coinflip(self, ctx, member: discord.Member):
        await ctx.message.delete()
        choises = ["You've Won!", "You've lost", "You've lost", "You've lost"]
        rancoin = random.choice(choises)
        member = ctx.author if not member else member

        cf = discord.Embed(colour=discord.Colour.dark_orange(), timestamp=ctx.message.created_at)

        cf.set_author(name=f"Coinflip - {member}")
        cf.add_field(name="Throwing Coin...", value=rancoin, inline=False)
        await ctx.send(embed=cf)

    @coinflip.error
    async def coinflip_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.delete()
            cf_error = discord.Embed(colour=discord.Colour.dark_orange(), timestamp=ctx.message.created_at)

            cf_error.set_footer(text="Error!", icon_url=ctx.author.avatar_url)
            cf_error.add_field(name="Damn, something went wrong. Contact an Administrator", value="#00001")

            await ctx.send(embed=cf_error)

    # Gets the User Avatar
    @commands.command()
    @commands.guild_only()
    async def avatar(self, ctx, *, user: discord.Member = None):
        await ctx.message.delete()
        if user is None:
            user = ctx.author

        await ctx.send(f"Avatar of User **{user.name}:**\n{user.avatar_url_as(size=1024)}")


def setup(bot):
    bot.add_cog(miscCog(bot))
