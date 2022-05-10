import urllib,requests,urllib.error,json
import discord
from discord.ext import commands

all_commands = {
	"help":"Shows all commands",
	"track":"Tracks the origin from IP",
	"avatar":"Get the avatar of a user",
	"uinfo":"Get the information of a user",
	"convert":"Convert amount of currency from one to another",
	"currencies":"Shows all available currencies",
	"play":"Plays a song",
	"act":"Changes the activity",
	"stopact":"Stops current activity",
	"imbored":"Suggests an acitivy to do",
	"randomword":"Generates a random English word",
	"tell":"Saying something",
	"whatis":"Search for the definition(s) of a word",
}

class cmds(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def help(self, ctx):
		embed=discord.Embed(title="All Commands",color=discord.Color.blue())
		for x,x2 in all_commands.items():
			embed.add_field(name=x,value=x2,inline=False)
		await ctx.send(embed=embed)
	@commands.command()
	async def tell(self, ctx, *, sent):
		await ctx.message.delete()
		embed=discord.Embed(title="The superior says:",description=sent,color=discord.Color.blue())
		await ctx.send(embed=embed)
	@commands.command()
	async def currencies(self, ctx):
		with urllib.request.urlopen("https://api.frankfurter.app/currencies") as url:
		    data = json.loads(url.read().decode())
		embed=discord.Embed(title="Currencies:",color=discord.Color.blue())
		for i,b in data.items():
			embed.add_field(name=i,value=b,inline=True)
		await ctx.send(embed=embed)
	@commands.command()
	async def imbored(self, ctx):
		with urllib.request.urlopen("https://www.boredapi.com/api/activity") as url:
			suggestion = json.loads(url.read().decode())
		embed=discord.Embed(title="Activity suggestion",description=suggestion['activity'],color=discord.Color.blue())
		await ctx.send(embed=embed)
	@commands.command()
	async def randomword(self,ctx):
		with urllib.request.urlopen("https://random-words-api.vercel.app/word") as url:
			randword = json.loads(url.read().decode())
		embed=discord.Embed(title=randword[0]['word'],description=randword[0]['definition'],color=discord.Color.blue())
		await ctx.send(embed=embed)
	@commands.command()
	async def whatis(self, ctx, *, word):
		try:
			with urllib.request.urlopen(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}") as url:
				definition = json.loads(url.read().decode())
		except urllib.error.HTTPError as err:
			embed=discord.Embed(title="Word Not Found!",description="The inputted word cannot be found.",color=discord.Color.blue())
		else:
			if len(definition[0]['meanings']) > 1:
				embed=discord.Embed(title=word,description='Definitions:',color=discord.Color.blue())
				for i in range(len(definition[0]['meanings'])):
					embed.add_field(name=definition[0]['meanings'][i]['partOfSpeech'],value=definition[0]['meanings'][i]['definitions'][0]['definition'])
			else:
				embed=discord.Embed(title=f"{word} ({definition[0]['meanings'][0]['partOfSpeech']})",description=definition[0]['meanings'][0]['definitions'][0]['definition'],color=discord.Color.blue())
		await ctx.send(embed=embed)
	@commands.command()
	async def hi(self, ctx,):
		embed=discord.Embed(title="Greeting",description="Hello!",color=discord.Color.blue())
		await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(cmds(bot))