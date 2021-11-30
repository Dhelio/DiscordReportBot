import discord
import datetime
from datetime import date
import asyncio
from discord.flags import Intents
from discord.user import User
from ReportStage import ReportPrompt, ReportStage
from Utils import *
from Reports import Reports

intents = discord.Intents.default()
intents.members = True
reports : Reports = None
client = discord.Client(intents=intents)

async def PostReport(Id : int):
    console(LogType.DEBUG, "PostReport", f"Enumerating guilds.")
    for guild in client.guilds:
        console(LogType.DEBUG, "PostReport", f"{guild.name}")
        #if guild.name == "DhlWorksTestServer" or "Youbiquo":
        if guild.name == "DhlWorksTestServer":
            for channel in guild.channels:
                console(LogType.DEBUG, "PostReport", f"{channel.name}")
                if channel.name == "weekly-report":
                    answers = reports.GetUserAnswers(Id)
                    post : str = "L'utente **"+reports.GetUser(Id).displayName+"** ha postato un nuovo report!\n"
                    post += f"<@{Id}> -- {guild.get_member(Id).avatar_url}\n"
                    post += "**"+ReportPrompt.WHAT_BEFORE+"**\n"
                    post += answers[ReportStage.WHAT_BEFORE.value] + "\n\n"
                    post += "**"+ReportPrompt.DIFFICULTIES+"**\n"
                    post += answers[ReportStage.DIFFICULTIES.value] + "\n\n"
                    post += "**"+ReportPrompt.DELAYS+"**\n"
                    post += answers[ReportStage.DELAYS.value] + "\n\n"
                    post += "**"+ReportPrompt.WHAT_NEXT+"**\n"
                    post += answers[ReportStage.WHAT_NEXT.value] + "\n\n"
                    await channel.send(post)

@client.event
async def on_ready():
    global reports
    log_init()
    log(LogType.DEBUG, "on_ready", "Bot avviato e loggato.")
    reports = Reports()
    print(f'Bot inizializzato.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    message.content = message.content.lower()
    if message.content == 'ciao' or message.content == 'aiuto' or message.content == 'help':
        msg : str = "Ciao!\n"
        msg += "Posso registrarti alla lista dei report. Scrivi semplicemente 'registrami' per essere abilitato.\n"
        msg += "Se vuoi registrarti con un nome diverso rispetto al tuo nome utente, scrivimi 'registrami come' seguito dal nome desiderato. Per esempio, 'registrami come Pippo Baudo' farà comparire come nome nei report Pippo Baudo.\n"
        msg += "Se invece sei già registrato e vuoi cambiare nome, scrivimi 'rinominami in' seguito dal nome desiderato. Per esempio, 'rinominami in Frank Sinatra' ti rinominerà il report in 'Frank Sinatra'\n"
        await message.channel.send(msg)
    elif message.content == 'registrami':
        reports.AddUser(message.author.id, message.author.name, message.author.display_name)
        await message.channel.send('Ok. Sei registrato nella lista dei report.')
    elif message.content == '16011991':
        await RequestReports()
    elif message.content == "16011984":
        user = reports.GetUser(message.author.id)
        user.reportStage = ReportStage.IDLE
        await message.channel.send(user.reportPrompt)
    elif message.content == "we":
        await message.channel.send("Oh.")
    elif message.content == "grazie":
        await message.channel.send("Le grazie le fa la Madonna.")
    elif message.content.startswith("registrami come"):
        msg : str = message.content
        msg = msg.removeprefix("registrami come ")
        reports.AddUser(message.author.id, message.author.name, msg)
        await message.channel.send(f"Fatto, <@{message.author.id}>, ti ho registrato come {msg}.")
    elif message.content.startswith("rinominami in"):
        msg : str = message.content
        msg = msg.removeprefix("rinominami in ")
        reports.SetUserDisplayName(message.author.id, msg)
        await message.channel.send(f"Fatto, <@{message.author.id}>, ti ho rinominato in {msg}.")
    elif message.content == "cosa vorresti avere?":
        await message.channel.send("Vorrei avere l'1% dei soldi di Zanesco!")
    else:
        if reports.IsUserEnabled(message.author.id):
            if reports.GetUserStage(message.author.id) == ReportStage.DONE:
                await message.channel.send(f"Purtroppo al momento non stai eseguendo i report. Ti avviso io quando partono.")
                return
            reports.RegisterUserAnswer(message.author.id, message.content)
            reports.AdvanceUserStage(message.author.id)
            await message.channel.send(reports.GetUserStagePrompt(message.author.id))
            if reports.HasUserDone(message.author.id):
                await PostReport(message.author.id)

async def RequestReports():
    global reports
    for guild in client.guilds:
        console(LogType.DEBUG, "Bot_RequestReports", f'Analyzing guild {guild.name}')
        console(LogType.DEBUG, "Bot_RequestReports",f'Getting {guild.name} members list...')
        members = await guild.chunk()
        for member in members:
            console(LogType.DEBUG, "Bot_RequestReports", f'Analyzing member {member.name}')
            user : User = reports.GetUser(member.id)
            if not user == None:
                console(LogType.DEBUG, "Bot_RequestReports", f'User {user.name} is enabled for reports with display name {user.displayName}. Resetting report stage...')
                user.ResetStage()
                await member.send(user.reportPrompt)

async def ReportLoop():
    await client.wait_until_ready()
    while not client.is_closed():
        if date.today().weekday() == 4: # se è venerdì...
            if datetime.datetime.now() > datetime.time(12,0,0) and datetime.datetime.now() < datetime.time(18,0,0):
                await RequestReports()
                await asyncio.sleep(3600*24)
            else:
                await asyncio.sleep(3600)
        else:
            await asyncio.sleep(3600*24)
                
    
client.loop.create_task(ReportLoop())
client.run('OTE0NzkzODc4ODE1NjYyMTMw.YaSOMA.6H9mu7iWi8q-UoAP06IH498Hbkc')