import discord
from discord.ext import tasks
from datetime import datetime as dt
import datetime
import re
import json
import pickle

user = []
remember = []
timeL = []
date = []

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#get saved data from files to variables
with open('channelid.txt', 'r') as f:
    cid = int(f.read())
try:
    with open("user.pickle", "rb") as fu:
        user = pickle.load(fu)
except:
    with open("user.pickle", "wb") as fu:
        print("user.pickle not found, creating file...")
try:
    with open("remember.pickle", "rb") as fr:
        remember = pickle.load(fr)
except:
    with open("remember.pickle", "wb") as fr:
        print("remember.pickle not found, creating file...")
try:
    with open("timeL.pickle", "rb") as ft:
        timeL = pickle.load(ft)
except:
    with open("timeL.pickle", "wb") as ft:
        print("timeL.pickle not found, creating file...")
try:
    with open("date.pickle", "rb") as fd:
        date = pickle.load(fd)
except:
    with open("date.pickle", "wb") as fd:
        print("date.pickle not found, creating file...")
try:
    with open('config.json') as f:
      data = json.load(f)
      for c in data['botConfig']:
         print('Prefix: ' + c['prefix'])
         print('Token: ' + c['token'])
except:
    print("config file not found!")
    exit()
print(f"channel id saved: {str(cid)}")

#save data to files
def updateFile():
    with open("user", "wb") as fu:  # Pickling
        pickle.dump(user, fu)
    with open("remember", "wb") as fr:  # Pickling
        pickle.dump(remember, fr)
    with open("timeL", "wb") as ft:  # Pickling
        pickle.dump(timeL, ft)
    with open("date", "wb") as fd:  # Pickling
        pickle.dump(date, fd)

#convert HHam/ph time to HH:MM
def HHtoHHMM(time):
    if time == "12am":
        return "00:00"
    elif time == "1am":
        return "01:00"
    elif time == "2am":
        return "02:00"
    elif time == "3am":
        return "03:00"
    elif time == "4am":
       return "04:00"
    elif time == "5am":
       return "05:00"
    elif time == "6am":
       return "06:00"
    elif time == "7am":
       return "07:00"
    elif time == "8am":
       return "08:00"
    elif time == "9am":
       return "09:00"
    elif time == "10am":
       return "10:00"
    elif time == "11am":
       return "11:00"
    elif time == "12pm":
       return "12:00"
    elif time == "1pm":
       return "13:00"
    elif time == "2pm":
       return "14:00"
    elif time == "3pm":
       return "15:00"
    elif time == "4pm":
       return "16:00"
    elif time == "5pm":
       return "17:00"
    elif time == "6pm":
       return "18:00"
    elif time == "7pm":
       return "19:00"
    elif time == "8pm":
       return "20:00"
    elif time == "9pm":
       return "21:00"
    elif time == "10pm":
       return "22:00"
    elif time == "11pm":
       return "23:00"

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    CheckReminders.start()
    TodaysReminders.start()
    now = dt.now()
    current_time = now.strftime("%H:%M")
    for i in timeL:
        print(f"{current_time}: reminders stored for {user[timeL.index(i)]} about {remember[timeL.index(i)]} at {i}")
    return

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    now = dt.now()
    current_time = now.strftime("%H:%M")
    current_date = now.strftime("%d")
    current_month = now.strftime("%m")
    id = "<@" + str(message.author.id) + ">"
    if message.content.startswith(f'{c["prefix"]}test'):
        await message.channel.send("I am alive")
    if message.content.startswith(f'{c["prefix"]}rmb'):
        temp = message.content.replace("$rmb","")
        breakdown = temp.split()
        if(breakdown[-1] != None):
            if breakdown[-1].lower() == "today":
                date.append(now.strftime("%d/%m"))
            elif breakdown[-1].lower() == "tmr":
                dd = int(current_date) + 1
                dd = str(dd).zfill(2)
                mm = current_month
                dd = (dd + "/" + mm)
                date.append(dd)
            elif breakdown[-1].lower() =="monday":
                today = datetime.date.today()
                day = today + datetime.timedelta((0 - today.weekday()) % 7)
                date.append(day.strftime("%d/%m"))
            elif breakdown[-1].lower() =="tuesday":
                today = datetime.date.today()
                day = today + datetime.timedelta((1 - today.weekday()) % 7)
                date.append(day.strftime("%d/%m"))
            elif breakdown[-1].lower() =="wednesday":
                today = datetime.date.today()
                day = today + datetime.timedelta((2 - today.weekday()) % 7)
                date.append(day.strftime("%d/%m"))
            elif breakdown[-1].lower() =="thursday":
                today = datetime.date.today()
                day = today + datetime.timedelta((3 - today.weekday()) % 7)
                date.append(day.strftime("%d/%m"))
            elif breakdown[-1].lower() =="friday":
                today = datetime.date.today()
                day = today + datetime.timedelta((4 - today.weekday()) % 7)
                date.append(day.strftime("%d/%m"))
            elif breakdown[-1].lower() =="saturday":
                today = datetime.date.today()
                day = today + datetime.timedelta((5 - today.weekday()) % 7)
                date.append(day.strftime("%d/%m"))
            elif breakdown[-1].lower() =="sunday":
                today = datetime.date.today()
                day = today + datetime.timedelta((6 - today.weekday()) % 7)
                date.append(day.strftime("%d/%m"))
            else:
                date.append(now.strftime("%d/%m"))
        time = re.search("([0-1]?[0-9]|2[0-3]):[0-5][0-9]",temp)
        if(time != None):
            temp = temp.replace(time.group(), "").rstrip()
            user.append(id)
            remember.append(temp)
            timeL.append(time.group())
            print(user[-1], remember[-1], timeL[-1])
            await message.channel.send(f"{id}I will remind you about{temp} at {time.group()}")
        time = re.search("([0-9]|1[0-2])([AaPp][Mm])",temp)
        if (time != None):
            temp = temp.replace(time.group(), "").rstrip()
            time = str(time.group())
            print(time)
            time = HHtoHHMM(time.lower())
            print(time)
            user.append(id)
            remember.append(temp)
            timeL.append(time)
            print(f"{current_time}: reminder added for {id} about {temp} at {time}")
            await message.channel.send(f"{id}I will remind you about {temp} at {time}")
        updateFile()
        return
    if message.content.startswith(f'{c["prefix"]}clearall'):
        for i in timeL:
            del user[timeL.index(i)]
            del remember[timeL.index(i)]
            del date[timeL.index(i)]
            del timeL[timeL.index(i)]
            updateFile()
        await message.channel.send(f"{id}, all reminders cleared!")
    if message.content.startswith(f'{c["prefix"]}showall'):
        await message.channel.send(f"{id}, reminders you have are:")
        for i in timeL:
            print(f"{current_time}: reminders stored for {user[timeL.index(i)]} about {remember[timeL.index(i)]} at {i}")
            await message.channel.send(f"{user[timeL.index(i)]}, reminders about {remember[timeL.index(i)]} at {i} {date[timeL.index(i)]}")
    if message.content.startswith(f'{c["prefix"]}here'):
        channelid = message.channel.id
        with open('channelid.txt', 'w') as f:
            f.write(str(channelid))
        await message.channel.send(f"{id}, I will announce reminders in this channel now")
#check for reminders every second
@tasks.loop(seconds=1)
async def CheckReminders():
    BotChannel = client.get_channel(cid)
    now = dt.now()
    current_time = now.strftime("%H:%M")
    current_date = now.strftime("%d/%m")
    for x in date:
        if current_date == x:
            for i in timeL:
                if current_time == i:
                    print(f"{current_time}: annoucing reminder for {user[timeL.index(i)]} about {remember[timeL.index(i)]}")
                    await BotChannel.send(f"{user[timeL.index(i)]}, reminder about {remember[timeL.index(i)]}")
                    del user[timeL.index(i)]
                    del remember[timeL.index(i)]
                    del date[timeL.index(i)]
                    del timeL[timeL.index(i)]
                    updateFile()
#announce reminders for today at midnight
@tasks.loop(minutes=1)
async def TodaysReminders():
    BotChannel = client.get_channel(cid)
    now = dt.now()
    current_time = now.strftime("%H:%M")
    current_date = now.strftime("%d/%m")
    print(f"{current_time} checking for reminders today")
    for x in date:
        if current_date == x:
            for i in timeL:
                if current_time == i:
                    print(
                        f"{current_time}: annoucing reminder for {user[timeL.index(i)]} about {remember[timeL.index(i)]}")
                    await BotChannel.send(f"{user[timeL.index(i)]}, reminder about {remember[timeL.index(i)]}")

client.run(c['token'])