import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import chess

client = discord.Client()
conf_pref = open("prefixes.txt")
prefixes = []
bot = commands.Bot(command_prefix=['!', 'o!', 'outplay!'])
bot.remove_command('help')
game = chess.Match()


@bot.command()
async def help(ctx):
    thumbnail = discord.File('res/shield.png', 'thumbnail.png')
    embed = discord.Embed(title="Help page", description="Outplay is a simple Chess bot.", color=0xf4536f)
    embed.add_field(name="`prefixes [add|remove|list]`",
                    value="Allows you to change command prefixes. Defaults are  _!_ ,  _o!_   "
                          "and  _outplay!_. The bot can still be called by mentioning it.",
                    inline=False)
    embed.add_field(name="`challenge [user]`",
                    value="Challenges the mentioned user to a chess duel. The invitation can be **accepted** "
                          "or **rejected** using reactions",
                    inline=False)
    embed.add_field(name="`move [notation]`",
                    value="Makes a move. The proper notation is  `XY:XY` , where _X_  is a **letter**  "
                          "and _Y_  is a **number**. ",
                    inline=False)
    embed.add_field(name="`draw`",
                    value="Starts a poll to **draw** the session. Draw occurs when both players agree "
                          "or the other player doesn't respond in **48 hours**",
                    inline=False)
    embed.set_thumbnail(url='attachment://thumbnail.png')
    await ctx.send(file=thumbnail, embed=embed)


@bot.command()
async def start(ctx):
    game.start()
    await ctx.send(file=discord.File(game.image()))


@bot.command()
async def move(ctx, arg):
    game.move(arg, True)
    await ctx.send(file=discord.File(game.image()))

load_dotenv('keys.env')
bot.run(os.getenv('TOKEN'))
