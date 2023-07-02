import yaml
import os
import discord

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

with open('app/configs/config.yaml', 'r', encoding="utf8") as file:
    config = yaml.safe_load(file)


with open('app/configs/text.yaml', 'r', encoding="utf8") as file:
    text = yaml.safe_load(file)


BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')  # config['discord']['bot']['token']
bot = commands.Bot(command_prefix=['/'], intents=discord.Intents.all())
