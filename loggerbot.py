from datetime import datetime, timedelta
import os, json, asyncio, sys
from telethon import TelegramClient, events, Button
from telethon.sync import TelegramClient as TMPTelegramClient
from telethon.errors import PhoneNumberFloodError, SessionPasswordNeededError, FloodWaitError
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateUsernameRequest, UpdateProfileRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

from telethon.tl.functions.photos import UploadProfilePhotoRequest

ADMIN = 910209349

API_KEY = 7058291
API_HASH = "5b9ea5b6baa2905c7ae2822a04b8e835"
STRING_SESSION = ""
proxy = {
    'proxy_type': 'socks5', # (mandatory) protocol to use (see above)
    'addr': '',      # (mandatory) proxy IP address
    'port': ,           # (mandatory) proxy port number
    'username': '',      # (optional) username if the proxy requires auth
    'password': '',      # (optional) password if the proxy requires auth
    'rdns': True            # (optional) whether to use remote or local resolve, default remote
}
ADMINS = []
Getter = None
Number = None
TempClient = None
Grab = None
activeusers = False
inAdding = False
canAdd = True
maxusers = 0
AddedUsers = []
tentativi = 0
countusers = 0
raspingintelligentelist = {}
if os.path.exists("SSs.json"):
    with open("SSs.json", "r+") as f:
        SSs = json.load(f)
else:
    SSs = {}
    with open("SSs.json", "w+") as f:
        json.dump(SSs, f)

if os.path.exists("ArchSSs.json"):
    with open("ArchSSs.json", "r+") as f:
        ArchSSs = json.load(f)
else:
    ArchSSs = {}
    with open("ArchSSs.json", "w+") as f:
        json.dump(ArchSSs, f)


def saveSS():
    global SSs
    with open("SSs.json", "w+") as f:
        json.dump(SSs, f)


def saveArchSS():
    global ArchSSs
    with open("ArchSSs.json", "w+") as f:
        json.dump(ArchSSs, f)


async def addUsers(client, Users, group):
    global canAdd, AddedUsers, countusers, maxusers, tentativi
    AddedUsers = []
    tentativi = 0
    for user in Users:
        if maxusers == 0:
            if canAdd:
                AddedUsers.append(user)
                try:
                    await client(InviteToChannelRequest(group, [user]))
                    await asyncio.sleep(0.2)
                    countusers = countusers + 1
                except:
                    tentativi = tentativi + 1
                    pass
            else:
                break
        elif maxusers > 0 and countusers < maxusers:
            if canAdd:
                AddedUsers.append(user)
                try:
                    await client(InviteToChannelRequest(group, [user]))
                    await asyncio.sleep(0.2)
                    countusers = countusers + 1
                except:
                    tentativi = tentativi + 1
                    pass
            else:
                break


async def timeoutAdd(timeout):
    global canAdd
    await asyncio.sleep(timeout)
    canAdd = False


print("\033[92mdiminuire il controllo degli altri admin per le impostazioni seller?[Y/N]: (per argomento)")
try:
    controllolimitato = sys.argv[1].upper().startswith("Y")
except:
    controllolimitato = True
    print("controllo seller limitato: True, nessun argomento passato. es: python3 nomescript.py N")
bot = TelegramClient("bot", API_KEY, API_HASH, proxy=proxy)
archivialimitati = True
def raspacontrol():
    global raspingintelligentelist, ArchSSs
    R53 = False
    for voipdacontrollare in raspingintelligentelist:
        if datetime.now().date()> raspingintelligentelist[voipdacontrollare].date():
            R53 = True
            SSs[voipdacontrollare] = ArchSSs[voipdacontrollare]
            saveSS()
            del (ArchSSs[voipdacontrollare])
            saveArchSS()
    return R53

@bot.on(events.NewMessage(incoming=True))
async def RaspaManager(e):
    global ADMIN, Getter, Number, TempClient, proxy, API_KEY, API_HASH, ArchSSs, SSs, Grab, inAdding, canAdd, AddedUsers, ADMINS, controllolimitato, countusers, activeusers, maxusers, tentativi,archivialimitati, raspingintelligentelist
    if e.is_private:
        if e.chat_id == ADMIN or e.chat_id in ADMINS:
            if e.text == "/start":
                Getter, Number, TempClient = None, None, None
                if archivialimitati:
                    if raspacontrol():
                        await e.respond("**Contenitore di voip\n\n@ItsMatDev**",
                                        buttons=[[Button.inline("☎️ » Voip", "voip")]])
                    else:
                        await e.respond("**Contenitore di voip\n\n@ItsMatDev**",
                                        buttons=[[Button.inline("☎️ » Voip", "voip")]])
                else:
                    await e.respond("**Contenitore di voip\n\n@ItsMatDev**",
                                    buttons=[[Button.inline("☎️ » Voip", "voip")]
                                    ])

            elif Getter != None:
                if Getter == 0:
                    Getter = None
                    if not e.text in SSs:
                        if not e.text in ArchSSs:
                            TempClient = TMPTelegramClient(StringSession(), API_KEY, API_HASH, proxy=proxy)
                            await TempClient.connect()
                            try:
                                await TempClient.send_code_request(phone=e.text, force_sms=False)
                                Number = e.text
                                Getter = 1
                                await e.respond("**⚠️ » Inserisci il codice di accesso**",
                                                buttons=[[Button.inline("❌ Annulla", "voip")]])
                            except PhoneNumberFloodError:
                                await e.respond("**❌ » Troppi tentativi, prova un altro numero! [FloodWait]**",
                                                buttons=[[Button.inline("🔄 Riprova", "addvoip")]])
                            except:
                                await e.respond("**❌ » Numero non valido**",
                                                buttons=[[Button.inline("🔄 Riprova", "addvoip")]])
                        else:
                            await e.respond("**🔖 » Voip archiviato, riaggiungilo**",
                                            buttons=[[Button.inline("📁 Voip Archiviati", "arch")],
                                                     [Button.inline("🔄 Riprova", "addvoip")]])
                    else:
                        await e.respond("**❌ » Voip già aggiunto**", buttons=[[Button.inline("🔄 » Riprova", "addvoip")]])
                elif Getter == 1:
                    try:
                        await TempClient.sign_in(phone=Number, code=e.text)
                        SSs[Number] = StringSession.save(TempClient.session)
                        Getter, Number = None, None
                        saveSS()
                        await e.respond("**✅ » Voip Aggiunto**",
                                        buttons=[[Button.inline("🔙 » Indietro", "voip")]])
                    except SessionPasswordNeededError:
                        Getter = 2
                        await e.respond("**🔑 » Inserisci La Password**",
                                        buttons=[[Button.inline("❌ » Annulla", "voip")]])
                    except:
                        Getter, Number = None, None
                        await e.respond("**❌ » Codice Errato**", buttons=[[Button.inline("🔄 » Riprova", "addvoip")]])
                elif Getter == 2:
                    try:
                        await TempClient.sign_in(phone=Number, password=e.text)
                        SSs[Number] = StringSession.save(TempClient.session)
                        Getter, Number = None, None
                        saveSS()
                        await e.respond("**✅ » Voip Aggiunto**",
                                        buttons=[[Button.inline("🔙 » Indietro", "voip")]])
                    except:
                        Getter, Number = None, None
                        await e.respond("**❌ » Password Errata**", buttons=[[Button.inline("🔄 Riprova", "addvoip")]])
                elif Getter == 3:
                    Getter = None
                    if e.text in SSs:
                        await e.respond(f"**⚙️ » Gestione »** `{e.text}`", buttons=[
                            [Button.inline("📁 » FILE", "getSSS")],
                            [Button.inline("📁 » Archivia", "arch;" + e.text)],
                            [Button.inline("ℹ️ » Informazioni", "visualizza;" + e.text),
                             Button.inline("🔧 » Modifica / Ricevi codice", "setta;" + e.text)], [
                                Button.inline("➖ » Rimuovi", "del;" + e.text)], [Button.inline("🔙 » Indietro", "voip")]])
                    else:
                        await e.respond("**❌ » Voip Non Trovato**", buttons=[[Button.inline("🔄 » Riprova", "voips")]])
                elif Getter == 4:
                    Getter = None
                    if e.text in ArchSSs:
                        await e.respond(f"**🔧 » Gestione »** `{e.text}`", buttons=[
                            [Button.inline("🔄 » Riaggiungi", "add;" + e.text),
                             Button.inline("➖ » Rimuovi", "delarch;" + e.text)], [Button.inline("🔙 Indietro", "voip")]])
                    else:
                        await e.respond("**❌ » Voip Non Trovato ❌**", buttons=[[Button.inline("🔄 Riprova", "voips")]])
                elif Getter == 5:
                    Getter = None
                    if e.text != None and e.text != "":
                        if "t.me/" in e.text or "telegram.me/" in e.text or e.text.startswith("@"):
                            if not " " in e.text:
                                Grab = e.text
                                await e.respond("**✅ Gruppo Impostato Correttamente ✅**",
                                                buttons=[[Button.inline("✔ Raspa", "add")],
                                                         [Button.inline("🔙 Indietro", "grab")]])
                            else:
                                await e.respond("**❌ Al momento puoi inserire un solo gruppo ❌**",
                                                buttons=[[Button.inline("🔄 Riprova", "setgrab")]])
                        else:
                            await e.respond("**❌ Devi inserire un link o una @ di un gruppo ❌**",
                                            buttons=[[Button.inline("🔄 Riprova", "setgrab")]])
                    else:
                        await e.respond("**⚠️ Formato Non Valido ⚠️**",
                                        buttons=[[Button.inline("🔄 Riprova", "setgrab")]])
                elif Getter == 6:
                    Getter = None
                    skipped = 0
                    if e.text != None and e.text != "":
                        if "t.me/" in e.text or "telegram.me/" in e.text or e.text.startswith("@"):
                            if not " " in e.text:
                                inAdding = True
                                limitati = 0
                                banned = []
                                limited = []
                                Users = []
                                gruppo1_skipped =0
                                gruppo2_skipped = 0
                                countusers = 0
                                msg = await e.respond(
                                    "**✅ Aggiunta Membri In Corso ✅**\nATTENDI " + str(len(SSs) * 125) + " secondi (circa)..",
                                    buttons=[[Button.inline("❌ Interrompi", "stop")]])
                                for SS in SSs:
                                    isAlive = False
                                    CClient = TMPTelegramClient(StringSession(SSs[SS]), API_KEY, API_HASH, proxy=proxy)
                                    await CClient.connect()
                                    try:
                                        me = await CClient.get_me()
                                        if me == None:
                                            isAlive = False
                                        else:
                                            isAlive = True
                                    except:
                                        isAlive = False
                                    if isAlive:
                                        async with CClient as client:
                                            try:
                                                if "/joinchat/" in Grab:
                                                    if Grab.endswith("/"):
                                                        l = len(Grab) - 2
                                                        Grab = Grab[0:l]
                                                    st = Grab.split("/")
                                                    L = st.__len__() - 1
                                                    group = st[L]
                                                    try:
                                                        await client(ImportChatInviteRequest(group))
                                                    except:
                                                        pass
                                                else:
                                                    try:
                                                        await client(JoinChannelRequest(Grab))
                                                    except:
                                                        pass
                                                ent = await client.get_entity(Grab)
                                                try:
                                                    users = client.iter_participants(ent.id, aggressive=True)
                                                    ent2 = await client.get_entity(e.text)
                                                    await asyncio.sleep(0.5)
                                                    users2 = client.iter_participants(ent2.id, aggressive=True)
                                                    Users2 = []
                                                    async for user2 in users2:
                                                        Users2.append(user2.id)

                                                    async for user in users:
                                                        try:
                                                            if not user.bot and not user.id in Users:
                                                                if not user.id in Users2:
                                                                    if activeusers:
                                                                        accept = True
                                                                        try:
                                                                            lastDate = user.status.was_online
                                                                            num_months = (
                                                                                                 datetime.now().year - lastDate.year) * 12 + (
                                                                                                 datetime.now().month - lastDate.month)
                                                                            if (num_months > 1):
                                                                                accept = False
                                                                        except:

                                                                            continue
                                                                        if accept:
                                                                            Users.append(user.id)
                                                                    else:
                                                                        Users.append(user.id)

                                                        except:
                                                            pass
                                                except FloodWaitError as err:
                                                    await msg.edit(
                                                        f"**⏳ » Attendi {err.seconds} , il voip attuale sarà skippato. e passerò al prossimo voip dopo aver aspettato ⏳**")
                                                    await asyncio.sleep(err.seconds + 4)
                                                    gruppo2_skipped = gruppo2_skipped + 1
                                                    skipped = skipped + 1
                                                    pass
                                            except FloodWaitError as err:
                                                await msg.edit(
                                                    f"**⏳ » Attendi {err.seconds} , il voip attuale sarà skippato. e passerò al prossimo voip dopo aver aspettato ⏳**")
                                                await asyncio.sleep(err.seconds + 4)
                                                gruppo2_skipped = gruppo2_skipped + 1
                                                skipped = skipped + 1
                                                pass
                                            except:
                                                gruppo1_skipped = gruppo1_skipped+1
                                                skipped = skipped +1
                                                pass
                                            try:
                                                if "/joinchat/" in e.text:
                                                    if e.text.endswith("/"):
                                                        l = len(e.text) - 2
                                                        text = e.text[0:l]
                                                    else:
                                                        text = e.text
                                                    st = text.split("/")
                                                    L = st.__len__() - 1
                                                    group2 = st[L]
                                                    try:
                                                        await client(ImportChatInviteRequest(group2))
                                                    except:
                                                        pass
                                                else:
                                                    try:
                                                        await client(JoinChannelRequest(e.text))
                                                    except:
                                                        pass
                                                gialimitato = False

                                                canAdd = True
                                                await asyncio.gather(addUsers(client, Users, ent2.id), timeoutAdd(120))
                                                spambotchat = await client.get_entity("spambot")
                                                await client.send_message(spambotchat, "/start")
                                                messaggiospambot = await client.get_messages(spambotchat, limit=1)
                                                try:
                                                    if "re free" in messaggiospambot[0].message or "libero" in \
                                                            messaggiospambot[0].message:
                                                        print("free")
                                                    else:
                                                        gialimitato = True
                                                        limitati = limitati + 1
                                                        limited.append(SS)
                                                        print("not free")
                                                        try:
                                                            start = messaggiospambot[0].message.index(
                                                                "account is now limited until ") + len(
                                                                "account is now limited until ")
                                                            end = messaggiospambot[0].message.index(", 16:38 UTC",
                                                                                                    start)
                                                            e = messaggiospambot[0].message[start:end]
                                                            date2 = datetime.strptime(e, '%d %b %Y')
                                                            date2 += timedelta(days=1)
                                                            raspingintelligentelist[SS] = date2

                                                        except ValueError:
                                                            print("error")
                                                except Exception as e5:
                                                    print(e5)



                                                if tentativi > countusers and not gialimitato:
                                                    date2 = (datetime.now() + timedelta(hours=6))
                                                    raspingintelligentelist[SS] = date2
                                                    limitati = limitati + 1
                                                    limited.append(SS)

                                                for user in AddedUsers:
                                                    if user in Users:
                                                        Users.remove(user)
                                            except FloodWaitError as err:
                                                await msg.edit(
                                                    f"**⏳ Attendi altri {err.seconds} , il voip attuale sarà skippato. e passerò al prossimo voip dopo aver aspettato ⏳**")
                                                await asyncio.sleep(err.seconds + 4)
                                                gruppo2_skipped = gruppo2_skipped + 1
                                                skipped = skipped + 1
                                                pass
                                            except:
                                                gruppo2_skipped = gruppo2_skipped + 1
                                                skipped = skipped +1
                                                pass
                                    else:
                                        banned.append(SS)
                                        await e.respond(
                                            f"**⚠️ »** __Il voip__ `{SS}` potrebbe esser stato disconnesso o bannato da telegram")
                                if archivialimitati:
                                    if limited.__len__() > 0:
                                        for n2 in limited:
                                            if n2 in SSs:
                                                if not n2 in ArchSSs:
                                                    ArchSSs[n2] = SSs[n2]
                                                    saveArchSS()
                                                del (SSs[n2])
                                                saveSS()

                                if banned.__len__() > 0:
                                    for n in banned:
                                        if n in SSs:
                                            del (SSs[n])
                                    saveSS()
                                inAdding = False
                                if gruppo2_skipped > gruppo1_skipped:
                                    await msg.edit("**✅ Aggiunta Membri Completata ✅**" + "\nAggiunti: " + str(
                                        countusers) + "  ⏳⏳⏳  su un massimo di : " + str(
                                        maxusers) + "\n\n📱Voip skippati(riprova, per tentare di farli funzionare tutti.): " + str(
                                        skipped) + " su " + str(
                                        len(SSs) +limitati) + "\n♨️Voip limitati : " + str(limitati) + " su " + str(len(
                                        SSs) +limitati) + "\n\n🔬DIAGNOSI: la problematica maggiore è sul secondo gruppo.\n🤗consiglio: non sono compatibili gruppi privati, o canali."+"\nADDING INTELLIGENTE🧠 is: " + str(archivialimitati),
                                                   buttons=[[Button.inline("🔙 Indietro", "back")]])
                                elif gruppo1_skipped > gruppo2_skipped:
                                    await msg.edit("**✅ Aggiunta Membri Completata ✅**" + "\nAggiunti: " + str(
                                        countusers) + "  ⏳⏳⏳  su un massimo di : " + str(
                                        maxusers) + "\n\n📱Voip skippati(riprova, per tentare di farli funzionare tutti.): " + str(
                                        skipped) + " su " + str(len(
                                        SSs) +limitati) + "\n♨️Voip limitati : " + str(limitati) + " su " + str(len(
                                        SSs) +limitati) + "\n\n🔬DIAGNOSI: la problematica maggiore è sul primo gruppo.\n🤗consiglio: non sono compatibili gruppi privati, o canali."+"\nADDING INTELLIGENTE🧠 is: " + str(archivialimitati),
                                                   buttons=[[Button.inline("🔙 Indietro", "back")]])
                                else:
                                    await msg.edit("**✅ Aggiunta Membri Completata ✅**" + "\nAggiunti: " + str(
                                        countusers) + "  ⏳⏳⏳  su un massimo di : " + str(
                                        maxusers) + "\n\n📱Voip skippati(riprova, per tentare di farli funzionare tutti.): " + str(
                                        skipped) + " su " + str(len(
                                        SSs) + limitati) + "\n♨️Voip limitati : " + str(limitati) + " su " + str(len(
                                        SSs) + limitati)+"\nADDING INTELLIGENTE🧠 is: " + str(archivialimitati), buttons=[[Button.inline("🔙 Indietro", "back")]])

                            else:
                                await e.respond("**❌ Al momento puoi inserire un solo gruppo ❌**",
                                                buttons=[[Button.inline("🔄 Riprova", "add")]])
                        else:
                            await e.respond("**❌ Devi inserire un link o una @ di un gruppo ❌**",
                                            buttons=[[Button.inline("🔄 Riprova", "add")]])
                    else:
                        await e.respond("**⚠️ » Formato Non Valido**", buttons=[[Button.inline("🔄 Riprova", "add")]])
                elif Getter == 9:
                    Getter = None
                    try:
                        await TempClient(UpdateUsernameRequest(e.text))
                        await e.respond("✅ » Username Impostato",
                                        buttons=[[Button.inline("🔙 » Indietro", "back")]])
                    except:
                        await e.respond("❌ » Username occupato o non valido!",
                                        buttons=[[Button.inline("🔙 » Indietro", "back")]])
                elif Getter == 10:
                    Getter = None
                    try:
                        path = await bot.download_media(e.media)
                        print(path)
                        await TempClient(UploadProfilePhotoRequest(
                            await TempClient.upload_file(path)
                        ))
                        await e.respond("✅ » Foto impostata",
                                        buttons=[[Button.inline("🔙 » Indietro", "back")]])
                    except Exception as e:
                        print(str(e))
                        await e.respond("❌ » Foto non impostata!\n__Formato non valido!__",
                                        buttons=[[Button.inline("🔙 » Indietro", "back")]])
                elif Getter == 12:
                    Getter = None
                    try:
                        await TempClient(UpdateProfileRequest(
                            first_name=e.text
                        ))
                        await e.respond("✅ » Nome impostato",
                                        buttons=[[Button.inline("🔙 » Indietro", "back")]])
                    except:
                        await e.respond("❌ » Nome non impostato",
                                        buttons=[[Button.inline("🔙 » Indietro", "back")]])
                elif Getter == 13:
                    Getter = None
                    try:
                        await TempClient(UpdateProfileRequest(
                            last_name=e.text
                        ))
                        await e.respond("✅ » Cognome impostato",
                                        buttons=[[Button.inline("🔙 » Indietro", "back")]])
                    except:
                        await e.respond("❌ » Cognome non impostato",
                                        buttons=[[Button.inline("🔙 » Indietro", "back")]])
                elif Getter == 19 and e.chat_id == ADMIN:
                    Getter = None
                    maxusers = int(e.text)
                    await e.respond("utenti massimi settati a: " + str(maxusers),
                                    buttons=[[Button.inline("🔙 Indietro", "back")]])

            else:
                text1 = e.text.split(" ")
                try:
                    if "/admin" in text1[0] and e.chat_id == ADMIN:
                        ADMINS.append(int(text1[1]))
                        await e.respond("reso admin " + text1[1])
                    elif "/unadmin" in text1[0] and e.chat_id == ADMIN:
                        ADMINS.remove(int(text1[1]))
                        await e.respond("rimosso admin " + text1[1])
                except Exception as e4:
                    print(str(e4))


@bot.on(events.CallbackQuery())
async def callbackQuery(e):
    global ADMIN, Getter, Number, TempClient, API_KEY, proxy, API_HASH, ArchSSs, SSs, Grab, inAdding, ADMINS, controllolimitato, activeusers, maxusers,archivialimitati,raspingintelligentelist
    if e.sender_id == ADMIN or e.sender_id in ADMINS:
        if e.data == b"back":
            Getter, Number, TempClient = None, None, None
            await e.edit("**Contenitore di voip\n\n@ItsMatDev**", buttons=[[Button.inline("☎️ » Voip", "voip")]])
        elif e.data == b"adminpanel":
            if controllolimitato and e.sender_id != ADMIN:
                await e.answer("non hai la possibilità di accedervi.. \ncontrollo limitato.", alert=True)
            else:
                await e.edit("scegli un opzione:", buttons=[[Button.inline("max utenti📌", "maxutentiset")],
                                                            [Button.inline("solo attivi🌀", "attiviset")],
                                                            [Button.inline("OTTIENI FILE VOIP📳", "getSSS")],
                                                            [Button.inline("ADDING INTELLIGENTE🧠", "limitatiset")],
                                                            [Button.inline("RI-AGGIUNGI INTELLIGENTE🧠", "readd")],
                                                            [Button.inline("INFO LIMITATI🧠", "limitinfo")],
                                                            [Button.inline("🔙 Indietro", "back")]])
        elif e.data == b"maxutentiset":
            if controllolimitato and e.sender_id != ADMIN:
                await e.answer("non hai la possibilità di accedervi.. \ncontrollo limitato.", alert=True)
            else:
                Getter = 19
                await e.edit("inserisci un numero utenti:", buttons=[[Button.inline("🔙 Indietro", "back")]])
        elif e.data == b"readd":
            if controllolimitato and e.sender_id != ADMIN:
                await e.answer("non hai la possibilità di accedervi.. \ncontrollo limitato.", alert=True)
            else:
                raspcontrollo =raspacontrol()
                await e.answer("DEI VOIP SONO STATI RIAGGIUNTI?🧠 is: " + str(raspcontrollo), alert=True)
        elif e.data == b"limitinfo":
            if controllolimitato and e.sender_id != ADMIN:
                await e.answer("non hai la possibilità di accedervi.. \ncontrollo limitato.", alert=True)
            else:
                for data4 in raspingintelligentelist:
                    await e.client.send_message(e.sender_id, "il voip "+ data4 +" sarà slimitato il : "+ raspingintelligentelist[data4].strftime('%d/%m/%Y %H:%M'))
                await e.client.send_message(e.sender_id, "**Contenitore di voip\n\n@ItsMatDev**",
                                buttons=[[Button.inline("📞 Voip", "voip")]])
        elif e.data == b"limitatiset":
            if controllolimitato and e.sender_id != ADMIN:
                await e.answer("non hai la possibilità di accedervi.. \ncontrollo limitato.", alert=True)
            else:
                archivialimitati = not archivialimitati
                await e.answer("ADDING INTELLIGENTE🧠 is: " + str(archivialimitati), alert=True)
        elif e.data == b"attiviset":
            if controllolimitato and e.sender_id != ADMIN:
                await e.answer("non hai la possibilità di accedervi.. \ncontrollo limitato.", alert=True)
            else:
                activeusers = not activeusers
                await e.answer("solo attivi is: " + str(activeusers), alert=True)

        elif e.data == b"getSSS":
            if controllolimitato and e.sender_id != ADMIN:
                await e.answer("non hai la possibilità di accedervi.. \ncontrollo limitato.", alert=True)
            else:
                await e.respond("🗂 » File voip", file="SSs.json")
        elif e.data == b"stop":
            await e.edit("**✅ Aggiunta Interrotta ✅**", buttons=[[Button.inline("🔙 Indietro", "back")]])
            python = sys.executable
            if controllolimitato:
                os.execl(python, python, *sys.argv, "Y")
            else:
                os.execl(python, python, *sys.argv, "N")
        elif inAdding:
            await e.answer("❌» Questa sezione è bloccata!", alert=True)
        elif e.data == b"voip":
            Getter, Number, TempClient = None, None, None
            await e.edit(f"💫 » Voip Aggiunti »**{SSs.__len__()}**",
                         buttons=[[Button.inline("➕ » Aggiungi", "addvoip"), Button.inline("🔐 » Gestione", "voips")],
                                  [Button.inline("📁 » Archivio", "arch")], [Button.inline("🗂 » File", "getSSS")], [Button.inline("🔙 » Indietro", "back")]])
        elif e.data == b"addvoip":
            Getter = 0
            await e.edit("**☎️ » Inserisci il numero**",
                         buttons=[Button.inline("❌ Annulla", "voip")])
        elif e.data == b"voips":
            if SSs.__len__() > 0:
                Getter = 3
                msg = "☎️ » Invia il numero del voip che vuoi gestire\n\n**📚 » LISTA VOIP**"
                for n in SSs:
                    msg += f"\n`{n}`"
                await e.edit(msg, buttons=[Button.inline("❌ Annulla", "voip")])
            else:
                await e.edit("**❌ » Non hai aggiunto nessun voip **",
                             buttons=[[Button.inline("➕ » Aggiungi", "addvoip")], [Button.inline("🔙 » Indietro", "voip")]])
        elif e.data == b"arch":
            if ArchSSs.__len__() > 0:
                Getter = 4
                msg = f"📁 » Voip Archiviati » **{ArchSSs.__len__()}**\n\n__☎️ » Invia il numero del voip archiviato che vuoi gestire__\n\n**LISTA VOIP ARCHIVIATI**"
                for n in ArchSSs:
                    msg += f"\n`{n}`"
                await e.edit(msg, buttons=[Button.inline("❌ » Annulla", "voip")])
            else:
                await e.edit("**❌ » Non hai archiviato nessun voip**", buttons=[[Button.inline("🔙 » Indietro", "voip")]])
        elif e.data == b"grab":
            if Grab == None:
                await e.edit("**❌ Gruppo Non Impostato ❌\n\nℹ️ Puoi impostarlo usando il bottone qui sotto!**",
                             buttons=[[Button.inline("✍🏻 Imposta", "setgrab")],
                                      [Button.inline("🔙 Indietro", "back")]])
            else:
                await e.edit(f"__👥 Gruppo impostato »__ **{Grab}**",
                             buttons=[[Button.inline("✍🏻 Modifica", "setgrab")],
                                      [Button.inline("🔙 Indietro", "back")]])
        elif e.data == b"setgrab":
            Getter = 5
            await e.edit("__👥 Invia la @ o il link del gruppo da cui vuoi rubare gli utenti!__",
                         buttons=[Button.inline("❌ Annulla", "back")])
        elif e.data == b"add":
            if SSs.__len__() > 0:
                if Grab != None:
                    Getter = 6
                    await e.edit("__➕ Invia la @ o il link del gruppo in cui vuoi aggiungere gli utenti!__",
                                 buttons=[[Button.inline("❌ Annulla", "back")]])
                else:
                    await e.edit("**❌ Impostare il gruppo da cui rubare gli utenti ❌**",
                                 buttons=[[Button.inline("👥 Ruba", "grab")], [Button.inline("🔙 Indietro", "back")]])
            else:
                await e.edit("**❌ Non hai aggiunto nessun voip ❌**",
                             buttons=[[Button.inline("➕ Aggiungi", "addvoip")], [Button.inline("🔙 Indietro", "back")]])
        else:
            st = e.data.decode().split(";")
            if st[0] == "setnome":
                if st[1] in SSs:
                    Getter = 12
                    TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH, proxy=proxy)
                    await TempClient.connect()
                    me = await TempClient.get_me()
                    await e.edit("**🥀 » Inserisci il nome**\nNome attuale: " + me.first_name)
            elif st[0] == "setcognome":
                if st[1] in SSs:
                    Getter = 13
                    TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH, proxy=proxy)
                    await TempClient.connect()
                    me = await TempClient.get_me()
                    await e.edit(
                        "**👑 » Inserisci il cognome**\nAttuale: " + str(me.last_name))
            elif st[0] == "getmsg":
                TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH, proxy=proxy)
                await TempClient.connect()
                messages = await TempClient.get_messages(777000, limit=1)
                await e.client.send_message(e.sender_id, "**🚨 » MESSAGGIO D'ACCESSO RICEVUTO**\n\n"+ messages[0].message)
            elif st[0] == "setta":
                if st[1] in SSs:
                    await e.edit(
                        "**⚙️ » Impostazioni voip:** " + st[1] + "\n__🔙 » /start__",
                        buttons=[
                            [Button.inline("🌩 » Codice d'accesso", "getmsg;" + st[1])], [Button.inline("💠 » Imposta username", "setusername;" + st[1])],
                                 [Button.inline("🖼 » Imposta foto profilo", "setphoto;" + st[1])],
                                 [Button.inline("🥀 » Imposta nome", "setnome;" + st[1])],

                                 [Button.inline("👑 » Imposta cognome", "setcognome;" + st[1])]])
            elif st[0] == "visualizza":
                if st[1] in SSs:
                    try:
                        TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH, proxy=proxy)
                        await TempClient.connect()
                        me = await TempClient.get_me()
                        path = await TempClient.download_profile_photo("me")
                        await bot.send_file(e.sender_id, path,
                                            caption="🌐 » Username: " + str(me.username) + "\n❇️ » Nome :" + me.first_name + "\n💠 » Cognome: " + str(
                                                me.last_name) + "\n🆔 » ID: " + str(
                                                me.id) + "\n🔙 » /start",
                                            buttons=[[Button.inline("🔧IMPOSTAZIONI VOIP🔧", "setta;" + st[1])]])

                    except Exception as e:
                        print(str(e))
            elif st[0] == "setusername":
                if st[1] in SSs:
                    Getter = 9
                    TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH, proxy=proxy)
                    await TempClient.connect()
                    me = await TempClient.get_me()
                    await e.edit("**🌐 » Invia l'username da impostare**\n__☑️ » Attuale: " + me.username,
                                 buttons=[[Button.inline("🔙 » Indietro", "back")]])
            elif st[0] == "setphoto":
                if st[1] in SSs:
                    Getter = 10
                    TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH, proxy=proxy)
                    await TempClient.connect()
                    await e.edit("**🖼 » Invia la foto da impostare **",
                                 buttons=[[Button.inline("🔙 » Indietro", "voip")]])
            elif st[0] == "arch":
                if st[1] in SSs:
                    if not st[1] in ArchSSs:
                        ArchSSs[st[1]] = SSs[st[1]]
                        saveArchSS()
                    del (SSs[st[1]])
                    saveSS()
                    await e.edit("**✅ » Voip Archiviato Correttamente**",
                                 buttons=[[Button.inline("🔙 Indietro", "voip")]])
                else:
                    await e.edit("**❌ » Voip Non Trovato**", buttons=[[Button.inline("🔙 Indietro", "voip")]])
            elif st[0] == "add":
                if st[1] in ArchSSs:
                    SSs[st[1]] = ArchSSs[st[1]]
                    saveSS()
                    del (ArchSSs[st[1]])
                    saveArchSS()
                    await e.edit("**✅ » Voip Riaggiunto**",
                                 buttons=[[Button.inline("🔙 Indietro", "voip")]])
                else:
                    await e.edit("**❌ » Voip Non Trovato**", buttons=[[Button.inline("🔙 Indietro", "voip")]])
            elif st[0] == "del":
                if st[1] in SSs:
                    CClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH, proxy=proxy)
                    await CClient.connect()
                    try:
                        me = await CClient.get_me()
                        if me != None:
                            async with CClient as client:
                                await client.log_out()
                    except:
                        pass
                    del (SSs[st[1]])
                    saveSS()
                    await e.edit("**✅ » Voip Rimosso **", buttons=[[Button.inline("🔙 Indietro", "voip")]])
                else:
                    await e.edit("**❌ » Voip Già Rimosso**", buttons=[[Button.inline("🔙 Indietro", "voip")]])
            elif st[0] == "delarch":
                if st[1] in ArchSSs:
                    CClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH, proxy=proxy)
                    await CClient.connect()
                    try:
                        me = await CClient.get_me()
                        if me != None:
                            async with CClient as client:
                                await client.log_out()
                    except:
                        pass
                    del (ArchSSs[st[1]])
                    saveArchSS()
                    await e.edit("**✅ » Voip Rimosso Correttamente**", buttons=[[Button.inline("🔙 Indietro", "voip")]])
                else:
                    await e.edit("**❌ » Voip Già Rimosso**", buttons=[[Button.inline("🔙 Indietro", "voip")]])
            elif st[0] == "info":
                await e.answer(f"ℹ️ » L' errore è avvenuto nel seguente voip » {st[1]} ")


print("mi raccomando, inserisci il token del bot..")
bot.start()

bot.run_until_disconnected()
