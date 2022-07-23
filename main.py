import discord
import subprocess
from timeit import default_timer as timer


bot_prefix="!"
TOKEN = "GoodLuckGettingMyToken"
client = discord.Client()


@client.event
async def on_ready():
    print('UltraHackingBot is ready for interactions!')



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    user_message = str(message.content).lower().strip().split(" ")

    if message.content.startswith(bot_prefix+'ping'):
        try:
            start_time = timer()
            shell_output = subprocess.check_output(["ping", "-c", "1", str(user_message[1])])
            shell_output = shell_output.decode('utf-8')
        except Exception as e:
            await createEmbed(message=message, title="Ping Result: FAIL", description=e, failed=True)
        await createEmbed(message=message, title="Ping Result", description=shell_output, failed=False, miliseconds=round(number=(timer() - start_time), ndigits=3))

    if message.content.startswith(bot_prefix+'traceroute'):
        try:
            start_time = timer()
            shell_output = subprocess.check_output(["traceroute", str(user_message[1])])
            shell_output = shell_output.decode('utf-8')
        except Exception as e:
            await createEmbed(message=message, title="Traceroute Result: FAIL", description=e, failed=True)
        await createEmbed(message=message, title="Traceroute", description=shell_output, failed=False, miliseconds=round(number=(timer() - start_time), ndigits=3))



def createEmbed(message, title, description, failed=True, miliseconds="ERR "):
    if failed:
        color=0xff0000
    else:
        color=0x00ff04

    embed=discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text=f"Task took {miliseconds}ms")
    return message.channel.send(embed=embed)




client.run(TOKEN)
