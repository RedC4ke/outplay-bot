import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import pickle
import account
import chess.game
import chess.embed


bot = commands.Bot(command_prefix=['!', 'o!', 'outplay!'])
bot.remove_command('help')
invites = {}
players = {}
chessThumbnail = discord.File('res/shield.png', 'thumbnail.png')


def load_players():
    path = 'res/players.sav'
    if os.path.getsize(path) > 0:
        players.update(pickle.load(open(path, 'rb')))


def save_players():
    pickle.dump(players, open('res/players.sav', 'wb'))


@bot.event
async def on_ready():
    chess.game.load()
    load_players()


@bot.event
async def on_reaction_add(reaction, user):
    match = invites.get(reaction.message.id, None)

    if (match is not None) and (user != bot.user) and (reaction.emoji == '👍'):
        for this in match.players:
            record = players.get(this.user, None)
            if record.chess.current_game is not None:
                return 0

        for this in match.players:
            players.get(this.user).chess.current_game = match.id

        match.start()
        invites[reaction.message.id] = None
        await chess.embed.board(reaction.message.channel, match)


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help page", description="Outplay is a simple Chess bot.", color=0xf4536f)
    # embed.add_field(name="`prefixes [add|remove|list]`",
    #                value="Allows you to change command prefixes. Defaults are  _!_ ,  _o!_   "
    #                      "and  _outplay!_. The bot can still be called by mentioning it.",
    #                inline=False)
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
    await ctx.send(file=chessThumbnail, embed=embed)


@bot.command()
async def challenge(ctx, user: discord.User):
    u1 = ctx.message.author
    u2 = user

    for u in [u1, u2]:
        player = players.get(u, None)
        if player is None:
            print('sffs')
            players[u] = account.Player(u)

    match = chess.game.ChessMatch(players.get(u1), players.get(u2))
    embed = chess.embed.challenge(ctx.message.author, user, match.id)

    message = await ctx.send(file=chessThumbnail, embed=embed)
    invites[message.id] = match
    for emoji in ['👍', '👎']:
        await message.add_reaction(emoji)


@bot.command()
async def move(ctx, arg):
    author = ctx.message.author
    player = players.get(author)
    game_id = player.chess.current_game
    game = chess.game.current_games.get(game_id, None)
    if (game is not None) and (game.current_player == author):
        game.move(arg)

    await ctx.send(file=discord.File(game.image()))

load_dotenv('keys.env')
bot.run(os.getenv('TOKEN'))

