import ast
import asyncio
import json
import discord
from discord.ext import commands
import sqlite3


class PetShop(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.pets = [
            {"name": "Dog", "price": 100, "emoji": "🐶"},
            {"name": "Cat", "price": 200, "emoji": "🐱"},
            {"name": "Rabbit", "price": 1000, "emoji": "🐰"},
            {"name": "Hamster", "price": 3000, "emoji": "🐹"},
            {"name": "chicken", "price": 5000, "emoji": "🐓"},
            {"name": "eagle", "price": 15000, "emoji": "🦅"},
            {"name": "Shark", "price": 10000, "emoji": "🦈"},
            {"name": "snake", "price": 30000,  "emoji": "🐍"},
            {"name": "wolf", "price": 35000, "emoji": "🐺"},
            {"name": "Lion", "price": 50000, "emoji": "🦁"}
        ]

    @commands.command()
    async def pets(self, ctx):
        embed = discord.Embed(
            title="Pet Shop",
            description="Welcome to the Pet Shop! Here are the pets that we have:",
            color=discord.Color.blue()
        )
        for pet in self.pets:
            embed.add_field(name=pet['name'],
                            value=f"Price: {pet['price']} coins | {pet['emoji']}", inline=False)
        embed.set_footer(text="To buy a pet, type '!buy <pet name> <quantity>'")

        await ctx.reply(embed=embed)

    @commands.command()
    async def buy(self, ctx, pet_name: str, quantity: int = 1):
     member = ctx.author

     db = sqlite3.connect("main.sqlite")
     cursor = db.cursor()

    # Get pet price and name
     pet = next((pet for pet in self.pets if pet["name"].lower() == pet_name.lower()), None)
     if pet is None:
        await ctx.reply("Invalid pet name!")
        return
     pet_price = pet["price"]
     pet_name = pet["name"]

    # Check if user has enough balance to buy pets
     cursor.execute(f"SELECT wallet FROM main WHERE user_id = {member.id}")
     wallet = cursor.fetchone()
     if wallet is None:
        wallet = (0,)
     total_price = pet_price * quantity
     if total_price > wallet[0]:
        await ctx.send("You don't have enough balance to buy these pets.")
        return

    # Update wallet and pet status
     cursor.execute("UPDATE main SET wallet = wallet - ?, pets = pets || ? WHERE user_id = ?",
                   (total_price, f"{quantity}x{pet_name},", member.id))
     db.commit()

     await ctx.reply(f"Congratulations! You have bought {quantity} {pet_name}(s) for 🪙{total_price} coins.")

     


    @commands.command()
    async def viewpets(self, ctx, member: discord.Member = None):
     if member is None:
        member = ctx.author

     db = sqlite3.connect("main.sqlite")
     cursor = db.cursor()

    # Get user's pets
     cursor.execute("SELECT pets FROM main WHERE user_id = ?", (member.id,))
     pets = cursor.fetchone()

    # Count the number of each pet type
     pet_counts = {}
     for pet in pets[0].split(","):
        if pet != "":
            name = pet.split("x")[1].strip()
            count = int(pet.split("x")[0])
            pet_counts[name] = pet_counts.get(name, 0) + count

    # Create embed to display user's pets
     pet_emojis = [f"{next((pet['emoji'] for pet in self.pets if pet['name'].lower() == name.lower()), None)} {count}x{name}" for name, count in pet_counts.items()]
     embed = discord.Embed(
        title=f"{member.display_name}'s Pets",
        description="Here are your pets:",
        color=discord.Color.green()
     )
     embed.add_field(name="Pets", value="\n".join(pet_emojis), inline=False)

     await ctx.reply(embed=embed)






    @commands.command()
    async def sell(self, ctx, pet_name: str, quantity: int = 1):
        member = ctx.author

          # Connect to database
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        # Count the number of each pet type
        cursor = self.db.cursor()
        cursor.execute(f"SELECT pets FROM main WHERE user_id = {member.id}")
        pets_str = cursor.fetchone()[0] or ""  # default value if no pets
        pet_counts = {}
        for pet in pets_str.split(","):
            if pet:
                name, count = pet.split("x")
                pet_counts[name] = int(count)

        # Get pet price and name
        pet = next((p for p in self.pets if p["name"].lower() == pet_name.lower()), None)
        if pet is None:
            await ctx.reply("Invalid pet name!")
            return
        pet_price = pet["price"]
        pet_string = f"{quantity}x{pet_name},"

        # Check if user has enough of the pet to sell
        if pet_counts.get(pet_name, 0) < quantity:
            await ctx.send("You don't have enough of this pet to sell.")
            return

        # Update wallet and pet status
        total_price = pet_price * quantity
        cursor.execute("UPDATE main SET wallet = wallet + ?, pets = REPLACE(pets, ?, '') WHERE user_id = ?",
                       (total_price, pet_string, member.id))
        self.db.commit()

        # Send confirmation message
        await ctx.reply(f"You have sold {quantity} {pet_name}(s) for {total_price} coins.")









async def setup(bot):
    await bot.add_cog(PetShop(bot))
 