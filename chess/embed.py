import discord
import asyncio


def challenge(u1: discord.User, u2: discord.User, match_id):
    embed = discord.Embed(title="A challenge!",
                          description=u1.mention + ' has invited ' + u2.mention + ' to a chess duel.',
                          color=0xf57c00)
    embed.add_field(name='Game id:', value=str(match_id) + '  ', inline=False)
    embed.add_field(name=':+1:  accept', value='\u200b', inline=True)
    embed.add_field(name=':-1:  decline', value='\u200b', inline=True)
    embed.set_thumbnail(url='attachment://thumbnail.png')

    return embed


def board(ctx, match):
    thumbnail = discord.File('res/shield.png', 'thumbnail.png')
    render = discord.File(match.image(), 'render.png')
    embed = discord.Embed(title='Turn ' + str(match.turn),
                          description='Chess match between **' + match.players[0].user.name + '** and **' +
                                      match.players[1].user.name + '**',
                          color=0x6ff9ff)
    embed.set_thumbnail(url='attachment://thumbnail.png')
    embed.set_image(url='attachment://render.png')
    embed.add_field(name='Current move:',
                    value=match.current_player.user.mention,
                    inline=False)
    embed.set_footer(text='Type !move XY:XY. For more info see !help.')

    return ctx.send(files=[render, thumbnail], embed=embed)



