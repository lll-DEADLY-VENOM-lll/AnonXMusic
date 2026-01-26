from pyrogram import Client
import config
from ..logging import LOGGER

assistants = []
assistantids = []

class Userbot(Client):
    def __init__(self):
        self.clients = []
        # सभी sessions को एक लिस्ट में डाल दिया
        self.sessions = [
            config.STRING1, 
            config.STRING2, 
            config.STRING3, 
            config.STRING4, 
            config.STRING5
        ]

        # लूप के ज़रिये क्लाइंट्स सेटअप करना
        for i, session in enumerate(self.sessions, start=1):
            if session:
                client = Client(
                    name=f"AviaxAss{i}",
                    api_id=config.API_ID,
                    api_hash=config.API_HASH,
                    session_string=str(session),
                    no_updates=True,
                )
                self.clients.append(client)
                # self.one, self.two आदि सेट करना ताकि पुराना कोड न टूटे
                setattr(self, ["one", "two", "three", "four", "five"][i-1], client)

    async def start(self):
        LOGGER(__name__).info("Assistants चालू हो रहे हैं...")
        
        for i, client in enumerate(self.clients, start=1):
            await client.start()
            
            # ऑटोमैटिक ग्रुप जॉइनिंग (बिना किसी गलती के)
            try:
                await client.join_chat("HEROKUoCLUB")
                await client.join_chat("NOBITA_SUPPORT")
            except Exception as e:
                LOGGER(__name__).warning(f"Assistant {i} ग्रुप जॉइन नहीं कर पाया: {e}")

            # लॉग ग्रुप में मैसेज भेजना
            try:
                await client.send_message(config.LOG_GROUP_ID, f"Assistant {i} Started ✅")
            except Exception:
                LOGGER(__name__).error(
                    f"Assistant {i} लॉग ग्रुप को एक्सेस नहीं कर पाया। कृपया उसे एडमिन बनाएं!"
                )
                if i == 1: exit() # अगर पहला असिस्टेंट फ़ेल हो तो बंद करें

            # डेटा सेव करना
            client.id = client.me.id
            client.name = client.me.mention
            client.username = client.me.username
            
            assistants.append(i)
            assistantids.append(client.id)
            
            LOGGER(__name__).info(f"Assistant {i} चालू हो गया: {client.name}")

    async def stop(self):
        LOGGER(__name__).info("Assistants बंद हो रहे हैं...")
        for client in self.clients:
            try:
                await client.stop()
            except Exception:
                pass
