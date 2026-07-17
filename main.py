import os, asyncio, random
from threading import Thread
from flask import Flask
from highrise import BaseBot, User, Position
from highrise.models import SessionMetadata
from emotes import EMOTES

app = Flask('')

@app.route('/')
def home(): 
    return "Le bot Leviae Pro Ultimate fonctionne en ligne !"

def run_web_server(): 
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

Thread(target=run_web_server).start()

BOT_USERNAME = "leviae"
OWNERS = ["65592020383c55ed5c45aabd"]
MODERATORS = ["65592020383c55ed5c45aabd"]
VIP_LIST = [] 
CHAT_LOCKED = False 
INSULTES_LISTE = ["fdp", "con", "salope"]
GREETING_RESPONSES = ["Hello! 👋", "Hi there! 🎉", "Welcome! 🌟"]

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.following_user_id = None
        self.follow_task = None
        self.bot_position = Position(x=0.0, y=0.0, z=0.0, facing="FrontRight")
        self.user_emote_tasks = {}

    async def loop_emote_handler(self, user_id: str, emote_id: str):
        try:
            while True:
                await self.highrise.send_emote(emote_id, user_id)
                await asyncio.sleep(10.0)
        except asyncio.CancelledError:
            pass
        except Exception:
            pass

    async def cancel_user_emote(self, user_id: str):
        if user_id in self.user_emote_tasks:
            task = self.user_emote_tasks[user_id]
            if not task.done():
                task.cancel()
                try:
                    await task 
                except:
                    pass
            del self.user_emote_tasks[user_id]
        
        try:
            await self.highrise.send_emote("idle-wave", user_id)
        except:
            pass

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
        try: 
            await self.highrise.set_bio("Créé par @gentleman_0")
        except: pass
        await self.highrise.chat("✅ <#AAFFAA>Leviae Ultimate is online! Type !help.")
        self.follow_task = asyncio.create_task(self.follow_loop())

    async def on_user_join(self, user: User, position: Position):
        if user.id in VIP_LIST:
            await self.highrise.chat(f"👑 <#FFD700>[VIP] Please warmly welcome @{user.username} into the room!<#FFFFFF>")
        else:
            await self.highrise.chat(f"{random.choice(GREETING_RESPONSES)} @{user.username}! Type !help")

    async def on_user_leave(self, user: User):
        if user.id == self.following_user_id:
            self.following_user_id = None
        await self.cancel_user_emote(user.id)

    async def on_chat(self, user: User, message: str) -> None:
        global CHAT_LOCKED
        nettoye = message.lower().strip()

        for insulte in INSULTES_LISTE:
            if insulte in nettoye:
                try: await self.highrise.chat(f"⚠️ Keep the chat clean @{user.username}!")
                except: pass
                return

        if CHAT_LOCKED and user.id not in OWNERS and user.id not in MODERATORS:
            return

        if nettoye == "stop":
            await self.cancel_user_emote(user.id)
            return

        if nettoye in EMOTES:
            await self.cancel_user_emote(user.id)
            await asyncio.sleep(0.2)
            
            emote_id = EMOTES[nettoye]
            self.user_emote_tasks[user.id] = asyncio.create_task(
                self.loop_emote_handler(user.id, emote_id)
            )
            return

        if nettoye == "!follow":
            self.following_user_id = user.id
            await self.highrise.chat(f"🏃 Je te suis @{user.username}")
            return

        if nettoye == "!unstuck":
            self.following_user_id = None
            try:
                await self.highrise.walk_to(Position(x=4.0, y=0.0, z=4.0, facing="FrontRight"))
                await self.highrise.chat("📍 Position réinitialisée.")
            except: pass
            return

        if nettoye == "!come" and (user.id in OWNERS or user.id in MODERATORS):
            try:
                users = await self.highrise.get_room_users()
                for u, pos in users.content:
                    if u.id == user.id and isinstance(pos, Position):
                        await self.highrise.walk_to(Position(x=pos.x + 0.5, y=pos.y, z=pos.z, facing="FrontLeft"))
            except: pass
            return

        if nettoye == "!lock" and (user.id in OWNERS or user.id in MODERATORS):
            CHAT_LOCKED = True
            await self.highrise.chat("🔒 Le chat a été verrouillé par le staff.")
            return

        if nettoye == "!unlock" and (user.id in OWNERS or user.id in MODERATORS):
            CHAT_LOCKED = False
            await self.highrise.chat("🔓 Le chat est maintenant déverrouillé.")
            return

        if nettoye in ["!list", "!liste"]:
            await self.highrise.chat("📖 [Emotes List] Tapez au choix : !list1 (1-50) | !list2 (51-100) | !list3 (101-149) | !list4 (150-178)")
            return

        if nettoye == "!list1":
            await self.highrise.chat("📜 1:swagbounce 2:duckwalk 3:pennywise 4:floorsleeping 5:laidback 6:ghost 7:annoyed 8:touch 9:jinglebell 10:space 11:metal 12:flex 13:orangejustice 14:shy 15:blowkiss")
            await self.highrise.chat("📜 16:stargazer 17:knock 18:curtsy 19:slap 20:singing 21:swinging 22:kawai 23:pose9 24:tiktok9 25:floss 26:breakdance 27:wild 28:hipshake 29:griddy 30:shrink")
            await self.highrise.chat("📜 31:spiritual 32:martial 33:hero 34:tiktok2 35:popularvibe 36:headball 37:trueheart 38:mine 39:robotic 40:graceful 41:meditate 42:frollicking 43:ballet 44:woah 45:shuffle")
            await self.highrise.chat("📜 46:frog 47:lying 48:laughing2 49:boxer 50:tiktok10")
            return

        if nettoye == "!list2":
            await self.highrise.chat("📜 51:attention 52:dab 53:timejump 54:puppet 55:aerobics 56:guitar 57:tiktok7 58:tiktok11 59:tapdance 60:pose10 61:scared 62:arrogance 63:wrong 64:halo 65:anime")
            await self.highrise.chat("📜 66:hyped 67:boo 68:trampoline 69:emojighost 70:float 71:sleigh 72:cheerleader 73:ninjarun 74:gangnam 75:snake 76:pinguin 77:loopaerobics 78:howl 79:launch 80:creepypuppet")
            await self.highrise.chat("📜 81:gravity 82:confused 83:creepycute 84:smoothwalk 85:nervous 86:gordonshuffle 87:rofl 88:icecream 89:celebrate 90:panic 91:punkguitar 92:singleladies 93:punch 94:shoppingcart 95:tiktok4")
            await self.highrise.chat("📜 96:nightfever 97:snowangel 98:headblowup 99:roll 100:open")
            return

        if nettoye == "!list3":
            await self.highrise.chat("📜 101:superrun 102:disappear 103:layingdown2 104:uwu 105:harlemshake 106:blackpink 107:employee 108:cute 109:tiktok14 110:russian 111:handstand 112:elbowbump 113:floating 114:mindblown 115:zombie2")
            await self.highrise.chat("📜 116:disco 117:jumpb 118:heartshape 119:judochop 120:levelup 121:peace 122:suckthumb 123:think 124:headbobbing 125:tired 126:crying 127:dizzy 128:pray 129:exasperated 130:sad")
            await self.highrise.chat("📜 131:deathdrop 132:hot 133:hug 134:sadloop 135:lookup 136:posh 137:wings 138:there 139:superpunch 140:sleep 141:weird 142:fainting 143:monsterfail 144:hero2 145:handsup")
            await self.highrise.chat("📜 146:fail2 147:ropepull 148:bow 149:model")
            return

        if nettoye == "!list4":
            await self.highrise.chat("📜 150:splitsdrop 151:sick 152:embarrassed 153:proposing 154:enthusiastic 155:cold 156:telekinesis 157:hadoken 158:sneeze 159:fail1 160:naughty 161:hugyourself 162:theatrical")
            await self.highrise.chat("📜 163:greedy 164:baseball 165:sumo 166:death2 167:smirking 168:voguehands 169:eyeroll 170:giveup 171:bunnyhop 172:exasperatedb 173:happy 174:heart 175:photo")
            await self.highrise.chat("📜 176:émote176 177:émote177 178:émote178")
            return

        if nettoye == "!help":
            await self.highrise.chat("🤖 [Leviae Help] 🌟 Cat 1 (Emotes): Tape le chiffre (1-178) OU le nom. Écris !list pour voir le catalogue.")
            await self.highrise.chat("🏃 [Leviae Help] Cat 2 (Move): Écris !follow pour que je te suive, ou !unstuck pour me réinitialiser.")
            if user.id in OWNERS or user.id in MODERATORS:
                await self.highrise.chat("🛡️ [Staff Only] 💬 Cat 3 (General): !help | 🛡️ Cat 4 (Admin): !lock, !unlock, !come")
            return

if __name__ == "__main__":
    from highrise.__main__ import main
    main()
