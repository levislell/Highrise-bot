import os
import asyncio
import random
import subprocess
import sys
import time
from threading import Thread
from flask import Flask
from highrise import BaseBot, User, Position
from highrise.models import SessionMetadata, Position

# ==========================
# WEB SERVER (For Render Free 24/7)
# ==========================
app = Flask('')

@app.route('/')
def home():
    return "Leviae Pro Ultimate Bot is running online!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Démarrage automatique du serveur web pour Render
Thread(target=run_web_server).start()

# ==========================
# CONFIG
# ==========================
BOT_USERNAME = "leviae"
OWNERS = ["65592020383c55ed5c45aabd"]
MODERATORS = ["65592020383c55ed5c45aabd"]

# ==========================
# DATA (CHATBOT & RIDDLES)
# ==========================
CHATBOT_RESPONSES = [
    "Hey! Do you need any help? Type <#FFD700>!help<#FFFFFF> 🤖",
    "Hello! I hope you are having an amazing day in this room! ✨",
    "Yes? I'm Leviae, the official room bot! 🎵",
    "What's up? Type an emote name or number to start dancing! 💃"
]

GREETING_RESPONSES = [
    "Hello there! Welcome to our room! 👋",
    "Hi! Great to see you here, enjoy your stay! 🎉",
    "Welcome! Feel free to chill and dance! 🌟"
]

RIDDLES = [
    {"question": "What has hands but cannot clap?", "answer": "clock"},
    {"question": "What has to be broken before you can use it?", "answer": "egg"},
    {"question": "I’m tall when I’m young, and I’m short when I’m old. What am I?", "answer": "candle"},
    {"question": "What month of the year has 28 days?", "answer": "all"},
    {"question": "What is full of holes but still holds water?", "answer": "sponge"}
]

# ==========================
# EMOTES DICTIONARY (53 Emotes)
# ==========================
EMOTES = {
    "dance": "idle-dance-casual", "wave": "idle-wave", "freshprince": "dance-freshprince",
    "swagbounce": "dance-swagbounce", "duckwalk": "dance-duckwalk", "pennywise": "dance-pennywise",
    "floorsleeping": "idle-floorsleeping", "sexy": "dance-sexy", "laidback": "sit-idle-laidBack",
    "ghost": "emote-ghost-idle", "annoyed": "idle-loop-annoyed", "touch": "dance-touch",
    "jinglebell": "dance-jinglebell", "space": "idle-space", "metal": "dance-metal",
    "flex": "emoji-flex", "orangejustice": "dance-orangejustice", "shy": "emote-shy2",
    "blowkiss": "emote-blowkisses", "stargazer": "emote-stargazer", "knock": "emote-knocking-screen",
    "curtsy": "emote-curtsy", "slap": "emote-slap", "twerk": "dance-twerk", "singing": "idle_singing",
    "swinging": "idle-dance-swinging", "kawai": "dance-kawai", "pose9": "emote-pose9",
    "tiktok9": "dance-tiktok9", "floss": "dance-floss", "breakdance": "dance-breakdance",
    "wild": "dance-wild", "hipshake": "dance-hipshake", "griddy": "dance-griddy",
    "shrink": "emote-shrink", "lust": "emote-lust", "spiritual": "dance-spiritual",
    "martial": "dance-martial-artist", "hero": "emote-hero", "tiktok2": "dance-tiktok2",
    "popularvibe": "dance-popularvibe", "headball": "emote-headball", "trueheart": "dance-true-heart",
    "cursing": "emoji-cursing", "mine": "dance-mine", "robotic": "dance-robotic",
    "graceful": "emote-graceful", "meditate": "emote-meditate-idle", "repos": "sit-idle-cute",
    "kpop": "emote-kpop-dance1", "photo": "emote-collab-photo-left"
}
EMOTES_LISTE = list(EMOTES.values())

# ==========================
# MAIN BOT CLASS
# ==========================
class Bot(BaseBot):
    emote_tasks = {}
    current_riddle = None
    
    following_user_id = None
    follow_task = None

    async def start_loop(self, user_id: str, emote_name: str):
        if user_id in self.emote_tasks:
            self.emote_tasks[user_id].cancel()
        async def loop_emote():
            while True:
                try: 
                    await self.highrise.send_emote(emote_name, user_id)
                except: 
                    pass
                await asyncio.sleep(5)
        self.emote_tasks[user_id] = asyncio.create_task(loop_emote())

    async def bot_life_loop(self):
        while True:
            if self.following_user_id is None:
                try:
                    random_x = round(random.uniform(1.0, 15.0), 2)
                    random_z = round(random.uniform(1.0, 15.0), 2)
                    target_position = Position(x=random_x, y=0.0, z=random_z, facing="FrontRight")
                    await self.highrise.walk_to(target_position)
                    await asyncio.sleep(3)
                    await self.highrise.send_emote(random.choice(EMOTES_LISTE))
                except Exception as e:
                    print(f"Movement error: {e}")
            await asyncio.sleep(15)

    async def follow_loop(self):
        while self.following_user_id:
            try:
                room_users = await self.highrise.get_room_users()
                for user, position in room_users.content:
                    if user.id == self.following_user_id:
                        if isinstance(position, Position):
                            target_pos = Position(x=position.x + 0.5, y=position.y, z=position.z, facing="FrontLeft")
                            await self.highrise.walk_to(target_pos)
                        break
            except Exception as e:
                print(f"Follow error: {e}")
            await asyncio.sleep(2.5)

    async def on_start(self, session_metadata: SessionMetadata):
        print("🤖 Bot connected successfully!")
        await self.highrise.chat("✅ <#AAFFAA>Leviae Ultimate is online! Type <#FFD700>!help<#AAFFAA>.")
        asyncio.create_task(self.bot_life_loop())

    async def on_user_join(self, user: User, position: Position):
        await self.highrise.chat(f"👋 Welcome mon copain <#00BFFF>{user.username}<#FFFFFF>! Type <#FFD700>!help")

    async def on_user_leave(self, user: User):
        if user.id == self.following_user_id:
            self.following_user_id = None
            if self.follow_task:
                self.follow_task.cancel()
            await self.highrise.chat("🚶 La personne suivie a quitté le salon. Arrêt du suivi.")

    async def on_tip(self, sender: User, receiver: User, tip: int):
        if receiver.username.lower() == BOT_USERNAME.lower():
            await self.highrise.chat(f"💎 Thank you <#FFD700>{sender.username}<#FFFFFF> for the tip of <#FF79C6>{tip} gold<#FFFFFF>!")
            await self.start_loop(sender.id, "idle-dance-casual")

    async def on_chat(self, user: User, message: str):
        text = message.lower().strip()

        if self.current_riddle and text == self.current_riddle["answer"]:
            await self.highrise.chat(f"🎉 <#AAFFAA>Correct! @{user.username} found the answer: <#FFFFFF>{self.current_riddle['answer'].upper()}!")
            self.current_riddle = None
            return

        if text.isdigit():
            index = int(text) - 1
            if 0 <= index < len(EMOTES_LISTE):
                await self.start_loop(user.id, EMOTES_LISTE[index])
                return

        if text.startswith("!"):
            emote_name = text[1:]
            
            # Commande d'aide
            if emote_name == "help":
                await self.highrise.chat("ℹ️ Envoyez un numéro pour danser, ou écrivez !riddle pour jouer !")
                return

            # Commande d'énigme
            if emote_name == "riddle":
                self.current_riddle = random.choice(RIDDLES)
                await self.highrise.chat(f"🧠 Énigme : {self.current_riddle['question']}")
                return

            # ==========================================
            # NOUVELLE COMMANDE : MODIFIER LA BIO
            # Usage dans le chat : !bio Nouveau texte ici
            # ==========================================
            if message.startswith("!bio "):
                # On vérifie si c'est bien l'owner (toi) qui tape la commande
                if user.id in OWNERS:
                    # On extrait le texte après le "!bio "
                    nouvelle_bio = message[5:].strip()
                    try:
                        await self.highrise.change_profile(bio=nouvelle_bio)
                        await self.highrise.chat(f"📝 <#AAFFAA>La bio du bot a été mise à jour : \"{nouvelle_bio}\"")
                    except Exception as e:
                        await self.highrise.chat(f"❌ Erreur lors de la mise à jour de la bio.")
                        print(f"Erreur changement bio: {e}")
                else:
                    await self.highrise.chat("❌ Seul le créateur du bot peut utiliser cette commande.")
                return

            # Si c'est une émote de la liste
            if emote_name in EMOTES:
                await self.start_loop(user.id, EMOTES[emote_name])
                return
