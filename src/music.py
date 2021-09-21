import discord
from discord.ext import commands
import youtube_dl


"""
MUSIC COMMANDS ARE CURRENTLY BEING WORKED ON SO MIGHT NOT WORK FULLY
"""


class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def join(self, ctx):
        if(ctx.author.voice is None):
            await ctx.reply("*You're not in a voice channel.*")
        voiceChannel = ctx.author.voice.channel
        if(ctx.voice_client is None): # if bot is not in voice channel
            await voiceChannel.connect()
        else: # bot is in voice channel move it to new one
            await ctx.voice_client.move_to(voiceChannel)

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
        
    @commands.command()
    async def play(self,ctx, url:str = None):
        if(url == None):
            await ctx.reply("*Check your arguments!*\n```/play VIDEO_URL```")
        else:
            ctx.voice_client.stop() # stop current song
            
            # FFMPEG handle streaming in discord, and has some standard options we need to include
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            YTDL_OPTIONS = {"format":"bestaudio"}
            vc = ctx.voice_client
            
            # Create stream to play audio and then stream directly into vc
            with youtube_dl.YoutubeDL(YTDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info["formats"][0]["url"]
                source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
                vc.play(source) # play the audio
                await ctx.send(f"*Playing {info['title']} -* 🎵")
    
    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.reply("*Paused -* ⏸️")
    
    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.reply("*Resuming -* ▶️")
      
            
def setup(bot):
    bot.add_cog(music(bot))