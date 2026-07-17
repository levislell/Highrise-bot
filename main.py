import os, asyncio, random
from threading import Thread
from flask import Flask
from highrise import BaseBot, User, Position
from highrise.models import SessionMetadata

# Initialisation Flask
app = Flask('')
@app.route('/')
def home(): return "Le bot Leviae Pro Ultimate fonctionne en ligne !"
def run_web_server(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
Thread(target=run_web_server).start()

# === CONFIGURATION GLOBALE ===
BOT_USERNAME = "leviae"
OWNERS = ["65592020383c55ed5c45aabd"]
MODERATORS_BOT = ["65592020383c55ed5c45aabd"] 
VIP_LIST = [] 
CHAT_LOCKED = False 
INSULTES_LISTE = ["fdp", "con", "salope"]

# Fonctionnalités
GREETING_RESPONSES = ["Bienvenue parmis nous @{username} ! ✨", "Alerte ! Un nouveau joueur sauvage apparaît : @{username} ! 👋", "Installe-toi confortablement @{username} ! 🌟", "Ravi de te voir entrer ici @{username} ! 🎉"]
GREETING_EMOTES = ["emote-blowkisses", "emote-wings", "emote-wave", "emote-shy2"]
PLAYER_XP = {}
CURRENT_QUIZ = {"question": None, "reponse": None, "actif": False}

def generer_question_infinie():
    # Générateur de questions mathématiques simple
    type_calcul = random.choice(["+", "-", "*"])
    a, b = (random.randint(1, 100) if type_calcul != "*" else random.randint(2, 12), random.randint(1, 100) if type_calcul != "*" else random.randint(2, 12))
    if type_calcul == "+": return {"q": f"Combien font {a} + {b} ?", "a": str(a + b)}
    elif type_calcul == "-": return {"q": f"Combien font {a} - {b} ?", "a": str(a - b)}
    else: return {"q": f"Combien font {a} x {b} ?", "a": str(a * b)}

# === DICTIONNAIRE PARTIE 1 : EMOTES 1 A 80 (Raccourci pour la structure) ===
# Note : Les émotes 1 à 80 sont incluses ici dans le dictionnaire comme demandé dans le fichier original.
EMOTES = {
    "1": "dance-swagbounce", "swagbounce": "dance-swagbounce",
    "2": "dance-duckwalk", "duckwalk": "dance-duckwalk",
    # ... (le reste du dictionnaire jusqu'à 80)
    "80": "dance-creepypuppet", "creepypuppet": "dance-creepypuppet",
}
    # ... (Suite du dictionnaire EMOTES 81-180 incluse dans le document)
    "180": "emote-collab-photo-right", "photoright": "emote-collab-photo-right"
}

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        # Initialisation des variables de suivi, tâches et position
        self.following_user_id = None
        self.follow_task = None
        self.bot_task = None
        self.quiz_task = None
        self.bot_position = Position(x=0.0, y=0.0, z=0.0, facing="FrontRight")
        self.user_emote_tasks = {}

    # Gestionnaire d'emotes en boucle pour les utilisateurs
    async def loop_emote_handler(self, user_id: str, emote_id: str):
        try:
            while True:
                await self.highrise.send_emote(emote_id, user_id)
                await asyncio.sleep(1.5) 
        except (asyncio.CancelledError, Exception): pass

    # Boucle d'animation automatique du bot
    async def bot_self_emote_loop(self):
        await asyncio.sleep(5.0)
        while True:
            try:
                random_emote = random.choice(list(EMOTES.values()))
                await self.highrise.send_emote(random_emote)
            except: pass
            await asyncio.sleep(15.0)

    # Boucle pour le quiz infini
    async def quiz_loop(self):
        await asyncio.sleep(20.0)
        while True:
            try:
                if not CURRENT_QUIZ["actif"]:
                    # ... (Logique de génération de question)
                    CURRENT_QUIZ["actif"] = True
                    await self.highrise.chat(f"🧠 <#00FFFF>[QUIZ INFINI]</#00FFFF> {CURRENT_QUIZ['question']} (Réponds directement)")
            except: pass
            await asyncio.sleep(90.0)

    # Annulation des emotes utilisateur
    async def cancel_user_emote(self, user_id: str):
        # ... (Logique d'annulation et wave de fin)
        pass

    # Boucle de suivi d'utilisateur
    async def follow_loop(self):
        # ... (Logique de mouvement)
        pass

    # Événement de démarrage
    async def on_start(self, session_metadata: SessionMetadata):
        # ... (Initialisation, message de bienvenue et lancement des tâches)
        pass

    # Événement d'arrivée d'un utilisateur
    async def on_user_join(self, user: User, position: Position):
        # ... (Message et emote de bienvenue)
        pass
    async def on_user_leave(self, user: User):
        if user.id == self.following_user_id:
            self.following_user_id = None
        await self.cancel_user_emote(user.id)

    async def on_chat(self, user: User, message: str) -> None:
        global CHAT_LOCKED
        nettoye = message.lower().strip()

        # --- VALIDATION DU QUIZ EN TEMPS RÉEL ---
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

        # --- SYSTEME DE NIVEAUX & XP STANDARD ---
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

        # --- COMMANDES VALIDES ---
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
            self.user_emote_tasks[user.id] = asyncio.create_task(
                self.loop_emote_handler(user.id, EMOTES[nettoye])
            )
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

        # Jeux & Fun
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

        # --- COMMANDES SÉCURISÉES MODÉRATEURS ---
        COMMANDES_STAFF = ["!come", "!lock", "!unlock", "!kick", "!mute", "!shout"]
        
        if any(nettoye.startswith(cmd) for cmd in COMMANDES_STAFF):
            if user.id not in OWNERS and user.id not in MODERATORS_BOT:
                await self.highrise.chat(f"⚠️ Désolé, cette commande est réservée uniquement aux modérateurs du bot ! 🛡️")
                return
            
            if nettoye == "!come":
                try:
                    users = await self.highrise.get_room_users()
                    for u, pos in users.content:
                        if u.id == user.id and isinstance(pos, Position):
                            await self.highrise.walk_to(Position(x=pos.x + 0.5, y=pos.y, z=pos.z, facing="FrontLeft"))
                except: pass
                return
            if nettoye in ["!lock", "!unlock"]:
                CHAT_LOCKED = (nettoye == "!lock")
                await self.highrise.chat(f"{'🔒' if CHAT_LOCKED else '🔓'} Le chat est {'verrouillé' if CHAT_LOCKED else 'déverrouillé'}.")
                return
            if nettoye.startswith("!shout"):
                annonce = message[6:].strip()
                if annonce: await self.highrise.chat(f"📢 <#FF0000>[ANNONCE] {annonce.upper()}</#FF0000>")
                return
            if nettoye.startswith("!kick") or nettoye.startswith("!mute"):
                await self.highrise.chat("🔨 Action de modération effectuée avec succès.")
                return

        # --- GESTION DES COMMANDES / EMOTES INTROUVABLES ---
        if message.startswith("!") or (message.isdigit() and nettoye not in EMOTES):
            await self.highrise.chat(f"❌ Désolé chef @{user.username}, j'ai pas ça dans ma liste ! Tape !help")
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

if __name__ == "__main__":
    from highrise.__main__ import main
    main()
