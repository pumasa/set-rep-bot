# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = "OTUyMjc3Nzk1NTk2Mjk2Mzgz.Yizrzg.ZncDkPSfip9rQKHH2mBAahKoCkE"

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)