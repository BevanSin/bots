# Pretense Discord Bot

This bot is designed to pull the info from the Savegame file 'player_stats.json' which is created by the mission Pretense created by Dzsekeb, and publish it to a Discord channel.

Pretense Mission - https://www.digitalcombatsimulator.com/en/files/3331159/

In the channel each pilot is published in order of highest XP to lowest with a timestamp at the top for when it was last posted.

## Instructions

To install, open a command prompt and browse to the folder you want to install the bot and run

`git clone https://github.com/BevanSin/bots`

In the *pretense-scoreboard* folder copy the `sample_config.json` and save as `config.json` file which needs to be updated with your variables: 

> **DISCORD_BOT_TOKEN** - replace DISCORD_BOT_TOKEN with the token for your discord bot

> **JSON_FILE_PATH** - replace JSON_SAVE_FILE_LOCATION with the file location of the save file i.e.  d:\temp\player_stats.json

> **CHANNEL_ID_NUMBER** - replace the CHANNEL_ID_NUMBER with the ID number of the discord channel you want to post the scores into.

> **UPDATE_INTERVAL** - this is the interval in seconds for scoreboard updates and defaults to 60 seconds

run `python scoreboardbot.py`

You should see the pilot, their XP and Rank in your discord channel.

## Ranks

This is a static table within the python at the moment.  If the mission creator updates these this will need to be modified.  I'll do my best to keep it up to date :)