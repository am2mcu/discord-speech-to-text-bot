import discord
from discord.ext import commands
import os
import transcript
import tts
import weather_api

TOKEN = os.environ.get("TOKEN")

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

@bot.command()
async def weather(ctx, *msg):
    if (msg == ()):
        await ctx.reply("The city is missing")
        return

    weather_info = await weather_api.short_broadcast(" ".join(msg))

    if (type(weather_info) == type("")): # when there isn't error weather_info is a dictionary
        embed = discord.Embed(title=weather_info, color=0x666666)
        await ctx.reply(embed=embed)
        return

    embed = discord.Embed(title=weather_info["weather_condition"], description=weather_info["temperature"] + "\n" + weather_info["humidity"], color=0x666666)
    embed.set_thumbnail(url=weather_info["icon_link"])
    await ctx.reply(embed=embed)

@bot.command()
async def weather_full(ctx, *msg):
    if (msg == ()):
        await ctx.reply("The city is missing")
        return

    weather_info = await weather_api.full_broadcast(" ".join(msg))

    if (type(weather_info) == type("")): # when there isn't error weather_info is a dictionary
        embed = discord.Embed(title=weather_info, color=0x666666)
        await ctx.reply(embed=embed)
        return

    embed = discord.Embed(
        title=weather_info["weather_condition"],
        description=weather_info["location"] + "\n" + weather_info["time"],
        color=0x666666
        )
    embed.set_thumbnail(url=weather_info["icon_link"])
    embed.add_field(name="Temperature", value=weather_info["temperature"], inline=True)
    embed.add_field(name="Hummidity", value=weather_info["humidity"], inline=True)
    embed.add_field(name="Wind Speed", value=weather_info["wind_speed"], inline=True)
    await ctx.reply(embed=embed)

bot.run(TOKEN)