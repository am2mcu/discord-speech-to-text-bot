import discord
from discord.ext import commands
import config
import transcript
import tts

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

    await bot.process_commands(message)

@bot.command()
async def id(message):
    debug("in command func")
    await message.reply(message.author.id)

# Speech to text
@bot.command()
async def text(ctx):
    if ctx.message.attachments != []:
        await ctx.channel.send("Transcripting the audio, Wait for it...")

        result = await transcript.main(ctx.message.attachments[0].url)
        print(result)

        if (result == ""):
            await ctx.reply("Failed to transcript the audio")
        else:
            await ctx.reply(result)
    else:
        await ctx.reply("Provide an audio")

# Text to speech
@bot.command()
async def speech(message, *text):
    text = " ".join(text)
    await message.channel.send("Generating the audio, Wait for it...")
    await message.reply(file=discord.File(await tts.get_audio(text), "audio.mp3"))

bot.run(TOKEN)