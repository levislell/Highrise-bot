import os, asyncio, random, sys, time
from threading import Thread
from flask import Flask
from highrise import BaseBot, User, Position
from highrise.models import SessionMetadata

# ==========================
# 1. SERVEUR WEB (Pour Render Free 24h/24)
# ==========================
app = Flask('')

@app.route('/')
def home(): 
    return "Le bot Leviae Pro Ultimate fonctionne en ligne !"

def run_web_server(): 
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

Thread(target=run_web_server).start()
# ==========================
# 2. CONFIGURATION GENERALE
# ==========================
BOT_USERNAME = "leviae"
OWNERS = ["65592020383c55ed5c45aabd"]
MODERATORS = ["65592020383c55ed5c45aabd"]
VIP_LIST = [] 
CHAT_LOCKED = False 
INSULTES_LISTE = ["fdp", "con", "salope"]
USER_SPAM_TRACKER = {}
# ==========================
# 3. PHRASES ET JEUX AUTOMATIQUES (Textes en anglais)
# ==========================
CHATBOT_RESPONSES = [
    "Need help? Type <#FFD700>!help<#FFFFFF> ! 🤖",
    "Hope you are having a wonderful time! ✨",
    "Yes? I am Leviae, the official bot! 🎵",
    "What's up? Send the exact name of an emote to loop it! 💃"
]
GREETING_RESPONSES = ["Hello! 👋", "Hi there! 🎉", "Welcome! 🌟"]
RIDDLES = [
    {"question": "What has hands but cannot clap?", "answer": "clock"},
    {"question": "What has to be broken before you can use it?", "answer": "egg"},
    {"question": "I’m tall when I’m young, and I’m short when I’m old. What am I?", "answer": "candle"}
]
# ==========================
# 4. LISTE DES ÉMOTES
# ==========================
EMOTES = {
    "swagbounce": "dance-swagbounce", "duckwalk": "dance-duckwalk", "pennywise": "dance-pennywise",
    "floorsleeping": "idle-floorsleeping", "laidback": "sit-idle-laidBack",
    "ghost": "emote-ghost-idle", "annoyed": "idle-loop-annoyed", "touch": "dance-touch",
    "jinglebell": "dance-jinglebell", "space": "idle-space", "metal": "dance-metal",
    "flex": "emoji-flex", "orangejustice": "dance-orangejustice", "shy": "emote-shy2",
    "blowkiss": "emote-blowkisses", "stargazer": "emote-stargazer", "knock": "emote-knocking-screen",
    "curtsy": "emote-curtsy", "slap": "emote-slap", "singing": "idle_singing",
    "swinging": "idle-dance-swinging", "kawai": "dance-kawai", "pose9": "emote-pose9",
    "tiktok9": "dance-tiktok9", "floss": "dance-floss", "breakdance": "dance-breakdance",
    "wild": "dance-wild", "hipshake": "dance-hipshake", "griddy": "dance-griddy",
    "shrink": "emote-shrink", "spiritual": "dance-spiritual",
    "martial": "dance-martial-artist", "hero": "emote-hero", "tiktok2": "dance-tiktok2",
    "popularvibe": "dance-popularvibe", "headball": "emote-headball", "trueheart": "dance-true-heart",
    "mine": "dance-mine", "robotic": "dance-robotic",
    "graceful": "emote-graceful", "meditate": "emote-meditate-idle", "frollicking": "emote-frollicking",
    "ballet": "dance-ballet", "woah": "dance-woah", "shuffle": "dance-shuffle",
    "frog": "emote-frog", "lying": "emoji-lying", "laughing2": "emote-laughing2",
    "boxer": "emote-boxer", "tiktok10": "dance-tiktok10", "attention": "emote-attention",
    "dab": "emote-dab", "timejump": "emote-timejump", "puppet": "emote-puppet",
    "aerobics": "dance-aerobics", "guitar": "idle-guitar",
    "tiktok7": "idle-dance-tiktok7", "tiktok11": "dance-tiktok11", "tapdance": "idle-loop-tapdance",
    "pose10": "emote-pose10", "scared": "emoji-scared", "arrogance": "emoji-arrogance",
    "wrong": "dance-wrong", "halo": "emoji-halo", "anime": "dance-anime",
    "hyped": "emote-hyped", "boo": "emote-boo", "trampoline": "emote-trampoline",
    "emojighost": "emoji-ghost", "float": "emote-float", "sleigh": "emote-sleigh",
    "cheerleader": "dance-cheerleader", "ninjarun": "emote-ninjarun", "gangnam": "emote-gangnam",
    "snake": "emote-snake", "pinguin": "dance-pinguin", "loopaerobics": "idle-loop-aerics",
    "howl": "emote-howl", "launch": "emote-launch", "creepypuppet": "dance-creepypuppet",
    "gravity": "emote-gravity", "confused": "emote-confused", "creepycute": "emote-creepycute",
    "smoothwalk": "dance-smoothwalk", "nervous": "idle-nervous", "gordonshuffle": "emote-gordonshuffle",
    "rofl": "emote-rofl", "icecream": "dance-icecream", "celebrate": "emote-celebrate",
    "panic": "emote-panic", "punkguitar": "emote-punkguitar", "singleladies": "dance-singleladies",
    "punch": "emoji-punch", "shoppingcart": "dance-shoppingcart",
    "tiktok4": "idle-dance-tiktok4", "nightfever": "emote-nightfever", "snowangel": "emote-snowangel",
    "headblowup": "emote-headblowup", "roll": "emote-roll", "open": "sit-open",
    "floorsleeping2": "idle-floorsleeping2", "teleporting": "emote-teleporting", "hearteyes": "emote-hearteyes",
    "tiktok8": "dance-tiktok8", "angry": "idle-angry", "astronaut": "emote-astronaut",
    "relaxed": "sit-relaxed", "fashionista": "emote-fashionista", "kissing": "emote-kissing",
    "rainbow": "emote-rainbow", "toilet": "idle-toilet", "snowball": "emote-snowball",
    "peekaboo": "peekaboo", "frustrated": "emote-frustrated", "jetpack": "emote-jetpack",
    "looping": "emote-looping", "idlehowl": "idle-howl", "emotetapdance": "emote-tapdance",
    "death": "emote-death", "secrethandshake": "emote-secrethandshake", "fruity": "dance-fruity",
    "zombie": "dance-zombie", "robot": "emote-robot", "zombierun": "emote-zombierun",
    "charging": "emote-charging", "fighter": "idle-fighter", "kicking": "emote-kicking",
    "layingdown": "idle_layingdown"
}
EMOTES_LISTE = list(EMOTES.values())
# ==========================
# 5. ENTRÉE DE LA CLASSE DU BOT (Logique et Commandes)
# ==========================
class Bot(BaseBot):
    emote_tasks, current_riddle, following_user_id, follow_task = {}, None, None, None
    bot_position = Position(x=0.0, y=0.0, z=0.0, facing="FrontRight")

    async def start_loop(self, uid, name):
        if uid in self.emote_tasks:
            self.emote_tasks[uid].cancel()
            try:
                await self.emote_tasks[uid]
            except asyncio.CancelledError:
                pass

        async def loop():
            while True:
                try: 
                    await self.highrise.send_emote(name, uid)
                except Exception as e: 
                    print(f"Emote loop error: {e}")
                await asyncio.sleep(5)
                
        self.emote_tasks[uid] = asyncio.create_task(loop())

    async def bot_life_loop(self):
        while True:
            if self.following_user_id is None:
                try:
                    self.bot_position = Position(x=round(random.uniform(1.0, 15.0), 2), y=0.0, z=round(random.uniform(1.0, 15.0), 2), facing="FrontRight")
                    await self.highrise.walk_to(self.bot_position)
                    await asyncio.sleep(3)
                    await self.highrise.send_emote(random.choice(EMOTES_LISTE))
                except Exception as e:
                    print(f"Bot life error: {e}")
            await asyncio.sleep(15)

    async def follow_loop(self):
        while self.following_user_id is not None:
            try:
                users = await self.highrise.get_room_users()
                for u, pos in users.content:
                    if u.id == self.following_user_id and isinstance(pos, Position):
                        self.bot_position = Position(x=pos.x + 0.5, y=pos.y, z=pos.z, facing="FrontLeft")
                        await self.highrise.walk_to(self.bot_position)
            except Exception as e:
                print(f"Follow loop error: {e}")
            await asyncio.sleep(2.5)

    async def on_start(self, session_metadata: SessionMetadata):
        try: 
            # Configuration exacte de votre biographie personnelle
            await self.highrise.set_bio("Créé par @gentleman_0")
            print("Bio mise à jour avec succès : Créé par @gentleman_0")
        except Exception as e: 
            print(f"Failed to update bio: {e}")
            
        await self.highrise.chat("✅ <#AAFFAA>Leviae Ultimate is online! Type !help.")
        asyncio.create_task(self.bot_life_loop())
        self.follow_task = asyncio.create_task(self.follow_loop())

    async def on_user_join(self, user: User, position: Position):
        if user.id in VIP_LIST:
            await self.highrise.chat(f"👑 <#FFD700>[VIP] Please warmly welcome @{user.username} into the room!<#FFFFFF>")
        else:
            await self.highrise.chat(f"{random.choice(GREETING_RESPONSES)} @{user.username}! Type !help")

    async def on_user_leave(self, user: User):
        if user.id == self.following_user_id:
            self.following_user_id = None
        if user.id in self.emote_tasks:
            self.emote_tasks[user.id].cancel()
            del self.emote_tasks[user.id]

    async def on_chat(self, user: User, message: str) -> None:
        global CHAT_LOCKED
        nettoye = message.lower().strip()

        for insulte in INSULTES_LISTE:
            if insulte in nettoye:
                try:
                    await self.highrise.chat(f"⚠️ Keep the chat clean @{user.username}!")
                except: pass
                return

        if CHAT_LOCKED and user.id not in OWNERS and user.id not in MODERATORS:
            return

        if nettoye == "!stop":
            if user.id in self.emote_tasks:
                self.emote_tasks[user.id].cancel()
                del self.emote_tasks[user.id]
                await self.highrise.chat(f"@{user.username}, emote loop stopped.")
            return

        if nettoye in EMOTES:
            await self.start_loop(user.id, EMOTES[nettoye])
            return

        if nettoye == "!help":
            await self.highrise.chat("🤖 [Leviae Help] Commands: Send any emote name to loop it. Use !stop to end. Other: !riddle, !chat, !follow, !unstuck")
            if user.id in OWNERS or user.id in MODERATORS:
                await self.highrise.chat("🛡️ Admin Commands: !lock, !unlock, !come")
            return

        if nettoye == "!chat":
            await self.highrise.chat(random.choice(CHATBOT_RESPONSES))
            return

        if nettoye == "!riddle":
            self.current_riddle = random.choice(RIDDLES)
            await self.highrise.chat(f"❓ [Riddle] {self.current_riddle['question']}")
            return

        if self.current_riddle and nettoye == self.current_riddle['answer']:
            await self.highrise.chat(f"🎉 Well done @{user.username}! The correct answer was indeed: {self.current_riddle['answer']}")
            self.current_riddle = None
            return

        if nettoye == "!follow":
            self.following_user_id = user.id
            await self.highrise.chat(f"🏃 Following you now @{user.username}!")
            return

        if nettoye == "!unstuck":
            self.following_user_id = None
            self.bot_position = Position(x=5.0, y=0.0, z=5.0, facing="FrontRight")
            await self.highrise.walk_to(self.bot_position)
            await self.highrise.chat(f"✅ Position reset for the bot.")
            return

        if user.id in OWNERS or user.id in MODERATORS:
            if nettoye == "!come":
                self.following_user_id = None
                try:
                    room_users = await self.highrise.get_room_users()
                    for u, pos in room_users.content:
                        if u.id == user.id and isinstance(pos, Position):
                            self.bot_position = Position(x=pos.x, y=pos.y, z=pos.z, facing="FrontRight")
                            await self.highrise.walk_to(self.bot_position)
                            await self.highrise.chat("Coming over right now!")
                except Exception as e:
                    print(f"Error on !come: {e}")
                return

            if nettoye == "!lock":
                CHAT_LOCKED = True
                await self.highrise.chat("🔒 Room chat is now locked. Only staff can talk.")
                return

            if nettoye == "!unlock":
                CHAT_LOCKED = False
                await self.highrise.chat("🔓 Room chat is now unlocked.")
                return
