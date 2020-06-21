import discord
from discord.ext import commands
import os
import random
import asyncio

# Needed only for our Levelsystem
if not os.path.exists('users.json'):
    open('users.json', 'w').close()

"""
If you encounter any Problems with adding new Stuff, consider checking the Official Documentation of Discord.py
Rewrite Documentation:
http://discordpy.readthedocs.io/en/rewrite/api.html
Rewrite Commands Documentation:
http://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html
"""

#============================================
#========= Set the Bots Prefix(es) ==========
#============================================

def get_prefix(bot, message):
    # You can set multiple Prefixes, just seperate them with a ","
    prefixes = ['!']

    # Check if we are in a Server. If not, we can set a Custom Prefix for PM's and Groups
    if not message.guild:
        # Just return the Prefix we like for PM's and Groups
        return ':'

    return commands.when_mentioned_or(*prefixes)(bot, message)


async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(database="DB", user="user", password="password")

bot.loop.run_until_complete(create_db_pool())
#============================================
#============== Define "bot" ================
#===== Remove the default help Command ======
#============================================

bot = commands.Bot(command_prefix=get_prefix, description='None')
bot.remove_command("help")


#============================================
#=============== Loading Cogs ===============
#============================================

# Let us find all Cogs we have added. Seperate your Cogs with a ","
initial_extensions = ['cogs.example',
                      'cogs.members',
                      'cogs.cmd',
                      'cogs.mod',
                      'cogs.misc',
                      'cogs.levelsystem',
                      'cogs.games'
                      ] 

# Here we actually load all Cogs we added above
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


#============================================
#============= Basic Bot Events =============
#============================================

# Simple on_message event. Usefull to find Problems if your Bot does not work correctly later by adding varius print statements
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    print("Written by sxge#2868")

# With this we make the Bot Start
@bot.event
async def on_ready():
    #http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready

    print(f'\n\n Logged in! \n -> Bot-Name: {bot.user.name} \n -> Bot-ID {bot.user.id}\n -> Discord.py Version: {discord.__version__}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f"Starting..."))
    print(f'Hello! I am now fully booted up and ready to use')
    print("Thanks to the 'Progress' Discord-Server for helping me whenever i needed help coding!")
    print("Invite-link: https://discord.gg/HDSjxfu")
    print("Written by sxge#2868")


#============================================
#===== Make an automated Status Change ======
#============== Every X Seconds =============
#============================================

async def status_chng():
    await bot.wait_until_ready()

    while not bot.is_closed():
        await bot.change_presence(activity=discord.Game(name="Hello! I am a Open Source Bot"))
        await asyncio.sleep(30)
        # Replace 30 with the Amount of Seconds you want the Bot to change its Status
        await bot.change_presence(activity=discord.Game(name="I was developed by sxge#2868"))

# Lets make the status_chng a loop so it runs endless
bot.loop.create_task(status_chng())





# Last but not least, the most important Part. The Bot Token.
# /--------------------------------------------\
# |                WARNING:                    |
# |!!! NEVER EVER GIVE IT TO SOMEONE ELSE !!!  |
# \____________________________________________/
# You can get your Discord Account banned when other People have your token.
# Just dont give it to someone else ok? Promise me that. If you do, dont cry if your Discord Account gets banned. You've been warned



# Anyway, since sometimes you might need help with your main.py file and if you post a screenshort or send the whole file to someone else,
# you might forget about the token. So for Security we load it from a seperate Text file called token.txt

#============================================
#=== Read and get the Token of token.txt ====
#============================================

with open('token.txt', 'r') as f:
    token = f.read().strip()

bot.run(token)
