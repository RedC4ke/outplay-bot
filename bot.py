import discord
import chess

client = discord.Client()
conf_pref = open("prefixes.txt")
prefixes = []


@client.event
async def on_ready():
    for line in conf_pref:
        prefixes.append(line)

    print("Cyny gejm! U r {0.user}"
          .format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    for prefix in prefixes:
        if message.content.startswith(prefix + "help"):
            embed = discord.Embed(title="Help page", description="Outplay is a simple Chess bot.", color=0xf4536f)
            embed.set_thumbnail(url='https://i.imgur.com/E7JJZMv.png')
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
            await message.channel.send(embed=embed)

        # if message.content.startswith(prefix+"challenge")


client.run('ODExOTQ0OTE1NjM4Mjg4NDA1.YC5koQ.lMRS2eiw-Mu3u0KTYeaRdzrzy6U')
