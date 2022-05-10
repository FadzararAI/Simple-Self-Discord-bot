import asyncio
import os
import requests
import youtube_dl
from commands import utilities

import discord
from discord.ext import commands
from discord.utils import get
from discord import TextChannel

prefix='|'
bot = commands.Bot(self_bot=True,command_prefix=prefix)
token = "MzA4MjYwMjY5ODcwNTQ2OTU0.YAUqcQ.JZ1wgmBGb9xSIR4Y2YhrAEo2Sok"
bot.remove_command('help')

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
sessions = []
def check_session(ctx):
	if len(sessions) > 0:
		for i in sessions:
			if i.guild == ctx.guild and i.channel == ctx.author.voice.channel:
				return i
		session = utilities.Session(ctx.guild, ctx.author.voice.channel, id=len(sessions))
		sessions.append(session)
		return session
	else:
		session = utilities.Session(ctx.guild, ctx.author.voice.channel, id=0)
		sessions.append(session)
		return session


def prepare_continue_queue(ctx):
	fut = asyncio.run_coroutine_threadsafe(continue_queue(ctx), bot.loop)
	try:
		fut.result()
	except Exception as e:
		print(e)


async def continue_queue(ctx):
	session = check_session(ctx)
	if not session.q.theres_next():
		#await ctx.send("Acabou a queue, brother.")
		return
	session.q.next()

	voice = discord.utils.get(bot.voice_clients, guild=session.guild)
	source = await discord.FFmpegOpusAudio.from_probe(session.q.current_music.url, **FFMPEG_OPTIONS)

	if voice.is_playing():
		voice.stop()

	voice.play(source, after=lambda e: prepare_continue_queue(ctx))
	#voice.source = discord.PCMVolumeTransfomer(voice.source,0.5)
	await ctx.send(session.q.current_music.thumb)
	await ctx.send(f"Playing: {session.q.current_music.title}")


@bot.command(name='play')
async def play(ctx, *, arg):
	try:
		voice_channel = ctx.author.voice.channel
	except AttributeError as e:
		print(e)
		await ctx.send("Not connected to any VC")
		return
	session = check_session(ctx)
	with youtube_dl.YoutubeDL({'format': 'bestaudio', 'noplaylist': 'True'}) as ydl:
		try:
			requests.get(arg)
		except Exception as e:
			print(e)
			info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
		else:
			info = ydl.extract_info(arg, download=False)

	url = info['formats'][0]['url']
	thumb = info['thumbnails'][0]['url']
	title = info['title']

	session.q.enqueue(title, url, thumb)
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	if not voice:
		await voice_channel.connect()
		voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	if voice.is_playing():
		#await ctx.send(thumb)
		await ctx.send(f"Added to queue: {title}")
		return
	else:
		#await ctx.send(thumb)
		await ctx.send(f"Playing Now: {title}")
	session.q.set_last_as_current()

	source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
	voice.play(source, after=lambda ee: prepare_continue_queue(ctx))
	#voice.source = discord.PCMVolumeTransfomer(voice.source,0.5)


@bot.command(name='next', aliases=['skip'])
async def skip(ctx):
	session = check_session(ctx)
	# If there isn't any song to be played next, return.
	if not session.q.theres_next():
		await ctx.send("There's no next song")
		return
	voice = discord.utils.get(bot.voice_clients, guild=session.guild)
	if voice.is_playing():
		voice.stop()
		return
	else:
		session.q.next()
		source = await discord.FFmpegOpusAudio.from_probe(session.q.current_music.url, **FFMPEG_OPTIONS)
		voice.play(source, after=lambda e: prepare_continue_queue(ctx))
		#voice.source = discord.PCMVolumeTransfomer(voice.source,0.5)
		return


@bot.command(name='queue')
async def print_info(ctx):
	session = check_session(ctx)
	#await ctx.send(f"Session ID: {session.id}")
	await ctx.send(f"Currently Playing: {session.q.current_music.title}")
	queue = [q[0] for q in session.q.queue]
	await ctx.send(f"Queue: {queue}")


@bot.command(name='pause')
async def pause(ctx):
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	if voice.is_playing():
		voice.pause()
	else:
		await ctx.send("Song is already paused")


@bot.command(name='resume')
async def resume(ctx):
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	if voice.is_paused:
		voice.resume()
	else:
		await ctx.send("Song is already playing")


@bot.command(name='stop')
async def stop(ctx):
	session = check_session(ctx)
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	if voice.is_playing:
		voice.stop()
		session.q.clear_queue()
	else:
		#await ctx.send("Não tem nada tocando ô abobado.")
		pass
@bot.event
async def on_ready():
	bot.load_extension("commands.help")
	bot.load_extension("commands.ip")
	bot.load_extension("commands.userinfo")
	bot.load_extension("commands.avatar")
	bot.load_extension("commands.activity")
	bot.load_extension("commands.currency")
	print("Bot is up")

bot.run(token, bot=False)