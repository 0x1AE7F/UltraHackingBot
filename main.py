import discord
import subprocess
from timeit import default_timer as timer
import cachemaster
import search_exploits


# Color definitions for printing
class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


bot_prefix = "!"
TOKEN = "GoodLuckStealingMyToken hehe (got leaked a couple of times XD)"
client = discord.Client()


@client.event
async def on_ready():
    # This line is very messy but it makes the ready message a little more "vibrant"
    print(f'[INFO]: {colors.OKBLUE}Ultra{colors.WARNING}Hacking{colors.OKGREEN}Bot{colors.ENDC} is {colors.BOLD}{colors.UNDERLINE}{colors.OKCYAN}ready{colors.ENDC}!')


@client.event
async def on_message(message):
    # Resets shell output variable to prevent the bot from printing the same output twice
    shell_output = ""

    # Checks if message author is the bot
    if message.author == client.user:
        return

    # Makes user input lowercase, strips newline symbols and splits all args
    user_message = str(message.content).lower().strip().split(" ")

    if message.content.startswith(bot_prefix+'ping'):
        print(f"{colors.OKCYAN}[RUN]: ping{colors.ENDC}")
        try:
            # Start new timer
            start_time = timer()
            # Run shell command and capture output
            shell_output = subprocess.check_output(
                ["ping", "-c", "1", str(user_message[1])])
            shell_output = shell_output.decode('utf-8')
        # Check if any errors occurred
        except Exception as e:
            print(f"{colors.FAIL}[ERROR]: ping: {e}{colors.ENDC}")
            # Calls function to create error embed
            await createEmbed(message=message, title="Ping Result: FAIL", description=e, failed=True)
            return
        # Calls func to send result in embed
        await createEmbed(message=message, title="Ping Result", description=shell_output, failed=False, milliseconds=round(number=(timer() - start_time), ndigits=3))
        print(f"{colors.OKGREEN}[PASS]: ping{colors.ENDC}")
        return

    if message.content.startswith(bot_prefix+'traceroute'):
        print(f"{colors.OKCYAN}[RUN]: traceroute{colors.ENDC}")
        try:
            # Start new timer
            start_time = timer()
            # Run shell command and capture output
            shell_output = subprocess.check_output(
                ["traceroute", str(user_message[1])])
            shell_output = shell_output.decode('utf-8')
        # Check if any errors occurred
        except Exception as e:
            print(f"{colors.FAIL}[ERROR]: traceroute: {e}{colors.ENDC}")
            # Calls func to create error embed
            await createEmbed(message=message, title="Traceroute Result: FAIL", description=e, failed=True)
            return
        # Calls func to send result in embed
        await createEmbed(message=message, title="Traceroute", description=shell_output, failed=False, milliseconds=round(number=(timer() - start_time), ndigits=3))
        print(f"{colors.OKGREEN}[PASS]: traceroute{colors.ENDC}")
        return

    if message.content.startswith(bot_prefix+'cvelookup'):
        existing_cache_entry = True
        # UnboundLocalError: local variable 'descriptions_result' referenced before assignment <-- FIX BELOW
        description_result = ""
        link_result = ""

        print(f"{colors.OKCYAN}[RUN]: cvelookup{colors.ENDC}")
        try:
            # Start new timer
            start_time = timer()
            # Checks if we can satify request with cache
            if cachemaster.check_cache(user_message[1]):
                search_result = cachemaster.read_cache(
                    user_message[1].replace(" ", "+"))

            else:
                # Calls func to scan CVE Mitre website for known exploits of given query
                existing_cache_entry = False
                search_result = search_exploits.search_cve_mitre(
                    str(user_message[1].replace(" ", "+")))

            # Checks to prevent errors and return users an answer instead of a blank ("[]") list
            if search_result == None:
                await createEmbed(message=message, title="CVEMitre: No Results found!", description=f"Search with query: {user_message[1]} returned no results!", failed=True)
                print(f"{colors.OKGREEN}[PASS]: cvelookup{colors.ENDC}")
                return
            if search_result[0] == None:
                description_result = "No description found."
            else:
                description_result = search_result[0]
            if search_result[1] == None:
                link_result = "No URL found!"
            else:
                link_result = search_result[1]


            if not existing_cache_entry:
                # Creates a new cache entry because there is no entry for this request yet
                cachemaster.new_cache_entry(user_message[1].replace(
                    " ", "+"), description_result, link_result, search_result[2])
        except Exception as e:
            print(f"{colors.FAIL}[ERROR]: cvelookup: {e}{colors.ENDC}")
            await createEmbed(message=message, title="CVEMitre Result: FAIL", description=e, failed=True)
            return
        await createEmbed(message=message, title="CVEMitre Result", description=f"Description: {str(description_result)}\n\nURL: {str(link_result)}\n\n\nSee More: {search_result[2]}", failed=False, milliseconds=round(number=(timer() - start_time), ndigits=3))
        print(f"{colors.OKGREEN}[PASS]: cvelookup{colors.ENDC}")
        return


def createEmbed(message, title, description, failed=True, milliseconds="ERR "):
    if failed:
        color = 0xff0000
    else:
        color = 0x00ff04

    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text=f"Task took {milliseconds}ms")
    return message.channel.send(embed=embed)


client.run(TOKEN)
