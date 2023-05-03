import asyncio
import discord
import youtube_dl
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice = None
        self.player = None

    async def _get_voice_client(self, ctx: commands.Context) -> discord.VoiceClient:
        """Helper method to get the bot's voice client for a given guild"""
        if self.voice is None:
            self.voice = await ctx.author.voice.channel.connect()
        elif self.voice.channel != ctx.author.voice.channel:
            await self.voice.move_to(ctx.author.voice.channel)
        return self.voice

    async def _play_song(self, url: str, ctx: commands.Context) -> None:
        """Helper method to play a song from a given URL"""
        voice_client = await self._get_voice_client(ctx)
        source = await discord.FFmpegOpusAudio.from_probe(url)
        if self.player is None:
            self.player = voice_client.play(source)
        else:
            self.player.stop()
            self.player = voice_client.play(source)

    @commands.command()
    async def play(self, ctx: commands.Context, *, query: str) -> None:
        """Play a song from a given YouTube URL or search query"""
        if ctx.author.voice is None:
            await ctx.send("You need to be in a voice channel to use this command.")
            return

        # Check if the bot is already playing a song
        if self.player is not None and self.player.is_playing():
            self.player.pause()

        # Search for the video on YouTube
        with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            url = info['url']
            title = info['title']
            await ctx.send(f"Now playing: {title}")

        # Play the song
        await self._play_song(url, ctx)

    @commands.command()
    async def stop(self, ctx: commands.Context) -> None:
        """Stop the currently playing song"""
        if self.player is not None and self.player.is_playing():
            self.player.stop()

    @commands.command()
    async def pause(self, ctx: commands.Context) -> None:
        """Pause the currently playing song"""
        if self.player is not None and self.player.is_playing():
            self.player.pause()

    @commands.command()
    async def resume(self, ctx: commands.Context) -> None:
        """Resume the currently paused song"""
        if self.player is not None and self.player.is_paused():
            self.player.resume()

    @commands.command()
    async def leave(self, ctx: commands.Context) -> None:
        """Disconnect the bot from the voice channel"""
        if self.voice is not None:
            await self.voice.disconnect()
            self.voice = None
            self.player = None
        else:
            await ctx.send("I'm not in a voice channel!")

async def setup(bot):
      await bot.add_cog(Music(bot))


