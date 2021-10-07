# Created by ProfessorPiggos
# See LICENSE file for LICENSE, GNU AFFERO GENERAL PUBLIC LICENSE v3
# As of Python version 3.7, dictionaries are ordered. In Python 3.6 and earlier, dictionaries are unordered.

# This must be changed to a valid host of your source code if you modify the bot in any way. 
# This is a requirement of the license, and is in this bot to encourage sharing of modifications.
# If you modify or remove the info command in any way to limit the sharing of source code, you must provide another way to share it with users.
sourcecodelink = 'https://github.com/ProfessorPiggos/HyCord/'

import nextcord
import aiohttp
import asyncio
import json
import sys
from nextcord.ext import commands, tasks
from datetime import datetime, timezone
import re

import logging
logging.basicConfig(level=logging.INFO) # Setting up logging

try:
    with open("prefix.txt","r") as prefixfile:
        prefix = prefixfile.readlines()[0]
        prefixfile.close()
except Exception:
    prefix = ','
    logging.info('error reading prefix, setting to comma')

intents = nextcord.Intents.default()
description = "Bot that interfaces Hypixel API Data into Discord"
bot = commands.Bot(command_prefix=prefix, description=description, intents=intents)

dumpcount = -1 #setting up counter for dump, it's at -1 since tasks run right away

# Saving all of the configuration files. This could be changed to a singular config file, but this works for now.
with open("discordtoken.txt", "r") as tokenfile:
    token = tokenfile.readlines()[0]
    tokenfile.close()

try:
    with open("notifications.txt", "r") as settingsfile:
        settings = settingsfile.readlines()[0]
        settingsfile.close()
        if settings == "on":
            notificationsOn = True
        else:
            notificationsOn = False
except IOError:
    notificationsOn = True

try:
    with open("hypixelapikey.txt", "r") as keyfile:
        apikey = keyfile.readlines()[0]
        keyfile.close()
except IOError:
    if notificationsOn:
        logging.warning("No Hypixel API key specified. Notification service has been disabled. Please add a hypixel api key if you would like to use notifications.")
    notificationsOn = False

if notificationsOn:
    GAMESLIST = ['join','leave','BEDWARS',"DUELS","SKYBLOCK","BUILD_BATTLE",'PIT','SMP','PROTOTYPE','SKYWARS','MCGO','ARCADE','TNTGAMES','UHC','MURDER_MYSTERY','SURVIVAL_GAMES','QUAKECRAFT','GINGERBREAD']
    USERGAMESLIST = ['Join','Leave','Bedwars','Duels','Skyblock','Build Battle', 'The Pit', 'SMP', 'Prototype Games', 'Skywars','Cops and Crims', 'Arcade Games', 'TNT Games', 'UHC', 'Murder Mystery', 'Blitz Survival Games', 'Quakecraft', 'Turbo Kart Racers']
    try:
        with open('data.json','r') as listfile:
            jslist = json.load(listfile)
            if not "track" in jslist:
                jslist['track'] = {}
            if not 'listcmd' in jslist:
                jslist['listcmd'] = {}
            if not 'settings' in jslist:
                jslist['settings'] = {}
            if not 'online' in jslist:
                jslist['online'] = {}
            listfile.close()
    except (IOError,TypeError):
        jslist = {
            'track': {},
            'listcmd': {},
            'settings': {},
            'online': {}
        }
        logging.info("JSON File not found. Creating one.")

try:
    with open('ownerid.txt','r') as owneridfile:
        ownerid = int(owneridfile.readlines()[0]) # Might add support for multiple admins later.
        ownerfeatures = True
        owneridfile.close()
except IOError:
    ownerfeatures = False
    logging.info("Owner ID not specified. Stop command disabled.")


class Notifications(commands.Cog): #Notification service, can be disabled with notifications.txt
    def __init__(self,bot):
        self.check.start()

    @tasks.loop(seconds=20)
    async def onlinecheck(self):
        for a in jslist['online']:
            if jslist['online'][a]['trueonline']:
                curname = jslist['online'][a]['displayname']
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.hypixel.net/status?key={apikey}&uuid={a}') as r:
                        if r.status == 200:
                            js = await r.json()   
                            if not js['session']['online']:
                                for b in jslist['track'][a]:
                                    if jslist['settings'][str(b)]['leave']:
                                        user = await bot.fetch_user(b)
                                        await user.send(f'**{curname} left**')
                            elif jslist['online'][a]['game'] != js['session']['gameType'] and js['session']['gameType'] != "MAIN" and js['session']['gameType'] != "LIMBO" and js['session']['mode'] != "LOBBY":
                                jslist['online'][a]["game"] = js["session"]["gameType"]
                                jslist['online'][a]["mode"] = js["session"]["mode"]
                                game = USERGAMESLIST[GAMESLIST.index(jslist['online'][a]["game"])]
                                mode = jslist['online'][a]["mode"]
                                for b in jslist['track'][a]:
                                    if jslist['settings'][str(b)][js['session']['gameType']]:
                                        user = await bot.fetch_user(b)
                                        await user.send(f'**{curname}** joined the game "{game}". They are currently in the mode "{mode}".')
    @tasks.loop(seconds=45)
    async def check(self):
        global dumpcount
        unixtime = int(datetime.now(timezone.utc).timestamp() * 1000)
        for a in jslist['track']:
            if not a in jslist['online']:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.hypixel.net/status?key={apikey}&uuid={a}') as r:
                        if r.status == 200:
                            js = await r.json()
                            if js['session']['online']:
                                    jslist['online'][a] = {}
                                    jslist['online'][a]['trueonline'] = True
                                    jslist['online'][a]["game"] = js["session"]["gameType"]
                                    jslist['online'][a]["mode"] = js["session"]["mode"]
                                    async with aiohttp.ClientSession() as session2:
                                        async with session2.get(f'https://api.mojang.com/user/profiles/{a}/names') as t:
                                            if t.status == 200:
                                                js2 = await t.json()
                                                curname = js2[(len(js2)-1)]["name"]
                                                jslist['online'][a]['displayname'] = curname
                                                try:
                                                    game = USERGAMESLIST[GAMESLIST.index(jslist['online'][a]["game"])]
                                                except Exception: #if user in limbo or lobby or smthn
                                                    game = jslist['online'][a]["game"]
                                                mode = jslist['online'][a]["mode"]
                                            else:
                                                logging.error("Error with Mojang API")
                                                continue
                            else:
                                async with aiohttp.ClientSession() as session2:
                                    async with session2.get(f'https://api.hypixel.net/player?key={apikey}&uuid={a}') as y:
                                        if y.status == 200:
                                            js3 = await y.json()
                                            #try:
                                            if js3['player']['lastLogin'] >= (unixtime - 44500):
                                                curname = js3['player']['displayname']
                                                jslist['online'][a] = {}
                                                jslist['online'][a]['displayname'] = curname
                                                jslist['online'][a]['trueonline'] = False
                                            else:
                                                continue
                                            #except KeyError:
                                                #continue # no hypixel history for player

                            output = f'**{curname} joined.**'
                            if jslist['online'][a]['trueonline']:
                                output +=  f' They are currently on the game "{game}", on the mode "{mode}".'
                            else:
                                jslist['online'].pop(a)
                            for b in jslist['track'][a]:
                                if jslist['settings'][str(b)]['join']:
                                    user = await bot.fetch_user(b)
                                    await user.send(output)
                            if js['session']['online'] and not self.onlinecheck.is_running():
                                self.onlinecheck.start()        
                        elif r.status == 429:
                            logging.error("Too many requests or API Down.")
                            continue
                        elif r.status == 403 or r.status == 400:
                            logging.critical("API key error or request broken.")
                            continue
        dumpcount += 1
        if dumpcount == 13:
            dumpcount = 0
            outfile = open("data.json", "w")
            json.dump(jslist,outfile,indent=6)
            outfile.close()

    @check.before_loop
    async def before_check(self):
        await bot.wait_until_ready()
        logging.info('Notification service started.')

    @commands.command(aliases=['online','whosonline','currentonline','myonlinelist','currentlyonline'], brief="Shows a list of all players on your notification list that are currently online")
    async def onlinelist(self, ctx):
        user = ctx.message.author.id
        playerlist = []
        try:
            for a in jslist['online']:
                if user in jslist['track'][a]:
                    curname = jslist['online'][a]['displayname']
                    list.append(playerlist, curname)
            if len(playerlist) != 1:
                output = ("**" + str(len(playerlist)) + " players:** ")
                for i in range(len(playerlist)-1):
                    currentname = playerlist[i]
                    output += (f"{currentname}, ")
                else:
                    currentname = playerlist[len(playerlist)-1]
                    output += (f"and {currentname}.")
            else:
                output = f"**1 player:** {playerlist[0]}"
            await ctx.send(output)
        except Exception:
            await ctx.send("There is no one in the list.")
            
    @commands.command(aliases=['add','notif','addnotification'],brief='Adds to your notification list',)
    async def addnotif(self, ctx, arg):
        maxnotifsize = 10
        if not str(ctx.message.author.id) in jslist['settings']:
            await ctx.send(f"You need to run {prefix}notifsettings before adding notifications. Use {prefix}help notifsettings for syntax.")
            return
        if str(ctx.message.author.id) in jslist['listcmd'] and len(jslist['listcmd'][str(ctx.message.author.id)]) >= maxnotifsize and ctx.message.author.id != ownerid:
            owner = await bot.fetch_user(ownerid)
            await ctx.send(f"Sorry, your user notification limit of {maxnotifsize} has been reached. Either remove someone from your notification list, or ask {owner} to increase the limit.")
            return
        if len(jslist['track']) <= 32:
            if re.match(r'^[A-Za-z0-9_]+$', arg):
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.mojang.com/users/profiles/minecraft/{arg}') as r:
                        if r.status == 200:
                            js = await r.json()
                            uuid = js["id"]
                        else:
                            await ctx.send("Sorry, this player does not exist or the API is down.")
                            return
                if not str(ctx.message.author.id) in jslist['listcmd']:
                    jslist['listcmd'][str(ctx.message.author.id)] = []
                if not uuid in jslist["track"]:
                    jslist['track'][uuid] = []
                    jslist['track'][uuid].append(int(ctx.message.author.id))
                    jslist['listcmd'][str(ctx.message.author.id)].append(str.casefold(arg))
                    await ctx.send("You have been added to the notification list for " + arg + ".")
                elif not int(ctx.message.author.id) in jslist["track"][uuid]:
                    jslist['track'][uuid].append(int(ctx.message.author.id))
                    jslist['listcmd'][str(ctx.message.author.id)].append(str.casefold(arg))
                    await ctx.send("You have been added to the notification list for " + arg + ".")
                else:
                    await ctx.send(f"You are already on the notification list for {arg}.")
            else:
                await ctx.send("That is not a valid name.")
        else:
            logging.warning("Max list size for notifications has been reached.")
            user = await bot.fetch_user(ownerid)
            await ctx.send(f"Sorry, the global notification list is full. Please contact {user} to let them know.")

    @commands.command(aliases=['remove','removenotif','removenotification'],brief='Removes from your notification list')
    async def delnotif(self, ctx,arg):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.mojang.com/users/profiles/minecraft/{arg}') as r:
                if r.status == 200:
                    js = await r.json()
                    uuid = js["id"]
                else:
                    await ctx.send("Sorry, this player does not exist or the API is down.")
        try:
            if int(ctx.message.author.id) in jslist["track"][uuid]:
                jslist['track'][uuid].remove(int(ctx.message.author.id))
                jslist['listcmd'][str(ctx.message.author.id)].remove(str.casefold(arg))
                await ctx.send(f"You have been removed from the notificiation list for {arg}")
                if len(jslist['track'][uuid]) == 0:
                    jslist['track'].pop(uuid)
        except KeyError:
            await ctx.send(f"You aren't on the notificiation list for {arg}.")

    @commands.command(aliases=['list','listnotification','listnotifications'],brief='Lists your notifications')
    async def listnotif(self,ctx):
        try:
            if len(jslist['listcmd'][str(ctx.message.author.id)]) != 1:
                output = ("**" + str(len(jslist['listcmd'][str(ctx.message.author.id)])) + " players:** ")
            
                for i in range(len(jslist['listcmd'][str(ctx.message.author.id)])-1):
                    currentname = jslist['listcmd'][str(ctx.message.author.id)][i]
                    output += (f"{currentname}, ")
                else:
                    currentname = jslist['listcmd'][str(ctx.message.author.id)][len(jslist['listcmd'][str(ctx.message.author.id)])-1]
                    output += (f"and {currentname}.")
            else:
                output = f"**1 player:** {jslist['listcmd'][str(ctx.message.author.id)][0]}"
            await ctx.send(output)
        except Exception:
            await ctx.send("There is no one in the list.")

    @commands.command(aliases=['settings','options','notifset','notifoptions','set'],brief='Configures notifications. Run for more info.')
    async def notifsettings(self,ctx,*args):
        jslist['settings'][str(ctx.message.author.id)] = {}
        if args == ():
            await ctx.send(f"The setup process isn't great right now, hopefully it will get better later. You will enter on or off for every game/task listed below. **All notifcations except join notifications are unavailable for players with their API disabled.** Please have a space in between each one. Your command should look like {prefix}notifsettings on off off on on... etc. The game list is as follows:\n\n**Server Join Notifications\nServer Leave Notifications\nBedwars\nDuels\nSkyblock\nBuild Battle\nThe Pit\nSMP\nPrototype Games\nSkywars\nCops and Crims\nArcade Games\nTNT Games\nUHC\nMurder Mystery\nSurvival Games\nQuakecraft\nTurbo Kart Racers**")
        elif len(args) == len(GAMESLIST):
            playersettings = list(args)
            for i, a in enumerate(playersettings):
                a = str.casefold(a)
                if a != 'off':
                    jslist['settings'][str(ctx.message.author.id)][GAMESLIST[i]] = True
                else:
                    jslist['settings'][str(ctx.message.author.id)][GAMESLIST[i]] = False
            await ctx.send(f"Settings have sucessfully been set. You can now use the {prefix}addnotif command, or use this command again.")
        elif len(args) == 1:
            argument = str.casefold(str(args[0]))
            if argument == 'joinonly':
                jslist['settings'][str(ctx.message.author.id)][GAMESLIST[0]] = True
                for i in range(len(GAMESLIST)-1):
                    jslist['settings'][str(ctx.message.author.id)][GAMESLIST[i+1]] = False
                await ctx.send(f"Only join notifications will be sent. You can now use the {prefix}addnotif command.")
            if argument == 'allon':
                for i in range(len(GAMESLIST)):
                    jslist['settings'][str(ctx.message.author.id)][GAMESLIST[i]] = True
                await ctx.send(f"All notifications will be sent. You can now use the {prefix}addnotif command.")

        else:
            for i in range(len(GAMESLIST)):
                jslist['settings'][str(ctx.message.author.id)][GAMESLIST[i]] = True
            await ctx.send(f"You didn't have the correct amount of arguments. You should have {len(GAMESLIST)} arguments. Everything set to on.")

@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name + '. Bot ID is ' + str(bot.user.id) + '.')

@bot.command(aliases=['status','playing'],brief='Gets the status of any player')
async def getstatus(ctx, arg):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.slothpixel.me/api/players/' + arg + '/status') as r:
            if r.status == 200:
                js = await r.json()
                if js["online"]:
                    await ctx.send(arg + " is online on " + js["game"]["type"] + ", on the mode " + js["game"]["mode"] + ".")
                else:
                    await ctx.send("Sorry, " + arg + " isn't online right now :(")

@bot.command(aliases=['players','hypixelplayers'],brief='Gets Hypixel player count')
async def playercount(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.slothpixel.me/api/counts') as r:
            if r.status == 200:
                js = await r.json()
                await ctx.send("There are currently " + str(js["playerCount"]) + " players online on Hypixel.")

@bot.command(aliases=['playerguild','findguild','guildbyplayer'],brief='Gets info of a guild by player name')
async def guildfinder(ctx, arg):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.slothpixel.me/api/guilds/' + arg) as r:
            if r.status == 200:
                js = await r.json()
                if js["description"] != None:
                    desc = js["description"]
                    if len(js["preferred_games"]) >= 3:
                        await ctx.send(arg + " is on the guild " + js["name"] + ". " + js["name"] + ' has a guild level of ' + str(js["level"]) + ', and their guild description is "' + desc + '". ' + "Their top 3 games are " + js["preferred_games"][0] + ", " + js["preferred_games"][1] + ", and " + js["preferred_games"][2] + ".")
                    else:
                        await ctx.send(arg + " is on the guild " + js["name"] + ". " + js["name"] + ' has a guild level of ' + str(js["level"]) + ', and their guild description is "' + desc + '".')
                else:
                    if len(js["preferred_games"]) >= 3:
                        await ctx.send(arg + " is on the guild " + js["name"] + ". " + js["name"] + ' has a guild level of ' + str(js["level"]) + '. ' + "Their top 3 games are " + js["preferred_games"][0] + ", " + js["preferred_games"][1] + ", and " + js["preferred_games"][2] + ".")
                    else:
                        await ctx.send(arg + " is on the guild " + js["name"] + ". " + js["name"] + ' has a guild level of ' + str(js["level"]) + '.')
            else:
                await ctx.send(arg + " isn't in a guild.")

@bot.command(aliases=['guild','guildsearch','guildbyname'],brief='Gets info of a guild by guild name')
async def guildinfo(ctx, *, arg):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.slothpixel.me/api/guilds/name/' + arg) as r:
            if r.status == 200:
                js = await r.json()
                if js["description"] != None:
                    desc = js["description"]
                    if len(js["preferred_games"]) >= 3:
                        await ctx.send(js["name"] + ' has a guild level of ' + str(js["level"]) + ', and their guild description is "' + desc + '". ' + "Their top 3 games are " + js["preferred_games"][0] + ", " + js["preferred_games"][1] + ", and " + js["preferred_games"][2] + ".")
                    else:
                        await ctx.send(js["name"] + ' has a guild level of ' + str(js["level"]) + ', and their guild description is "' + desc + '".')
                else:
                    if len(js["preferred_games"]) >= 3:
                        await ctx.send(js["name"] + ' has a guild level of ' + str(js["level"]) + '. ' + "Their top 3 games are " + js["preferred_games"][0] + ", " + js["preferred_games"][1] + ", and " + js["preferred_games"][2] + ".")
                    else:
                        await ctx.send(js["name"] + ' has a guild level of ' + str(js["level"]) + '.')
@bot.command(aliases=['info'], brief='Gives info about the bot.')
async def botinfo(ctx):
    await ctx.send(f'**This bot has many features related to the Hypixel API. Use {prefix}help to look through all of the commands you can use. \n The source code for the bot is available at **{sourcecodelink}**. ProfessorPiggos is the main developer on the project.')

if ownerfeatures:
    @bot.command(aliases=['s','stopbot'], brief='Stops the bot. Only the host of the bot can use this.')
    async def stop(ctx):
        if int(ctx.message.author.id) == ownerid:
            outfile = open("data.json", "w")
            json.dump(jslist,outfile,indent=6)
            outfile.close()
            if Notifications.check.is_running():
                Notifications.check.stop()
                print(Notifications.check.is_running())
                loopcount1 = 0
                await ctx.send("**Shutting down offline player check...**")
                while Notifications.check.is_running():
                    await asyncio.sleep(0.25)
                    loopcount1 += 1
                    if (loopcount1 >= 48):
                        await ctx.send("**This is taking a while, but the bot is still running.**")
                        loopcount1 = 0
                await ctx.send("**Offline check shut down.**")
            if Notifications.onlinecheck.is_running():
                Notifications.onlinecheck.stop()
                print(Notifications.onlinecheck.is_running())
                loopcount2 = 0
                await ctx.send("**Shutting down online player check...**")
                while Notifications.onlinecheck.is_running():
                    await asyncio.sleep(0.25)
                    loopcount2 += 1
                    if (loopcount2 >= 48):
                        await ctx.send("**This is taking a while, but the bot is still running.**")
                        loopcount2 = 0
                await ctx.send("**Online check shut down.**")
            await ctx.send("Bot has been shut down. Goodbye.")
            loop = asyncio.get_event_loop()
            loop.call_soon_threadsafe(loop.stop)
            loop.call_soon_threadsafe(sys.exit())
        else:
            await ctx.send("it's not going to work for you, don't even try it")

if notificationsOn:
    bot.add_cog(Notifications(bot))
try:
    bot.run(token)
except RuntimeError: # To avoid issues after stopping async event loop.
    pass
