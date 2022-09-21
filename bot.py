import discord
from discord.ext import commands
import config
import transcript

TOKEN = config.TOKEN

# debugger
def debug(msg):
    # print(msg)
    pass

# Initialize Bot and Denote The Command Prefix
bot = commands.Bot(command_prefix="?", intents=discord.Intents(messages=True, guilds=True))

# Runs when Bot Succesfully Connects
@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')

@bot.event
async def on_message(message):
    debug("in func")

    # Make sure the Bot doesn't respond to its own messages
    if message.author == bot.user:
        debug("return : bot")
        return
    
    if any((phrase == message.content.lower()) for phrase in ['hello', 'hi', 'hey']):
        debug("got here")
        await message.reply(f'Hi {message.author.name}')

    if message.attachments != []:
        await message.channel.send("Transcripting the audio, Wait for it...")

        result = await transcript.main(message.attachments[0].url)
        print(result)

        if (result == ""):
            await message.reply("Failed to transcript the audio")
        else:
            await message.reply(result)

    await bot.process_commands(message)

@bot.command()
async def id(message):
    debug("in command func")
    await message.reply(message.author.id)

bot.run(TOKEN)