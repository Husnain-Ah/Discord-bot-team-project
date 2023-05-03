import random
import sqlite3
from discord.ext import commands

class Fight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    async def fight(self, ctx, amount: int, opponent: commands.MemberConverter):
        if amount < 1:
            await ctx.send("You cannot bet less than 1.")
            return

        user = ctx.author

        # Check if the user and opponent are the same person
        if user == opponent:
            await ctx.send("You cannot gamble against yourself.")
            return

        # Check if the opponent is a bot
        if opponent.bot:
            await ctx.send("You cannot gamble against a bot.")
            return

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT wallet FROM main WHERE user_id = {user.id}")
        result = cursor.fetchone()

        if result is None:
            await ctx.send("You don't have any money to gamble.")
            return

        wallet = result[0]

        if wallet < amount:
            await ctx.send("You don't have enough money to make that bet.")
            return

        cursor.execute(f"SELECT wallet FROM main WHERE user_id = {opponent.id}")
        result = cursor.fetchone()

        if result is None:
            await ctx.send(f"{opponent.display_name} doesn't have any money to gamble.")
            return

        opponent_wallet = result[0]

        if opponent_wallet < amount:
            await ctx.send(f"{opponent.display_name} doesn't have enough money to make that bet.")
            return

        win = random.choice([True, False])

        if win:
            winnings = amount * 2
            cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (wallet + winnings, user.id))
            cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (opponent_wallet - amount, opponent.id))
            db.commit()
            await ctx.send(f"{user.display_name} won {winnings} from {opponent.display_name}!")
        else:
            cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (wallet - amount, user.id))
            cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (opponent_wallet + amount, opponent.id))
            db.commit()
            await ctx.send(f"{opponent.display_name} won {amount} from {user.display_name}!")




        cursor.close()
        db.close()

async def setup(bot):
   await bot.add_cog(Fight(bot))


