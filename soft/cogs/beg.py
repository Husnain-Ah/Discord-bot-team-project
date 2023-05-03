import random
import asyncio
import sqlite3
import discord
from discord.ext import commands

class Beg(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def beg(self, ctx):
        member = ctx.author
        earnings = random.randint(1, 10001)
        
        try:
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT wallet FROM main WHERE user_id = {member.id}")
            wallet = cursor.fetchone()
            if wallet is None:
                wallet = (0,)

            new_wallet_balance = wallet[0] + int(earnings)
            sql = "UPDATE main SET wallet = ? WHERE user_id = ?"
            val = (new_wallet_balance, member.id)
            cursor.execute(sql, val)
            db.commit()

            cursor.execute(f"SELECT wallet FROM main WHERE user_id = {member.id}")
            updated_wallet_balance = cursor.fetchone()[0]

            wallet_icon = "💰"
            bank_icon = "🏦"
            wallet_str = f"{wallet_icon} {updated_wallet_balance}"

            responses = [
                f" 'Oh you poor soul, take' 🪙 {earnings:,}",
                f" 'I suppose you can have this' 🪙 {earnings:,} 'but don't come back too soon.'",
                f" 'You must be really desperate. Here, take' 🪙 {earnings:,}.",
                f" 'I don't normally give money away, but you look like you need it. Take' 🪙 {earnings:,}.",
                f" 'I'm feeling  generous today. Take'  🪙 {earnings:,} 'and don't waste it all at once.'",
            ]
            response = random.choice(responses)

            embed = discord.Embed(
                title=f"{member.display_name}'s Balance",
                color=discord.Color.blue(),
            )
            #embed.set_thumbnail(url=member.avatar_url)   
            embed.add_field(name="Wallet", value=wallet_str, inline=False)
            await ctx.reply(response, embed=embed)

            db.commit()
            cursor.close()
            db.close()

        except sqlite3.Error as e:
            print(f"Error accessing database: {e}")
            await ctx.reply("An error occurred while accessing the database.")
        except Exception as e:
            print(f"Error: {e}")
            await ctx.reply("An unexpected error occurred.")           

async def setup(bot):
    await bot.add_cog(Beg(bot))
