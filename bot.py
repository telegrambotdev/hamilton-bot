from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from json import load
from os import listdir, environ
import database
# Tipos de chats
import alltypes
import group
import private

if environ.get("CONFIG_URL"):
    print("Downloading configuration file...")
    from urllib.request import urlretrieve
    url = environ.get("CONFIG_URL")
    urlretrieve(url, filename="config.ini")
    print("Complete")

app = Client("Hamilton-bot")
app.all = alltypes
app.conf = load(open("bot.json"))
app.db = database.crub(database.sqlite, file="banco.db")
app.langs = {}
for fname in listdir("lang/"):
    code = fname.split(".")[0]
    app.langs[code] = load(open("lang/"+fname))


def select_lang(msg, chat_type=None):
    lang = app.db.get_lang(msg.chat.id)
    if lang:
        code = lang[0][0]
    else:
        code = "pt-br"
    msg.lang = app.langs[code]
    if chat_type:
        msg.lang = msg.lang["commands"][chat_type]
    return code


app.select_lang = select_lang


@app.on_callback_query()
async def callback(client, msg):
    args = msg.data.split()
    command = args[0]
    args.pop(0)
    if command == "setlang":
        await client.all.setlang(client, msg, args)


@app.on_message(filters.new_chat_members)
async def new_members(client, msg):
    me = await client.get_me()
    client.select_lang(msg)
    try:
        welcome = app.db.getwelcome(msg.chat.id)
    except Exception:
        welcome = msg.lang["default"]["welcome"]
    chat = msg.chat
    for member in msg.new_chat_members:
        if member.id == me.id:
            await client.send_message(chat.id, "Hello!")
            continue
        await client.send_message(
            chat.id,
            text=welcome.format(
                username=member.username,
                first_name=member.first_name,
                last_name=member.last_name,
                user_id=member.id,
                chat_name=chat.title,
                chat_id=chat.id
            )
        )

app.add_handler(MessageHandler(group.handler, filters.group))
app.add_handler(MessageHandler(private.handler, filters.private))

app.run()
