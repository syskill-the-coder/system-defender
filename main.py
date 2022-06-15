print("Loading modules...")
import discord
from discord.ext import commands, tasks
from colorama import Fore, init
import sys
import pickle
import os
import random
from discord import Permissions
import traceback
from tkinter import messagebox
print("Loading asyncio...")
import asyncio
print("Defining variables,classes and functions...")
version = "SysDef DEV 0.0"
token = "TOKEN HERE"
if token == "TOKEN HERE":
  print("Enter a valid token please...")
  messagebox.showerror("Error", "Please enter a valid token in the code.")
  exit(1)
channeltoggle = True


txt_icon = """
 .d8888b.                 888                         
d88P  Y88b                888                         
Y88b.                     888                         
 "Y888b.  888  888.d8888b 888888 .d88b. 88888b.d88b.  
    "Y88b.888  88888K     888   d8P  Y8b888 "888 "88b 
      "888888  888"Y8888b.888   88888888888  888  888 
Y88b  d88PY88b 888     X88Y88b. Y8b.    888  888  888 
 "Y8888P"  "Y88888 88888P' "Y888 "Y8888 888  888  888 
               888                                    
          Y8b d88P                                    
           "Y88P"                                     

8888888b.          .d888                     888                
888  "Y88b        d88P"                      888                
888    888        888                        888                
888    888 .d88b. 888888 .d88b. 88888b.  .d88888 .d88b. 888d888 
888    888d8P  Y8b888   d8P  Y8b888 "88bd88" 888d8P  Y8b888P"   
888    88888888888888   88888888888  888888  88888888888888     
888  .d88PY8b.    888   Y8b.    888  888Y88b 888Y8b.    888     
8888888P"  "Y8888 888    "Y8888 888  888 "Y88888 "Y8888 888     
"""


try:
    savefile = open("prefixes.pypickle", "rb")
except:
    savefile = open("prefixes.pypickle", "wb")
    savefile.close()
    del savefile
    savefile = open("prefixes.pypickle", "rb")
custom_prefixes = pickle.load(savefile)

#You'd need to have some sort of persistance here,
#possibly using the json module to save and load
#or a database


default_prefixes = ['&']

async def determine_prefix(bot, message):
    guild = message.guild
    if guild:
        return custom_prefixes.get(guild.id, default_prefixes)
    else:
        return default_prefixes

bot = commands.Bot(command_prefix = determine_prefix)


@bot.command()
@commands.has_permissions(administrator=True)
@commands.guild_only()
async def setprefix(ctx, *, prefix="?"):
    custom_prefixes[ctx.guild.id] = prefix.split() or default_prefixes
    with open("savefile.pypickle", "wb") as savefile:
        pickle.dump(custom_prefixes, savefile)
    await ctx.send(f"Prefix set to `{prefix}` ")




class MyHelp(commands.HelpCommand):
    def get_command_signature(self, command):
        return '**-----------------------------------------**\n' \
               '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title=f"Help for {version}")
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "Commands:")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title="Error", description=str(error))
            await ctx.send(embed=embed)
        else:
            raise error

    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=error)
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command))
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)




bot.help_command = MyHelp()
init(convert=True)

@bot.event
async def on_ready():
    print(f"{Fore.GREEN} {txt_icon}\n"
          f"Is online.")
    await bot.change_presence(activity=discord.Game(name="?help"), status=discord.Status.do_not_disturb)


@bot.event
async def on_guild_channel_create(channel):
    embed = discord.Embed(title="Server :white_check_mark:", description="This server is protected by\n"
                                                      "System Defender, made by The_SysKill.\n"
                                                      "To toggle these messages, type ?channel_toggle.")
    if channeltoggle:
        await channel.send(embed=embed)

@bot.event
async def on_guild_join(guild):
    print(f"{Fore.GREEN}Joined guild {guild.name}.")

@bot.event
async def on_guild_remove(guild):
    print(f"{Fore.RED}Left guild {guild.name}")

@bot.event
async def on_member_ban(guild,member):
    print(f"{Fore.RED}{member.name}#{member.discriminator} was banned from {guild.name}.")

@bot.event
async def on_member_unban(guild, member):
    print(f"{Fore.GREEN}{member.name}#{member.discriminator} was unbanned from {guild.name}.")

@bot.event
async def on_member_join(member):
    print(f"{Fore.GREEN}{member.name}#{member.discriminator} Joined a mutual guild.")

@bot.event
async def on_member_remove(member):
    print(f"{Fore.RED}{member.name}#{member.discriminator} Left a mutual guild")

@bot.command(help="Toggles the messages when new channels are created")
async def channel_toggle(ctx):
    global channeltoggle
    channeltoggle = not channeltoggle
    await ctx.send(embed=discord.Embed(title="Toggle", description=f"New channel messages is now set to {channeltoggle}"))

@bot.command()
async def shutup(ctx):
  if str(ctx.message.author) == "†hê_§¥§Kïll#1878":
    await ctx.send("Ok, imma stfu")
    await bot.change_presence(status=discord.Status.offline)
    await bot.logout()
@bot.command()
async def msg(ctx, target:discord.Member, *, message):
    dm = await target.create_dm()
    embed = discord.Embed(title="Message", description=f"You received a message from guild {ctx.guild.name},\n"
                                                       f"This was sent by <@!{ctx.message.author.id}>.", color=0xffff00)
    embed.add_field(name="Message:", value=message.replace("\\n", "\n"))
    try:
        if message == "DevError":
            assert 1 == 2
        await dm.send(embed=embed)
    except:
        embed = discord.Embed(title="Error",description=f"Failed to dm {target.display_name}." ,color=0xff0000)

        await ctx.send(embed=embed)
@msg.error
async def error(ctx, error):
    if isinstance(error, discord.ext.commands.MemberNotFound):
        await ctx.send(embed=discord.Embed(title="Message", description="I could not find that user.", color=0xff000f))

@bot.command()
async def is_mobile(ctx, target:discord.Member):
    if target.is_on_mobile():
        await ctx.send("True")
    else:
        await ctx.send("False")



@bot.command()
async def role_higher_than(ctx, target:discord.Member, silent = False):
    if max(ctx.message.author.roles) > max(target.roles):
        if not silent:
            await ctx.send(f"You have more hierarchy than {target.display_name}.")
        return True
    else:
        if not silent:
            await ctx.send(f"You have less or equal hierarchy than {target.display_name}.")
        return False

@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
   await member.remove_roles(mutedRole)
   await ctx.send(f"Unmuted {member.display_name}")


@bot.command(description="Mutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
   await member.add_roles(mutedRole)
   await ctx.send(f"Muted {member.display_name}")


@bot.command()
async def dev_error(ctx):
    assert 5 > 6

@bot.event
async def on_message(message):
    if "REACT TO THIS MESSAGE" in message.content.upper():
        await message.add_reaction("👍")
    await bot.process_commands(message)



custom_prefixes = {}

#You'd need to have some sort of persistance here,
#possibly using the json module to save and load
#or a database


default_prefixes = ['&']

async def determine_prefix(bot, message):
    guild = message.guild
    if guild:
        return custom_prefixes.get(guild.id, default_prefixes)
    else:
        return default_prefixes



@bot.command()
@commands.has_permissions(administrator=True)
@commands.guild_only()
async def setprefix(ctx, *, prefixes=""):
    custom_prefixes[ctx.guild.id] = prefixes.split() or default_prefixes
    await ctx.send(f"Prefixes set to `{prefixes}` ")


bot.run(token)
