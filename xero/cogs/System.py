import discord, os, math, pymongo, asyncio
from settings import *
from colorama import Fore
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed

# Connect to mongodb database
mongoClient = pymongo.MongoClient(os.environ.get('BOT_DB'))
db = mongoClient.get_database("XeroBOT").get_collection("servers+id")
db2 = mongoClient['XeroBOT']
limits = db2['limits']
gjoins = db2['gannouncements']
blacklist = db2['blacklist']


class System(commands.Cog):
    def __init__(self, client, db):
        self.client = client
        self.db = db

    # Commands
    @commands.command(
        name='reload',
        description='Reload the cog',
        usage='reload `[cog name]`'
    )
    @commands.is_owner()
    async def reload(self, ctx, extension):
        await ctx.channel.purge(limit=1)
        self.client.reload_extension(f'cogs.{extension}')
        print(f"Reloaded Cog: {extension}")
        await ctx.send(
            embed=create_embed(
                f"**{extension}** has been reloaded"
            ),
            delete_after=10
        )

    @commands.command(
        name='load',
        description='Load the cog',
        usage='load `[cog name]`'
    )
    @commands.is_owner()
    async def load(self, ctx, extension):
        await ctx.channel.purge(limit=1)
        self.client.load_extension(f'cogs.{extension}')
        print(f'Cog {extension} loaded successfully')
        await ctx.send(
            embed=create_embed(
                f"Cog **{extension}** loaded successfully"
            ),
            delete_after=10
        )

    @commands.command(
        name='unload',
        description='Unload the cog',
        usage='unload `[cog name]`'
    )
    @commands.is_owner()
    async def unload(self, ctx, extension):
        await ctx.channel.purge(limit=1)
        self.client.unload_extension(f'cogs.{extension}')
        print(f'Cog {extension} unloaded successfully')
        await ctx.send(
            embed=create_embed(
                f"Cog **{extension}** unloaded successfully"
            ),
            delete_after=10
        )

    @commands.command(
        name='servers',
        description='List the servers that the bot is in',
        usage='servers',
        aliases=["serverlist"]
    )
    @commands.is_owner()
    async def servers(self, ctx, page: int = 1):
        output = ''
        guilds = self.client.guilds
        pages = math.ceil(len(guilds)/15)
        if 1 <= page <= pages:
            counter = 1+(page-1)*15
            for guild in guilds[(page-1)*15:page*15]:
                gn = guild.name
                gi = str(guild.id)
                gm = str(len(guild.members))
                output += f'**{counter}.** `{gn}` **|** `{gi}` **|** `{gm}`\n'
                counter += 1
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(136,3,252),
                description=output,
                title='__**Server List**__',
                timestamp=ctx.message.created_at
            )
            embed.set_footer(
                text=f'Page {page} of {pages}'
            )
            msg = await ctx.send(
                embed=embed
            )
            await msg.add_reaction("<a:lrArrow:767064087367647242>")
            await msg.add_reaction("<a:r_rightarrow:781535142698942515>")
            #while True:
            #  if msg.author.add_reaction("<a:lrArrow:767064087367647242>"):
            #    page.back()
            #  elif msg.author.add_reaction("<a:r_rightarrow:781535142698942515>"):
            #    page.next()
        else:
            await ctx.send(
                embed=create_embed(
                    'Invalid Page Number.'
                ),
                delete_after=10
            )

    @commands.command(
        name='leaveserver',
        description='Leave the server of your choice',
        usage='leaveserver `[number on list]`'
    )
    @commands.is_owner()
    async def leaveserver(self, ctx, pos: int):
        guilds = self.client.guilds
        guild = guilds[pos-1]
        await guild.leave()
        await ctx.send(
            embed=create_embed(
                f'Left {guild.name}'
            )
        )

    @commands.command(
        name='blacklist',
        description='Blacklist users from using the bot',
        usage='blacklist `[userid]`'
    )
    @commands.is_owner()
    async def blacklist(self, ctx, userid: int, reason=None):
        if blacklist.find_one({'user_id': userid}):
            await ctx.send(
                embed=create_embed(
                    'User ID already blacklisted.'
                )
            )
        else:
            if self.client.get_user(userid) != None:
                blacklist.insert_one({'user_id': userid})
                await ctx.send(
                    embed=create_embed(
                        f'User, <@{userid}> is now blacklisted.'
                    )
                )
                user = self.client.get_user(userid)
                await user.send(embed=create_embed(f'You have been blacklisted from Xero.\nHeat Level: `2`\nReason: `{reason}`'))
            else:
                await ctx.send(
                    embed=create_embed(
                        'Unknown User ID. Please make sure that user is in a server that I am in!'
                    ),
                    delete_after=30
                )

    @commands.command(
        name='showblacklist',
        description='List of all blacklisted users.',
        usage='showblacklist `[page]`'
    )
    @commands.is_owner()
    async def showblacklist(self, ctx, page: int = 1):
        output = ''
        blacklisted = blacklist.find()
        pages = math.ceil(blacklisted.count()/10)
        if 1 <= page <= pages:
            counter = 1+(page-1)*10
            for user in blacklisted[(page-1)*10:page*10]:
                user = self.client.get_user(user['user_id'])
                output += f'**{counter}.** `{user.name}` | `{user.id}`\n'
                #output += f'**{counter}.** `{user}` | `{user}`\n'
                counter += 1
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(136,3,252),
                title='**__Blacklisted Users__**',
                description=output,
                timestamp=ctx.message.created_at
            )
            embed.set_footer(
                text=f'Page {page} of {pages}'
            )
            await ctx.send(
                embed=embed
            )
        else:
            await ctx.send(
                embed=create_embed(
                    'The specified page does not exist'
                ),
                delete_after=10
            )

    @commands.command(
        name='unblacklist',
        description='Remove\'s a user from the blacklist.',
        usage='unblacklist `[userid]`'
    )
    @commands.is_owner()
    async def unblacklist(self, ctx, userid: int):
        if blacklist.find_one({'user_id': userid}):
            blacklist.delete_one({'user_id': userid})
            await ctx.send(
                embed=create_embed(
                    f'User, <@{userid}> has been unblacklisted.'
                ),
                delete_after=30
            )
        else:
            await ctx.send(
                embed=create_embed(
                    f'User, <@{userid}> is not blacklisted.'
                ),
                delete_after=10
            )

    @commands.command(
        name='restart',
        description='Force restart the bot',
        usage='restart'
    )
    @commands.is_owner()
    async def restart(self, ctx):
        embed = discord.Embed(colour=discord.Colour.from_rgb(136,3,252), title="Restarting.." ,description="**Xero is currently restarting. Please wait up to 10 seconds..**")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/794934130550898718/795829789931864134/20210105_014320.jpg")
        await ctx.send(embed=embed)
        await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=f"Requested Restart.."))
        channel = self.client.get_channel(id=os.environ.get('ONLINE_CHANNEL_ID'))
        await channel.edit(name="🟡")
        print(Fore.RED + '[Xero] Client Restarting..' + Fore.RESET)
        os._exit(0)

      

    # Error handler
    @reload.error
    async def reload_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(
                embed=create_embed(
                    f'Cog not found, please use `;help reload` for list of cogs'
                )
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                embed=create_embed(
                    f"Missing required argument, please use `;help reload` for correct usage"
                )
            )

    @load.error
    async def load_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(
                embed=create_embed(
                    f'Cog not found, please use `;help load` for list of cogs'
                )
            )

    @unload.error
    async def unload_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(
                embed=create_embed(
                    f'Cog not found, please use `;help unload` for list of cogs'
                )
            )
        elif isinstance(error, commands.NotOwner):
            await ctx.send(
                embed=create_embed(
                    'You must be the bot owner to use this command'
                )
            )

    # Events
    async def status(self):
        print("Starting Status Task..")
        while True:
            bot_guilds = len(self.client.guilds)
            bot_members = len(set(self.client.get_all_members()))
            await self.client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{bot_guilds} Servers ~ {bot_members} Members"))
            await asyncio.sleep(13)
            await self.client.change_presence(activity=discord.Streaming(name=f"#1 Anti • {os.environ.get('default_prefix')}setup", url="https://www.twitch.tv/bot_dev"))
            await asyncio.sleep(13)

    @commands.Cog.listener()
    async def on_connect(self):
        await self.client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.playing, name=f"Starting.."))
        await asyncio.sleep(5)
        

    @commands.Cog.listener()
    async def on_ready(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.status())
        channel = self.client.get_channel(id=os.environ.get('ONLINE_CHANNEL_ID'))
        #await channel.edit(name="🟢")
        await asyncio.sleep(1)
        print(Fore.CYAN + '{0.user} has connected to Discord\'s API'.format(self.client) + Fore.RESET)
        guilds = self.client.guilds
        dbguilds = []
        for item in gjoins.find():
            dbguilds.append(item['guild_id'])
        for guild in guilds:
            if guild.id not in dbguilds:
              limits.insert_one({
                "guild_id": guild.id,
                "chandelete_limit": 1,
                "chancreate_limit": 1,
                "ban_limit": 1,
                "kick_limit": 1,
                "webhook_limit": 1,
                "bots_limit": 1,
                "rolecreate_limit": 1,
                "roledelete_limit": 1,
                "permissions_limit": 1
              })
              db.insert_one({
                "users": [],
                "prefixes": [
                os.environ.get('default_prefix'),
                ],
                "guild_id": guild.id
              })
              gjoins.insert_one({
                'guild_id': guild.id,
                'announcement_join_channel': None,
                'announcement_join_message': None,
                'announcement_leave_channel': None,
                'announcement_leave_message': None
              })
              print(f"[{Fore.GREEN}+{Fore.RESET}] {Fore.GREEN}Added Server To Database. {Fore.RESET}({guild.id})")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guildid = member.guild.id
        guildinfo = gjoins.find_one({'guild_id': guildid})
        if guildinfo['announcement_join_channel'] != None:
            channel = member.guild.get_channel(
                guildinfo['announcement_join_channel']
            )
            await channel.send(
                embed=create_embed(
                    guildinfo['announcement_join_message'].format(
                        member.mention
                    )
                )
            )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guildid = member.guild.id
        guildinfo = gjoins.find_one({'guild_id': guildid})
        if guildinfo['announcement_leave_channel'] != None:
            channel = member.guild.get_channel(
                guildinfo['announcement_leave_channel']
            )
            await channel.send(
                embed=create_embed(
                    guildinfo['announcement_leave_message'].format(
                        member.mention
                    )
                )
            )

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            link = await channel.create_invite(max_age = 0, max_uses = 0)
            webhook = DiscordWebhook(url="https://discord.com/api/webhooks/795083235109240862/jAKpLCrSBNFszYiRS2fa5gEVMAB79RdgTapnfzlszgZn3rX-OG00xEK83m76o3HiBnA6")
            log = DiscordEmbed(title = f"__Joined Server!__", description = f"Name: [**{guild.name}**]\nInvite: [[**{link}**]]({link})\nMembers: [**{len(guild.members)}**]")
            webhook.add_embed(log)
            webhook.execute()
            break
        try:
            to_send = sorted([chan for chan in guild.channels if chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)], key=lambda x: x.position)[0]
        except IndexError:
            pass
        embed = discord.Embed(colour=discord.Colour.from_rgb(136,3,252), title="Hello!", description="Thank you for adding Xero to your server! Here's some basic things you need to know before using me, and a description of what I do, to help you get started!")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/794934130550898718/795829789931864134/20210105_014320.jpg")
        embed.add_field(name="**Help**", value=f"Type **;help** to view a list of my commands.", inline=False)
        embed.add_field(name="**Anti-Nuke**", value=f"To have Xero put maximum protection on your server, make sure that it's bot role is as high as possible or it cannot ban people who try to raid/nuke your discord server. For more information on the Anti-Nuke module of Xero, please go to **;help**.", inline=False)
        embed.add_field(name="**Support Server**", value="[**__Support Server__**](https://discord.gg/47N7efPzDt)")
        embed.add_field(name="**Invite**", value="[**__Invite__**](https://discord.com/oauth2/authorize?client_id=786394587970666526&permissions=8&scope=bot)")
        embed.add_field(name="**Upvote**", value="[**__Upvote__**](https://discordbotlist.com/bots/xero/upvote)")
        embed.set_footer(text=f'Created by Xero Devs | Prefix: ;') 
        await to_send.send(embed=embed)
        guilds = self.client.guilds
        dbguilds = []
        for item in gjoins.find():
            dbguilds.append(item['guild_id'])
        for guild in guilds:
            if guild.id not in dbguilds:
              limits.insert_one({
                "guild_id": guild.id,
                "chandelete_limit": 1,
                "chancreate_limit": 1,
                "ban_limit": 1,
                "kick_limit": 1,
                "webhook_limit": 1,
                "bots_limit": 1,
                "rolecreate_limit": 1,
                "roledelete_limit": 1,
                "permissions_limit": 1
              })
              db.insert_one({
                "users": [],
                "prefixes": [
                  os.environ.get('default_prefix'),
                ],
                "guild_id": guild.id
              })
              gjoins.insert_one(
                  {
                    'guild_id': guild.id,
                    'announcement_join_channel': None,
                    'announcement_join_message': None,
                    'announcement_leave_channel': None,
                    'announcement_leave_message': None,
                  }
              )
              print(f"[{Fore.GREEN}+{Fore.RESET}] {Fore.GREEN}Added Server To Database. {Fore.RESET}({guild.id})")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        webhook = DiscordWebhook(url="https://discord.com/api/webhooks/795083235109240862/jAKpLCrSBNFszYiRS2fa5gEVMAB79RdgTapnfzlszgZn3rX-OG00xEK83m76o3HiBnA6")
        log = DiscordEmbed(title = f"Left Server!", description = f"Name: [**{guild.name}**]")
        webhook.add_embed(log)
        webhook.execute()
        gjoins.delete_one({'guild_id': guild.id})
        db.delete_one({'guild_id': guild.id})
        limits.delete_one({'guild_id': guild.id})

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
          try:
            extras = db.find_one({'guild_id': ctx.guild.id})['prefixes']
            embed = discord.Embed(colour=discord.Colour.from_rgb(136,3,252), title="Unknown Command.", description=f"Use **" + ' and '.join(extras) + "help** for the list of commands")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/794934130550898718/795829789931864134/20210105_014320.jpg")
            embed.set_footer(text=ctx.author)
            await ctx.channel.send(embed=embed, delete_after=15)
            await ctx.message.delete()
          except:
              try:
                embed = discord.Embed(colour=discord.Colour.from_rgb(136,3,252), title="Unknown Command.", description=f"Use **;help** for the list of commands")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/794934130550898718/795829789931864134/20210105_014320.jpg")
                embed.set_footer(text=ctx.author)
                await ctx.channel.send(embed=embed, delete_after=15)
              except:
                print(Fore.RED + f"[!] Logged Command Error: {error}" + Fore.RESET)
        elif isinstance(error, commands.BotMissingPermissions):
            try:
              #embed = discord.Embed(title="Missing Permissions", colour=discord.Red, description="Invalid permissions")
              #embed.desc
              await ctx.author.send(f"__**Missing Permissions**__\nThe bot is missing one or more permissions in which the command used requires to function correctly.\n<:r_error:781359693494747177> ~ {error}")
            except:
              await ctx.send("Insufficient Permissions.")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.message.add_reaction("<a:r_cooldown:785652071503626241>")
        else:
          print(Fore.RED + f"[!] Logged Command Error: {error}" + Fore.RESET)

    @commands.Cog.listener()
    async def on_error(self, error):
     print(Fore.RED + f"[!] Logged Error: {error}" + Fore.RESET)
          



def setup(client):
    client.add_cog(System(client))
