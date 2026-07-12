import os
import asyncio
import random
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
# EMOTES DICTIONARY
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
    "graceful": "emote-graceful", "meditate": "emote-meditate-idle", "repos": "sit-idle-cute"
}
EMOTES_LISTE = list(EMOTES.values())
# ==========================
# MAIN BOT CLASS
# ==========================
class Bot(BaseBot):
    emote_tasks = {}
    current_riddle = None

    async def start_loop(self, user_id: str, emote_name: str):
        if user_id in self.emote_tasks:
            self.emote_tasks[user_id].cancel()
        async def loop_emote():
            while True:
                try: await self.highrise.send_emote(emote_name, user_id)
                except: pass
                await asyncio.sleep(5)
        self.emote_tasks[user_id] = asyncio.create_task(loop_emote())

    async def bot_life_loop(self):
        while True:
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

    async def on_start(self, session_metadata: SessionMetadata):
        print("🤖 Bot connected successfully!")
        await self.highrise.chat("✅ <#AAFFAA>Leviae Ultimate is online! Type <#FFD700>!help<#AAFFAA>.")
        asyncio.create_task(self.bot_life_loop())

    async def on_user_join(self, user: User, position: Position):
        await self.highrise.chat(f"👋 Welcome mon copain <#00BFFF>{user.username}<#FFFFFF>! Type <#FFD700>!help")

    async def on_tip(self, sender: User, receiver: User, tip: int):
        if receiver.username.lower() == BOT_USERNAME.lower():
            await self.highrise.chat(f"💎 Thank you <#FFD700>{sender.username}<#FFFFFF> for the tip of <#FF79C6>{tip} gold<#FFFFFF>!")
            await self.start_loop(sender.id, "idle-dance-casual")

    async def on_chat(self, user: User, message: str):
        text = message.lower().strip()
        parts = message.split()

        if self.current_riddle and text == self.current_riddle["answer"]:
            await self.highrise.chat(f"🎉 <#AAFFAA>Correct! @{user.username} found the answer: <#FFFFFF>{self.current_riddle['answer'].upper()}!")
            self.current_riddle = None
            return

        if text.isdigit():
            index = int(text) - 1
            if 0 <= index < len(EMOTES_LISTE):
                await self.start_loop(user.id, EMOTES_LISTE[index])
                return

        if text in EMOTES:
            await self.start_loop(user.id, EMOTES[text])
            return

        if text == "stop":
            if user.id in self.emote_tasks:
                self.emote_tasks[user.id].cancel()
                del self.emote_tasks[user.id]
                await self.highrise.chat(f"⛔ Dance loop stopped for {user.username}.")
            else:
                await self.highrise.chat("❌ You don't have any active loops.")
            return

        if text == "!help":
            menu = (
                "<#FFD700>━━━ Ultimate Help Menu ━━━\n"
                "<#FF79C6>🎮 !help fun <#FFFFFF>: Games & Fun\n"
                "<#9370DB>🎵 !emotes <#FFFFFF>: Show all 51 emotes\n"
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
                "• !clearchat\n"
                "• !say [text] <#AFAFAF>(Make bot speak)\n"
                "• !wallet <#AFAFAF>(Check bot gold balance)\n"
                "• !bio [text] <#AFAFAF>(Change bot profile bio)"
            )
            await self.highrise.chat(menu_mod)
            return

        elif text == "!riddle":
            if self.current_riddle:
                await self.highrise.chat(f"🧠 Active riddle: <#FF79C6>{self.current_riddle['question']}")
            else:
                self.current_riddle = random.choice(RIDDLES)
                await self.highrise.chat(f"🧠 <#FFD700>Riddle: <#FFFFFF>{self.current_riddle['question']}")

        elif text == "!coinflip":
            result = random.choice(["Heads 🪙", "Tails 🪙"])
            await self.highrise.chat(f"🎰 @{user.username} flipped a coin and got: <#FFD700>{result}")

        elif text.startswith("!love"):
            if len(parts) < 2:
                await self.highrise.chat("❌ Usage: !love [username]")
            else:
                target = parts[1].replace("@", "")
                percent = random.randint(0, 100)
                heart = "❤️" if percent > 50 else "💔"
                await self.highrise.chat(f"💞 Compatibility between @{user.username} & @{target}: <#FF79C6>{percent}% {heart}")

        elif text == "!emotes":
            liste_numerotee = [f"{i}.{nom}" for i, nom in enumerate(EMOTES.keys(), start=1)]
            await self.highrise.chat(f"💃 <#9370DB>Emotes: <#FFFFFF>{', '.join(liste_numerotee)}")

        elif text == "!id":
            await self.highrise.chat(f"👤 Your Highrise ID: <#00BFFF>{user.id}")

        elif text == "!players":
            room_users = await self.highrise.get_room_users()
            await self.highrise.chat(f"📢 Active players in this room: <#AAFFAA>{len(room_users)}")

        elif text.startswith("!say") or text.startswith("!kick") or text.startswith("!ban") or text.startswith("!mute") or text == "!clearchat" or text == "!wallet" or text.startswith("!bio"):
            if user.id not in OWNERS and user.id not in MODERATORS:
                await self.highrise.chat("❌ Permission denied.")
                return

            if text.startswith("!say"):
                content = message[4:].strip()
                if content: await self.highrise.chat(content)

            elif text == "!clearchat":
                for _ in range(10): await self.highrise.chat(" ")
                await self.highrise.chat("🧹 <#AAFFAA>Chat cleared by staff.")

            elif text == "!wallet":
                wallet = await self.highrise.get_wallet()
                gold = wallet.content.amount if wallet.content else 0
                await self.highrise.chat(f"💰 Bot Wallet Balance: <#FFD700>{gold} Gold")

            elif text.startswith("!bio"):
                new_bio = message[4:].strip()
                if new_bio:
                    try:
                        await self.highrise.change_user_bio(new_bio)
                        await self.highrise.chat("📝 Bot bio updated successfully!")
                    except Exception as e: await self.highrise.chat(f"❌ Error: {str(e)}")

            elif text.startswith("!kick") or text.startswith("!ban") or text.startswith("!mute"):
                if len(parts) < 2:
                    await self.highrise.chat("❌ Missing username. Example: !kick @username")
                    return
                
                target_user = parts[1].replace("@", "")
                users = await self.highrise.get_room_users()
                
                for u, pos in users:
                    if u.username.lower() == target_user.lower():
                        if text.startswith("!kick"):
                            await self.highrise.kick_user(u.id)
                            await self.highrise.chat(f"🚪 {u.username} has been kicked out.")
                        elif text.startswith("!ban"):
                            await self.highrise.ban_user(u.id, action="ban")
                            await self.highrise.chat(f"🔨 {u.username} has been permanently banned.")
                        elif text.startswith("!mute"):
                            minutes = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 5
                            await self.highrise.mute_user(u.id, minutes * 60)
                            await self.highrise.chat(f"🤫 {u.username} has been muted for {minutes} minutes.")
                        break

        elif "bot" in text or "leviae" in text:
            await self.highrise.chat(random.choice(CHATBOT_RESPONSES))
        elif any(word in text for word in ["hello", "hi", "hey"]):
            await self.highrise.chat(f"{random.choice(GREETING_RESPONSES)} @{user.username}")

# ==========================
# EXECUTION
# ==========================
def start_bot():
    room_id = os.environ.get("ROOM_ID", "65e361f8aef42a7b0ed22029")
    api_token = os.environ.get("API_TOKEN", "f1f9d1cae9063a6a0a50ccfc95d0864005990c820d5f7dcf3463a6a11ecd3cfa")

    from highrise.__main__ import ARGS
    from highrise.network import BotLoop

    ARGS.bot_path = "main:Bot"
    ARGS.room_id = room_id
    ARGS.api_token = api_token

    bot_loop = BotLoop()
    bot_loop.run()

if __name__ == "__main__":
    Thread(target=run_web_server).start()
    start_bot()