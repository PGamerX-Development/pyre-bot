#All the imports for the bot
import discord
from discord.ext import commands
import os
import certifi
import motor.motor_asyncio
from pathlib import Path
from colorama import Fore
from utlility.mongo import Document

#Beginning of the code.
wd = str(Path(__file__).parents[0])
print(f"{Fore.GREEN} {wd}")

#INTENTS-----
intent = discord.Intents.all()
#----------
#DEFAULT PREFIX 
DEFAULTPREFIX = "!"
#Initialize the bot. 
bot = commands.Bot(command_prefix = DEFAULTPREFIX, intents = intent, case_insensitive = True)

#Creating some bot attributes. Yeah, this makes life easier and simpler to be used in any cog.:D 
bot.connection_url = str("TheMongoDB") #Connection URL OF BOT. You will need to get it from MongoDB Website.
ca = certifi.where() #Ya, so this is just setting up a certificate for bot to connect to mongo db. Throws TLS error else. :D>  (in some cases its not req, it was req in my case though.)
bot.default_prefix = DEFAULTPREFIX

#==============================================================BOT EVENTS==============================================================
@bot.event
async def on_ready():
	print(
		f"{Fore.WHITE}-----\n{Fore.GREEN}Logged in as: {bot.user.name} : {Fore.LIGHTCYAN_EX}{bot.user.id}\n{Fore.WHITE}-----\n{Fore.GREEN}My current prefix is: {bot.default_prefix}\n-----"
	)
	bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url), tlsCAFile = ca ) #So, basically this is just bot attribute which will be created when the bot is online. This means, that bot will connect to DB only when there is actually a need. Hmm .... 
	bot.db = bot.mongo["PyroBot"] # SO ... Basically, this will just create a DB , if it exists alrady ,it uses that. Simple!
	bot.settings = Document(bot.db , "settings")
	bot.profile = Document(bot.db, "currentprofile")



#===============================================================================================================================
cogs = [] #So we just make a variable which is an empty list.
for filename in os.listdir(wd+'/cogs'): #We iterate through all the files in the "cogs" folder.
	if filename.endswith('.py'): #If the file name has its extension `.py` Then :
		cogs.append("cogs."+ filename[:-3]) #Just add the name of file as "cogs.the name of the file" So basically, we just wanna create a list of all the files in the cogs directory to load them.

if __name__ == '__main__': #So its just a if statement which ensures that the name of the file is MAIn like ensuring its not a COG.
	for extension in cogs: #Iterate through our cog list
		bot.load_extension(extension) #Just load the BOT EXTENSION. 

#=================FOR REPLIT ONLY==========
#TOKEN = os.getenviron()
#bot.run(TOKEN)
#=======================

bot.run("TOKEN")

