import discord
import os
import json
import asyncio

from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(
            type=discord.ActivityType.custom,
            name="I'm Cuteee~♡",
            state="Hi~♡ Your Cuteee Maid Here♡"
        ),
    )
    try:
        synced = await bot.tree.sync()
    except Exception as e:
        print(e)

def load_list():
    try:
        with open('list.json', 'r') as f:
            config = json.load(f)
            return config.get('channels', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_list(channels):
    with open('list.json', 'w') as f:
        json.dump({'channels': channels}, f, indent=4)

#Command Section

@bot.tree.command(name="add", description="Add me to this channel Master~!")
@app_commands.checks.has_permissions(manage_channels=True)
async def add_channel(interaction: discord.Interaction):
    channels = load_list()
    channel_id = interaction.channel.id

    HISTORY_DIR = "history"
    CHAT_PATH = os.path.join(HISTORY_DIR, f"{channel_id}.json")

    os.makedirs(HISTORY_DIR, exist_ok=True)

    def create_history():
        if not os.path.exists(CHAT_PATH) or os.path.getsize(CHAT_PATH) == 0:
            with open(CHAT_PATH, "w") as f:
                json.dump({}, f)
    
    if channel_id in channels:
        await interaction.response.send_message(
            "I Already here Master~!",
            ephemeral=True
        )
    else:
        channels.append(channel_id)
        save_list(channels)
        await interaction.response.send_message(
            "Done~! I'm here in this channel Master!",
            ephemeral=True
        )
    
    create_history()

@bot.tree.command(name="remove", description="I'll leave this channel Master~!")
@app_commands.checks.has_permissions(manage_channels=True)
async def remove_channel(interaction: discord.Interaction):
    channels = load_list()
    channel_id = interaction.channel.id
    
    if channel_id not in channels:
        await interaction.response.send_message(
            "I'm not live in stay channel Master~",
            ephemeral=True
        )
        return
    
    channels.remove(channel_id)
    save_list(channels)
    await interaction.response.send_message(
        "Bye Bye Master~ I'll leave this channel~",
        ephemeral=True
    )

@bot.tree.command(name="purge", description="I'll help Delete multiple messages Master~!")
@app_commands.describe(amount="Number of messages to delete up to 100")
@app_commands.checks.has_permissions(manage_messages=True)
async def purge(interaction: discord.Interaction, amount: int = 1):
    if not 1 <= amount <= 100:
        return await interaction.response.send_message("Master, Please enter between 1-100 messages", ephemeral=True)
    
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"I Deleted {len(deleted)} messages Master~!", ephemeral=True)

#Event Section#

@bot.event
async def on_message(message):
    if message.author == bot.user or message.channel.id not in load_list():
        return
    
    if bot.user.mentioned_in(message):
        async with message.channel.typing():
            try:
                process = await asyncio.create_subprocess_exec(
                    "python", "model.py", message.content, str(message.author.id), str(message.channel.id),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
            
                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(),
                        timeout=30.0
                    )   
                    if process.returncode == 0:
                        response = stdout.decode().strip()
                        if response:
                            if "<think>" in response:
                                response = response.split("</think>")[-1].strip()
                                if response == "":
                                    return
                                else:
                                    await message.reply(response)
                            else:
                                await message.reply(response)

                except asyncio.TimeoutError:
                    process.kill()

            except Exception as e:
                process.kill()
                
    await bot.process_commands(message)


load_dotenv()
bot.run(os.getenv("YOUR TOKEN"))
