import discord #Importing discord. 
from discord.ext import commands #Importing the commands extension from discord
from colorama import Fore #Importing Fore (A library used to print colored text in terminal) Yea, I like fancy stuff
import asyncio
from discord import utils

class Webhooks(commands.Cog): #initiate the class
	
	def __init__(self, bot): #initializing the class (ofc, how is the bot supposed to know that this class will contain code for bot to run lol)
		self.bot = bot #self.bot = bot :D> Simply assigning the bot variable to the class :D> 

	@commands.Cog.listener() #Creating a listener 
	async def on_ready(self): #Function which is invoked when the bot is "READY" 
		print(f"{Fore.GREEN}{self.__class__.__name__} cog has been loaded\n{Fore.WHITE}-----") #Prints, cog is loaded 
 
	@commands.command(name = "setname", aliases = ["sn"], description = "Set a name for yourself.", usage = "<setname> <yourname>") 
	async def set_name(self, ctx, profile: int = None,  *, name:str = None):

		if profile >3:
			await ctx.send("Profiles can be only 1 to 3")
			return
		if profile < 1:
			await ctx.send("Profiles can be only 1 to 3")
			return
		if name == None: 
			await ctx.send('Please enter a name for yourself. I am not supposed to just "assume" any name.') 
			return
		filter_dict = {"user_id":ctx.author.id, "profile": profile}
		check = await self.bot.settings.find_many_by_custom(filter_dict)
		if not check:
			data = {"user_id": ctx.author.id, "name": name, "avatar": "", "is_enabled":"true", "profile": profile}
			await self.bot.settings.insert(data)
			await ctx.send("Success! Your brand new profile has been created!")
		if check:
			pfp = check[0]["avatar"]
			enable_status = check[0]["is_enabled"]
			profile_count = check[0]["profile"]
			new_data = {"user_id":ctx.author.id, "name":name, "avatar":pfp, "is_enabled": enable_status, "profile":profile_count}
			await self.bot.settings.upsert_custom(filter_dict, new_data)
			await ctx.send("Your profile has been updated successfully!")

	@commands.command(name= "setavatar", aliases = ["sa"], description = "Set an avatar for your character!", usage = "<setvatar> <image>") #creating a second command , for users to set their image. yeah their own image hurray !
	@commands.dm_only() #Esnures this command can be run onlyon DM ONLY.
	async def set_avatar(self,ctx, profile:int):
		if profile >3:
			await ctx.send("Profiles can be only 1 to 3")
			return
		if profile <1:
			await ctx.send("Profiles can be only 1 to 3")
			return
		em = discord.Embed(description = "Please send an image for your avatar in next 18 seconds.", color = ctx.author.colour)
		await ctx.send(embed = em, delete_after = 18)
		def check(m):
			return len(m.attachments) != 0 and m.channel == ctx.channel and m.author == ctx.author 
		try: #Try and error :D> 
			msg = await self.bot.wait_for("message", check = check, timeout = 15) 
			x = str(msg.attachments).split() 
			t = x[3] 
			d = t.strip("'>]") 
			f = d.strip("url='") 
			filter_dict = {"user_id":ctx.author.id, "profile": profile}
			checks = await self.bot.settings.find_many_by_custom(filter_dict)

			if checks:
				name = checks[0]["name"]
				enable_status = checks[0]["is_enabled"]
				profile_count = checks[0]["profile"]
				new_data = {"user_id":ctx.author.id, "name":name, "avatar":f, "is_enabled": enable_status, "profile":profile_count}
				await self.bot.settings.upsert_custom(filter_dict, new_data)
				await ctx.send("Your pfp has been updated successfully.")
				return
			await ctx.send("Hey, you have not set any name. Expecting to set a avatar for yourself hmm?")
		except asyncio.TimeoutError:
			await ctx.send("This request has timed out. Please try again.")

	@commands.command(name = "activate", description = "Set the current active profile for the bot!")
	@commands.guild_only()
	async def activation(self, ctx, profile: int):
		filter_dict = {"user_id": ctx.author.id, "profile": profile}
		check = await self.bot.settings.find_many_by_custom(filter_dict)
		if not check:
			await ctx.send("Nope. No command 4u, Check the profile number ;-;")
			return
		#checking = await self.bot.profile.get_by_id(ctx.author.id)
		#if not checking:
			#data = {"_id":ctx.author.id, "current_profile": profile}
			#await self.bot.profile.upsert(data)
			#await ctx.send(f"Your current profile has been set to {profile}")
			#return
		info = {"_id":ctx.author.id, "current_profile": profile}
		await self.bot.profile.upsert(info)
		await ctx.send(f"Your current profile has been set to {profile}")
		

		

	@commands.Cog.listener()
	async def on_message(self, msg):
		if msg.content.startswith("!"):
			return
		search = await self.bot.profile.get_by_id(msg.author.id)
		if not search:
			return
		profilevalue = search["current_profile"]
		filter_dict = {"user_id": msg.author.id, "profile":profilevalue}
		checks = await self.bot.settings.find_many_by_custom(filter_dict)
		if not checks:
			return
		enable_status = checks[0]["is_enabled"]
		if enable_status == "false":
			return
		name = checks[0]["name"]
		pfp = checks[0]["avatar"]
		hook = await msg.channel.webhooks()
		webhook = utils.get(hook, name = "Proxy")
		if webhook is None:
			webhook = await msg.channel.create_webhook(name = "Proxy")
		await webhook.send(msg.content, username = name, avatar_url = pfp)
		await msg.delete()

	@commands.command(name = "toggle", description = "Choose if you wish to switch off the webhooks!")
	async def toggle_command(self, ctx, profile:int):
		if profile >3:
			await ctx.send("Profiles can be set from 1 to 3")
			return
		if profile <1:
			await ctx.send("Profiles can be set from 1 to 3")
			return
		filter_dict = {"user_id":ctx.author.id, "profile":profile}
		check = await self.bot.settings.find_many_by_custom(filter_dict)
		if not check:
			await ctx.send("This profile does not exists. Please create one by typing `!setname <your name>`")
			return
		name = check[0]["name"]
		pfp = check[0]["avatar"]
		profile_count = check[0]["profile"]
		enable_status = check[0]["is_enabled"]
		if enable_status == "true":
			data = {"user_id":ctx.author.id, "name":name, "avatar":pfp, "is_enabled": "false", "profile":profile_count}
			await self.bot.settings.upsert_custom(filter_dict, data)
			await ctx.send(f"You have successfully switched off Webhook proxy for `{profile}`")
			return
		data = {"user_id":ctx.author.id, "name":name, "avatar":pfp, "is_enabled": "true", "profile":profile_count}
		await self.bot.settings.upsert_custom(filter_dict, data)
		await ctx.send(f"You have successfully toggled the webhook proxy for `{profile}`")
		

		

		


def setup(bot):
	bot.add_cog(Webhooks(bot))
