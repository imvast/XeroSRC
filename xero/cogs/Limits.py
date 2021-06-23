# IMPORTS #
import discord, time, pymongo, os
from settings import *
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed

# MongoDB Setup
mongoClient = pymongo.MongoClient(os.environ.get('BOT_DB'))
db = mongoClient.get_database("XeroBOT").get_collection("servers+id")
db2 = mongoClient['XeroBOT']
limits = db2['limits']
gjoins = db2['gannouncements']
blacklist = db2['blacklist']

def blacklist_check():
    def predicate(ctx):
        author_id = ctx.author.id
        if blacklist.find_one({'user_id': author_id}):
            return False
        return True
    return commands.check(predicate)
    

class Limits(commands.Cog):
    def __init__(self, client, db):
        self.client = client
        self.db = db
    

    @commands.group(
      name="limit",
      aliases=["limits"],
      invoke_without_command=True,
      case_insensitive=True
    )
    @commands.cooldown(1, 2, commands.BucketType.channel)
    @blacklist_check()
    async def limit(self, ctx):
      embed = discord.Embed(title="Setting Anti Limits", description="\nTo get started with Anti limits there is one command that you will use: `;limit set [anti] [amount]`")
      embed.add_field(
        name="Types",
        value="A list of current changeable limits. Make sure to use the exact word and spelling when changing for there to be no issues."
      )
      embed.add_field(
        name="Set",
        value="Sets the limit of the chosen anti feature. Usage: `;limit set <type> <limit/amount>`\nExample: `;limit set bans 10`"
      )
      await ctx.send(embed=embed)


    @limit.command(
      name="types",
    )
    async def limit_types(self, ctx):
      embed = discord.Embed(
        title="Limit Types (BETA)", 
        description="➤ Bans • This will set the limit for Anti-Ban.\n➤ Kicks • This will set the limit for Anti-Kick.\n➤ Chan+ • This will set the limit for Anti-Channel-Creation."
      )
      await ctx.send(embed=embed)


    @limit.command(
      name="set",
      description="Sets a limit for an anti."
    )
    @commands.cooldown(1, 2, commands.BucketType.channel)
    @blacklist_check()
    async def limit_set(self, error, ctx, type: str, new_limit):
      if type == "Bans" or type == "bans":
       try:
         info = limits.find_one(
            {'guild_id': ctx.guild.id}
         )
         blimit = info['ban_limit']
         blimit[0] = new_limit
         limits.update_one(
            {'guild_id': ctx.guild.id},
            {
                '$set': {
                    'ban_limit': blimit
                }
            }
         )
         await ctx.send(
            embed=create_embed(
                f'{type} Limit has been set to: **{new_limit}**'
            )
         )
       except:
        raise error
        #await ctx.send(f"There was an error while setting limits for: `{type}`")
      elif type == "Kicks" or type == "kicks":
       try:
         info = limits.find_one(
            {'guild_id': ctx.guild.id}
         )
         klimit = info['kick_limit']
         klimit[0] = new_limit
         limits.update_one(
            {'guild_id': ctx.guild.id},
            {
                '$set': {
                    'kick_limit': klimit
                }
            }
         )
         await ctx.send(
            embed=create_embed(
                f'{type} Limit has been set to: **{new_limit}**'
            )
         )
       except:
        await ctx.send(f"There was an error while setting limits for: `{type}`")
      elif type == "Chan+" or type == "chan+":
       try:
         info = limits.find_one(
            {'guild_id': ctx.guild.id}
         )
         cclimit = info['chancreate_limit']
         cclimit[0] = new_limit
         limits.update_one(
            {'guild_id': ctx.guild.id},
            {
                '$set': {
                    'chancreate_limit': cclimit
                }
            }
         )
         await ctx.send(
            embed=create_embed(
                f'{type} Limit has been set to: **{new_limit}**'
            )
         )
       except:
        await ctx.send(f"There was an error while setting limits for: `{type}`")



def setup(client):
    client.add_cog(Limits(client))