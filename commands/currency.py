import urllib,requests,json
import discord
from discord.ext import commands
@commands.command()
async def convert(ctx,frm,to,*,amount):
	cash = amount.replace(".","")
	with urllib.request.urlopen(f'https://api.frankfurter.app/latest?amount={cash}&from={frm}&to={to}') as url:
		data = json.loads(url.read().decode())
		rates = data['rates']
		embed=discord.Embed(title="Currency Converting",description=amount,color=discord.Color.blue())
		embed.add_field(name=f"{frm} to {to}",value=rates[to],inline=False)
	await ctx.send(embed=embed)
def setup(bot):
    bot.add_command(convert)