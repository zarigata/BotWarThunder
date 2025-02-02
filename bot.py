"""
.-------------------.
|     [CONFIDENCIAL]|
| RASTREADOR DE     |
| GUERRA THUNDER    |
| VERSÃO: ALFA      |
|                   |
| [ULTRA SECRETO]   |
'-------------------'

BRIEFING DA MISSÃO:
- OPERAÇÃO: SISTEMA DE RASTREAMENTO DE BATALHA
- AUTORIZAÇÃO: ULTRA SECRETO
- STATUS: ATIVO
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
    [*] ACESSANDO REGISTROS DE BATALHA CONFIDENCIAIS...
    [*] DESCRIPTOGRAFANDO DADOS...
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
    [*] CRIPTOGRAFANDO DADOS...
    [*] SALVANDO NO BANCO DE DADOS...
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
    [*] ANALISANDO RESULTADO DA BATALHA...
    """
    result = result.lower().strip()
    win_options = ['v', '1', 'win', 'victoria', 'vitória']
    loss_options = ['d', '0', 'loss', 'derrota']
    
    if result in win_options:
        return 'VITÓRIA'
    elif result in loss_options:
        return 'DERROTA'
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

    def add_match(self, squadron, tanks, planes, helicopters, spaa, bomber, result):
        match = {
            'squadron': squadron,
            'tanks': tanks,
            'planes': planes,
            'helicopters': helicopters,
            'spaa': spaa,
            'bomber': bomber,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
        self.matches.append(match)
        save_match_history(match)
        
        if result == 'VITÓRIA':
            self.win_streak += 1
            self.best_streak = max(self.win_streak, self.best_streak)
        else:
            self.win_streak = 0

    def get_stats(self):
        total_matches = len(self.matches)
        if total_matches == 0:
            return "Nenhuma batalha registrada"
            
        wins = sum(1 for match in self.matches if match['result'] == 'VITÓRIA')
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
    [*] SISTEMA DE RASTREAMENTO DE BATALHA ONLINE...
    [*] AGUARDANDO IMPLANTAÇÃO...
    """
    print(f'''
    ╔══════════════════════════════╗
    ║  RASTREADOR DE GUERRA THUNDER║
    ║  SISTEMA: {platform.system()} ║
    ║  BOT: {bot.user.name}        ║
    ║  STATUS: ONLINE              ║
    ╚══════════════════════════════╝
    ''')
    try:
        synced = await bot.tree.sync()
        print(f"[*] Sincronizou {len(synced)} comandos")
    except Exception as e:
        print(f"[!] ERRO: {str(e)}")

@bot.tree.command(name="comecar", description="Iniciar operações de combate")
async def comecar(interaction: discord.Interaction):
    """
    [*] INICIANDO OPERAÇÕES DE COMBATE...
    [*] IMPLANTANDO SISTEMA DE RASTREAMENTO DE BATALHA...
    """
    if interaction.channel_id in active_matches:
        await interaction.response.send_message("[!] OPERAÇÕES DE COMBATE JÁ EM ANDAMENTO!", ephemeral=True)
        return

    # Get users in voice channel
    try:
        voice_channel = interaction.user.voice.channel
        squad_members = ", ".join([member.name for member in voice_channel.members]) if voice_channel else "Nenhum membro na sala de voz"
    except:
        squad_members = "Nenhum membro na sala de voz"

    active_matches[interaction.channel_id] = MatchTracker(interaction.channel_id)
    
    embed = discord.Embed(
        title="[INÍCIO DA MISSÃO] Sessão de Rastreamento de Combate Iniciada",
        description="[!] COMANDANTE: Use /rg para registrar engajamentos e /final para concluir a missão.",
        color=discord.Color.from_rgb(50, 168, 82)  # Verde militar
    )
    
    embed.add_field(name="[MEMBROS DO ESQUADRÃO]", value=squad_members, inline=False)
    
    await interaction.response.send_message(embed=embed)
    active_matches[interaction.channel_id].current_embed = await interaction.channel.send(embed=embed)

@bot.tree.command(name="rg", description="Registrar resultado da batalha")
async def rg(
    interaction: discord.Interaction,
    squadron: str,
    result: str,
    tanks: int,
    planes: int = 0,
    helicopters: int = 0,
    spaa: int = 0,
    bomber: int = 0
):
    """
    [*] REGISTRANDO RESULTADO DA BATALHA...
    [*] ANALISANDO RESULTADOS...
    """
    if interaction.channel_id not in active_matches:
        await interaction.response.send_message("[!] NENHUMA OPERAÇÃO DE COMBATE ENCONTRADA! Use /comecar primeiro!", ephemeral=True)
        return

    result = normalize_result(result)
    if not result:
        await interaction.response.send_message("[!] RESULTADO DE BATALHA INVÁLIDO!", ephemeral=True)
        return

    tracker = active_matches[interaction.channel_id]
    tracker.add_match(squadron, tanks, planes, helicopters, spaa, bomber, result)

    embed = discord.Embed(
        title="[RELATÓRIO DE COMBATE] Resultado da Batalha Registrado",
        color=0x32a852 if result == "VITÓRIA" else 0x8b0000  # Verde militar para vitória, vermelho escuro para derrota
    )
    embed.add_field(name="[ESQUADRÃO INIMIGO]", value=squadron, inline=True)
    embed.add_field(name="[RESULTADO]", value=result, inline=True)
    embed.add_field(name="[BLINDADOS]", value=f"{tanks} unidades", inline=True)
    embed.add_field(name="[FORÇA AÉREA]", value=f"{planes} unidades", inline=True)
    embed.add_field(name="[HELICÓPTEROS]", value=f"{helicopters} unidades", inline=True)
    embed.add_field(name="[DEFESA ANTIAÉREA]", value=f"{spaa} unidades", inline=True)
    embed.add_field(name="[BOMBARDEIROS]", value=f"{bomber} unidades", inline=True)

    if result == "VITÓRIA":
        embed.add_field(name="[SEQUÊNCIA DE VITÓRIAS]", value=f"{tracker.win_streak} batalhas", inline=True)
        embed.add_field(name="[MELHOR CAMPANHA]", value=f"{tracker.best_streak} batalhas", inline=True)

    tracker.current_embed = embed
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="history", description="Acessar registros de batalha confidenciais")
async def history(interaction: discord.Interaction, days: int = 7):
    """
    [*] ACESSANDO REGISTROS DE BATALHA CONFIDENCIAIS...
    [*] DESCRIPTOGRAFANDO DADOS...
    """
    history = load_match_history()
    
    if not history["matches"]:
        await interaction.response.send_message("[!] NENHUM REGISTRO ENCONTRADO NO BANCO DE DADOS!", ephemeral=True)
        return
        
    cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
    recent_matches = [
        match for match in history["matches"]
        if datetime.fromisoformat(match["timestamp"]).timestamp() >= cutoff_date
    ]
    
    if not recent_matches:
        await interaction.response.send_message(f"[!] NENHUMA BATALHA REGISTRADA NOS ÚLTIMOS {days} DIAS!", ephemeral=True)
        return
        
    wins = sum(1 for match in recent_matches if match['result'] == 'VITÓRIA')
    total = len(recent_matches)
    win_rate = (wins / total) * 100
    
    embed = discord.Embed(
        title=f"[RELATÓRIO DE INTELIGÊNCIA] Últimos {days} Dias",
        description=f"[ESTATÍSTICAS]\nTotal de Engajamentos: {total}\nTaxa de Vitória: {win_rate:.2f}%",
        color=discord.Color.from_rgb(50, 168, 82)  # Verde militar
    )
    
    # Show last 10 matches
    match_list = ""
    for match in recent_matches[-10:]:
        date = datetime.fromisoformat(match["timestamp"]).strftime("%Y-%m-%d %H:%M")
        vehicles = []
        if match['tanks'] > 0:
            vehicles.append(f"{match['tanks']} blindados")
        if match['planes'] > 0:
            vehicles.append(f"{match['planes']} aviões")
        if match['helicopters'] > 0:
            vehicles.append(f"{match['helicopters']} helicópteros")
        if match.get('spaa', 0) > 0:
            vehicles.append(f"{match['spaa']} defesa antiaérea")
        if match.get('bomber', 0) > 0:
            vehicles.append(f"{match['bomber']} bombardeiros")
            
        vehicles_str = " com " + ", ".join(vehicles) if vehicles else ""
        match_list += f"{'✅' if match['result'] == 'VITÓRIA' else '❌'} [{date}] {match['squadron']}{vehicles_str}\n"
    
    embed.add_field(name="Batalhas Recentes", value=match_list or "Sem batalhas recentes", inline=False)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="delete", description="Destruir último registro de batalha")
async def delete(interaction: discord.Interaction):
    """
    [*] INICIANDO PROTOCOLO DE DESTRUIÇÃO DE REGISTRO...
    [*] AGUARDANDO CONFIRMAÇÃO...
    """
    history = load_match_history()
    
    if not history["matches"]:
        await interaction.response.send_message("[!] NENHUM REGISTRO ENCONTRADO NO BANCO DE DADOS!", ephemeral=True)
        return
    
    deleted_match = history["matches"].pop()
    
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)
    
    embed = discord.Embed(
        title="[!] DESTRUIÇÃO DE REGISTRO CONCLUÍDA",
        description="O seguinte registro de batalha foi removido do banco de dados:",
        color=discord.Color.from_rgb(139, 0, 0)  # Vermelho escuro
    )
    embed.add_field(name="[FORÇA INIMIGA]", value=deleted_match["squadron"], inline=True)
    embed.add_field(name="[RESULTADO]", value=deleted_match["result"], inline=True)
    embed.add_field(name="[BLINDADOS]", value=f"{deleted_match['tanks']} unidades", inline=True)
    embed.add_field(name="[FORÇA AÉREA]", value=f"{deleted_match['planes']} unidades", inline=True)
    embed.add_field(name="[HELICÓPTEROS]", value=f"{deleted_match['helicopters']} unidades", inline=True)
    embed.add_field(name="[DEFESA ANTIAÉREA]", value=f"{deleted_match.get('spaa', 'N/A')} unidades", inline=True)
    embed.add_field(name="[ESTRATÉGICO]", value=f"{deleted_match.get('bomber', 'N/A')} unidades", inline=True)
    embed.add_field(name="[TIMESTAMP]", value=deleted_match["timestamp"], inline=True)
    embed.set_footer(text="[!] ESTE REGISTRO FOI PERMANENTEMENTE DELETADO")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="final", description="Concluir operações de combate")
async def final(interaction: discord.Interaction):
    """
    [*] INICIANDO PROTOCOLO DE CONCLUSÃO DE MISSÃO...
    [*] GERANDO RELATÓRIO FINAL...
    """
    if interaction.channel_id not in active_matches:
        await interaction.response.send_message("[!] NENHUMA OPERAÇÃO DE COMBATE ENCONTRADA!", ephemeral=True)
        return

    tracker = active_matches[interaction.channel_id]
    if not tracker.matches:
        await interaction.response.send_message("[!] NENHUMA BATALHA REGISTRADA NESTA SESSÃO!", ephemeral=True)
        return

    total_matches = len(tracker.matches)
    wins = sum(1 for match in tracker.matches if match['result'] == 'VITÓRIA')
    win_rate = (wins / total_matches) * 100

    embed = discord.Embed(
        title="[MISSÃO CONCLUÍDA] Relatório Final de Combate",
        description=f"Duração da Operação: {datetime.now() - tracker.start_time}",
        color=discord.Color.from_rgb(50, 168, 82)  # Verde militar
    )
    embed.add_field(name="[TOTAL DE ENGAJAMENTOS]", value=str(total_matches), inline=True)
    embed.add_field(name="[VITÓRIAS]", value=str(wins), inline=True)
    embed.add_field(name="[TAXA DE SUCESSO]", value=f"{win_rate:.1f}%", inline=True)
    embed.add_field(name="[MELHOR SEQUÊNCIA]", value=str(tracker.best_streak), inline=True)
    embed.set_footer(text="[!] MISSÃO CUMPRIDA - AGUARDANDO PRÓXIMA IMPLANTAÇÃO")

    await interaction.response.send_message(embed=embed)
    del active_matches[interaction.channel_id]

def run_bot():
    """
    [*] INICIANDO SISTEMA DE RASTREAMENTO DE BATALHA...
    [*] AGUARDANDO IMPLANTAÇÃO...
    """
    bot.run(config['discord_token'])

if __name__ == "__main__":
    run_bot()
