# Telegram YouTube Downloader Bot

A Telegram bot that can download videos from YouTube and other platforms in different quality options and post them to a Telegram channel.

## Features

- Download videos in different quality options (high, medium, low)
- Download audio-only version of videos
- Forward downloaded content to a Telegram channel
- User-friendly commands and feedback

## Project Structure

```
telegram-youtube-bot/
├── bot.py               # Main bot code
├── requirements.txt     # Dependencies
├── .env.example         # Example environment variables file
├── .gitignore           # Files to be ignored by git
└── README.md            # Project documentation
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- A Telegram Bot Token (get from @BotFather)
- Telegram Channel ID where videos will be posted

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/telegram-youtube-bot.git
   cd telegram-youtube-bot
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

5. Edit the `.env` file with your bot token and channel ID:
   ```
   BOT_TOKEN=your_bot_token_here
   CHANNEL_ID=your_channel_id_here
   ```

6. Run the bot:
   ```bash
   python bot.py
   ```

### Ubuntu Server Deployment

1. Connect to your Ubuntu server:
   ```bash
   ssh username@your_server_ip
   ```

2. Install system dependencies:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv git
   ```

3. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/telegram-youtube-bot.git
   cd telegram-youtube-bot
   ```

4. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Create and edit the `.env` file:
   ```bash
   cp .env.example .env
   nano .env  # Add your bot token and channel ID
   ```

7. Set up a systemd service for running the bot:
   ```bash
   sudo nano /etc/systemd/system/telegram-bot.service
   ```

8. Add the following content to the service file:
   ```
   [Unit]
   Description=Telegram YouTube Downloader Bot
   After=network.target

   [Service]
   User=your_username
   WorkingDirectory=/home/your_username/telegram-youtube-bot
   ExecStart=/home/your_username/telegram-youtube-bot/venv/bin/python bot.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

9. Enable and start the service:
   ```bash
   sudo systemctl enable telegram-bot
   sudo systemctl start telegram-bot
   ```

10. Check the status:
    ```bash
    sudo systemctl status telegram-bot
    ```

11. View logs if needed:
    ```bash
    sudo journalctl -u telegram-bot -f
    ```

## Usage

- `/start` - Start the bot
- `/help` - Show available commands and options
- `/send_video [URL]` - Download and send video in high quality
- `/send_video [URL] [quality]` - Download with specified quality (high, medium, low, audio)

## License

MIT License
