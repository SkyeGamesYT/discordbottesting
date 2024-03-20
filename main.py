import asyncio
import datetime
import pytz
import requests
from discord.ext import commands
import sqlite3
from key_generator.key_generator import generate
import discord
from keep_alive import keep_alive


connection = sqlite3.connect("database.db")
print(connection.total_changes)
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS warningsdatabase2 (user_id INTEGER, moderator TEXT, reason TEXT, warn_id TEXT)")
connection.commit()

client = commands.Bot(
    command_prefix='$',
    intents=discord.Intents.all()
)

@client.event
async def on_ready():
    client.remove_command('help')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="skye's hideout"))
    print('Bot is ready!')


@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def slap(ctx, member:discord.User):
  if ctx.author.id >= 0:
    await ctx.send(f"{ctx.message.author.mention} slaps {member.mention}!") 








  
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason = None):
    await member.send(f"You were banned from {ctx.guild} for {reason} by {ctx.author}")
    await member.ban(reason = reason)
    embedVar = discord.Embed(title="Banned User", description=f"{member} was banned by {ctx.author} for {reason}", color=00000)
    await ctx.send(embed=embedVar)








@client.command()
async def echo(ctx, *,args):
    if ctx.author.id >= 0:
        await ctx.send(args)







@client.command(name='unban')
@commands.has_permissions(ban_members=True)
async def _unban(ctx, id: int, *, reason = None):
    user = await client.fetch_user(id)
    await ctx.guild.unban(user, reason = reason)
    embedVar = discord.Embed(title="Unbanned User", description=f"{user} was unbanned by {ctx.author} for {reason}", color=0x00ff00)
    await ctx.send(embed=embedVar)







@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, reason = None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")  # Assuming you have a role named "Muted"

    if not role:
        # The "Muted" role does not exist, so create it
        role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            # Disallow the "Muted" role to send messages in all channels
            await channel.set_permissions(role, send_messages=False)

    await member.add_roles(role)
    embedVar = discord.Embed(title="User Muted", description=f"{member} was muted by {ctx.author} for {reason}", color=0x00ff00)
    await ctx.send(embed=embedVar)



@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a member to mute.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    else:
        await ctx.send("An error occurred while executing this command.")






@client.command()
@commands.has_permissions(manage_roles=True)
async def warn(ctx, id: int, reason=None):
  conn = sqlite3.connect('database.db')
  cursor = conn.cursor()
  moderator = str(ctx.author.name)
  member = await client.fetch_user(id)
  print(member)
  key = generate()
  warnid = key.get_key()
  print(warnid)
  cursor.execute("INSERT INTO warningsdatabase2 VALUES (?, ?, ?, ?)", (id, moderator, reason, warnid))
  conn.commit()
  embedVar = discord.Embed(title="User Warned", description=f"{member} has been warned by {moderator} for {reason}", color=)
  await ctx.send(embed=embedVar)
  
  






  
@client.command()
@commands.has_permissions(manage_roles=True)
async def warnings(ctx, id: int):
  conn = sqlite3.connect('database.db')
  cursor = conn.cursor()
  member = ctx.guild.get_member(id)
  cursor.execute("SELECT * FROM warningsdatabase2 WHERE user_id = ?", (id,))
  result = cursor.fetchall()

  if result:
      embedVar = discord.Embed(title=f"Warnings for {member}", description="Warnings", color=0x00ff00)
      for row in result:
        moduser = row[1]  # Extract moderator from each row
        warningNumber = row[3]  # Extract warning number from each row
        embedVar.add_field(name=f"Moderator: {moduser}", value=f"Reason: {row[2]}, Warning Number: {warningNumber}", inline=False)
      await ctx.send(embed=embedVar)
  else:
    await ctx.send("No warnings found for the member.")

    conn.close()  # Close the database connection after using it



@client.command()
async def show_tables(ctx):
  conn = sqlite3.connect('database.db')
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM warningsdatabase2")
  table = cursor.fetchall()
  print(table)


@client.command(name="delwarn")
@commands.has_permissions(manage_roles=True)
async def delwarn(ctx, id: int, warnNumb: str):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    member = ctx.guild.get_member(id)

    if member:
        cursor.execute("select warn_id FROM warningsdatabase2 WHERE user_id = ?", (id,))
        warnings = cursor.fetchall()
        print("warnings:", warnings)  # add this line for debugging
        found = False
        for warning in warnings:
            print("warning id:", warning)  # add this line for debugging
            if warnNumb == warning[0]:
                cursor.execute(f"DELETE FROM warningsdatabase2 WHERE warn_id = ?", (warnNumb,))
                conn.commit()
                embed_var = discord.Embed(title="Warning Deleted", description=f"Warning #{warnNumb} was deleted by {ctx.author}")
                await ctx.send(embed=embed_var)
                found = True
                break
        if not found:
            await ctx.send("Warning number not found.")
    else:
        await ctx.send("Member not found.")


@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member, reason =  None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")  # Assuming you have a role named "muted"

    if role in member.roles:
        await member.remove_roles(role)
        embedVar = discord.Embed(title="User Unmuted", description=f"{member} was unmuted by {ctx.author} for {reason}", color=0x00ff00)
        await ctx.send(embed=embedVar)
    else:
        await ctx.send(f"{member.mention} is not muted.")





@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a member to unmute.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    else:
        await ctx.send("An error occurred while executing this command.")







keep_alive.keep_alive()
client.run( ${{ secrets.TOKEN }} )
connection.close()
