import aiohttp
import discord 
import json
from discord.ext import commands

with open('config.json') as f:
    config = json.load(f)

class Gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users = {}

    @commands.command()
    async def ask(self, ctx: commands.Context, *, prompt: str):
        if not prompt:
            error_embed = discord.Embed(title="Error", description="Please provide a prompt for the GTP command.", color=discord.Color.red())
            await ctx.reply(embed=error_embed)
            return
    
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "text-davinci-002",
                "prompt": prompt,
                "temperature": 0.5,
                "max_tokens": 50, 
                "presence_penalty": 0,
                "frequency_penalty": 0,
                "best_of": 1,
            }
            headers = {"Authorization": f"Bearer {config['openai_api_key']}"}
            async with session.post("https://api.openai.com/v1/completions", json=payload, headers=headers) as resp:
                response = await resp.json()
                embed = discord.Embed(title="Chat GTP's Response:", description=response["choices"][0]["text"])
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/5726/5726775.png")
                

                await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Gpt(bot))

