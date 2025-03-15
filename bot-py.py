import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
import yt_dlp
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Check if environment variables are set
if not BOT_TOKEN or not CHANNEL_ID:
    raise ValueError("Please set BOT_TOKEN and CHANNEL_ID environment variables")

# Initialize bot
bot = Bot(token=BOT_TOKEN)

# Initialize dispatcher
dp = Dispatcher()

# Enable logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Quality options
QUALITY_OPTIONS = {
    "high": "best",
    "medium": "best[height<=720]",
    "low": "best[height<=480]",
    "audio": "bestaudio"
}

# Default quality
DEFAULT_QUALITY = "high"

# Function to download the video using yt-dlp with quality option
def download_video(url, quality="high", download_path="downloaded_video.mp4"):
    # Get format based on quality or default to best
    format_option = QUALITY_OPTIONS.get(quality.lower(), QUALITY_OPTIONS[DEFAULT_QUALITY])
    
    # Set audio-only download path if needed
    if quality.lower() == "audio":
        download_path = download_path.replace(".mp4", ".mp3")
    
    ydl_opts = {
        'format': format_option,
        'outtmpl': download_path,
        'noplaylist': True,
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': False
    }
    
    logger.info(f"Downloading {url} with quality {quality}")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            return True, info.get('title', 'Video'), download_path
        except Exception as e:
            logger.error(f"Download error: {str(e)}")
            return False, str(e), download_path

@dp.message(Command("help"))
async def send_help(message: types.Message):
    help_text = (
        "📹 *YouTube Downloader Bot* 📹\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/send_video [URL] - Download and send with high quality\n"
        "/send_video [URL] [quality] - Download with specified quality\n\n"
        "Available quality options:\n"
        "• high - Best quality (default)\n"
        "• medium - Medium quality (720p)\n"
        "• low - Low quality (480p)\n"
        "• audio - Audio only\n\n"
        "Example: `/send_video https://youtube.com/watch?v=example medium`"
    )
    await message.reply(help_text, parse_mode="Markdown")

# Command handler to send the video
@dp.message(Command("send_video"))
async def send_video(message: types.Message):
    # Parse the command arguments
    parts = message.text.split()
    
    if len(parts) < 2:
        await message.reply("❌ Please provide a URL. Usage: /send_video [URL] [quality]")
        return
    
    url = parts[1]
    
    # Get quality if specified, otherwise use default
    quality = DEFAULT_QUALITY
    if len(parts) >= 3 and parts[2].lower() in QUALITY_OPTIONS:
        quality = parts[2].lower()
    
    # Download the video from the URL
    base_path = "downloaded_video"
    download_path = f"{base_path}.mp4"
    
    status_message = await message.reply(f"🔄 Downloading {quality} quality video... This may take a moment.")
    
    try:
        success, result, actual_path = download_video(url, quality, download_path)
        
        if not success:
            await status_message.edit_text(f"❌ Error downloading video: {result}")
            return
            
        await status_message.edit_text("✅ Video downloaded successfully! Uploading to channel...")
        
        # Check if file exists and is not empty
        if not os.path.exists(actual_path) or os.path.getsize(actual_path) == 0:
            await status_message.edit_text("❌ Failed to download. Empty or missing file.")
            return

        # Create an FSInputFile object for the file
        file = FSInputFile(path=actual_path)
        
        file_type = "audio" if quality == "audio" else "video"
        quality_text = f" ({quality} quality)" if file_type == "video" else ""
        
        # Upload the file to the channel
        if file_type == "video":
            uploaded_message = await bot.send_video(
                chat_id=CHANNEL_ID, 
                video=file,
                caption=f"{result}{quality_text}"
            )
            file_id = uploaded_message.video.file_id
            
            # Forward to the user
            await bot.send_video(
                chat_id=message.chat.id, 
                video=file_id, 
                caption=f"Here is your requested video: {result}{quality_text}"
            )
        else:
            # Send as audio file
            uploaded_message = await bot.send_audio(
                chat_id=CHANNEL_ID, 
                audio=file,
                caption=f"{result} (audio only)"
            )
            file_id = uploaded_message.audio.file_id
            
            # Forward to the user
            await bot.send_audio(
                chat_id=message.chat.id, 
                audio=file_id, 
                caption=f"Here is your requested audio: {result}"
            )

        await status_message.edit_text(f"✅ {file_type.capitalize()} sent successfully!")
        logger.info(f"Successfully sent {file_type} to user {message.from_user.id}: {result}")

    except Exception as e:
        error_message = f"❌ Error processing request: {str(e)}"
        await status_message.edit_text(error_message)
        logger.error(error_message)
    finally:
        # Clean up - remove the downloaded file
        for ext in [".mp4", ".mp3"]:
            potential_file = base_path + ext
            if os.path.exists(potential_file):
                os.remove(potential_file)

# Start command
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    user = message.from_user
    logger.info(f"User {user.id} ({user.username}) started the bot")
    await message.reply(
        "👋 Welcome to the YouTube Downloader Bot!\n\n"
        "Use /send_video [URL] [quality] to download and send videos.\n"
        "For quality options and more information, use /help."
    )

# Error handler
@dp.errors()
async def errors_handler(exception):
    logger.exception(exception)

# Main function to start the bot
async def main():
    logger.info("Starting bot")
    # Start the bot
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
