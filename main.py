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
    
    # Variables pour la fonction Follow (Suivi)
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
            # Ne bouge pas de manière aléatoire si le bot est en train de suivre quelqu'un
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
        """Boucle permettant au bot de suivre les déplacements d'un joueur en temps réel"""
        while self.following_user_id:
            try:
                room_users = await self.highrise.get_room_users()
                for user, position in room_users.content:
                    if user.id == self.following_user_id:
                        if isinstance(position, Position):
                            # On calcule une position juste à côté du joueur ciblé
                            target_pos = Position(x=position.x + 0.5, y=position.y, z=position.z, facing="FrontLeft")
                            await self.highrise.walk_to(target_pos)
                        break
            except Exception as e:
                print(f"Follow error: {e}")
            await asyncio.sleep(2.5)

    async def on_start(self, session_metadata: SessionMetadata):
        print("🤖 Bot connected successfully!")
        try:
            # Modification automatique du profil avec la mention de votre pseudo créateur
            await self.highrise.change_profile(bio="Bot créateur @gentleman_0")
            print("📝 Bio mise à jour avec succès !")
        except Exception as e:
            print(f"Erreur mise à jour bio: {e}")
            
        await self.highrise.chat("✅ <#AAFFAA>Leviae Ultimate is online! Type <#FFD700>!help<#AAFFAA>.")
        asyncio.create_task(self.bot_life_loop())

    async def on_user_join(self, user: User, position: Position):
        await self.highrise.chat(f"👋 Welcome mon copain <#00BFFF>{user.username}<#FFFFFF>! Type <#FFD700>!help")

    async def on_user_leave(self, user: User):
        # Si la personne suivie quitte le salon, le bot arrête le suivi automatiquement
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
        parts = message.split()

        # Réponses aux énigmes actives
        if self.current_riddle and text == self.current_riddle["answer"]:
            await self.highrise.chat(f"🎉 <#AAFFAA>Correct! @{user.username} found the answer: <#FFFFFF>{self.current_riddle['answer'].upper()}!")
            self.current_riddle = None
            return

        # Déclenchement d'émote par numéro (sans préfixe)
        if text.isdigit():
            index = int(text) - 1
            if 0 <= index < len(EMOTES_LISTE):
                await self.start_loop(user.id, EMOTES_LISTE[index])
                return

        # Déclenchement d'émote par son nom (avec point d'exclamation, ex: !photo)
        if text.startswith("!"):
            emote_name = text[1:]  # Enlève le "!" pour lire le nom
            if emote_name in EMOTES:
                await self.start_loop(user.id, EMOTES[emote_name])
                return

        # Gestion du système de suivi (Follow / Unfollow) [MODÉRATEURS & OWNERS]
        if text.startswith("!follow"):
            if user.id in MODERATORS or user.id in OWNERS:
                if len(parts) > 1:
                    target = parts[1].replace("@", "").lower()
                    
                    if target == "stop":
                        self.following_user_id = None
                        if self.follow_task:
                            self.follow_task.cancel()
                        await self.highrise.chat("⛔ Arrêt du suivi.")
                        return
                        
                    # Recherche de l'utilisateur ciblé dans le salon
                    room_users = await self.highrise.get_room_users()
                    found_user = None
                    for u, pos in room_users.content:
                        if u.username.lower() == target:
                            found_user = u
                            break
                    
                    if found_user:
                        self.following_user_id = found_user.id
                        if self.follow_task:
                            self.follow_task.cancel()
                        self.follow_task = asyncio.create_task(self.follow_loop())
                        await self.highrise.chat(f"🚶 Je commence à suivre @{found_user.username} !")
                    else:
                        await self.highrise.chat("❌ Cet utilisateur n'est pas dans la pièce.")
                else:
                    await self.highrise.chat("💡 Usage: !follow [username] ou !follow stop")
            return

        # Arrêt des boucles de danse
        if text == "stop":
            if user.id in self.emote_tasks:
                self.emote_tasks[user.id].cancel()
                del self.emote_tasks[user.id]
                await self.highrise.chat(f"⛔ Dance loop stopped for {user.username}.")
            else:
                await self.highrise.chat("❌ You don't have any active loops.")
            return

        # Commandes d'aide textuelles
        if text == "!help":
            menu = (
                "<#FFD700>━━━ Ultimate Help Menu ━━━\n"
                "<#FF79C6>🎮 !help fun <#FFFFFF>: Games & Fun\n"
                "<#9370DB>🎵 !emotes <#FFFFFF>: Show all 53 emotes\n"
                "<#00BFFF>📢 !help room <#FFFFFF>: Room info & Utils\n"
                "<#FF4500>🛡️ !help mod <#FFFFFF>: Moderator actions"
            )
            await self.highrise.chat(menu)
            return

        elif text == "!help fun":
            menu_fun = (
                "<#FF79C6>━━━ Fun & Games ━━━\n"
                "• <#FFFFFF>!riddle <#AFAFAF>: Launch a riddle game\n"
                "• !coinflip <#AFAFAF>: Play heads or tails\n"
                "• !love [username] <#AFAFAF>: Love compatibility test\n"
                "• Type <#FF4500>stop<#FFFFFF> to freeze dancing"
            )
            await self.highrise.chat(menu_fun)
            return

        elif text == "!help room":
            menu_room = (
                "<#00BFFF>━━━ Room & Utilities ━━━\n"
                "• <#FFFFFF>!players <#AFAFAF>: Count active users\n"
                "• !id <#AFAFAF>: Get your user ID"
            )
            await self.highrise.chat(menu_room)
            return

        elif text == "!help mod":
            menu_mod = (
                "<#FF4500>━━━ Mod Commands ━━━\n"
                "• <#FFFFFF>!kick [username]\n"
                "• !ban [username]\n"
                "• !mute [username] [minutes]\n"
                "• !follow [username] <#AFAFAF>(Suivre quelqu'un)\n"
                "• !follow stop <#AFAFAF>(Arrêter le suivi)\n"
                "• !say [text]\n"
                "• !wallet\n"
                "• !bio [text]"
            )
            await self.highrise.chat(menu_mod)
            return

        # Commande Jeu de l'énigme
        elif text == "!riddle":
            if self.current_riddle:
                await self.highrise.chat(f"🧠 Active riddle is already running! Question: {self.current_riddle['question']}")
            else:
                self.current_riddle = random.choice(RIDDLES)
                await self.highrise.chat(f"🧠 [RIDDLE]: {self.current_riddle['question']} 🤔")
            return

        # Commande Pile ou Face
        elif text == "!coinflip":
            result = random.choice(["HEADS 🪙", "TAILS 🪙"])
            await self.highrise.chat(f"🪙 {user.username} flipped a coin and got: <#FFD700>{result}<#FFFFFF>!")
            return

        # Commande Taux d'amour
        elif text.startswith("!love"):
            if len(parts) > 1:
                target = parts[1]
                percent = random.randint(0, 100)
                await self.highrise.chat(f"❤️ Love Test between {user.username} & {target}: <#FF79C6>{percent}%<#FFFFFF>!")
            else:
                await self.highrise.chat("❤️ Usage: !love [username]")
            return

        # Commande Liste des émoticones
        elif text == "!emotes":
            await self.highrise.chat("🎵 Ajoutez un '!' devant le nom de l'émote pour danser ! Exemples: !photo, !kpop, !twerk ou tapez son numéro.")
            return

        # Commande de Modération : Faire parler le bot
        elif text.startswith("!say "):
            if user.id in MODERATORS or user.id in OWNERS:
                say_text = message[5:]
                await self.highrise.chat(say_text)
            return

        # Commande de Modération : Changer la bio à la volée
        elif text.startswith("!bio "):
            if user.id in OWNERS:
                new_bio = message[5:]
                try:
                    await self.highrise.change_profile(bio=new_bio)
                    await self.highrise.chat("✅ Bio updated via command!")
                except Exception as e:
                    await self.highrise.chat(f"❌ Error updating bio: {e}")
            return

        # Commande de Modération : Consulter le portefeuille
        elif text == "!wallet":
            if user.id in OWNERS:
                try:
                    wallet = await self.highrise.get_wallet()
                    await self.highrise.chat(f"💰 Bot Wallet Balance: {wallet.content.amount} gold.")
                except Exception as e:
                    await self.highrise.chat(f"❌ Error fetching wallet: {e}")
            return
