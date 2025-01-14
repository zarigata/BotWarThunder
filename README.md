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

A Discord bot for tracking War Thunder matches and squad statistics.

## Features
- Track match results for your squad
- Record vehicle usage (tanks, planes, helicopters)
- Calculate win rates and streaks
- Beautiful embedded messages
- Cross-platform support (Windows & Linux)

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Configure the bot:
- Edit `config.json` and add your Discord bot token
- Adjust Ollama settings if needed

## 🚀 F3V3R DR34M DOCKER RUNTIME GUIDE 🚀

### Prerequisites
- Docker Desktop (Windows/Linux)
- Docker Compose
- Python 3.11+

### Installation Steps

1. **Clone the Repo** 
   ```bash
   git clone https://github.com/your-username/war-thunder-tracker.git
   cd war-thunder-tracker
   ```

2. **Configure IP Settings**
   Edit `config.yml` to set custom IP/ports for Ollama and Stable Diffusion

3. **Build & Run Docker Containers**
   ```bash
   docker-compose up --build
   ```

### Configuration Options

- `config.yml`: Customize runtime settings
- Supports cross-platform deployment (Windows/Linux)
- Default Ollama Model: `llama3.2`

### Troubleshooting

- Ensure Docker is running
- Check container logs with `docker-compose logs`
- Verify network connectivity

### License
🔥 F3V3R DR34M CREW EDITION 2025 🔥

## Usage

### Commands
- `/comecar` - Start a new tracking session
- `/rg` - Register a match result
  - Parameters:
    - squadron: Your squadron name
    - tanks: Number of tanks used
    - planes: Number of planes used
    - plane_types: Types of planes used (e.g., "2xF-4C, 1xF-14")
    - helicopters: Number of helicopters used
    - result: "win" or "lose"
- `/final` - End the session and show statistics

## Credits
Created by F3V3R DR34M T34M
