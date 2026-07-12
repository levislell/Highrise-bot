import os, asyncio, random, sys, time
from threading import Thread
from flask import Flask
from highrise import BaseBot, User, Position
from highrise.models import SessionMetadata

# ==========================
# SERVEUR WEB (Pour Render Free 24h/24)
# ==========================
app = Flask('')
@app.route('/')
def home(): 
    return "Le bot Leviae Pro Ultimate fonctionne en ligne !"

def run_web_server(): 
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

Thread(target=run_web_server).start()

# ==========================
# CONFIGURATION GENERALE
# ==========================
BOT_USERNAME = "leviae"
OWNERS = ["65592020383c55ed5c45aabd"]
MODERATORS = ["65592020383c55ed5c45aabd"]
VIP_LIST = [] 
CHAT_LOCKED = False 
INSULTES_LISTE = ["fdp", "con", "salope"]
USER_SPAM_TRACKER = {}

# ==========================
# PHRASES ET JEUX AUTOMATIQUES
# ==========================
CHATBOT_RESPONSES = [
    "Besoin d'aide ? Écris <#FFD700>!help<#FFFFFF> ! 🤖",
    "J'espère que vous passez un super moment ! ✨",
    "Oui ? Je suis Leviae, le bot officiel ! 🎵",
    "Quoi de neuf ? Envoie le nom exact d'une émote ou son numéro ! 💃"
]
GREETING_RESPONSES = ["Bonjour ! 👋", "Salut ! 🎉", "Bienvenue ! 🌟"]
RIDDLES = [
    {"question": "Aiguilles mais ne coud pas ?", "answer": "montre"},
    {"question": "À casser avant usage ?", "answer": "oeuf"},
    {"question": "Grand jeune, petit vieux ?", "answer": "bougie"}
]
# ==========================
# LISTE DES ÉMOTES - SECTION A
# ==========================
EMOTES = {
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
    "graceful": "emote-graceful", "meditate": "emote-meditate-idle", "frollicking": "emote-frollicking",
    "ballet": "dance-ballet", "woah": "dance-woah", "shuffle": "dance-shuffle",
    "frog": "emote-frog", "lying": "emoji-lying", "laughing2": "emote-laughing2",
    "boxer": "emote-boxer", "tiktok10": "dance-tiktok10", "attention": "emote-attention",
    "dab": "emote-dab", "timejump": "emote-timejump", "puppet": "emote-puppet",
    "gagging": "emoji-gagging", "aerobics": "dance-aerobics", "guitar": "idle-guitar",
    "tiktok7": "idle-dance-tiktok7", "tiktok11": "dance-tiktok11", "tapdance": "idle-loop-tapdance",
    "pose10": "emote-pose10", "scared": "emoji-scared", "arrogance": "emoji-arrogance"
}
# ==========================
# LISTE DES ÉMOTES - SECTION B
# ==========================
EMOTES_SUITE = {
    "wrong": "dance-wrong", "halo": "emoji-halo", "anime": "dance-anime",
    "hyped": "emote-hyped", "boo": "emote-boo", "trampoline": "emote-trampoline",
    "emojighost": "emoji-ghost", "float": "emote-float", "sleigh": "emote-sleigh",
    "cheerleader": "dance-cheerleader", "ninjarun": "emote-ninjarun", "gangnam": "emote-gangnam",
    "snake": "emote-snake", "pinguin": "dance-pinguin", "loopaerobics": "idle-loop-aerobics",
    "howl": "emote-howl", "launch": "emote-launch", "creepypuppet": "dance-creepypuppet",
    "gravity": "emote-gravity", "confused": "emote-confused", "creepycute": "emote-creepycute",
    "smoothwalk": "dance-smoothwalk", "nervous": "idle-nervous", "gordonshuffle": "emote-gordonshuffle",
    "rofl": "emote-rofl", "icecream": "dance-icecream", "celebrate": "emote-celebrate",
    "panic": "emote-panic", "punkguitar": "emote-punkguitar", "singleladies": "dance-singleladies",
    "punch": "emoji-punch", "shoppingcart": "dance-shoppingcart", "poop": "emoji-poop",
    "tiktok4": "idle-dance-tiktok4", "nightfever": "emote-nightfever", "snowangel": "emote-snowangel",
    "headblowup": "emote-headblowup", "roll": "emote-roll", "open": "sit-open",
    "floorsleeping2": "idle-floorsleeping2", "teleporting": "emote-teleporting", "hearteyes": "emote-hearteyes",
    "tiktok8": "dance-tiktok8", "angry": "idle-angry", "astronaut": "emote-astronaut",
    "relaxed": "sit-relaxed", "fashionista": "emote-fashionista", "kissing": "emote-kissing",
    "rainbow": "emote-rainbow", "toilet": "idle-toilet", "snowball": "emote-snowball",
    "peekaboo": "emote-peekaboo", "frustrated": "emote-frustrated", "jetpack": "emote-jetpack",
    "looping": "emote-looping", "idlehowl": "idle-howl", "emotetapdance": "emote-tapdance",
    "death": "emote-death", "secrethandshake": "emote-secrethandshake", "fruity": "dance-fruity",
    "zombie": "dance-zombie", "robot": "emote-robot", "zombierun": "emote-zombierun",
    "charging": "emote-charging", "fighter": "idle-fighter", "kicking": "emote-kicking",
    "layingdown": "idle_layingdown"
}
EMOTES.update(EMOTES_SUITE)
EMOTES_LISTE = list(EMOTES.values())

# ==========================
# ENTRÉE DE LA CLASSE DU BOT
# ==========================
class Bot(BaseBot):
    emote_tasks, current_riddle, following_user_id, follow_task = {}, None, None, None
    bot_position = Position(x=0.0, y=0.0, z=0.0, facing="FrontRight")

    async def start_loop(self, uid, name):
        if uid in self.emote_tasks: self.emote_tasks[uid].cancel()
        async def loop():
            while True:
                try: await self.highrise.send_emote(name, uid)
                except: pass
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
                except: pass
            await asyncio.sleep(15)
    async def follow_loop(self):
        while self.following_user_id is not None:
            try:
                users = await self.highrise.get_room_users()
                for u, pos in users.content:
                    if u.id == self.following_user_id and isinstance(pos, Position):
                        self.bot_position = Position(x=pos.x + 0.5, y=pos.y, z=pos.z, facing="FrontLeft")
                        await self.highrise.walk_to(self.bot_position)
            except: pass
            await asyncio.sleep(2.5)

    async def on_start(self, session_metadata: SessionMetadata):
        try: await self.highrise.change_profile(bio="Créé par @gentleman_0")
        except: pass
        await self.highrise.chat("✅ <#AAFFAA>Leviae Ultimate est en ligne ! Tapez !help.")
        asyncio.create_task(self.bot_life_loop())

    async def on_user_join(self, user: User, position: Position):
        if user.id in VIP_LIST:
            await self.highrise.chat(f"👑 <#FFD700>[VIP] Accueillez chaleureusement @{user.username} qui vient d'entrer !<#FFFFFF>")
        else:
            await self.highrise.chat(f"{random.choice(GREETING_RESPONSES)} @{user.username} ! Écris !help")

    async def on_user_leave(self, user: User):
        if user.id == self.following_user_id:
            self.following_user_id = None
            if self.follow_task: self.follow_task.cancel()

    async def on_tip(self, sender: User, receiver: User, tip: int):
        if receiver.username.lower() == BOT_USERNAME.lower():
            await self.highrise.chat(f"💎 Merci @{sender.username} pour les {tip} golds !")
            await self.start_loop(sender.id, "idle-dance-casual")

    async def on_chat(self, user: User, message: str):
        global CHAT_LOCKED
        text = message.lower().strip()
        now = time.time()
        
        if CHAT_LOCKED and user.id not in OWNERS + MODERATORS: return

        if user.id not in USER_SPAM_TRACKER: USER_SPAM_TRACKER[user.id] = []
        USER_SPAM_TRACKER[user.id] = [t for t in USER_SPAM_TRACKER[user.id] if now - t < 3]
        USER_SPAM_TRACKER[user.id].append(now)

        if len(USER_SPAM_TRACKER[user.id]) > 4 and user.id not in OWNERS + MODERATORS:
            try: await self.highrise.moderate_room(user.id, "mute", 60)
            except: pass
            return

        if any(i in text for i in INSULTES_LISTE) and user.id not in OWNERS + MODERATORS:
            try: await self.highrise.moderate_room(user.id, "kick")
            except: pass
            return

        if self.current_riddle and text == self.current_riddle["answer"]:
            await self.highrise.chat(f"🎉 Gagné ! @{user.username} a trouvé : {self.current_riddle['answer'].upper()} !")
            self.current_riddle = None
            return

        if text.isdigit():
            idx = int(text) - 1
            if 0 <= idx < len(EMOTES_LISTE): await self.start_loop(user.id, EMOTES_LISTE[idx])
            return

        if text in EMOTES:
            await self.start_loop(user.id, EMOTES[text])
            return

        if text.startswith("!"):
            cmd = text[1:]
            
            if cmd == "help":
                await self.highrise.chat("📚 <#FFD700>MENU PRINCIPAL :<#FFFFFF>\nTapez la catégorie :\n🔹 !help animation\n🔹 !help moderation\n🔹 !help jeux\n🔹 !help event\n🔹 !help serveur\n🔹 !help boutique")
                return
            if message.lower() == "!help animation":
                await self.highrise.chat("💃 ANIMATION :\n👉 Écris juste le nom de l'émote (ex: sexy, griddy)\n👉 Chiffre 1 à 147\n👉 !danceall [nom/num]\n👉 !stopall")
                return
            if message.lower() == "!help moderation":
                await self.highrise.chat("🛡️ MODÉRATION :\n👉 !kick @pseudo | !mute @pseudo [min] | !ban @pseudo\n👉 !follow @pseudo | !stop | !tipmod [montant]")
                return
            if message.lower() == "!help jeux":
                await self.highrise.chat("🧠 JEUX :\n👉 !riddle\n👉 !attirer")
                return
            if message.lower() == "!help event":
                await self.highrise.chat("🎉 EVENTS :\n👉 !tirage (Gagnant au hasard)\n👉 !vip @pseudo (Ajouter VIP)\n👉 !unvip @pseudo (Retirer VIP)\n👉 !statut (Nombre de joueurs)")
                return
            if message.lower() == "!help serveur":
                await self.highrise.chat("⚙️ SERVEUR :\n👉 !lock (Bloquer chat) | !unlock (Débloquer)\n👉 !rs (Réseaux Sociaux) | !regles (Règlement)")
                return
            if message.lower() == "!help boutique":
                await self.highrise.chat("🛒 BOUTIQUE SALON :\n💰 Modérateur : 500 Gold/mois\n👑 VIP permanent : 200 Gold\n📢 Pub Salon : 100 Gold/10 min")
                return
            if cmd == "tirage" and user.id in OWNERS + MODERATORS:
                u_list = await self.highrise.get_room_users()
                humans = [u.username for u, p in u_list.content if u.username.lower() != BOT_USERNAME.lower()]
                if humans: await self.highrise.chat(f"🎁 TIRAGE AU SORT ! Le gagnant est : 🎉 @{random.choice(humans)} 🎉")
                return

            if text.startswith("!vip ") and user.id in OWNERS + MODERATORS:
                name = text[5:].replace("@", "").strip()
                for u, p in (await self.highrise.get_room_users()).content:
                    if u.username.lower() == name and u.id not in VIP_LIST:
                        VIP_LIST.append(u.id)
                        await self.highrise.chat(f"👑 @{u.username} est VIP !")
                return

            if text.startswith("!unvip ") and user.id in OWNERS + MODERATORS:
                name = text[7:].replace("@", "").strip()
                for u, p in (await self.highrise.get_room_users()).content:
                    if u.username.lower() == name and u.id in VIP_LIST:
                        VIP_LIST.remove(u.id)
                        await self.highrise.chat(f"❌ @{u.username} n'est plus VIP.")
                return

            if cmd == "statut":
                u_list = await self.highrise.get_room_users()
                await self.highrise.chat(f"📊 Il y a actuellement {len(u_list.content)} personnes dans ce salon !")
                return

            if cmd == "lock" and user.id in OWNERS + MODERATORS:
                CHAT_LOCKED = True
                await self.highrise.chat("🔒 Le chat a été verrouillé. Seul le staff peut écrire.")
                return

            if cmd == "unlock" and user.id in OWNERS + MODERATORS:
                CHAT_LOCKED = False
                await self.highrise.chat("🔓 Le chat est déverrouillé !")
                return

            if cmd == "rs":
                await self.highrise.chat("📱 Suivez le créateur du salon sur TikTok et insta : @gentleman_0 ! ✨")
                return

            if cmd == "regles":
                await self.highrise.chat("📜 RÈGLES : Respectez le staff, pas d'insultes, pas de spam ! 🎉")
                return

            if text.startswith("!danceall "):
                if user.id in OWNERS + MODERATORS:
                    tgt = text[10:].strip()
                    act = EMOTES[tgt] if tgt in EMOTES else (EMOTES_LISTE[int(tgt)-1] if tgt.isdigit() and 0<=int(tgt)-1<len(EMOTES_LISTE) else None)
                    if act:
                        u_list = await self.highrise.get_room_users()
                        for u, p in u_list.content: await self.start_loop(u.id, act)
                return

            if cmd == "stopall" and user.id in OWNERS + MODERATORS:
                for tid in list(self.emote_tasks.keys()): self.emote_tasks[tid].cancel()
                self.emote_tasks.clear()
                return

            if cmd == "attirer" and user.id in OWNERS + MODERATORS:
                u_list = await self.highrise.get_room_users()
                for u, p in u_list.content:
                    try: await self.highrise.teleport_user(u.id, Position(x=self.bot_position.x, y=self.bot_position.y, z=self.bot_position.z, facing="FrontRight"))
                    except: pass
                return

            if text.startswith("!kick ") and user.id in OWNERS + MODERATORS:
                name = text[6:].replace("@", "").strip()
                for u, p in (await self.highrise.get_room_users()).content:
                    if u.username.lower() == name: await self.highrise.moderate_room(u.id, "kick")
                return

            if text.startswith("!mute ") and user.id in OWNERS + MODERATORS:
                p = text.split()
                if len(p) >= 3:
                    name = p.replace("@", "").strip()
                    for u, pos in (await self.highrise.get_room_users()).content:
                        if u.username.lower() == name: await self.highrise.moderate_room(u.id, "mute", int(p)*60)
                return

            if text.startswith("!ban ") and user.id in OWNERS + MODERATORS:
                name = text[5:].replace("@", "").strip()
                for u, p in (await self.highrise.get_room_users()).content:
                    if u.username.lower() == name: await self.highrise.moderate_room(u.id, "ban", 999999)
                return

            if cmd == "riddle":
                self.current_riddle = random.choice(RIDDLES)
                await self.highrise.chat(f"🧠 Énigme : {self.current_riddle['question']}")
                return

            if text.startswith("!tipmod ") and user.id in OWNERS + MODERATORS:
                try:
                    amt = int(text[8:].strip())
                    for u, p in (await self.highrise.get_room_users()).content:
                        if u.id in MODERATORS: await self.highrise.tip_user(u.id, amt)
                except: pass
                return

            if text.startswith("!follow ") and user.id in OWNERS + MODERATORS:
                name = text[8:].replace("@", "").strip()
                for u, p in (await self.highrise.get_room_users()).content:
                    if u.username.lower() == name:
                        self.following_user_id = u.id
                        if self.follow_task: self.follow_task.cancel()
                        self.follow_task = asyncio.create_task(self.follow_loop())
                return

            if cmd == "stop" and user.id in OWNERS + MODERATORS:
                if self.following_user_id is not None:
                    self.following_user_id = None
                    if self.follow_task: self.follow_task.cancel()
                return

        # Chatbot automatique
        if any(kw in text for kw in ["bonjour", "salut", "slt", "cc", "cv", "ca va", "aide", "help", "leviae"]):
            await self.highrise.chat(random.choice(CHATBOT_RESPONSES))

# ==========================
# DÉMARRAGE SUR RENDER
# ==========================
if __name__ == "__main__":
    room_id = "65e361f8aef42a7b0ed22029"
    api_token = "f1f9d1cae9063a6a0a50ccfc95d0864005990c820d5f7dcf3463a6a11ecd3cfa"
    from highrise.__main__ import main
    sys.argv = ["highrise", "main:Bot", room_id, api_token]
    main()
