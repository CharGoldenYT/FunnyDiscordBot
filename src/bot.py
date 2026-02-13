import discord
from discord.client import Client

class DiscordBot:
    token: str
    client: Client
    message: str
    channelID: int

    def __init__(self, token: str, message: str, channelID: int):
        self.token = token
        self.client = Client(intents=discord.Intents.default())
        self.client.event(self.on_ready)
        self.channelID = channelID
        self.message = message

    async def on_ready(self):
        print(f"Logged in as {self.client.user}")
        await self.send_message()

    async def send_message(self):
        channel = self.client.get_channel(self.channelID)
        if channel is not None:
            await channel.send(self.message)
        else:
            print("Channel not found, make sure the channel ID is correct.")

        await self.client.close() # Close the bot after sending the message

    def run(self):
        self.client.run(self.token)