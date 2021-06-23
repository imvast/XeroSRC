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
    

class Info(commands.Cog):
    def __init__(self, client, db):
        self.client = client
        self.db = db
        self.messages = {}
    

    @commands.Cog.listener()
    async def on_message_delete(self, message): 
     if message.guild is None: 
          return
     if message.author.bot: 
          return
     if not message.content: 
          return 
     self.messages[message.channel.id] = message


    @commands.command(
        name="appeal",
        description="Appeal request for blacklisted users. `BETA`",
        usage="appeal"
    )
    @commands.cooldown(1, 2, commands.BucketType.channel)
    async def appeal(self, ctx):
      if blacklist.find_one({ 'user_id' : ctx.author.id }):
        if ctx.guild is None:
          await ctx.send(f"{ctx.author.mention}\nSadly, this feature isn't available to the public yet. Until it is ready, DM `saiv ツ#9999` your appeal request!")
          webhook = DiscordWebhook(url="https://discord.com/api/webhooks/796053206916005898/jTWUDv9_KOrta0-pi3EMGmEu5eLH7T-ESM13nLZ331y1Wufibwhwt61z-pjRihZLhg2S")
          log = DiscordEmbed(title = ctx.author.name, description = f"New Appeal Request From: `{ctx.author.id}`")
          webhook.add_embed(log)
          webhook.execute()
        else:
          await ctx.send("`This command can only be used in DMs.`")
      else:
        await ctx.author.send(embed=create_embed("**You are not blacklisted. 😇**"))

    @commands.command(
        name="accept_appeal"
    )
    @commands.is_owner()
    @commands.cooldown(1, 2, commands.BucketType.channel)
    async def accept_appeal(self, ctx, *, member: discord.Member):
      try:
        await member.send("You request has been accepted! Thanks for using Xero.")
        await ctx.send("Sent!")
      except:
        await ctx.send("Failed to send.")

    @commands.command(
        name="invite",
        description="Sends the bot's invite link.",
        usage="invite",
        aliases=["inv"]
    )
    @blacklist_check()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def invite(self, ctx):
        embed = discord.Embed(
        title = "<:NVLink:776617844213153833> Invite Me",
        colour = discord.Colour.from_rgb(136,3,252),
        description = "[__**Invite!**__](https://discord.com/api/oauth2/authorize?client_id=786394587970666526&permissions=8&scope=bot)"
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(
        name="updateinfo",
        description="Sends the bot's support server link.",
        usage="updateinfo",
        aliases=["ud-info", "udinfo"]
    )
    @blacklist_check()
    @commands.cooldown(1, 7, commands.BucketType.channel)
    async def updateinfo(self, ctx):
        embed = discord.Embed(
        title = "__Update Info__",
        colour = discord.Colour.from_rgb(136,3,252),
        description = "• `Officially Released`"
        )
        embed.set_footer(text="Version: -00 • Jan 4")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(
        name="info",
        description="Shows information about the bot",
        usage="info",
        aliases=['information', 'about', 'botinfo']
    )
    @blacklist_check()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def info(self, ctx):
      #variables
        servertotal = len(self.client.guilds)
        usertotal = len(set(self.client.get_all_members()))
        #extras = db2.find_one({'guild_id': ctx.guild.id})['prefixes']
        time = int(self.client.latency * 1000)
      #embed/message
        embed = discord.Embed(
        title = "<a:x_Pin:776513817281691659> Xero", url="https://discord.com/api/oauth2/authorize?client_id=786394587970666526&permissions=8&scope=bot", icon_url="https://cdn.discordapp.com/attachments/794934130550898718/795829789931864134/20210105_014320.jpg",
        colour = discord.Colour.from_rgb(136,3,252),
        description = "More info about Xero.\n[__**Upvote**__](https://discord.ly/xero) • [__**Invite**__](https://discord.ly/xero) • [__**Support**__](https://discord.gg/ECSBeyCD)", timestamp=ctx.message.created_at
        )
        embed.add_field(
          name='🔹 **__Version__**',
          value=os.environ.get('BOT_VERSION'),
          inline=True
        )
        embed.add_field(
          name='📚 **__Library__**',
          value=f'Discord.PY',
          inline=True
        )
        embed.add_field(
          name='<a:shineydev:776479283882360872> **__Creators__**',
          value=f'Saiv & Jays',
          inline=True
        )
        embed.add_field(
          name='<:1618_users_logo:776597644410748938> **__Servers & Users__**',
          value=f'Total Servers: `{servertotal}`\nTotal Users: `{usertotal}`',
          inline=True
        )
        embed.add_field(
          name='❓ **__Prefixes__**',
          value=f'Default: `;`\nServer:  `;`',# + ' and '.join(extras) + "`",
          inline=True
        )
        embed.add_field(
          name='<:r_check:780938741640200239> **__Latency__**',
          value=f'BOT: `{time}ms.`\nWebsocket: `9ms.`',
          inline=True
        )
        embed.set_thumbnail(
          url="https://cdn.discordapp.com/attachments/794934130550898718/795829789931864134/20210105_014320.jpg"
        )
        embed.set_footer(
          text=f"Uptime: 24/7 • Revamp Soon.."
        )
        message = await ctx.send(embed=embed)
        await message.add_reaction("<a:verify_purple:782792084817707018>")


    @commands.command(
        name='snipe',
        description='Sends most recent deleted message.',
        usage="snipe"
    )
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def snipe(self, ctx): 
        message = self.messages.get(ctx.channel.id)
        if message is None: 
            await ctx.send(embed=create_embed('Nothing to snipe.'))
        else:
            ma = str(message.author)
            mc = message.content
            embed = discord.Embed(colour=discord.Colour.from_rgb(255,255,254), description=f"{mc}", timestamp=message.created_at)
            embed.set_author(name=f"{ma}", icon_url=message.author.avatar_url)
            await ctx.send(embed=embed)


    @commands.command(
        name='whois',
        aliases=['userinfo', 'profile'],
        description='Displays info about the specified user.',
        usage="whois"
    )
    @commands.cooldown(1, 5, commands.BucketType.channel)
    @blacklist_check()
    async def whois(self, ctx, member: discord.Member = None):
      if not member:  # if member is no mentioned
          member = ctx.message.author  # set member as the author
      roles = [role for role in member.roles]
      embed = discord.Embed(colour=discord.Colour.from_rgb(255,255,254), timestamp=ctx.message.created_at, title=f"User Info - {member}")
      embed.set_thumbnail(url=member.avatar_url)
      embed.set_footer(text=f"Requested by {ctx.author}")
      embed.add_field(name="Display Name:", value=member.display_name)
      embed.add_field(name="ID:", value=member.id)
      embed.add_field(name="Creation Date:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
      embed.add_field(name="Joined Date:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
      embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
      embed.add_field(name="Highest Role:", value=member.top_role.mention)
      embed.add_field(name="Boosting:", value=member.premium_since)
      await ctx.send(embed=embed)


    @commands.command(
        name='serverinfo',
        description='Displays the server info',
        usage="serverinfo",
    )
    @commands.cooldown(1, 5, commands.BucketType.channel)
    @blacklist_check()
    async def serverinfo(self, ctx):
        guild = ctx.message.guild
        online = len([member.status for member in guild.members
                      if member.status == discord.Status.online or
                      member.status == discord.Status.idle or member.status == discord.Status.do_not_disturb])
        total_users = len(guild.members)
        total_bots = len([member for member in guild.members if member.bot == True])
        total_humans = total_users - total_bots
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        passed = (ctx.message.created_at - guild.created_at).days
        created_at = ("Created on {}.".format(guild.created_at.strftime("`%d %b %Y` at `%H:%M`"), passed))
        embed = discord.Embed(description=created_at, colour=discord.Colour.from_rgb(136,3,252))
        embed.add_field(name="<a:crown:776616530368004116> **Owner**", value=str(guild.owner), inline=True)
        embed.add_field(name="<a:whiteearth:776616643639771176> **Region**", value=str(guild.region), inline=True)
        embed.add_field(name="<a:boosts:776622883564290078> **Boosts**", value=guild.premium_subscription_count, inline=False)
        embed.add_field(name="🏷 **Roles**", value=len(guild.roles), inline=False)
        embed.add_field(name="<:1618_users_logo:776597644410748938> **Members**", value="`{}` **/** {}".format(online, total_users), inline=True)
        embed.add_field(name="🧍 **Humans**", value=total_humans, inline=True)
        embed.add_field(name="<:ClydeBot:776617480524136468> **Bots**", value=total_bots, inline=True)
        embed.add_field(name="<:DE_IconTextChannel:776616614224855040> **Text Channels**", value=text_channels, inline=True)
        embed.add_field(name="<:vc:776617624448139294> **Voice Channels**", value=voice_channels, inline=True)
        embed.set_footer(text=f"Server ID: {str(guild.id)}")
        
        if guild.icon_url:
            embed.set_author(name=guild.name, url=guild.icon_url)
            embed.set_thumbnail(url=guild.icon_url)
            await ctx.send(embed=embed)
        else:
            embed.set_author(name=guild.name)
            await ctx.send(embed=embed)
    

    # Error handlers

    @serverinfo.error
    async def serverinfo_error(self, ctx, error):
        await ctx.send(
            embed=create_embed(
                f"There was an error while attempting to get the server info."
            )
        )
        
    @whois.error
    async def whois_error(self, ctx, error):
      if isinstance(error, blacklist.find_one({'user_id': ctx.author.id})):
        await ctx.send(embed=create_embed("You are currently blacklisted.", embed.set_footer("Heat Level: 4")))
      else:  
        await ctx.send(
            embed=create_embed(
                f"Failed to get info on that user."
            )
        )

    @appeal.error
    async def appeal_error(self, ctx, error):
            if isinstance(error, commands.CommandOnCooldown):
                await ctx.send(
                    embed=create_embed(
                        f'**Appeal, is currently on cooldown.**\nCooldown Time Remaining: {int(error.retry_after)}s'
                    )
                )



def setup(client):
    client.add_cog(Info(client))
