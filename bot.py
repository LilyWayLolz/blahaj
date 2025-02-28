import discord
from discord import player
from discord import colour
from discord import SlashCommandGroup
from discord import File
from discord import default_permissions
from discord import commands
import random
import json
import typing
import datetime

with open('config.json', 'r') as f:
    config = json.load(f)
TOKEN = config['token']

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.moderation = True

bot = discord.Bot(command_prefix='-', intents = intents)
testingservers = [1281122097778921515, 713322963193167913]

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Blahaj World"))
    print("We Are Ready Now")

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message) and message.reference is None:
        await message.reply("🎆 The Haj is here! 🦈")
    elif "shark" in message.content.lower() and message.author.id != bot.user.id:
        await message.reply("shark")
    elif "yokoso" in message.content.lower() and message.author.id != bot.user.id:
        await message.reply("<:YOKOSO:1167289778190946334>")
    await bot.process_application_commands(message)

@bot.message_command(guild_ids = testingservers, name='Blåhaj says')
async def blahaj_says(ctx, message: discord.Message):
    await ctx.respond("Initializing speech bubble", ephemeral=True)
    await message.reply(file=File("blahaj_says.png"))

@bot.slash_command(guild_ids = testingservers, name='help', description='list of commands')
async def help(ctx):
    embed = discord.Embed(description="Blahaj commands", color=discord.Color.from_rgb(178, 208, 250))
    embed.add_field(name="", value="**Fun Commands** \n `-blahaj` \n `-shark` \n `-kill` \n \n **Moderation commands** \n `-domain_expansion` \n `-release`")
    embed.add_field(name="‎", value=">Show a random blahaj \n >Show a random blahaj \n >Kill someone (even yourself) \n \n \n >Timeout a user \n >Remove timeout from a user")
    embed.add_field(name = chr(173), value = chr(173))
    await ctx.respond(embed=embed)

@bot.slash_command(guild_ids = testingservers, name='blahaj', description='show a random blahaj')
async def blahaj(ctx):
    def random_blahaj():
        with open('blahaj.json') as dt:
            data = json.load(dt)
            random_index = random.randint(0, len(data) - 1)
            return data[random_index]["url"], data[random_index]["name"]

    blahajImageLink, blahajImageName = random_blahaj()
    embed = pycord.Embed(
        description=f"Here is a **{blahajImageName}** 🦈", color=pycord.Color.from_rgb(178, 208, 250))
    embed.set_image(url=blahajImageLink)
    await ctx.respond(embed=embed)

@bot.slash_command(guild_ids = testingservers, name='shark', description='show a random blahaj')
async def blahaj(ctx):
    def random_blahaj():
        with open('blahaj.json') as dt:
            data = json.load(dt)
            random_index = random.randint(0, len(data) - 1)
            return data[random_index]["url"], data[random_index]["name"]

    blahajImageLink, blahajImageName = random_blahaj()
    embed = discord.Embed(
        description=f"Here is a **{blahajImageName}** 🦈", color=discord.Color.from_rgb(178, 208, 250))
    embed.set_image(url=blahajImageLink)
    await ctx.respond(embed=embed)

@bot.slash_command(guild_ids = testingservers, name='domain_expansion', description ='Timeout a user')
@default_permissions(manage_roles=True)
async def domain_expansion(ctx, member: discord.Member, duration: int, reason: str | None = None):
    timeout_time = datetime.timedelta(seconds=duration)
    await member.timeout(datetime.datetime.now(datetime.timezone.utc) + timeout_time, reason=reason)
    await ctx.respond(file=File("Domain Expansion.mp4"))

@bot.slash_command(guild_ids = testingservers, name="release", description='Remove timeout from a user')
@default_permissions(manage_roles=True)
async def release(ctx, member: discord.Member):
    await member.edit(communication_disabled_until=None)
    await ctx.respond(file=File("Domain Reversal.mp4"))

@bot.slash_command(guild_ids = testingservers, name="kill", description='kill someone')
async def kill(ctx, target: discord.Member):
    if target != ctx.author:
        def random_kill():
            with open('kill.json') as dt:
                data = json.load(dt)
                random_index = random.randint(0, len(data) - 1)
                return data[random_index]["url"]

        killImageLink = random_kill()
        embed = discord.Embed(
            description=f"**{ctx.author}** ended **{target}**'s life!!", color=discord.Color.from_rgb(160, 0, 0))
        embed.set_image(url=killImageLink)

        role = discord.utils.get(target.guild.roles, id=(713714211552886875))
        await ctx.respond(embed=embed)
    else:
        def random_kill():
            with open('suicide.json') as dt:
                data = json.load(dt)
                random_index = random.randint(0, len(data) - 1)
                return data[random_index]["url"]

        killImageLink = random_kill()
        embed = discord.Embed(
            description=f"**{ctx.author}** committed suicide.", color=discord.Color.from_rgb(160, 0, 0))
        embed.set_image(url=killImageLink)

        role = discord.utils.get(target.guild.roles, id=(713714211552886875))
        await ctx.respond(embed=embed)

bot.run(TOKEN)