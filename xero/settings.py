import discord, os

os.environ['OWNERID']='750507937746649159' # saiv
#os.environ['OWNERID']='791946200881823744' # jays
os.environ['BOT_TOKEN']=''
os.environ['default_prefix']=';'
os.environ['BOT_DB']=''
os.environ['BOT_VERSION']='-03;B'
os.environ['ONLINE_CHANNEL_ID']='796204101150834698'


# EMBED HELPER
def create_embed(text):
    embed = discord.Embed(
        description=text,
        colour=discord.Colour.from_rgb(136,3,252),
    )
    return embed
