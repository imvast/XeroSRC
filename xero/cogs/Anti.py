# IMPORTS #
import discord, os, pymongo, datetime
from colorama import Fore
from discord.ext import commands

# MongoDB Setup
mongoClient = pymongo.MongoClient(os.environ.get('BOT_DB'))
db = mongoClient.get_database("XeroBOT").get_collection("servers+id")
db2 = mongoClient['XeroBOT']
limits = db2['limits']
gjoins = db2['gannouncements']
blacklist = db2['blacklist']

class Anti(commands.Cog):
    def __init__(self, client, db):
        self.client = client
        self.db = db


    # anti mass-channel-deletion
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        limit = limits.find_one({ "guild_id": channel.guild.id })['chandelete_limit']
        whitelistedUsers = self.db.find_one({ "guild_id": channel.guild.id })["users"]
        async for i in channel.guild.audit_logs(limit=limit, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.channel_delete):
            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return
            else:
              try:
                await i.user.ban(reason="Xero Anti • Trigger: Channel Deletion")
                return
              except:
                 print(f"{Fore.RED}[Anti Error]: Deleted Channel. ({channel.guild.name}){Fore.RESET}") 

    # anti mass-channel
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        limit = limits.find_one({ "guild_id": channel.guild.id })['chancreate_limit']
        whitelistedUsers = self.db.find_one({ "guild_id": channel.guild.id })["users"]
        async for i in channel.guild.audit_logs(limit=limit, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.channel_create):
            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return
            else:
              try:
                await i.user.ban(reason="Xero Anti • Trigger: Channel Creation")
                return
                await channel.delete()
              except:
                 print(f"{Fore.RED}[Anti Error]: Created Channel. ({channel.guild.name}){Fore.RESET}") 

    # anti ban
    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
      limit = limits.find_one({ "guild_id": member.guild.id })['ban_limit']
      whitelistedUsers = self.db.find_one({ "guild_id": member.guild.id })["users"]
      logs = await guild.audit_logs(limit=limit, action=discord.AuditLogAction.ban).flatten()
      logs = logs[0]
      if logs.user.id in whitelistedUsers or logs.user in whitelistedUsers: 
        return
      else:
        try:
          await logs.user.ban(reason="Xero Anti • Trigger: Banning Members")
          return
        except:
          print(f"{Fore.RED}[Anti Error]: Banned Member. ({guild.name}){Fore.RESET}") 

    # anti kick
    @commands.Cog.listener()
    async def on_member_remove(self, member):
      limit = limits.find_one({ "guild_id": member.guild.id })['kick_limit']
      whitelistedUsers = self.db.find_one({ "guild_id": member.guild.id })["users"]
      async for i in member.guild.audit_logs(limit=limit, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.kick):
          if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
            return
          else:
            try:
              await i.user.ban(reason="Xero Anti • Trigger: Kicking Members")
              return
            except:
             print(f"{Fore.RED}[Anti Error]: Kicked Member. ({member.guild.name}){Fore.RESET}") 

    # anti webhook
    @commands.Cog.listener()
    async def on_webhooks_update(self, channel):
        limit = limits.find_one({ "guild_id": channel.guild.id })['webhook_limit']
        whitelistedUsers = self.db.find_one({ "guild_id": channel.guild.id })["users"]
        async for i in channel.guild.audit_logs(limit=limit, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.webhook_create):
            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return
            else:
              try:
                await i.user.ban(reason="Xero Anti • Trigger: Webhook Creation")
                await i.target.delete()
                return
              except:
                print(f"{Fore.RED}[Anti Error]: Created Webhook. ({channel.guild.name}){Fore.RESET}") 

    # anti bot
    @commands.Cog.listener()
    async def on_member_join(self, member):
        limit = limits.find_one({ "guild_id": member.guild.id })['bots_limit']
        whitelistedUsers = self.db.find_one({ "guild_id": member.guild.id })["users"]
        if member.bot:
            async for i in member.guild.audit_logs(limit=limit, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.bot_add):
                if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                    return
                else:
                  try:
                    await member.ban(reason="Xero Anti • Trigger: Anti-Bot")
                    await i.user.ban(reason="Xero Anti • Trigger: Adding Bots")
                  except:
                    print(f"{Fore.RED}[Anti Error]: Added Bot. ({member.guild.name}){Fore.RESET}")

    # anti mass-role
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        limit = limits.find_one({ "guild_id": role.guild.id })['rolecreate_limit']
        whitelistedUsers = self.db.find_one({ "guild_id": role.guild.id })["users"]
        async for i in role.guild.audit_logs(limit=limit, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.role_create):
            if i.user.bot:
                return
            elif i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return
            else:
              try:
                await role.guild.ban(i.user, reason="Xero Anti • Trigger: Role Creation")
                return
              except:
                print(f"{Fore.RED}[Anti Error]: Role-Creation. ({role.guild.name}){Fore.RESET}")

    # anti mass-role-deletion
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        limit = limits.find_one({ "guild_id": role.guild.id })['roledelete_limit']
        whitelistedUsers = self.db.find_one({ "guild_id": role.guild.id })["users"]
        async for i in role.guild.audit_logs(limit=limit, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.role_delete):
            if i.user.bot:
                return
            elif i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return
            else:
              try:
                await role.guild.ban(i.user, reason="Xero Anti • Trigger: Role Deletion")
                return
              except:
                print(f"{Fore.RED}[Anti Error]: Role-Deletion. ({role.guild.name}){Fore.RESET}")

    # anti permissions
    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        limit = limits.find_one({ "guild_id": after.guild.id })['permissions_limit']
        whitelistedUsers = self.db.find_one({ "guild_id": after.guild.id })["users"]
        async for i in after.guild.audit_logs(limit=limit, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.role_update):
            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return

            if not before.permissions.ban_members and after.permissions.ban_members:
                await after.guild.ban(i.user, reason="Xero Anti • Trigger: Added Unsafe Permissions To A Role")
                return

            if not before.permissions.kick_members and after.permissions.kick_members:
                await after.guild.ban(i.user, reason="Xero Anti • Trigger: Added Unsafe Permissions To A Role")
                return

            if not before.permissions.administrator and after.permissions.administrator:
                await after.guild.ban(i.user, reason="Xero Anti • Trigger: Added Unsafe Permissions To A Role")
                return

            if i.target.id == before.guild.id:
                if after.permissions.kick_members or after.permissions.ban_members or after.permissions.administrator or after.permissions.mention_everyone or after.permissions.manage_roles:
                  try:
                    await after.guild.ban(i.user, reason="Xero Anti • Trigger: Added Unsafe Permissions To A Role")
                    await after.edit(permissions=1166401)
                  except:
                    print(f"{Fore.RED}[Anti Error]: Kick_Ban_Admin_Mention_Roles ({after.guild.name}){Fore.RESET}")
                    
            return

# anti link

# soon..




def setup(client):
    client.add_cog(Anti(client))