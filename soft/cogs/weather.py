import json
import discord
from discord.ext import commands
import requests



with open('config.json') as f:
    config = json.load(f)
    
class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def weather(self, ctx, *, location):
        """Displays the current weather for a given location"""
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={config['weather_api']}"
        response = requests.get(url).json()

        if response["cod"] != 200:
            await ctx.reply("Sorry, I couldn't find that location.")
            return

        weather = response["weather"][0]["description"]
        temp = round(response["main"]["temp"] - 273.15, 1)
        feels_like = round(response["main"]["feels_like"] - 273.15, 1)
        humidity = response["main"]["humidity"]
        wind_speed = response["wind"]["speed"]
        wind_dir = self.get_wind_direction(response["wind"]["deg"])

        location_name = response["name"]
        country_code = response["sys"]["country"]
        flag = self.get_country_flag(country_code)

        embed = discord.Embed(title=f"Weather for {location_name}, {country_code} {flag}",
                              description=f"{weather}\nTemperature: {temp}°C\nFeels like: {feels_like}°C\nHumidity: {humidity}%\nWind: {wind_speed} m/s {wind_dir}", color=discord.Color.random())
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1163/1163763.png")
        await ctx.reply(embed=embed)

    def get_wind_direction(self, degrees):
        """Converts wind direction from degrees to cardinal direction"""
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        index = round(degrees / (360.0 / len(directions)))
        return directions[index % len(directions)]

    def get_country_flag(self, country_code):
        """Returns the flag emoji for a given country code"""
        codepoints = {"A": 127462, "B": 127463, "C": 127464, "D": 127465, "E": 127466, "F": 127467, "G": 127468,
                      "H": 127469, "I": 127470, "J": 127471, "K": 127472, "L": 127473, "M": 127474, "N": 127475,
                      "O": 127476, "P": 127477, "Q": 127478, "R": 127479, "S": 127480, "T": 127481, "U": 127482,
                      "V": 127483, "W": 127484, "X": 127485, "Y": 127486, "Z": 127487}
        code = country_code.upper()
        if code in codepoints:
            return chr(codepoints[code])
        else:
            return ""
async def setup (bot):
    await bot.add_cog(Weather(bot))