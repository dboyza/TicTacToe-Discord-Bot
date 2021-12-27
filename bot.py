import discord
from discord import activity
from discord.ext import commands
from config import *
import datetime
from datetime import datetime
from tictactoe import *

activity = discord.Game(name="!play")
client = commands.Bot(command_prefix='!', activity=activity)


# Prints login in terminal when bot starts running
@client.event
async def on_ready():
    print('{0.user} is now online.'.format(client))


# !play command
@client.command(pass_context=True)
async def play(ctx):
    await playinfo(ctx)


# !challenge command
@client.command(pass_context=True)
async def challenge(ctx):
    await playgame(ctx, client)


client.run(KEY)
