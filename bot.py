
import asyncio
from datetime import datetime, timedelta
import discord
from discord.ext import commands

timeout_duration = 60  # in seconds


bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

# Keep track of user's levels and experience
users = {}


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command()
async def poll(ctx, *args):
    question = ' '.join(args)
    await ctx.send(f'Poll: {question}\n\nType `yes` to vote yes and `no` to vote no.')


@bot.command()
async def userinfo(ctx, member: discord.Member):
    """
    Description:
    Retrieve inforamtion about a specific member on the  server.

    Usage: $userinfo[@member]
    """
    await ctx.send(f'Username: {member.name}\nID: {member.id}\nStatus: {member.status}\nHighest role: {member.top_role}\nAccount created at: {member.created_at}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Add user's experience
    if message.author not in users:
        users[message.author] = 0
    users[message.author] += 10

    # Check if user has enough experience to level up
    level = int(users[message.author] / 100) + 1
    if users[message.author] % 100 == 0 and level <= 10:
        await message.channel.send(f'{message.author.mention} has leveled up to level {level}!')

    await bot.process_commands(message)

@bot.command()
async def listmembers (ctx):
    members =  ctx.guild.members
    memberlist = [member.mention for member in members]
    await ctx.send(f'\n'.join(memberlist))
    print("sned alist of member in response to $listmembers")


@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    """
    Bans a membre from the server

    Usage: $ban @member [reason]

    Arguments:
    -member: The memeber to ban.
    -reason (optional): The reason for the ban.
    """
    if ctx.author.id == ctx.guild.owner_id:
        await member.ban(reason=reason)
        await ctx.send(f"{member.name} was banned.")
        print("The admin of the server has banned a user")
    else:
        await ctx.send("You do not have permission to ban users.")


@bot.command()
async def unban(ctx, *, member):
    if ctx.author.guild_permissions.ban_members:
        async for entry in ctx.guild.bans():
            user = entry.user

            if (user.name, user.discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.mention} has been unbanned.")
                return
        await ctx.send(f"{member} was not found in the banned list.")
    else:
        await ctx.send("You do not have permission to unban members.")

# Unban all currently banned members


@bot.command()
@commands.has_permissions(ban_members=True)
async def unbanall(ctx):
    async for entry in ctx.guild.bans():
        user = entry.user
        await ctx.guild.unban(user, reason="Unbanned all users.")
        await ctx.send(f"Unbanned {user.mention}.")

    else:
        await ctx.send("You do not have permission to unban members.")


@bot.command()
async def hello(ctx):

        await ctx.send('Hello!')
        print("Sent 'Hello!' in response to '$hello'")


@bot.command()
async def experience(ctx, user: discord.User = None):
    if not user:
        user = ctx.author

    # Retrieve the user's experience points
    if user not in users:
        users[user] = 0
    exp = users[user]

    await ctx.send(f'{user.name} has {exp} experience points and is at level {int(exp / 100) + 1}.')

@bot.command()
@commands.has_role("Moderator")
async def timeout(ctx, user: discord.Member, timeout_duration: int):
    role = discord.utils.get(ctx.guild.roles, name='Timeout')
    if role is not None:
        await user.add_roles(role)
        await ctx.send(f'{user.mention} has been timed out for {timeout_duration} seconds.')
        await user.send(f'You have been timed out for {timeout_duration} seconds. You will not be able to send messages in the server until the timeout expires.')
        await asyncio.sleep(timeout_duration)
        await user.remove_roles(role)
        await ctx.send(f'{user.mention} has been un-timed out.')
    else:
        await ctx.send("Timeout role not found. Please create a role called 'Timeout' and try again.")

@bot.command()
@commands.has_role("admin")
async def check_timeout(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Timeout")
    if role in member.roles:
        for channel in ctx.guild.channels:
            perms = channel.permissions_for(member)
            if not perms.send_messages:
               
                await ctx.send(f"{member.mention} has minutes left in timeout.")
                return
        await ctx.send(f"{member.mention} is timed out, but cannot determine time remaining.")
    else:
        await ctx.send(f"{member.mention} is not timed out.")

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author
    avatar.url = member.avatar.url

    request = f"{ctx.author.name} requested the avatar of "  f"{member.name}"


    embed = discord.Embed()
    embed.colour = discord.Colour.blue()  # Set the color to blue
    embed.set_author(name=f"{member}'s avatar")
    embed.set_image(url=avatar.url)
    embed.set_author(name=request)  # Set the request as the message title

    await ctx.send(embed=embed)


@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        await channel.send(f"Welcome {member.mention} to the server!")


bot.run('MTA3NDY1ODIzMTA0NzE2ODA2MA.Gas7y4.8gs9o6NQEAAL6zj5NKtVpTarQgAIxXRgNonsl0')

