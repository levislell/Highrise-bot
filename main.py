import os, asyncio, random
from threading import Thread
from flask import Flask
from highrise import BaseBot, User, Position
from highrise.models import SessionMetadata

# Initialisation Flask pour la disponibilité en ligne
app = Flask('')
@app.route('/')
def home(): return "Le botroom11 Pro Ultimate fonctionne en ligne !"
def run_web_server(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
Thread(target=run_web_server).start()

# === CONFIGURATION GLOBALE ===
BOT_USERNAME = "botRoom11"
OWNERS = ["65592020383c55ed5c45aabd"]
MODERATORS_BOT = ["65592020383c55ed5c45aabd"] 
VIP_LIST = [] 
CHAT_LOCKED = False 
INSULTES_LISTE = ["fdp", "con", "salope"]

# Textes d'accueil
GREETING_RESPONSES = [
    "Bienvenue parmis nous @{username} ! Profite bien de la salle ! ✨",
    "Alerte ! Un nouveau joueur sauvage apparaît : @{username} ! 👋",
    "Installe-toi confortablement @{username}, le bot Leviae est là pour toi ! 🌟",
    "Ravi de te voir entrer ici @{username} ! Active le menu avec !help 🎉"
]
GREETING_EMOTES = ["emote-blowkisses", "emote-wings", "emote-wave", "emote-shy2"]

PLAYER_XP = {}
CURRENT_QUIZ = {"question": None, "reponse": None, "actif": False}

def generer_question_infinie():
    type_calcul = random.choice(["+", "-", "*"])
    if type_calcul == "+":
        a, b = random.randint(1, 100), random.randint(1, 100)
        return {"q": f"Combien font {a} + {b} ?", "a": str(a + b)}
    elif type_calcul == "-":
        a, b = random.randint(50, 100), random.randint(1, 49)
        return {"q": f"Combien font {a} - {b} ?", "a": str(a - b)}
    else:
        a, b = random.randint(2, 12), random.randint(2, 12)
        return {"q": f"Combien font {a} x {b} ?", "a": str(a * b)}
# === DICTIONNAIRE GLOBAL PARTIE A : EMOTES 1 A 65 ===
EMOTES = {
    "1": "dance-swagbounce", "swagbounce": "dance-swagbounce",
    "2": "dance-duckwalk", "duckwalk": "dance-duckwalk",
    "3": "dance-pennywise", "pennywise": "dance-pennywise",
    "4": "idle-floorsleeping", "floorsleeping": "idle-floorsleeping",
    "5": "emote-laidback", "laidback": "emote-laidback",
    "6": "dance-ghost", "ghost": "dance-ghost",
    "7": "dance-annoyed", "annoyed": "dance-annoyed",
    "8": "dance-touch", "touch": "dance-touch",
    "9": "dance-jinglebell", "jinglebell": "dance-jinglebell",
    "10": "dance-space", "space": "dance-space",
    "11": "dance-metal", "metal": "dance-metal",
    "12": "dance-flex", "flex": "dance-flex",
    "13": "dance-orangejustice", "orangejustice": "dance-orangejustice",
    "14": "dance-shy", "shy": "dance-shy",
    "15": "dance-blowkiss", "blowkiss": "dance-blowkiss",
    "16": "dance-stargazer", "stargazer": "dance-stargazer",
    "17": "dance-knock", "knock": "dance-knock",
    "18": "dance-curtsy", "curtsy": "dance-curtsy",
    "19": "dance-slap", "slap": "dance-slap",
    "20": "dance-singing", "singing": "dance-singing",
    "21": "dance-swinging", "swinging": "dance-swinging",
    "22": "dance-kawai", "kawai": "dance-kawai",
    "23": "dance-pose9", "pose9": "dance-pose9",
    "24": "dance-tiktok9", "tiktok9": "dance-tiktok9",
    "25": "dance-floss", "floss": "dance-floss",
    "26": "dance-breakdance", "breakdance": "dance-breakdance",
    "27": "dance-wild", "wild": "dance-wild",
    "28": "dance-hipshake", "hipshake": "dance-hipshake",
    "29": "dance-griddy", "griddy": "dance-griddy",
    "30": "dance-shrink", "shrink": "dance-shrink",
    "31": "dance-spiritual", "spiritual": "dance-spiritual",
    "32": "dance-martial", "martial": "dance-martial",
    "33": "dance-hero", "hero": "dance-hero",
    "34": "dance-tiktok2", "tiktok2": "dance-tiktok2",
    "35": "dance-popularvibe", "popularvibe": "dance-popularvibe",
    "36": "dance-headball", "headball": "dance-headball",
    "37": "dance-trueheart", "trueheart": "dance-trueheart",
    "38": "dance-mine", "mine": "dance-mine",
    "39": "dance-robotic", "robotic": "dance-robotic",
    "40": "dance-graceful", "graceful": "dance-graceful",
    "41": "dance-meditate", "meditate": "dance-meditate",
    "42": "dance-frollicking", "frollicking": "dance-frollicking",
    "43": "dance-ballet", "ballet": "dance-ballet",
    "44": "dance-woah", "woah": "dance-woah",
    "45": "dance-shuffle", "shuffle": "dance-shuffle",
    "46": "emote-frog", "frog": "emote-frog",
    "47": "emote-lying", "lying": "emote-lying",
    "48": "emote-laughing2", "laughing2": "emote-laughing2",
    "49": "emote-boxer", "boxer": "emote-boxer",
    "50": "dance-tiktok10", "tiktok10": "dance-tiktok10",
    "51": "emote-attention", "attention": "emote-attention",
    "52": "dance-dab", "dab": "dance-dab",
    "53": "dance-timejump", "timejump": "dance-timejump",
    "54": "dance-puppet", "puppet": "dance-puppet",
    "55": "dance-aerobics", "aerobics": "dance-aerobics",
    "56": "dance-guitar", "guitar": "dance-guitar",
    "57": "dance-tiktok7", "tiktok7": "dance-tiktok7",
    "58": "dance-tiktok11", "tiktok11": "dance-tiktok11",
    "59": "dance-tapdance", "tapdance": "dance-tapdance",
    "60": "dance-pose10", "pose10": "dance-pose10",
    "61": "dance-scared", "scared": "dance-scared",
    "62": "dance-arrogance", "arrogance": "dance-arrogance",
    "63": "dance-wrong", "wrong": "dance-wrong",
    "64": "dance-halo", "halo": "dance-halo",
    "65": "dance-anime", "anime": "dance-anime",
    "66": "dance-hyped", "hyped": "dance-hyped",
    "67": "dance-boo", "boo": "dance-boo",
    "68": "dance-trampoline", "trampoline": "dance-trampoline",
    "69": "dance-emojighost", "emojighost": "dance-emojighost",
    "70": "dance-float", "float": "dance-float",
    "71": "dance-sleigh", "sleigh": "dance-sleigh",
    "72": "dance-cheerleader", "cheerleader": "dance-cheerleader",
    "73": "dance-ninjarun", "ninjarun": "dance-ninjarun",
    "74": "dance-gangnam", "gangnam": "dance-gangnam",
    "75": "dance-snake", "snake": "dance-snake",
    "76": "dance-pinguin", "pinguin": "dance-pinguin",
    "77": "dance-loopaerobics", "loopaerobics": "dance-loopaerobics",
    "78": "dance-howl", "howl": "dance-howl",
    "79": "dance-launch", "launch": "dance-launch",
    "80": "dance-creepypuppet", "creepypuppet": "dance-creepypuppet",
    "81": "dance-gravity", "gravity": "dance-gravity",
    "82": "dance-confused", "confused": "dance-confused",
    "83": "dance-creepycute", "creepycute": "dance-creepycute",
    "84": "dance-smoothwalk", "smoothwalk": "dance-smoothwalk",
    "85": "dance-nervous", "nervous": "dance-nervous",
    "86": "dance-gordonshuffle", "gordonshuffle": "dance-gordonshuffle",
    "87": "dance-rofl", "rofl": "dance-rofl",
    "88": "dance-icecream", "icecream": "dance-icecream",
    "89": "dance-celebrate", "celebrate": "dance-celebrate",
    "90": "dance-panic", "panic": "dance-panic",
    "91": "dance-punkguitar", "punkguitar": "dance-punkguitar",
    "92": "dance-singleladies", "singleladies": "dance-singleladies",
    "93": "dance-punch", "punch": "dance-punch",
    "94": "dance-shoppingcart", "shoppingcart": "dance-shoppingcart",
    "95": "dance-tiktok4", "tiktok4": "dance-tiktok4",
    "96": "dance-nightfever", "nightfever": "dance-nightfever",
    "97": "dance-snowangel", "snowangel": "dance-snowangel",
    "98": "dance-headblowup", "headblowup": "dance-headblowup",
    "99": "dance-roll", "roll": "dance-roll",
    "100": "dance-open", "open": "dance-open",
    "101": "dance-superrun", "superrun": "dance-superrun",
    "102": "dance-disappear", "disappear": "dance-disappear",
    "103": "idle-layingdown2", "layingdown2": "idle-layingdown2",
    "104": "emote-uwu", "uwu": "emote-uwu",
    "105": "dance-harlemshake", "harlemshake": "dance-harlemshake",
    "106": "dance-blackpink", "blackpink": "dance-blackpink",
    "107": "emote-employee", "employee": "emote-employee",
    "108": "emote-cute", "cute": "emote-cute",
    "109": "dance-tiktok14", "tiktok14": "dance-tiktok14",
    "110": "dance-russian", "russian": "dance-russian",
    "111": "emote-handstand", "handstand": "emote-handstand",
    "112": "emote-elbowbump", "elbowbump": "emote-elbowbump",
    "113": "dance-floating", "floating": "dance-floating",
    "114": "emote-mindblown", "mindblown": "emote-mindblown",
    "115": "dance-zombie2", "zombie2": "dance-zombie2",
    "116": "dance-disco", "disco": "dance-disco",
    "117": "dance-jumpb", "jumpb": "dance-jumpb",
    "118": "emote-heartshape", "heartshape": "emote-heartshape",
    "119": "emote-judochop", "judochop": "emote-judochop",
    "120": "emote-levelup", "levelup": "emote-levelup",
    "121": "emote-peace", "peace": "emote-peace",
    "122": "emote-suckthumb", "suckthumb": "emote-suckthumb",
    "123": "emote-think", "think": "emote-think",
    "124": "emote-headbobbing", "headbobbing": "emote-headbobbing",
    "125": "emote-tired", "tired": "emote-tired",
    "126": "emote-crying", "crying": "emote-crying",
    "127": "emote-dizzy", "dizzy": "emote-dizzy",
    "128": "emote-pray", "pray": "emote-pray",
    "129": "emote-exasperated", "exasperated": "emote-exasperated",
    "130": "emote-sad", "sad": "emote-sad",
    "131": "emote-deathdrop", "deathdrop": "emote-deathdrop",
    "132": "emote-hot", "hot": "emote-hot",
    "133": "emote-hug", "hug": "emote-hug",
    "134": "emote-sadloop", "sadloop": "emote-sadloop",
    "135": "emote-lookup", "lookup": "emote-lookup",
    "136": "emote-posh", "posh": "emote-posh",
    "137": "emote-wings", "wings": "emote-wings",
    "138": "emote-there", "there": "emote-there",
    "139": "emote-superpunch", "superpunch": "emote-superpunch",
    "140": "emote-sleep", "sleep": "emote-sleep",
    "141": "emote-weird", "weird": "emote-weird",
    "142": "emote-fainting", "fainting": "emote-fainting",
    "143": "emote-monsterfail", "monsterfail": "emote-monsterfail",
    "144": "emote-hero2", "hero2": "emote-hero2",
    "145": "emote-handsup", "handsup": "emote-handsup",
    "146": "emote-fail2", "fail2": "emote-fail2",
    "147": "emote-ropepull", "ropepull": "emote-ropepull",
    "148": "emote-bow", "bow": "emote-bow",
    "149": "emote-model", "model": "emote-model",
    "150": "emote-splitsdrop", "splitsdrop": "emote-splitsdrop",
    "151": "emote-sick", "sick": "emote-sick",
    "152": "emote-embarrassed", "embarrassed": "emote-embarrassed",
    "153": "emote-proposing", "proposing": "emote-proposing",
    "154": "emote-enthusiastic", "enthusiastic": "emote-enthusiastic",
    "155": "emote-cold", "cold": "emote-cold",
    "156": "emote-telekinesis", "telekinesis": "emote-telekinesis",
    "157": "emote-hadoken", "hadoken": "emote-hadoken",
    "158": "emote-sneeze", "sneeze": "emote-sneeze",
    "159": "emote-fail1", "fail1": "emote-fail1",
    "160": "emote-naughty", "naughty": "emote-naughty",
    "161": "emote-hugyourself", "hugyourself": "emote-hugyourself",
    "162": "emote-theatrical", "theatrical": "emote-theatrical",
    "163": "emote-greedy", "greedy": "emote-greedy",
    "164": "emote-baseball", "baseball": "emote-baseball",
    "165": "emote-sumo", "sumo": "emote-sumo",
    "166": "emote-death2", "death2": "emote-death2",
    "167": "emote-smirking", "smirking": "emote-smirking",
    "168": "emote-voguehands", "voguehands": "emote-voguehands",
    "169": "emote-eyeroll", "eyeroll": "emote-eyeroll",
    "170": "emote-giveup", "giveup": "emote-giveup",
    "171": "emote-bunnyhop", "bunnyhop": "emote-bunnyhop",
    "172": "emote-exasperatedb", "exasperatedb": "emote-exasperatedb",
    "173": "emote-happy", "happy": "emote-happy",
    "174": "emote-heart", "heart": "emote-heart",
    "175": "emote-collab-photo-left", "photo": "emote-collab-photo-left",
    "176": "dance-tiktok8", "tiktok8": "dance-tiktok8",
    "177": "dance-twerk", "twerk": "dance-twerk",
    "178": "sit-idle-cute", "rest": "sit-idle-cute",
    "179": "emote-afk-idle", "afk": "emote-afk-idle",
    "180": "emote-collab-photo-right", "photoright": "emote-collab-photo-right"
}

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.following_user_id = None
        self.follow_task = None
        self.bot_task = None
        self.quiz_task = None
        self.bot_position = Position(x=0.0, y=0.0, z=0.0, facing="FrontRight")
        self.user_emote_tasks = {}

    async def loop_emote_handler(self, user_id: str, emote_id: str):
        try:
            while True:
                await self.highrise.send_emote(emote_id, user_id)
                await asyncio.sleep(9) 
        except asyncio.CancelledError: pass
        except Exception: pass

    async def bot_self_emote_loop(self):
        await asyncio.sleep(5.0)
        while True:
            try:
                random_emote = random.choice(list(EMOTES.values()))
                await self.highrise.send_emote(random_emote)
            except: pass
            await asyncio.sleep(15.0)

    async def quiz_loop(self):
        await asyncio.sleep(20.0)
        while True:
            try:
                if not CURRENT_QUIZ["actif"]:
                    choix = generer_question_infinie()
                    CURRENT_QUIZ["question"] = choix["q"]
                    CURRENT_QUIZ["reponse"] = choix["a"]
                    CURRENT_QUIZ["actif"] = True
                    await self.highrise.chat(f"🧠 <#00FFFF>[QUIZ INFINI]</#00FFFF> {CURRENT_QUIZ['question']} (Écris le chiffre directement dans le chat)")
            except: pass
            await asyncio.sleep(90.0)

    async def cancel_user_emote(self, user_id: str):
        if user_id in self.user_emote_tasks:
            task = self.user_emote_tasks[user_id]
            if not task.done():
                task.cancel()
                try: await task 
                except: pass
            del self.user_emote_tasks[user_id]
        try: await self.highrise.send_emote("idle-wave", user_id)
        except: pass

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
        try: await self.highrise.set_bio("Créé par @gentleman_0")
        except: pass
        await self.highrise.chat("✅ <#AAFFAA>Leviae Ultimate est en ligne ! Tapez !help.")
        self.follow_task = asyncio.create_task(self.follow_loop())
        self.bot_task = asyncio.create_task(self.bot_self_emote_loop())
        self.quiz_task = asyncio.create_task(self.quiz_loop())

    async def on_user_join(self, user: User, position: Position):
        welcome_message = random.choice(GREETING_RESPONSES).format(username=user.username)
        await self.highrise.chat(welcome_message)
        try:
            random_welcome_emote = random.choice(GREETING_EMOTES)
            await self.highrise.send_emote(random_welcome_emote)
        except: pass
    async def on_user_leave(self, user: User):
        if user.id == self.following_user_id:
            self.following_user_id = None
        await self.cancel_user_emote(user.id)

    async def on_chat(self, user: User, message: str) -> None:
        global CHAT_LOCKED
        nettoye = message.lower().strip()

        # --- 1. VALIDATION DU QUIZ EN TEMPS RÉEL ---
        if CURRENT_QUIZ["actif"] and nettoye == CURRENT_QUIZ["reponse"]:
            CURRENT_QUIZ["actif"] = False
            if user.id not in PLAYER_XP:
                PLAYER_XP[user.id] = {"xp": 0, "level": 1, "username": user.username}
            PLAYER_XP[user.id]["xp"] += 15 
            await self.highrise.chat(f"🏆 Bravo @{user.username} ! Bonne réponse ({CURRENT_QUIZ['reponse']}). Tu gagnes +15 XP ! 🧠")
            if PLAYER_XP[user.id]["xp"] >= (PLAYER_XP[user.id]["level"] * 5):
                PLAYER_XP[user.id]["level"] += 1
                PLAYER_XP[user.id]["xp"] = 0
                await self.highrise.chat(f"🎉 Gg @{user.username} ! Tu passes au <#FF1493>Niveau {PLAYER_XP[user.id]['level']}</#FF1493> ! ✨")
            return

        # --- 2. SYSTEME DE NIVEAUX & XP STANDARD ---
        if user.id not in PLAYER_XP:
            PLAYER_XP[user.id] = {"xp": 0, "level": 1, "username": user.username}
        PLAYER_XP[user.id]["xp"] += 1
        if PLAYER_XP[user.id]["xp"] >= (PLAYER_XP[user.id]["level"] * 5):
            PLAYER_XP[user.id]["level"] += 1
            PLAYER_XP[user.id]["xp"] = 0
            await self.highrise.chat(f"🎉 Gg @{user.username} ! Tu passes au <#FF1493>Niveau {PLAYER_XP[user.id]['level']}</#FF1493> ! ✨")

        # Modération Anti-Insultes
        for insulte in INSULTES_LISTE:
            if insulte in nettoye:
                try: await self.highrise.chat(f"⚠️ Keep the chat clean @{user.username}!")
                except: pass
                return
        if CHAT_LOCKED and user.id not in OWNERS and user.id not in MODERATORS_BOT:
            return

        # --- 3. COMMANDES UTILISATEUR VALIDES ---
        if nettoye == "stop":
            await self.cancel_user_emote(user.id)
            return
        if nettoye == "!id":
            await self.highrise.chat(f"🆔 @{user.username}, ton ID Highrise est : {user.id}")
            return
        if nettoye == "!ping":
            await self.highrise.chat(f"🏓 Pong @{user.username} ! Je fonctionne parfaitement.")
            return
                if nettoye in EMOTES:
            await self.cancel_user_emote(user.id)
            await asyncio.sleep(0.2)
            # Le .strip() nettoie les espaces invisibles comme sur le 144
            emote_officielle = EMOTES[nettoye].strip()
            self.user_emote_tasks[user.id] = asyncio.create_task(self.loop_emote_handler(user.id, emote_officielle))
            return

        if nettoye == "!follow":
            self.following_user_id = user.id
            await self.highrise.chat(f"🏃 Je te suis @{user.username}")
            return
        if nettoye == "!unstuck":
            self.following_user_id = None
            try: await self.highrise.walk_to(Position(x=4.0, y=0.0, z=4.0, facing="FrontRight"))
            except: pass
            return

        # Jeux & Divertissement
        if nettoye.startswith("!rate"):
            cible = message[5:].strip()
            if not cible: cible = f"@{user.username}"
            await self.highrise.chat(f"📊 Je donne la note de {random.randint(1, 10)}/10 à {cible} ! 🔥")
            return
        if nettoye.startswith("!love"):
            await self.highrise.chat(f"❤️ Compatibilité amoureuse : {random.randint(0, 100)}% !")
            return
        if nettoye.startswith("!8ball"):
            reponses = ["Oui absolument 🌟", "C'est certain 👌", "Essaie encore 🔄", "C'est impossible ❌"]
            await self.highrise.chat(f"🔮 8-Ball : {random.choice(reponses)}")
            return
        if nettoye == "!roll":
            await self.highrise.chat(f"🎲 @{user.username} a fait : {random.randint(1, 100)} !")
            return
        if nettoye.startswith("!kiss"):
            cible = message[5:].strip()
            if cible: await self.highrise.chat(f"💋 @{user.username} envoie un gros bisou à {cible} ! 💋")
            return
        if nettoye.startswith("!slap"):
            cible = message[5:].strip()
            if cible: await self.highrise.chat(f"💥 CLAP ! @{user.username} gifle {cible} ! 🤣")
            return
        if nettoye == "!joke":
            blagues = ["Quel est le comble pour un électricien ? De ne pas être au courant !", "Pourquoi les oiseaux volent vers le sud ? Parce que c'est trop long d'y aller à pied !"]
            await self.highrise.chat(f"🤣 {random.choice(blagues)}")
            return
        if nettoye == "!wallet":
            lvl = PLAYER_XP[user.id]["level"]
            xp = PLAYER_XP[user.id]["xp"]
            await self.highrise.chat(f"💳 [Profil] Niveau : {lvl} | XP : {xp}/{lvl*5}")
            return
        if nettoye == "!top":
            tri = sorted(PLAYER_XP.values(), key=lambda x: x["level"], reverse=True)[:3]
            txt = "🏆 [Classement] :\n"
            for i, p in enumerate(tri): txt += f"{i+1}. @{p['username']} (Niv {p['level']})\n"
            await self.highrise.chat(txt)
            return
        # Listes d'aide
        if nettoye in ["!list", "!liste"]:
            await self.highrise.chat("📖 [Listes] : !list1 | !list2 | !list3 | !list4")
            return

        if nettoye == "!help":
            await self.highrise.chat("✨▬▬▬▬▬ <#FFD700>ＬＥＶＩＡＥ  ＰＲＯ</#FFD700> ▬▬▬▬▬✨")
            await self.highrise.chat("🕺 <#00FFFF>✦ EMOTES :</#00FFFF> Écris le chiffre <#ADFF2F>(1-180)</#ADFF2F> ou le nom ! Tape <#FF69B4>!list</#FF69B4>")
            await self.highrise.chat("🎮 <#00FFFF>✦ JEUX :</#00FFFF> !rate | !love | !8ball | !roll | !kiss | !slap | !joke")
            await self.highrise.chat("⚙️ <#00FFFF>✦ STATS :</#00FFFF> !wallet | !top | !id | !ping")
            await self.highrise.chat("🏃 <#00FFFF>✦ MOVES :</#00FFFF> !follow | !unstuck | stop")
            if user.id in OWNERS or user.id in MODERATORS_BOT:
                await self.highrise.chat("🛡️ <#FF4500>✦ STAFF :</#FF4500> !lock | !unlock | !come | !shout | !kick | !mute")
            await self.highrise.chat("✨▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬✨")
            return

        # MESSAGE D'ERREUR (Déplacé ici pour ne plus bloquer !help et !list)
        if message.startswith("!") or (message.isdigit() and nettoye not in EMOTES):
            await self.highrise.chat(f"❌ Désolé chef @{user.username}, j'ai pas ça dans ma liste ! Tape !help")
            return

if __name__ == "__main__":
    from highrise.__main__ import main
    main()
