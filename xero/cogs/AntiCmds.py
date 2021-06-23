# IMPORTS #
import discord, os, pymongo, libneko
from libneko import pag
from settings import *
from discord.ext import commands

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


class AntiCmds(commands.Cog):
    def __init__(self, client, db):
        self.client = client
        #self.db = db

#def is_owner(self, ctx):
#    return ctx.message.author.id == int(os.environ.get('OWNERID'))
#def is_whitelisted(self, ctx):
#    return ctx.message.author.id in db.find_one({ "guild_id": ctx.guild.id })["users"] or ctx.message.author.id == int(os.environ.get('OWNERID'))
#def is_server_owner(self, ctx):
#    return ctx.message.author.id == ctx.guild.owner.id or ctx.message.author.id == int(os.environ.get('OWNERID'))


    @commands.command(
      name='setup',
      description="Setup the anti feature",
      usage="setup"
    )
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def setup(self, ctx):
        embed = discord.Embed(
        title = "Getting started with Xero's Anti-Nuke!",
        colour = discord.Colour.from_rgb(136,3,252),
        description = f"Xero anti-nuke is one of the most relyable and safe anti-nukes put on discord. With Xero, you can stop raiders, nukers, and people out to harm your server with its key features you can view by visiting `;help anti`. To whitelist a user from Xero's anti-nuke features, you must say `;whitelist [@user]`, but be aware that Xero will take __zero__ action towards what they decide to do to and with your server. Logs have been succesfully setup in this server and to change where you want logs to goto, please say `#log [#channel]`.")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/786394587970666526/c93f889c209a8ce071780c91c1aa968b.webp?size=1024")
        await ctx.send(embed=embed)
        channel = await ctx.guild.create_text_channel('xero-logs')
        await channel.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False)
        await channel.send(embed=create_embed("This is the logging channel where all the anti-nuke logs will be stored. `BETA`"))


    @commands.command(
      name='settings',
      description="Server Anti Settings",
      usage="settings"
    )
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def settings(self, ctx):
      banlimit = limits.find_one({'guild_id': ctx.guild.id})['ban_limit']
      kicklimit = limits.find_one({'guild_id': ctx.guild.id})['kick_limit']
      role_c = limits.find_one({'guild_id': ctx.guild.id})['rolecreate_limit']
      role_d = limits.find_one({'guild_id': ctx.guild.id})['roledelete_limit']
      channel_c = limits.find_one({'guild_id': ctx.guild.id})['chancreate_limit']
      channel_d = limits.find_one({'guild_id': ctx.guild.id})['chandelete_limit']
      webhook_c = limits.find_one({'guild_id': ctx.guild.id})['webhook_limit']
      embed = discord.Embed(title=f"__Xero Anti Settings__ ~ {ctx.guild.name}", color=discord.Color.from_rgb(54,57,63))
      embed.add_field(
        name="Anti-Ban",
        value=f"Maximum: `{banlimit}`\nPunishment: `Ban`\nEnabled: `True`",
        inline=True
      )
      embed.add_field(
        name="Anti-Kick",
        value=f"Maximum: `{kicklimit}`\nPunishment: `Ban`\nEnabled: `True`",
        inline=True
      )
      embed.add_field(
        name="Anti-Bot",
        value=f"Punishment: `Ban`\nEnabled: `True`",
        inline=True
      )
      embed.add_field(
        name="Anti-Role-Create",
        value=f"Maximum: `{role_c}`\nPunishment: `Ban`\nEnabled: `True`",
        inline=True
        )
      embed.add_field(
        name="Anti-Role-Delete",
        value=f"Maximum: `{role_d}`\nPunishment: `Ban`\nEnabled: `True`",
        inline=True
      )
      embed.add_field(
        name="Anti-Permissions",
        value=f"Punishment: `Ban`\nEnabled: `True`",
        inline=True
      )
      embed.add_field(
        name="Anti-Channel-Create",
        value=f"Maximum: `{channel_c}`\nPunishment: `Ban`\nEnabled: `True`",
        inline=True
      )
      embed.add_field(
        name="Anti-Channel-Delete",
        value=f"Maximum: `{channel_d}`\nPunishment: `Ban`\nEnabled: `True`",
        inline=True
      )
      embed.add_field(
        name="Anti-Webhook",
        value=f"Maximum: `{webhook_c}`\nPunishment: `Ban`\nEnabled: `True`",
        inline=True
      )
      embed.add_field(
        name="Anti-Link",
        value="Allowed: `None`\nPunishment: `None`\nEnabled: `False`",
        inline=True
        )
      embed.add_field(
        name="Anti-Spam",
        value="Amount: `None`\nPunishment: `None`\nEnabled: `False`",
        inline=True
      )
      embed.set_footer(text="BETA")
      await ctx.send(embed=embed)


    @commands.command(
      name="whitelisted",
      description="Whitelisted users",
      usage="whitelisted"
    )
    @blacklist_check()
    #@commands.check(is_server_owner)
    async def whitelisted(self, ctx):
      if ctx.message.author.id == ctx.guild.owner.id:
        data = db.find_one({ "guild_id": ctx.guild.id })['users']
        embed = discord.Embed(title=f"Whitelist for {ctx.guild.name}", description="__Whitelisted__\n")
        for i in data:
            embed.description += f"{self.client.get_user(i)} - {i}\n"

        await ctx.send(embed=embed)
      else:
        await ctx.send("> This command can only be used by the `server owner`.")

    @commands.command(
      name='whitelist',
      description="Setup the anti feature",
      usage="whitelist `[user]`"
    )
    @blacklist_check()
    #@commands.check(is_server_owner)
    async def whitelist(self, ctx, user: discord.User):
      if ctx.message.author.id == ctx.guild.owner.id:
        if not user:
            await ctx.send("No user was provided.")
            return
        elif not isinstance(user, discord.User):
            await ctx.send("Invalid user.")
            return
        elif user.id in db.find_one({ "guild_id": ctx.guild.id })["users"]:
            await ctx.send(f"{user} is already whitelisted.")
            return
        else:
            db.update_one({ "guild_id": ctx.guild.id }, { "$push": { "users": user.id }})
            await ctx.send(f"`{user}` is now whitelisted in this server.")
      else:
        await ctx.send("> This command can only be used by the `server owner`.")


    @commands.command(
      name='unwhitelist',
      description="Setup the anti feature",
      usage="unwhitelist `[user]`"
    )
    @blacklist_check()
    #@commands.check(is_server_owner)
    async def unwhitelist(self, ctx, user: discord.User):
      if ctx.message.author.id == ctx.guild.owner.id:
        if not user:
            await ctx.send("No user was provided.")
        elif not isinstance(user, discord.User):
            await ctx.send("Invalid user.")
        elif user.id not in db.find_one({ "guild_id": ctx.guild.id })["users"]:
            await ctx.send(f"{user} is not whitelisted.")
            return
        else:
            db.update_one({ "guild_id": ctx.guild.id }, { "$pull": { "users": user.id }})
            await ctx.send(f"`{user}` is no longer whitelisted in this server.")
      else:
        await ctx.send("> This command can only be used by the `server owner`.")


    @commands.command(
      name="unbanall",
      aliases=["massunban", "purgebans"]
    )
    @blacklist_check()
    @commands.has_permissions(ban_members=True)
    async def unbanall(self, ctx): 
      permissions = ctx.message.author.permissions_in(ctx.channel)
      if not permissions.ban_members:
        await ctx.send("Insufficient Permissions. Required: `Ban Members`")
      banlist = await ctx.guild.bans()
      @pag.embed_generator(max_chars=2048)
      def det_embed(paginator, page, page_index):
        banned = ""
        em = discord.Embed(title = f"List of Banned Members:", description=page)
        em.set_footer(text=f"{len(bans)} Members in Total.")
        return em
        page = pag.EmbedNavigatorFactory(factory=det_embed)
        for users in bans:
          banned += f"{users.user}\n"
          page += banned
          page.start(ctx)
      for users in banlist:
        try:
            bans = await ctx.guild.bans()
            await ctx.guild.unban(user=users.user)
        except:
            await ctx.send(F"Unbanall error: Failed to unban, `{users.user}`")



def setup(client):
    client.add_cog(AntiCmds(client))