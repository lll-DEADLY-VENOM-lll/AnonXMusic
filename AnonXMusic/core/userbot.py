import sys
from pyrogram import Client
import config
from ..logging import LOGGER

assistants = []
assistantids = []

class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="AnonXAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
        )
        self.two = Client(
            name="AnonXAss2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
        )
        self.three = Client(
            name="AnonXAss3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
        )
        self.four = Client(
            name="AnonXAss4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
        )
        self.five = Client(
            name="AnonXAss5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
        )

    async def start(self):
        LOGGER(__name__).info(f"Starting Assistants...")
        
        # Assistant 1
        if config.STRING1:
            await self.one.start()
            try:
                await self.one.join_chat("GOD_HYPER_O_P")
            except:
                pass
            assistants.append(1)
            # Log Group message skip kar diya gaya hai
            
            self.one.id = self.one.me.id
            self.one.name = self.one.me.mention
            self.one.username = self.one.me.username if self.one.me.username else "No Username"
            assistantids.append(self.one.id)
            LOGGER(__name__).info(f"Assistant Started as {self.one.name}")

        # Assistant 2
        if config.STRING2:
            await self.two.start()
            try:
                await self.two.join_chat("GOD_HYPER_O_P")
            except:
                pass
            assistants.append(2)
            
            self.two.id = self.two.me.id
            self.two.name = self.two.me.mention
            self.two.username = self.two.me.username if self.two.me.username else "No Username"
            assistantids.append(self.two.id)
            LOGGER(__name__).info(f"Assistant Two Started as {self.two.name}")

        # Assistant 3
        if config.STRING3:
            await self.three.start()
            try:
                await self.three.join_chat("GOD_HYPER_O_P")
            except:
                pass
            assistants.append(3)
            
            self.three.id = self.three.me.id
            self.three.name = self.three.me.mention
            self.three.username = self.three.me.username if self.three.me.username else "No Username"
            assistantids.append(self.three.id)
            LOGGER(__name__).info(f"Assistant Three Started as {self.three.name}")

        # Assistant 4
        if config.STRING4:
            await self.four.start()
            try:
                await self.four.join_chat("GOD_HYPER_O_P")
            except:
                pass
            assistants.append(4)
            
            self.four.id = self.four.me.id
            self.four.name = self.four.me.mention
            self.four.username = self.four.me.username if self.four.me.username else "No Username"
            assistantids.append(self.four.id)
            LOGGER(__name__).info(f"Assistant Four Started as {self.four.name}")

        # Assistant 5
        if config.STRING5:
            await self.five.start()
            try:
                await self.five.join_chat("HEROKU_CLUB")
            except:
                pass
            assistants.append(5)
            
            self.five.id = self.five.me.id
            self.five.name = self.five.me.mention
            self.five.username = self.five.me.username if self.five.me.username else "No Username"
            assistantids.append(self.five.id)
            LOGGER(__name__).info(f"Assistant Five Started as {self.five.name}")

    async def stop(self):
        LOGGER(__name__).info(f"Stopping Assistants...")
        try:
            if config.STRING1: await self.one.stop()
            if config.STRING2: await self.two.stop()
            if config.STRING3: await self.three.stop()
            if config.STRING4: await self.four.stop()
            if config.STRING5: await self.five.stop()
        except:
            pass
