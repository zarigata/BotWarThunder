# War Thunder Match Tracker Bot

```
.__________________.
|                  |
|  F3V3R DR34M     |
|  W4R THUND3R     |
|  TR4CK3R v1.0    |
|                  |
|  [2025 RUL3Z!]   |
|__________________|
```

## 🚀 Features
- Track War Thunder match results
- Discord bot integration
- Cross-platform support (Windows & Linux)
- Persistent match history

## 🛠️ Installation

### Local Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

### Docker Deployment
1. Build the Docker image:
```bash
docker build -t war-thunder-bot .
```

2. Run the Docker container:
```bash
docker run -d \
  -e DISCORD_TOKEN=your_token_here \
  --name war-thunder-bot \
  war-thunder-bot
```

## 🎮 Usage

### Commands
- `/comecar` - Start a new tracking session
- `/rg` - Register a match result
- `/history` - View past match history
- `/final` - End the current session

## 🔒 Configuration
Edit `config.json` to set your Discord token and other settings.

## 🏆 Credits
- Master: Z4R1G4T4
- Team: F3V3R DR34M

## 📜 License
Proprietary - F3V3R DR34M Team
