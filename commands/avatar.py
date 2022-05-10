import discord
from discord.ext import commands
@commands.command()
async def avatar(ctx,avatar: discord.Member = None):
    await ctx.send(embed=discord.Embed().set_image(url=avatar.avatar_url))
def setup(bot):
    bot.add_command(avatar)
