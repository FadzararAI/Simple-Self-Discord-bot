import urllib,requests,json
import discord
from discord.ext import commands
@commands.command()
async def track(ctx, *,ip):
	with urllib.request.urlopen(f'https://ipapi.co/{ip}/json/') as url:
		data = json.loads(url.read().decode())
	embed=discord.Embed(title="Location Tracker",description=ip,color=discord.Color.blue())
	embed.add_field(name="ISP",value=data['org'],inline=False)
	embed.add_field(name="Country",value=data['country'],inline=False)
	embed.add_field(name="City",value=data['city'],inline=True)
	embed.add_field(name="Region",value=data['region'],inline=True)
	embed.add_field(name="Latitude",value=data['latitude'],inline=True)
	embed.add_field(name="Longitude",value=data['longitude'],inline=True)
	embed.set_footer(text="Execution Completed")
	await ctx.send(embed=embed)
def setup(bot):
    bot.add_command(track)