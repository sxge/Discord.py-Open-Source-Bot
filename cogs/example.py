#============================================
# Welcome to the Cog - System!
# Cogs are used to make your Code look less messy.
# It is pretty easy to understand how they work.
# I will show you how everything is done.
# NOTE: I like do define and load my Cogs not in the same Way as most People but
# my Way is very easy to understand and you should not have many Problems with it.
#============================================

# First if, we need to import all the modules we need for our Commands.
# There are no Special imports we need to do in Cogs.
import discord
# The default discord import.
from discord.ext import commands
# I use the discord extension Module because its very common to use and easy to understand.

# If your Commands will need other Modules, just import them right here e.g. "import random" to use the random Module.

# So now we did our Imports and we want to create the actual Cog.
# For that we need to create a class.
class exampleCog(commands.Cog):
    def __init__(self, bot):
        # Because we dont want to use self.bot all the time, we just simple define self.bot with bot.
        self.bot = bot

    # Pay Attention to the Spacings now... This is such a Struggle for People who dont understand Python and caused so many "dumb" Problems already.
    # Instead of bot.command() we can now use @commands.command() since we are using Cogs.
    @commands.command()
    # We want this Command to be only aviable on a Server. The @commands.guild_only() flag is just perfect for us.
    @commands.guild_only()
    # Lets define the Name auf our Command and because we want to use the discord extension in here we also add ctx as an Parameter.
    async def ping(self, ctx):
        # After we defined the Name of our Command, we can now make the actual Command-Code.
        # In this Example, we only want the Bot to Answer with "Pong" when a User types "!ping" in the Chat. Easy, Right? 
        await ctx.send("Pong")
        # Now we are done with our first simple Command.

    # You can do as many Commands as you wish in here.


# This ends our Cog Setup function
def setup(bot):
    # Here we add the Cog to our bot so we can call it in main.py
    bot.add_cog(exampleCog(bot))