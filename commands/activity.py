import discord
from discord.ext import commands
@commands.command()
async def act(ctx, sts, *,msg):
	if sts == 'play':
		await ctx.bot.change_presence(activity=discord.Game(name=msg))
	elif sts == 'stream':
		await ctx.bot.change_presence(activity=discord.Streaming(name=msg))
	elif sts == 'listen':
		await ctx.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=msg))
	elif sts == 'watch':
		await ctx.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=msg))
	else:
		pass
@commands.command()
async def stopact(ctx):
	await ctx.bot.change_presence(activity=None)
def setup(bot):
	bot.add_command(act)
	bot.add_command(stopact)