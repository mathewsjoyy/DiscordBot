from discord.ext import commands
from dotenv import load_dotenv
from lxml import html
from trie.Trie import Trie
from dotenv import load_dotenv
import requests
import random
import discord
import requests
import os
import music
import crypto

# Load .env file
try:
    load_dotenv()
except Exception:
    print("No .env file found.")

PREFIX = "/"
COGS = [music, crypto]

# Make the bot
bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())

# Set up any cogs
for x in range(len(COGS)):
    COGS[x].setup(bot)


# Make prefix tree for bad words capture
trie = Trie()
table = {
    "\"": None,
    "'": None,
    "-": None,
    "`": None,
    "~": None,
    ",": None,
    ".": None,
    ":": None,
    ";": None,
    "_": None
}

def buildTrie():
    # Might need to change this
    file = None
    
    try:
        file = open('src/trie/badwords.txt', 'r') # For heroku
    except FileNotFoundError:
        file = open('C:\\Users\\mathe\\OneDrive\\Documents\\Coding\\DiscordBot\\src\\trie\\badwords.txt', 'r') # For local

    for line in file:
        line = line.strip()
        trie.insert(line)

def warn_user(user_id):
    user_id = '<@' + str(user_id) + '>'
    responses = [
        "You kiss your mother with that mouth, {}?",
        "Come on now, {}. Did you really need to say that?",
        "Damn {} people must really like you!",
        "{}, you just embarrassing yourself now..."]

    choice = random.choice(responses)
    choice = choice.format(user_id)

    return choice

# EVENTS #
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    # Check on images/videos are posts in images-videos channel
    if str(message.channel) == "images-videos" and message.content != "":
        await message.delete()
    
    # Check for racist terms
    text = message.content
    text = text.translate(str.maketrans(table))
    author_id = message.author.id

    if author_id != 504744916933672991: # Owner id
        isClean = True
        message_word_list = text.split()
        for word in message_word_list:
            if trie.search(word):
                isClean = False
                break
        if not isClean:
            # Delete the bad message and warn the user
            await message.delete()
            await message.channel.send(warn_user(author_id))

@bot.event
async def on_ready():
    buildTrie()
    print("Trie is built. ready to read messages.")
    await bot.get_channel(888736019590053898).send(f"We back online! All thanks to *sploosh* :D")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        replies = ["Err is that even a command?", "Can you type bro?", "Yeah... thats not a command buddy.", "Sorry forgot you can't spell"]
        await ctx.send(random.choice(replies))
    

# COMMANDS #
@bot.command()
async def hello(ctx):
    # Get a random fact
    url = 'http://randomfactgenerator.net/'
    page = requests.get(url)
    tree = html.fromstring(page.content)
    hr = str(tree.xpath('/html/body/div/div[4]/div[2]/text()'))
    
    await ctx.reply("**Hello Bozo!**\n" + "*Random Fact : *" + hr[:-9]+"]")
    
@bot.command()
async def randomNum(ctx, start:int = None, end:int = None):
    if(start == None or end == None):
        await ctx.reply("*Check your arguments!*\n```/randomNum START_NUMBER END_NUMBER```")
    else:
        randNum = random.randint(start, end)
        await ctx.reply(f"*{randNum}*")

@bot.command()
@commands.is_owner()
async def kick(ctx, member:discord.Member = None, *, reason="You smell bozo."):
    if(member == None):
        await ctx.reply("*Check your arguments!*\n```/kick @MEMBER REASON(optional)```")
    elif ctx.author.id in (member.id, bot.user.id):
        await ctx.reply("*You cant kick yourself/me you silly.*")
    else:
        await member.kick(reason=reason)

@bot.command()
@commands.is_owner()
async def ban(ctx, member:discord.Member = None, *, reason="Bye Bye! :D."):
    if(member == None):
        await ctx.reply("*Check your arguments!*\n```/kick @MEMBER REASON(optional)```")
    elif ctx.author.id in (member.id, bot.user.id):
        await ctx.reply("*You cant ban yourself/me you silly.*")
    else:
        await member.ban(reason=reason)
        
@bot.command()
@commands.is_owner()
async def close_bot(ctx):
    replies = ["Well bye!", "Guess I go now?", "Please let me stay..."]
    await ctx.send(random.choice(replies))
    await bot.close()
    

    
if __name__ == "__main__":
    bot.run(os.environ.get("BOT_TOKEN"))
    