import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import typing
import atexit
import copy

# ----------------
session: aiohttp.ClientSession | None = None
load_dotenv()

# -------- Bot Setup --------
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

GUILD_ID = int(os.getenv("GUILD_ID", "1299000909363155024"))
API_KEY = os.getenv("API_KEY")
API_BASE = "https://api.policeroleplay.community/v1/server"
ROBLOX_USER_API = "https://users.roblox.com/v1/users"
server_name = "test"
staff_role_id = int(os.getenv("STAFF_ROLE_ID", "1316076193459474525"))
join_link = "https://policeroleplay.community/join?code=&placeId=2534724415"

# Groups
erlc_group = app_commands.Group(name="erlc", description="ERLC related commands")
discord_group = app_commands.Group(name="discord", description="Discord-related commands")
bot.tree.add_command(erlc_group)
bot.tree.add_command(discord_group)

# ---------------- Session Helper ----------------
async def get_session():
    global session
    if session is None or session.closed:
        session = aiohttp.ClientSession()
    return session

# ---------------- Utility ----------------
def apply_footer(embed, guild):
    if guild and guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.set_footer(text=server_name)
    return embed

def roblox_link(player_str: str):
    try:
        name, user_id = player_str.split(":")
        return f"[{name}](https://www.roblox.com/users/{user_id}/profile)"
    except:
        return player_str

def error_embed(title: str, description: str, guild: discord.Guild = None):
    embed = discord.Embed(title=title, description=description, color=discord.Color.red())
    return apply_footer(embed, guild)

def success_embed(title: str, description: str, guild: discord.Guild = None):
    embed = discord.Embed(title=title, description=description, color=discord.Color.green())
    return apply_footer(embed, guild)

# ---------------- Global Checks ----------------
@bot.check
async def global_checks(ctx):
    # Prevent DMs
    if not ctx.guild:
        await ctx.send(embed=error_embed("❌ Command not available in DMs.", "Please use commands in a server."))
        return False
    # All commands except erlc info and user are staff-only
    if ctx.command.name in ("info", "user"):
        return True
    member = ctx.author
    if any(role.id == staff_role_id for role in member.roles):
        return True
    await ctx.send(embed=error_embed("❌ Permission Denied", "You must be a staff member to use this command.", ctx.guild))
    return False

# Slash commands check
async def slash_staff_check(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message(embed=error_embed("❌ Command not available in DMs.", "Please use commands in a server."), ephemeral=True)
        return False
    if interaction.command.name in ("info", "user"):
        return True
    member = interaction.user
    guild_member = interaction.guild.get_member(member.id)
    if not guild_member:
        guild_member = await interaction.guild.fetch_member(member.id)
    if any(role.id == staff_role_id for role in guild_member.roles):
        return True
    await interaction.response.send_message(embed=error_embed("❌ Permission Denied", "You must be a staff member to use this command.", interaction.guild), ephemeral=True)
    return False

# ---------------- Roblox Helpers ----------------
async def get_roblox_usernames(ids: list[int]) -> dict[int, str]:
    usernames = {}
    async with aiohttp.ClientSession() as session:
        for user_id in ids:
            async with session.get(f"{ROBLOX_USER_API}/{user_id}") as res:
                if res.status == 200:
                    data = await res.json()
                    usernames[user_id] = data.get("name", f"ID:{user_id}")
                else:
                    usernames[user_id] = f"ID:{user_id}"
    return usernames

async def fetch_players():
    session = await get_session()
    headers = {"server-key": API_KEY}
    async with session.get(f"{API_BASE}/players", headers=headers) as resp:
        return await resp.json() if resp.status == 200 else []

# ---------------- InfoView ----------------
class InfoView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, embed_callback):
        super().__init__(timeout=180)
        self.interaction = interaction
        self.embed_callback = embed_callback

        self.add_item(discord.ui.Button(
            label="Join Server",
            style=discord.ButtonStyle.link,
            url=join_link
        ))

    @discord.ui.button(label="Refresh", style=discord.ButtonStyle.blurple)
    async def refresh(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.interaction.user.id:
            await interaction.response.send_message(embed=error_embed("❌", "You can't use this button.", interaction.guild), ephemeral=True)
            return
        embed = await self.embed_callback()
        await interaction.response.edit_message(embed=embed)

# ---------------- ERLC Info Embed ----------------
async def create_server_info_embed(interaction: discord.Interaction) -> discord.Embed:
    session = await get_session()
    headers = {"server-key": API_KEY, "Accept": "*/*"}
    async with session.get(f"{API_BASE}", headers=headers) as res:
        server = await res.json()
    async with session.get(f"{API_BASE}/players", headers=headers) as res:
        players = await res.json()
    async with session.get(f"{API_BASE}/queue", headers=headers) as res:
        queue = await res.json()

    owner_id = server["OwnerId"]
    co_owner_ids = server.get("CoOwnerIds", [])
    usernames = await get_roblox_usernames([owner_id] + co_owner_ids)

    mods = [p for p in players if p.get("Permission") == "Server Moderator"]
    admins = [p for p in players if p.get("Permission") == "Server Administrator"]
    staff = [p for p in players if p.get("Permission") != "Normal"]

    embed = discord.Embed(
        title=f"{server_name} - Server Info",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="Basic Info",
        value=(f"> **Join Code:** [{server['JoinKey']}](https://policeroleplay.community/join/{server['JoinKey']})\n"
               f"> **Players:** {server['CurrentPlayers']}/{server['MaxPlayers']}\n"
               f"> **Queue:** {len(queue)}"),
        inline=False
    )
    embed.add_field(
        name="Staff Info",
        value=(f"> **Moderators:** {len(mods)}\n"
               f"> **Administrators:** {len(admins)}\n"
               f"> **Staff in Server:** {len(staff)}"),
        inline=False
    )
    embed.add_field(
        name=f"Server Ownership",
        value=(f"> **Owner:** [{usernames[owner_id]}](https://roblox.com/users/{owner_id}/profile)\n"
               f"> **Co-Owners:** {', '.join([f'[{usernames[uid]}](https://roblox.com/users/{uid}/profile)' for uid in co_owner_ids]) or 'None'}"),
        inline=False
    )

    return apply_footer(embed, interaction.guild)

# ---------------- Commands ----------------
# /erlc info (all users)
@erlc_group.command(name="info", description="Get ER:LC server info (all users)")
async def erlc_info(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message(embed=error_embed("❌ Not in a guild", "This command does not work in DMs."), ephemeral=True)
        return
    await interaction.response.defer()
    try:
        embed = await create_server_info_embed(interaction)
        view = InfoView(interaction, lambda: create_server_info_embed(interaction))
        await interaction.followup.send(embed=embed, view=view)
    except Exception as e:
        await interaction.followup.send(embed=error_embed("Error", f"Failed to fetch server info.\n{e}", interaction.guild))

# /user (all users)
@tree.command(name="user", description="Get Roblox user info")
@app_commands.describe(user_id="The Roblox user ID to fetch info for")
async def roblox_user_info(interaction: discord.Interaction, user_id: str):
    if not interaction.guild:
        await interaction.response.send_message(embed=error_embed("❌ Not in a guild", "This command does not work in DMs."), ephemeral=True)
        return
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://users.roblox.com/v1/users/{user_id}") as resp:
            if resp.status != 200:
                await interaction.followup.send(embed=error_embed("Error", f"Failed to fetch Roblox user. Status: {resp.status}", interaction.guild))
                return
            user_data = await resp.json()
    embed = discord.Embed(title="👤 Roblox User Info", color=discord.Color.blurple())
    embed.add_field(name="Username", value=user_data.get("name", "Unknown"), inline=True)
    embed.add_field(name="Display Name", value=user_data.get("displayName", "Unknown"), inline=True)
    embed.add_field(name="User ID", value=str(user_data.get("id", "Unknown")), inline=True)
    embed.add_field(name="Description", value=user_data.get("description", "None"), inline=False)
    embed.set_footer(text=server_name)
    await interaction.followup.send(embed=embed)

# TODO: Add other staff-only commands here (vehicles, players, callsigns, modcalls, killlogs, bans, etc.)
# Make sure to wrap each slash and prefix command with the slash_staff_check() for permission
# Example:
# @erlc_group.command(name="players", description="See all players in the server")
# @app_commands.check(slash_staff_check)
# async def erlc_players(...): ...

# ---------------- Bot Events ----------------
@bot.event
async def on_ready():
    try:
        if not getattr(bot, "synced", False):
            await bot.tree.sync()
            bot.synced = True
    except Exception as e:
        print(f"Failed to sync commands: {e}")

    bot.start_time = datetime.now(timezone.utc)
    await get_session()

    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(type=discord.ActivityType.watching, name="over the server")
    )
    print(f"{bot.user} is ready and watching over the server.")
    print("------------------------------------------------------------------")

# ---------------- Exit Handler ----------------
@atexit.register
def close_session():
    if session and not session.closed:
        asyncio.run(session.close())

# ---------------- Run Bot ----------------
bot.run(os.getenv("DISCORD_TOKEN"))
