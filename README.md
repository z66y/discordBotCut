# Discord Cut Bot

A Discord bot that manages and shares "Cut" (Arabic quotes) with a points system and leaderboard.

## Features

- **Random Cut Command** (`/كت`): Sends a random Cut from the collection
- **Custom Cut Command** (`/كت-بنفسك`): Sends a one-time Cut without saving it
- **Add Cut Command** (`/اضافة_كت`): Adds a new Cut to the collection
- **Leaderboard** (`/المتصدرين`): Displays top 10 users
- **Points System** (`/نقاطي`): Shows your current points
- **Help Command** (`/مساعدة`): Displays available commands

## Requirements

- Python 3.8 or higher
- Required packages:
  - discord.py==2.3.2
  - python-dotenv==1.0.0

## Installation

1. Clone the repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file and add your Discord bot token:
   ```
   DISCORD_TOKEN=your_token_here
   ```

## Usage

1. Run the bot:
   ```bash
   python bot.py
   ```
2. The bot will print an invite link with required permissions
3. Use the invite link to add the bot to your server

## Commands

- `/كت` - Sends a random Cut
- `/كت-بنفسك [cut]` - Sends a one-time Cut
- `/اضافة_كت [cut]` - Adds a new Cut
- `/المتصدرين` - Shows top 10 users
- `/نقاطي` - Shows your points
- `/مساعدة` - Shows available commands

## Data Storage

- Cuts are stored in `cuts.txt`
- User points are stored in `points.json`

## Permissions

The bot requires the following permissions:
- Send Messages
- Embed Links
- Read Messages
- Read Message History
- Manage Messages
- Attach Files
- Use External Emojis

## License

This project is open source and available under the MIT License.

## How to Deploy on Bot-Hosting.net

### 1. Files to Upload
- `bot.py` (main bot code)
- `requirements.txt` (dependencies)
- `.env` (contains your bot token)
- `cuts.txt` (can be empty)
- `points.json` (should contain `{}`)

### 2. requirements.txt
```
discord.py==2.3.2
python-dotenv==1.0.0
```

### 3. .env file
```
DISCORD_TOKEN=your_bot_token_here
```

### 4. cuts.txt
- Leave it empty or add some cuts (one per line).

### 5. points.json
```
{}
```

### 6. Run Command
```
python bot.py
```

### 7. Notes
- Make sure your bot has the required permissions on your Discord server.
- If you face any error, check the logs and make sure all files are present in the root directory.
- Do not upload unnecessary files or folders (like venv or __pycache__).

---

Good luck! If you need help, check your logs or contact support.

## Environment Variables

Create a `.env` file in the root directory with the following content:
```
DISCORD_TOKEN=your_bot_token_here
``` 