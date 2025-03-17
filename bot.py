import discord
from discord import File
from discord import default_permissions
import random
import json
import datetime

with open("config.json", "r") as f:
    config = json.load(f)

with open("replies.json", "r") as f:
    replies = json.load(f)

TOKEN = config["token"]
REPLIES = replies

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.moderation = True

bot = discord.Bot(command_prefix="-", intents=intents)
testingservers = [1281122097778921515, 713322963193167913, 1345800065800736768]


def find_matching_key(message: str, json_data: json):
    for key, _ in json_data.items():
        # print(str(key))
        # print(message)

        if str(key) in message:
            return key
    return None


def normalize_string(input_string):
    normalized_string = (
        input_string.replace("\t", "").replace("\n", "").replace("\0", "")
    )

    if normalized_string == "None":
        return ""

    return normalized_string.lower()


def random_blahaj():
    with open("blahaj.json") as dt:
        data = json.load(dt)
        random_index = random.randint(0, len(data) - 1)
        return data[random_index]["url"], data[random_index]["name"]


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.streaming, name="Blahaj World 🦈"
        )
    )
    print("We Are Ready Now")


@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message) and message.reference is None:
        await message.reply("🎆 The Haj is here! 🦈")
    else:
        con = normalize_string(message.content)
        if len(con) >= 1 and len(con):
            k = find_matching_key(con, REPLIES)
            if k and message.author.id != bot.user.id:
                # print(k)
                await message.reply(REPLIES[k])

    await bot.process_application_commands(message)            

    # elif "haj" in message.content.lower() and message.author.id != bot.user.id:
    #     await message.reply("https://tenor.com/view/blahaj-go-spinny-blahaj-blahaj-spin-spin-shark-spin-gif-25670993")
    # elif "shark" in message.content.lower() and message.author.id != bot.user.id:
    #     await message.reply("shark")
    # elif "yokoso" in message.content.lower() and message.author.id != bot.user.id:
    #     await message.reply("<:YOKOSO:1167289778190946334>")
    # elif "hate crime" in message.content.lower() and message.author.id != bot.user.id:
    #     await message.reply("https://tenor.com/view/blahaj-gif-27048745")
    # elif "blahaj lore" in message.content.lower() and message.author.id != bot.user.id:
    #     await message.reply("https://tenor.com/view/blahaj-blahaj-lore-shark-shark-plushie-shark-plush-gif-23049674")

    # wtf was I doing when I wrote this - kaus
    # oh yeah I wrote that code over a year ago while procrastinating in school then never updated it - kaus


@bot.message_command(guild_ids=testingservers, name="Blåhaj says")
async def blahaj_says(ctx, message: discord.Message):
    await ctx.respond("Initializing speech bubble", ephemeral=True)
    await message.reply(file=File("blahaj_says.png"))


@bot.slash_command(
    guild_ids=testingservers, name="help", description="list of commands"
)
async def help(ctx):
    responses = ""
    for key in REPLIES:
        responses += "\n> "
        responses += key
    responses = responses[:-2]
    
    embed = discord.Embed(
        description="Blahaj commands", color=discord.Color.from_rgb(178, 208, 250)
    )
    embed.add_field(
        name="Fun Commands",
        value="\n **blahaj** \n > Show a random blahaj \n **shark** \n > Show a random blahaj \n **kill** \n > Kill someone (even yourself) ",
    )
    embed.add_field(
        name="Moderation commands",
        value="\n **domain_expansion** \n > Timeout a user \n **release** \n > Remove timeout from a user",
    )
    embed.add_field(name="Stuff Blåhaj responds to!", value=responses)

    await ctx.respond(embed=embed)


@bot.slash_command(
    guild_ids=testingservers, name="blahaj", description="show a random blahaj"
)
async def blahaj(ctx):
    blahajImageLink, blahajImageName = random_blahaj()
    embed = discord.Embed(
        description=f"Here is a **{blahajImageName}** 🦈",
        color=discord.Color.from_rgb(178, 208, 250),
    )
    embed.set_image(url=blahajImageLink)

    await ctx.respond(embed=embed)


@bot.slash_command(
    guild_ids=testingservers, name="shark", description="show a random blahaj"
)
async def shark(ctx):
    blahajImageLink, blahajImageName = random_blahaj()
    embed = discord.Embed(
        description=f"Here is a **{blahajImageName}** 🦈",
        color=discord.Color.from_rgb(178, 208, 250),
    )
    embed.set_image(url=blahajImageLink)
    
    await ctx.respond(embed=embed)


@bot.slash_command(
    guild_ids=testingservers, name="domain_expansion", description="Timeout a user"
)
@default_permissions(manage_roles=True)
async def domain_expansion(
    ctx, member: discord.Member, duration: int, reason: str | None = None
):
    timeout_time = datetime.timedelta(seconds=duration)
    await member.timeout(
        datetime.datetime.now(datetime.timezone.utc) + timeout_time, reason=reason
    )
    await ctx.respond(file=File("Domain Expansion.mp4"))


@bot.slash_command(
    guild_ids=testingservers, name="release", description="Remove timeout from a user"
)
@default_permissions(manage_roles=True)
async def release(ctx, member: discord.Member):
    await member.edit(communication_disabled_until=None)
    await ctx.respond(file=File("Domain Reversal.mp4"))


@bot.slash_command(guild_ids=testingservers, name="kill", description="kill someone")
async def kill(ctx, target: discord.Member):

    if target != ctx.author:
        def random_kill():
            with open("kill.json") as dt:
                data = json.load(dt)
                random_index = random.randint(0, len(data) - 1)
                return data[random_index]["url"]

        killImageLink = random_kill()
        embed = discord.Embed(
            description=f"**{ctx.author}** ended **{target}**'s life!!",
            color=discord.Color.from_rgb(160, 0, 0),
        )
        embed.set_image(url=killImageLink)

        await ctx.respond(embed=embed)

    else:
        def random_kill():
            with open("suicide.json") as dt:
                data = json.load(dt)
                random_index = random.randint(0, len(data) - 1)
                return data[random_index]["url"]

        killImageLink = random_kill()
        embed = discord.Embed(
            description=f"**{ctx.author}** committed suicide.",
            color=discord.Color.from_rgb(160, 0, 0),
        )
        embed.set_image(url=killImageLink)

        await ctx.respond(embed=embed)


bot.run(TOKEN)