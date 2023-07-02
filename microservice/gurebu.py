import requests
import time
import datetime
import discord

from typing import List

WALLET: str = 'TPjereztht2j6Ffq3vGyMGwvNvKErVNYuv'
CHANNEL_ID: int = 1113420310784516108

client = discord.Client(intents=discord.Intents.all())
channel = client.get_channel(CHANNEL_ID)


def fetch(wallet: str):
    response = requests.get(f"http://localhost:3000/fetch-transactions/{wallet}")
    transactions = response.json()

    if response.status_code == 200 and len(transactions):
        data: List[str] = ["GUREBU DEPOSIT"]

        for transaction in transactions:
            date: datetime = transaction['date']
            direction: str = transaction['direction']
            amount: float = transaction['amount']
            data.append(f"Date: {date}, Direction: {direction}, Amount: {amount}")

        text = '\n'.join(i for i in data)
        channel.send(text)


if __name__ == '__main__':
    while True:
        fetch(WALLET)
        time.sleep(60)
