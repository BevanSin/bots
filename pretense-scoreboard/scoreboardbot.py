import discord
import json
import asyncio
from datetime import datetime

# Discord bot token
TOKEN = '<discordbottoken>'

# JSON file path
JSON_FILE_PATH = r'<JSON SAVE FILE LOCATION>'

# Discord channel ID
CHANNEL_ID = <CHANNELIDNUMBER>

# Time interval for updating the leaderboard (in seconds)
UPDATE_INTERVAL = 60

# Player ranks based on score
ranks = {
    1: {"name": "E-1 Airman basic", "requiredXP": 0},
    2: {"name": "E-2 Airman", "requiredXP": 2000},
    3: {"name": "E-3 Airman first class", "requiredXP": 4500},
    4: {"name": "E-4 Senior airman", "requiredXP": 7700},
    5: {"name": "E-5 Staff sergeant", "requiredXP": 11800},
    6: {"name": "E-6 Technical sergeant", "requiredXP": 17000},
    7: {"name": "E-7 Master sergeant", "requiredXP": 23500},
    8: {"name": "E-8 Senior master sergeant", "requiredXP": 31500},
    9: {"name": "E-9 Chief master sergeant", "requiredXP": 42000},
    10: {"name": "O-1 Second lieutenant", "requiredXP": 52800},
    11: {"name": "O-2 First lieutenant", "requiredXP": 66500},
    12: {"name": "O-3 Captain", "requiredXP": 82500},
    13: {"name": "O-4 Major", "requiredXP": 101000},
    14: {"name": "O-5 Lieutenant colonel", "requiredXP": 122200},
    15: {"name": "O-6 Colonel", "requiredXP": 146300},
    16: {"name": "O-7 Brigadier general", "requiredXP": 173500},
    17: {"name": "O-8 Major general", "requiredXP": 204000},
    18: {"name": "O-9 Lieutenant general", "requiredXP": 238000},
    19: {"name": "O-10 General", "requiredXP": 275700}
}

intents = discord.Intents(guilds=True, messages=True)
client = discord.Client(intents=intents)

def get_rank(x):
    for rank, data in ranks.items():
        if x >= data["requiredXP"]:
            rank_info = (data["name"])
    return rank_info if "rank_info" in locals() else None

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    
    # Get the target channel
    channel = client.get_channel(CHANNEL_ID)

    # Fetch the leaderboard message if it exists
    leaderboard_message_id = None
    async for message in channel.history(limit=1):
        if message.author == client.user:
            leaderboard_message_id = message.id
            break

    while True:
        await asyncio.sleep(UPDATE_INTERVAL)

        # Read the JSON file
        with open(JSON_FILE_PATH, 'r') as json_file:
            data = json.load(json_file)

        # Extract player scores from the JSON data
        player_scores = {}
        stats = data.get("stats", {})
        for player, stats in stats.items():
            if isinstance(stats, dict):  # Check if stats is a dictionary
                xp = stats.get("XP", 0)
                player_scores[player] = xp

        # Sort players by their score in descending order
        sorted_players = sorted(player_scores.items(), key=lambda x: x[1], reverse=True)

        # Generate the leaderboard with timestamp
        now = datetime.now()
        timestamp = now.strftime("%H:%M %d:%m:%Y")
        leaderboard = f"Rankings as at {timestamp}:\n\n"
        for rank, (player, score) in enumerate(sorted_players, start=1):
            rank_num = rank
            rank_info = get_rank(score)
            rank_name = rank_info
            leaderboard += f"{rank_num}. ```{player:<25} [XP: {score:>5}] \n Rank: {rank_name}```\n"

       # If there is a previous message, edit it with the updated leaderboard
        if leaderboard_message_id:
            try:
                leaderboard_message = await channel.fetch_message(leaderboard_message_id)
                await leaderboard_message.edit(content=leaderboard)
            except discord.NotFound:
                leaderboard_message_id = None  # The message was deleted, reset the ID
            except discord.Forbidden:
                # Unable to edit the message, ignore and continue
                pass
        # If there is no previous message, send a new message with the leaderboard
        else:
            try:
                leaderboard_message = await channel.send(leaderboard)
                leaderboard_message_id = leaderboard_message.id
            except discord.errors.Forbidden:
                # Unable to send a new message, ignore and continue
                pass

# Run the Discord bot
client.run(TOKEN)
