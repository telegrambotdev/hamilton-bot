commands = {
    "/start": lambda client, msg, args: msg.reply(msg.lang["start"]["ok"])
}


async def handler(client, msg):
    client.select_lang(msg, "private")
    commands["/setlang"] = client.all.getlangs
    commands["/help"] = client.all.help
    commands["/channel"] = client.all.channel
    commands["/status"] = client.all.status
    args = msg.text.split()
    command = args[0]
    args.remove(command)
    if command in commands:
        await commands[command](client, msg, args)
