import discord
from discord.ext import commands
@commands.command()
async def uinfo(ctx, Member: discord.Member = None):
	embed=discord.Embed(ctx=ctx,title="User Info")
	embed.set_thumbnail(url=Member.avatar_url)
	embed.add_field(name="Username",value=str(Member),inline=True)
	embed.add_field(name="ID",value=Member.id,inline=True)
	embed.add_field(name="Created At",value=Member.created_at.strftime("%d/%m/%Y"),inline=True)
	embed.add_field(name="Joined At",value=Member.joined_at.strftime("%d/%m/%Y"),inline=True)
	embed.add_field(name="Server Booster",value=Member.premium_since,inline=True)
	await ctx.send(embed=embed)
def setup(bot):
	bot.add_command(uinfo)