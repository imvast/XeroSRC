import discord, pymongo, os, platform, psutil, datetime, time, shutil
from colorama import Fore
from discord.ext import commands, tasks
from settings import *


mongoClient = pymongo.MongoClient(os.environ.get('BOT_DB'))
db = mongoClient.get_database("XeroBOT").get_collection("servers+id")
db2 = mongoClient['XeroBOT']
limits = db2['limits']
gjoins = db2['gannouncements']
blacklist = db2['blacklist']

try:
    exec(open('settings.py').read())
except:
    print(Fore.RED + '[!] Database Failure.' + Fore.RESET)


def get_prefix(client, message):
    if message.guild is None:
      return message.channel.send("To use my commands, invite me to your server and type: `;help`")
    else:
      extras = db.find_one({'guild_id': message.guild.id})
      prefixes = ";"#extras['prefixes']
      return commands.when_mentioned_or(*prefixes)(client, message)


client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, owner_id=int(os.environ.get('OWNERID')), intents=discord.Intents.all())
client.remove_command("help")

###
from cogs.Anti import Anti
from cogs.AntiCmds import AntiCmds
from cogs.Help import Help
from cogs.Info import Info
from cogs.Limits import Limits
#from cogs.Logs import Logs
from cogs.Moderation import Moderation
from cogs.System import System
client.add_cog(Anti(client, db))
client.add_cog(AntiCmds(client, db))
client.add_cog(Help(client, db))
client.add_cog(Info(client, db))
client.add_cog(Limits(client, db))
#client.add_cog(Logs(client, db))
client.add_cog(Moderation(client, db))
client.add_cog(System(client, db))
###


@client.event
async def on_message(message):
  if message.content == "<@!786394587970666526>":
   try:
     await message.channel.send(embed=create_embed("Hello! I am Xero. I was created by Jays & Saiv. For a list of my commands, type: `;help`!"))
   except:
     await message.channel.send("(Missing Permission ~ `Embed Links`)\nHello! I am Xero. I was created by Jays & Saiv. For a list of my commands, type: `;help`!")
  elif message.content == "<@!786394587970666526> shit bot":
   try:
     await message.reply("That's Not Nice! :((")
   except:
     pass
  elif message.content == "<@!786394587970666526> ily":
   try:
     await message.reply("ily2 ❤️")
   except:
     pass
  await client.process_commands(message)


@client.command()
@commands.is_owner()
async def rreac(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="__𝐑𝐞𝐚𝐜𝐭 𝐭𝐨 𝐯𝐞𝐫𝐢𝐟𝐲__", description="𝑅𝑒𝒶𝒸𝓉 𝓉𝑜 𝑔𝒶𝒾𝓃 𝒶𝒸𝒸𝑒𝓈𝓈 𝓉𝑜 𝓉𝒽𝑒 𝓇𝑒𝓈𝓉 𝑜𝒻 𝓉𝒽𝑒 𝓈𝑒𝓇𝓋𝑒𝓇!", colour=discord.Colour.from_rgb(255, 8, 243))
    embed.set_image(url="https://media1.tenor.com/images/7dd2774bd19a65b9c5c8d3e5c1605848/tenor.gif?itemid=17708133")
    await ctx.send(embed=embed)


@client.command()
@commands.is_owner()
async def hostinfo(ctx):
  uname = platform.uname()
  embed = discord.Embed(description=f"""```asciidoc\n==  VPS HOST INFORMATION  ==
 System    :: {uname.system}-x64
 Node Name :: {uname.node}
 Release   :: {uname.release}
 Version   :: {uname.version}
 Processor :: {uname.processor}
```""")
  await ctx.send(embed=embed)




@tasks.loop(hours=6, reconnect=True)
async def bot_restart():
    channel = client.get_channel(id=os.environ.get('ONLINE_CHANNEL_ID'))
    await channel.edit(name="🟡")
    await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.playing, name=f"Restarting By Default.."))
    os._exit(0)

client.run(os.environ.get('BOT_TOKEN'), reconnect=True)
