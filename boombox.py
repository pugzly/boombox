#
#         BoomBox - Discord MP3 streaming bot
#
#
#
#  Requirements (on my Debian VPS server, at least):
#       sudo apt install ffmpeg
#       python3 -m pip install -U discord.py
#       python3 -m pip install -U pynacl
#
#  @pooodle


import discord, os, random, asyncio
from discord.ext import commands, tasks


###  Edit bellow to fit your needs and preferences

DISCORD_API_TOKEN = 'M2391576SZD-------REPLACE-THIS-WITH-DISCORD-API-TOKEN-OF-YOUR-BOT------Nj02947wND'
CREATOR_ID = 1000006900000001   # YOUR Discord User ID, only for command '.quit'
MUSIC_DIR = '/home/user/mp3'    # Path to where your MP3's are stored
PREFIX = '.'                    # Replace this, if you want all your commands start with anything other than '.'


bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    #for guild in bot.guilds:
    #    for channel in guild.voice_channels:
    #        if channel.name == 'General':
    #            await play_random_song(channel)

async def play_random_song(guild_id):
    channel = None
    guild = discord.utils.get(bot.guilds, id=guild_id)
    for ch in guild.voice_channels:
        if ch.name == 'General':
            channel = ch
            break

    if not channel:
        return

    if not os.path.exists(MUSIC_DIR):
        return

    songs = [f for f in os.listdir(MUSIC_DIR) if f.endswith('.mp3')]
    if not songs:
        return

    song_path = os.path.join(MUSIC_DIR, random.choice(songs))

    # Extract the song name without the extension for displaying
    song_name = os.path.basename(song_path).rsplit('.', 1)[0]

    # Set the bot's status to show the song's name
    await bot.change_presence(activity=discord.Game(name=f"{song_name}"))

    # This part checks if the bot is already connected to a voice channel in the guild
    voice_client = discord.utils.get(bot.voice_clients, guild=guild)
    if not voice_client:
        voice_client = await channel.connect()

    if not voice_client.is_playing():
        voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=song_path), after=lambda e: bot.loop.create_task(play_next_song(guild_id)))

async def play_next_song(guild_id):
    voice_client = discord.utils.get(bot.voice_clients, guild=discord.utils.get(bot.guilds, id=guild_id))
    if voice_client:
        await play_random_song(guild_id)

@bot.command(name='play', help='Makes the bot join the General voice channel and starts playing music.')
@commands.has_permissions(administrator=True)
async def play(ctx):
    await play_random_song(ctx.guild.id)

@bot.command(name='stop', help='Stops playing the music and makes the bot leave the voice channel.')
@commands.has_permissions(administrator=True)
async def stop(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client:
        await voice_client.disconnect()
        await asyncio.sleep(2)               # Give it a couple seconds, for no particular reason

@bot.command(name='skip', help="Skips to the next song.")
@commands.has_permissions(administrator=True)
async def skip(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.stop()

@bot.command(name='quit', help='Stops the bot completely and exit program.')
async def quit_bot(ctx):
    if ctx.author.id == CREATOR_ID:
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice_client:
            await voice_client.disconnect()  # Stop the stream
            await asyncio.sleep(2)           # Give it a couple seconds to process the stop command
        await ctx.bot.close()                # Disconnect the bot

bot.run(DISCORD_API_TOKEN)
