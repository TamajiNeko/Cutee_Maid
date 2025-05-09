import discord
import os
import json
import asyncio
import requests
import random
import time

from googletrans import Translator
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

translator = Translator()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

Status = {}

# Test Mode for Debug

Voice_Mode = False #VC compatible mode
Test_Mode = False #model test mode

Modle = {} #Model swapper
if Test_Mode:
    Modle = "src/model_test.py"
else:
    Modle = "src/model.py"

# Function & Utilities

sleep_message = [
    "(⸝⸝ᴗ_ᴗ⸝⸝) z z 𐰁",
    "꒰｡- ᴗ - ｡꒱ ᶻzᶻzᶻz﹒﹒",
    "(っ˕ -｡)ᶻ 𝗓 𐰁",
    "(⸝⸝ᴗ﹏ᴗ⸝⸝) ᶻ 𝗓 𐰁",
    "ᶻ 𝗓 𐰁₍⑅ᐢ..ᐢ₎",
    "₍ᐡっˊ﹃ˋ๑ᐡ₎ᶻ 𝗓 𐰁",
    "/ᐠ - ˕ -マᶻ 𝗓 𐰁",
    "(⸝⸝⸝╸▵╺⸝⸝⸝)"
]

def status_check(): #Check API status
    global Status
    
    try:
        response = requests.get(os.getenv("API_Model"))
        
        if response.status_code == 200:
            data = response.json()
            
            if "data" in data and len(data["data"]) > 0:
                Status = 1
            else:
                Status = 0
        else:
            Status = 0

    except requests.exceptions.RequestException as e:
        Status = 0

async def update_status(): #Update Bot status when API status change
    await bot.wait_until_ready()
    while not bot.is_closed():
            status_check()
            if Status == 1:
                await bot.change_presence(
                    status=discord.Status.idle,
                    activity=discord.Activity(
                        type=discord.ActivityType.custom,
                        name="I'm Cuteee~♡",
                        state="Hi~♡ Your Cuteee Maid Here♡"
                    ),
                )
                print(time.strftime("\033[90m%Y-%m-%d %I:%M:%S\033[0m \033[38;2;59;120;255mINFO\033[0m     \033[35mAPI Status\033[0m Online ദ്ദി(˵ •̀ ᴗ - ˵ ) ✧", time.localtime()))
            else:
                await bot.change_presence(
                    status=discord.Status.dnd,
                    activity=discord.Activity(
                        type=discord.ActivityType.custom,
                        name="Sleeping~",
                        state="I'm sleeping ꒰｡- ᴗ - ｡꒱ ᶻzᶻzᶻz﹒﹒"
                    ),
                )
                print(time.strftime("\033[90m%Y-%m-%d %I:%M:%S\033[0m \033[38;2;59;120;255mINFO\033[0m     \033[35mAPI Status\033[0m Offline (｡T ω T｡)", time.localtime()))
            await asyncio.sleep(180)


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
    except Exception as e:
        print(e)
    print(time.strftime("\033[90m%Y-%m-%d %I:%M:%S\033[0m \033[38;2;59;120;255mINFO\033[0m     \033[35mBot Ready\033[0m Your Maid is ready to work~! (˶ᵔ ᵕ ᵔ˶)", time.localtime()))
    bot.loop.create_task(update_status())

def load_list(): #Load allowed list
    try:
        with open('list.json', 'r') as f:
            config = json.load(f)
            return config.get('channels', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_list(channels): #Add new channel to list
    with open('list.json', 'w') as f:
        json.dump({'channels': channels}, f, indent=4)

#Command, you can read commands descriptions

@bot.tree.command(name="add", description="Add me to this channel Master (˶˃ ᵕ ˂˶) .ᐟ.ᐟ")
@app_commands.checks.has_permissions(manage_channels=True)
async def add_channel(interaction: discord.Interaction):
    channels = load_list()
    channel_id = interaction.channel.id

    if channel_id in channels:
        await interaction.response.send_message(
            "I Already here Master~! (˶ᵔ ᵕ ᵔ˶)",
            ephemeral=True
        )
    else:
        channels.append(channel_id)
        save_list(channels)
        await interaction.response.send_message(
            "I'm here in this channel Master! (˵>ᗜ<˵) !!",
            ephemeral=True
        )


@bot.tree.command(name="remove", description="I'll leave this channel Master (˚ ˃̣̣̥⌓˂̣̣̥ )")
@app_commands.checks.has_permissions(manage_channels=True)
async def remove_channel(interaction: discord.Interaction):
    channels = load_list()
    channel_id = interaction.channel.id
    
    if channel_id not in channels:
        await interaction.response.send_message(
            "I'm not work in this channel Master~ (,,>ヮ<,,)!",
            ephemeral=True
        )
        return
    
    channels.remove(channel_id)
    save_list(channels)

    await interaction.response.send_message(
        "Goodbye Master~ I'll leave this channel~ (˶◜ᵕ◝˶)",
        ephemeral=True
    )

@bot.tree.command(name="purge", description="I'll help to clean multiple messages Master~♡")
@app_commands.describe(amount="Number of messages to delete up to 100")
@app_commands.checks.has_permissions(manage_messages=True)
async def purge(interaction: discord.Interaction, amount: int = 1):
    if not 1 <= amount <= 100:
        return await interaction.response.send_message("Master, Please enter between 1-100 messages ( ˶ˆᗜˆ˵ )", ephemeral=True)
    
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"Cleaned {len(deleted)} messages Master~! ദ്ദി(˵ •̀ ᴗ - ˵ ) ✧", ephemeral=True)

@bot.tree.command(name="clear", description="clear history that all master talk to me (˶˃⤙˂˶)")
@app_commands.checks.has_permissions(manage_channels=True)
async def add_channel(interaction: discord.Interaction):
    if Test_Mode:
        file_path = os.path.join("history", f"test_{interaction.channel_id}.json")
    else:
        file_path = os.path.join("history", f"{interaction.channel_id}.json")
        
    def clear_history():
        global chat_history
        chat_history = {} 
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(chat_history, f, indent=2) 

    clear_history()
    await interaction.response.send_message("Done Master! I'll tell everyone for this~ ദ്ദി(˵ •̀ ᴗ - ˵ ) ✧", ephemeral=True)
    await interaction.channel.send("Sorry all Master my manager asked me to delete all conversation infomation in this channel. I won't remember anything that you asked me before. (｡T ω T｡)")

#Event

async def check_auto_disconnect(voice_client): #lines 188-204 for VC compatible mode(Auto disconnect when no one on VC)
    if voice_client and voice_client.channel:
        members = voice_client.channel.members
        non_bots = [member for member in members if not member.bot]

        if len(non_bots) == 0:
            await voice_client.disconnect()

@bot.event
async def on_voice_state_update(member):
    if member.bot:
        return

    voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
    if voice_client:
        await asyncio.sleep(2)
        await check_auto_disconnect(voice_client)

@bot.event
async def on_message(message):
    if message.author == bot.user or message.channel.id not in load_list():
        return
    
    if bot.user.mentioned_in(message):
        status_check()
        if Status == 1:
            if message.channel.type == discord.ChannelType.text:
                async with message.channel.typing():
                    try:
                        process = await asyncio.create_subprocess_exec( #send content to model.py
                            "python", Modle, message.content,str(message.author.id), str(message.author.display_name), str(message.channel.id),
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE
                        )
                    
                        try:
                            stdout, stderr = await asyncio.wait_for(
                                process.communicate(),
                                timeout=120.0
                            )   
                            if process.returncode == 0:
                                response = stdout.decode().strip()
                                if response:
                                        await message.reply(response) #send message to channel

                        except asyncio.TimeoutError:
                            process.kill()

                    except Exception as e:
                        process.kill()
            elif message.channel.type == discord.ChannelType.voice and Voice_Mode == True: #For VC compatible mode (TTS services) and work on VC channel only
                if message.author.voice and message.author.voice.channel:
                    async with message.channel.typing():
                        try:
                            process = await asyncio.create_subprocess_exec( #send content to YOUR_VC_API_HANDLE
                                "python", "src/voice_model.py", message.content,str(message.author.id), str(message.author.display_name), str(message.channel.id),
                                stdout=asyncio.subprocess.PIPE,
                                stderr=asyncio.subprocess.PIPE
                            )
                            try:
                                stdout, stderr = await asyncio.wait_for(
                                    process.communicate(),
                                    timeout=120.0
                                ) 
                                if process.returncode == 0:
                                    response = stdout.decode().strip()
                                    voice_channel = message.author.voice.channel

                                    voice_client = message.guild.voice_client
                                    if not voice_client:
                                        voice_client = await voice_channel.connect()

                                    if not voice_client.is_playing():
                                        audio_source = discord.FFmpegPCMAudio(".bin/output.wav") #Sound directory (You must create .bin directory)
                                        voice_client.play(audio_source)

                                    if response: #you don't need translator, i just use VoiceVox TTS (only japanses)
                                        translate_response = await translator.translate(response, src='ja', dest='en')
                                        await message.reply(f"{translate_response.text} (Translated)")

                            except asyncio.TimeoutError:
                                process.kill()

                        except Exception as e:
                            process.kill()
        else:
            await message.channel.send(random.choice(sleep_message))


load_dotenv()
bot.run("YOUR TOKEN")