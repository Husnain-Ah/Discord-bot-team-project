from datetime import datetime
import random
import sqlite3
from unicodedata import name
import discord
from discord.ext import commands


class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def balance(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute(
            f"SELECT wallet, bank FROM main WHERE user_id = {member.id}")
        bal = cursor.fetchone()
        

       

        embed = discord.Embed(title=f"{member.display_name}'s Balance",
            color=discord.Color.random())
        embed.add_field(name="Wallet", value=f"`💵 {bal[0]}`")
        embed.add_field(name="Bank", value=f"`🏦 {bal[1]}`")
        embed.add_field(name="Networth", value=f"`📈 {bal[0] + bal[1]}`")
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/9830/9830821.png")
        

    
        await ctx.reply(embed=embed)


    @commands.command()
    async def deposit(self, ctx, amount: int):  
     member = ctx.author

     #if amount<= 0:
       #  await ctx.reply("You can only deposit a positive amount you fool :)")
       #  return

     db = sqlite3.connect("main.sqlite")
     cursor = db.cursor()

     # Check if user has enough balance to deposit
     cursor.execute(
        f"SELECT wallet FROM main WHERE user_id = {member.id}")
     wallet = cursor.fetchone()
     if wallet is None:
        wallet = (0,)
     if amount > wallet[0]:
        await ctx.reply("You don't have enough balance to deposit.")
        return

     # Update wallet and bank balances
     cursor.execute(
        f"UPDATE main SET wallet = wallet - {amount} WHERE user_id = {member.id}"
     )
     cursor.execute(
        f"UPDATE main SET bank = bank + {amount} WHERE user_id = {member.id}"
     )
     db.commit()

     await ctx.reply(f"You have deposited ${amount} into your bank account.")


    @commands.command()
    async def withdraw(self, ctx, amount: int):
        member = ctx.author

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        # Check if user has enough balance to withdraw
        cursor.execute(
            f"SELECT bank FROM main WHERE user_id = {member.id}")
        bank = cursor.fetchone()
        if bank is None:
            bank = (0,)
        if amount > bank[0]:
            await ctx.reply("You don't have enough balance in your bank account to withdraw.")
            return

        # Update wallet and bank balances
        cursor.execute(
            f"SELECT wallet, bank FROM main WHERE user_id = {member.id}")
        bal = cursor.fetchone()
        wallet_bal = bal[0] + amount
        bank_bal = bal[1] - amount
        cursor.execute(
            "UPDATE main SET wallet = ?, bank = ? WHERE user_id = ?",
            (wallet_bal, bank_bal, member.id)
        )

        await ctx.reply(f"You have withdrawn ${amount} from your bank account.")


    
        db.commit()
        cursor.close()
        db.close()


    @commands.command()
    async def checkrank(self, ctx):
     db = sqlite3.connect("main.sqlite")
     cursor = db.cursor()

    # Retrieve top 10 users based on wallet balance
     cursor.execute(
        "SELECT user_id, wallet FROM main ORDER BY wallet DESC LIMIT 10"
     )
     wallet_ranks = cursor.fetchall()

    # Retrieve top 10 users based on bank balance
     cursor.execute(
        "SELECT user_id, bank FROM main ORDER BY bank DESC LIMIT 10"
     )
     bank_ranks = cursor.fetchall()

     wallet_ranks_str = ""
     bank_ranks_str = ""


    # Format the wallet ranks into a string
     for i, rank in enumerate(wallet_ranks):
        user_id = rank[0]
        balance = rank[1]
        member = ctx.guild.get_member(user_id)
        if member is None:
            continue
        wallet_ranks_str += f"{i+1}. {member.display_name}: ${balance}\n"

    # Format the bank ranks into a string
     for i, rank in enumerate(bank_ranks):
        user_id = rank[0]
        balance = rank[1]
        member = ctx.guild.get_member(user_id)
        if member is None:
            continue
        bank_ranks_str += f"{i+1}. {member.display_name}: ${balance}\n"

    # Create the embed
     embed = discord.Embed(title="Balance Leaderboard", color=discord.Color.random())
     embed.add_field(name="Wallet Balance", value=wallet_ranks_str or "No data", inline=False)
     embed.add_field(name="Bank Balance", value=bank_ranks_str or "No data", inline=False)
     embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4330/4330710.png")
     await ctx.reply(embed=embed)




async def setup(bot):
    await bot.add_cog(Balance(bot))
