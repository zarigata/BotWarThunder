"""
.__________________.
|                  |
|  F3V3R DR34M     |
|  W4R THUND3R     |
|  TR4CK3R v1.0    |
|                  |
|  [2025 RUL3Z!]   |
|__________________|

CR3D1TZ:
- C0D3D BY: F3V3R DR34M T34M
- GR33TZ: ALL WAR THUNDER PLAYERS!
"""

import discord
from discord.ext import commands
from discord import app_commands
import json
import pandas as pd
from datetime import datetime
import os
from tabulate import tabulate
import platform
from typing import Literal

# Initialize our bot with all intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

# Global variables to store match data
active_matches = {}
HISTORY_FILE = 'match_history.json'

def load_match_history():
    """
    [*] L04D1NG M4TCH H1ST0RY...
    """
    if not os.path.exists(HISTORY_FILE):
        return {"matches": []}
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"matches": []}

def save_match_history(match_data):
    """
    [*] S4V1NG M4TCH H1ST0RY...
    """
    history = load_match_history()
    history["matches"].append({
        **match_data,
        "timestamp": datetime.now().isoformat()
    })
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def normalize_result(result: str) -> str:
    """
    [*] N0RM4L1Z1NG R3SULT...
    """
    result = result.lower().strip()
    win_options = ['w', 'v', '1', 'win', 'victory']
    loss_options = ['l', 'd', '0', 'loss', 'defeat']
    
    if result in win_options:
        return 'WIN'
    elif result in loss_options:
        return 'LOSS'
    else:
        return None

class MatchTracker:
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.matches = []
        self.start_time = datetime.now()
        self.win_streak = 0
        self.best_streak = 0
        self.current_embed = None

    def add_match(self, squadron, tanks, planes, helicopters, result):
        match = {
            'squadron': squadron,
            'tanks': tanks,
            'planes': planes,
            'helicopters': helicopters,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
        self.matches.append(match)
        save_match_history(match)
        
        if result == 'WIN':
            self.win_streak += 1
            self.best_streak = max(self.best_streak, self.win_streak)
        else:
            self.win_streak = 0

    def get_stats(self):
        total_matches = len(self.matches)
        if total_matches == 0:
            return "No matches recorded"
            
        wins = sum(1 for match in self.matches if match['result'] == 'WIN')
        win_rate = (wins / total_matches) * 100
        
        return {
            'total_matches': total_matches,
            'wins': wins,
            'losses': total_matches - wins,
            'win_rate': win_rate,
            'best_streak': self.best_streak
        }

@bot.event
async def on_ready():
    """
    [*] B0T 1N1T14L1Z3D SUCC3SSFULLY!
    [*] H4CK TH3 PL4N3T!
    """
    print(f'''
    ╔══════════════════════════════╗
    ║  W4R THUND3R TR4CK3R L04D3D  ║
    ║  SYST3M: {platform.system()}  
    ║  B0T: {bot.user.name}        
    ║  ST4TUS: 0NL1N3              ║
    ╚══════════════════════════════╝
    ''')
    try:
        synced = await bot.tree.sync()
        print(f"[*] SYNCED {len(synced)} commands!")
    except Exception as e:
        print(f"[!] ERR0R: {str(e)}")

@bot.tree.command(name="comecar", description="Start tracking a new match session")
async def comecar(interaction: discord.Interaction):
    """
    [*] 1N1T14L1Z1NG N3W M4TCH S3SS10N...
    """
    if interaction.channel_id in active_matches:
        await interaction.response.send_message("❌ There's already an active session in this channel!", ephemeral=True)
        return

    # Get users in voice channel
    voice_channel = interaction.user.voice.channel if interaction.user.voice else None
    squad_members = ""
    
    if voice_channel:
        users_in_vc = "\n".join([member.display_name for member in voice_channel.members])
        squad_members = f"```{users_in_vc}```"
    else:
        squad_members = "```No squad members in voice channel```"

    active_matches[interaction.channel_id] = MatchTracker(interaction.channel_id)
    
    embed = discord.Embed(
        title="🎮 War Thunder Match Tracking Session",
        description="Session started! Use /rg to register matches and /final to end the session.",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="Squad Members", value=squad_members, inline=False)
    
    await interaction.response.send_message(embed=embed)
    active_matches[interaction.channel_id].current_embed = await interaction.channel.send(embed=embed)

@bot.tree.command(name="rg", description="Register a match result (w/l, v/d, 1/0)")
async def rg(
    interaction: discord.Interaction,
    squadron: str,
    result: str,
    tanks: int,
    planes: int = 0,
    helicopters: int = 0
):
    """
    [*] R3G1ST3R1NG M4TCH R3SULT...
    """
    if interaction.channel_id not in active_matches:
        await interaction.response.send_message("❌ No active tracking session! Use /comecar first!", ephemeral=True)
        return

    # Normalize the result
    normalized_result = normalize_result(result)
    if normalized_result is None:
        await interaction.response.send_message(
            "❌ Invalid result! Please use:\n" + 
            "- Win: w, v, 1, win, victory\n" +
            "- Loss: l, d, 0, loss, defeat",
            ephemeral=True
        )
        return

    tracker = active_matches[interaction.channel_id]
    tracker.add_match(squadron, tanks, planes, helicopters, normalized_result)

    # Update embed with new match data
    embed = discord.Embed(
        title="ち🎮 War Thunder Match Tracking Session ",
        description="Current session statistics:",
        color=discord.Color.green() if normalized_result == 'WIN' else discord.Color.red()
    )

    # Format match history
    match_history = ""
    for idx, match in enumerate(tracker.matches, 1):
        result_emoji = "🟢" if match['result'] == 'WIN' else "🔴"
        vehicles = []
        if match['tanks'] > 0:
            vehicles.append(f"{match['tanks']} tanks")
        if match['planes'] > 0:
            vehicles.append(f"{match['planes']} planes")
        if match['helicopters'] > 0:
            vehicles.append(f"{match['helicopters']} helicopters")
            
        vehicles_str = " with " + ", ".join(vehicles) if vehicles else ""
        match_history += f"{result_emoji} Match {idx}: {match['squadron']}{vehicles_str}\n"

    embed.add_field(name="Match History", value=match_history or "No matches yet", inline=False)
    
    # Add current streak
    embed.add_field(name="Current Streak", value=f"🔥 {tracker.win_streak}" if tracker.win_streak > 0 else "No streak", inline=True)
    embed.add_field(name="Best Streak", value=f"⭐ {tracker.best_streak}", inline=True)

    # Update the existing embed message
    await tracker.current_embed.edit(embed=embed)
    await interaction.response.send_message("✅ Match registered!", ephemeral=True)

@bot.tree.command(name="history", description="View match history")
async def history(interaction: discord.Interaction, days: int = 7):
    """
    [*] L04D1NG M4TCH H1ST0RY...
    """
    history = load_match_history()
    
    if not history["matches"]:
        await interaction.response.send_message("No match history found!", ephemeral=True)
        return
        
    cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
    recent_matches = [
        match for match in history["matches"] 
        if datetime.fromisoformat(match["timestamp"]).timestamp() > cutoff_date
    ]
    
    if not recent_matches:
        await interaction.response.send_message(f"No matches found in the last {days} days!", ephemeral=True)
        return
        
    wins = sum(1 for match in recent_matches if match['result'] == 'WIN')
    total = len(recent_matches)
    win_rate = (wins / total) * 100
    
    embed = discord.Embed(
        title=f"📊 Match History (Last {days} days)",
        description=f"Total Matches: {total}\nWin Rate: {win_rate:.2f}%",
        color=discord.Color.blue()
    )
    
    # Show last 10 matches
    last_matches = recent_matches[-10:]
    match_list = ""
    for match in last_matches:
        date = datetime.fromisoformat(match["timestamp"]).strftime("%Y-%m-%d %H:%M")
        result_emoji = "🟢" if match['result'] == 'WIN' else "🔴"
        vehicles = []
        if match['tanks'] > 0:
            vehicles.append(f"{match['tanks']} tanks")
        if match['planes'] > 0:
            vehicles.append(f"{match['planes']} planes")
        if match['helicopters'] > 0:
            vehicles.append(f"{match['helicopters']} helicopters")
            
        vehicles_str = " with " + ", ".join(vehicles) if vehicles else ""
        match_list += f"{result_emoji} [{date}] {match['squadron']}{vehicles_str}\n"
    
    embed.add_field(name="Recent Matches", value=match_list or "No recent matches", inline=False)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="final", description="End the tracking session and show final statistics")
async def final(interaction: discord.Interaction):
    """
    [*] F1N4L1Z1NG TR4CK1NG S3SS10N...
    """
    if interaction.channel_id not in active_matches:
        await interaction.response.send_message("❌ No active tracking session!", ephemeral=True)
        return

    tracker = active_matches[interaction.channel_id]
    stats = tracker.get_stats()
    
    if isinstance(stats, str):
        await interaction.response.send_message(stats, ephemeral=True)
        return

    embed = discord.Embed(
        title="📊 Final Session Statistics",
        description=f"Session duration: {datetime.now() - tracker.start_time}",
        color=discord.Color.gold()
    )

    embed.add_field(name="Total Matches", value=stats['total_matches'], inline=True)
    embed.add_field(name="Wins", value=stats['wins'], inline=True)
    embed.add_field(name="Losses", value=stats['losses'], inline=True)
    embed.add_field(name="Win Rate", value=f"{stats['win_rate']:.2f}%", inline=True)
    embed.add_field(name="Best Streak", value=stats['best_streak'], inline=True)

    await interaction.response.send_message(embed=embed)
    del active_matches[interaction.channel_id]

def run_bot():
    """
    [*] ST4RT1NG B0T 3NG1N3...
    """
    bot.run(config['discord_token'])

if __name__ == "__main__":
    run_bot()
