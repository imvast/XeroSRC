import discord, pymongo, os
from settings import *
from discord.ext import commands
from discord.utils import get

# Connect to mongodb database
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
            return ctx.send("You are blacklisted. <:sad:796769105352589353>")
        return True
    return commands.check(predicate)

class Help(commands.Cog):
    def __init__(self, client, db):
        self.client = client
        self.db = db
        

    @commands.group(
        name='help',
        description='The help command.',
        invoke_without_command=True,
        case_insensitive=True,
        aliases=['h', 'cmds', 'commands']
    )
    @blacklist_check()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
          if ctx.guild is None:
            await ctx.send("To see my commands, invite me to your server!")
          else:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(136,3,252),
                description='For a more detailed description of commands, DM a high rank in Support\nFor more information about me, type: `;botinfo`',
                timestamp=ctx.message.created_at
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_author(
                name='Xero Commands\n',
                icon_url=ctx.author.avatar_url
            )
            embed.add_field(
                name='🛡️ Anti-Nuke',
                value="`setup`, `unbanall`, `whitelist/unwhitelist`, `whitelisted`, `settings`, `limits`",
                inline=False
            )
            embed.add_field(
                name='<:Info:782692301037240332> Info',
                value='`invite`, `udinfo`, `botinfo`, `serverinfo`, `userinfo`, `snipe`',
                inline=False
            )
            embed.add_field(
                name='<a:NeonDiscordStaff:767061505279262740> Moderation',
                value='`ban/idban/unban`, `kick`, `mute/unmute`, `nuke`, `purge`, `lock/unlock`, `slowmode`, `addrole/remrole`',
                inline=False
            )
            #extras = db.find_one({'guild_id': ctx.guild.id})['prefixes']
            embed.set_footer(
                text='Server Prefix: ;'# + ' and '.join(extras)
            )
            await ctx.send(embed=embed)


    @help.command(
        name='Anti',
        aliases=['antinuke'],
        description='Shows list of Anti features',
    )
    @blacklist_check()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def help_anti(self, ctx):
        if ctx.invoked_subcommand is None:
          if ctx.guild is None:
            await ctx.send("To see my commands, invite me to your server!")
          else:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(136,3,252),
                description='➣ Anti-Ban\n➣ Anti-Kick\n➣ Anti-Channel-Creation\n➣ Anti-Channel-Deletion\n➣ Anti-Role-Creation\n➣ Anti-Role-Deletion\n➣ Anti-Bot\n➣ Anti-Webhook\n➣ Anti-Permissions • Works but doesn\'t reset perms.'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_author(
                name='Xero Anti Features\n',
                icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)

    @help.command(
        name='Settings',
        aliases=['limits'],
        description='Shows info about settings',
    )
    @blacklist_check()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def help_settings(self, ctx):
      embed = discord.Embed(colour=discord.Colour.from_rgb(136,3,252), title="Getting Started with Xero's Anti Settings and Limits")
      embed.add_field(
        name="Limits",
        value="To use Xero's anti settings and limits features, visit `;settings` and it gives you a view of your servers current anti settings. For more information on the types of settings, visit: `;help anti` and for more information on the types of limits, visit: `;limits`"
      )
      await ctx.send(embed=embed)





def setup(client):
    client.add_cog(Help(client))