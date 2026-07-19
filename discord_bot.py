from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
CHANNEL_ID = int(CHANNEL_ID)

import discord
from monitor import approval_event, cancel_event


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
alert_channel = None

@client.event
async def on_ready():
    global alert_channel
    print(f'Logged in as {client.user}')
    alert_channel = client.get_channel(CHANNEL_ID)
    print("Alert channel:", alert_channel)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == "yes":
        approval_event.set()
        await message.channel.send("Approval received")

    elif message.content.lower() == "no":
        cancel_event.set()
        await message.channel.send("Cancelled")

async def send_message(text):
    await alert_channel.send(text)

def start_bot():
    client.run(TOKEN)